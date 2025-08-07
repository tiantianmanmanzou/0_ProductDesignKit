#!/usr/bin/env python3
"""
数据库数据验证检查器

检查数据库中实际存储的数据是否与代码定义的枚举值一致
这是静态代码检查无法发现的问题：数据库中可能存在不符合代码规范的历史数据

功能：
1. 连接数据库检查枚举字段的实际值
2. 与代码中定义的枚举值进行对比
3. 识别数据不一致问题
4. 生成数据修复建议
"""

import os
import sys
import re
import ast
import json
import argparse
from typing import Dict, List, Set, Tuple, Optional, Any
from datetime import datetime
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    print("⚠️ 警告: psycopg2 未安装，无法连接PostgreSQL数据库")
    print("请运行: pip install psycopg2-binary")
    sys.exit(1)

class DatabaseDataValidator:
    """数据库数据验证器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.backend_root = self.project_root / "backend"
        self.frontend_root = self.project_root / "frontend" / "src"
        
        # 数据库连接配置
        self.db_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'excel2doc',
            'user': 'excel2doc_user',
            'password': 'excel2doc_password'
        }
        
        # 枚举定义缓存
        self.backend_enums = {}
        self.frontend_enums = {}
        
        # 数据库枚举字段映射
        self.enum_field_mappings = {
            'projects': {
                'parse_status': 'ParseStatusEnum',
            },
            'tasks': {
                'task_status': 'TaskStatusEnum',
                'task_type': 'TaskTypeEnum',
            },
            'module_summaries': {
                'generation_status': 'GenerationStatusEnum',
                'summary_type': 'SummaryTypeEnum',
            },
            'users': {
                'status': 'UserStatusEnum',
            }
        }
        
        # 问题统计
        self.issues = {
            'database_enum_mismatch': [],
            'invalid_enum_values': [],
            'missing_enum_constraints': [],
            'data_migration_needed': []
        }

    def connect_database(self) -> Optional[Any]:
        """连接数据库"""
        try:
            conn = psycopg2.connect(**self.db_config)
            return conn
        except psycopg2.Error as e:
            print(f"❌ 数据库连接失败: {e}")
            return None

    def parse_python_enums(self) -> Dict[str, Dict[str, str]]:
        """解析Python枚举定义"""
        enum_definitions = {}
        
        # 查找所有Python文件
        for py_file in self.backend_root.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 解析AST
                try:
                    tree = ast.parse(content)
                except SyntaxError:
                    continue
                
                # 查找枚举类定义
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        # 检查是否是枚举类
                        bases = [base.id for base in node.bases if isinstance(base, ast.Name)]
                        if 'Enum' in bases or any('Enum' in base for base in bases):
                            enum_values = {}
                            
                            # 提取枚举值
                            for item in node.body:
                                if isinstance(item, ast.Assign):
                                    for target in item.targets:
                                        if isinstance(target, ast.Name):
                                            if isinstance(item.value, ast.Constant):
                                                enum_values[target.id] = item.value.value
                                            elif isinstance(item.value, ast.Str):  # Python < 3.8
                                                enum_values[target.id] = item.value.s
                            
                            if enum_values:
                                enum_definitions[node.name] = {
                                    'values': enum_values,
                                    'file': str(py_file.relative_to(self.project_root))
                                }
            
            except Exception as e:
                continue
        
        return enum_definitions

    def parse_typescript_enums(self) -> Dict[str, Dict[str, str]]:
        """解析TypeScript枚举定义"""
        enum_definitions = {}
        
        # 查找所有TypeScript文件
        for ts_file in self.frontend_root.rglob("*.ts"):
            try:
                with open(ts_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 使用正则表达式匹配枚举定义
                enum_pattern = r'export\s+enum\s+(\w+)\s*\{([^}]+)\}'
                matches = re.findall(enum_pattern, content, re.MULTILINE | re.DOTALL)
                
                for enum_name, enum_body in matches:
                    enum_values = {}
                    
                    # 解析枚举值
                    value_pattern = r'(\w+)\s*=\s*["\']([^"\']+)["\']'
                    value_matches = re.findall(value_pattern, enum_body)
                    
                    for key, value in value_matches:
                        enum_values[key] = value
                    
                    if enum_values:
                        enum_definitions[enum_name] = {
                            'values': enum_values,
                            'file': str(ts_file.relative_to(self.project_root))
                        }
            
            except Exception as e:
                continue
        
        return enum_definitions

    def get_database_enum_values(self, conn, table_name: str, column_name: str) -> Set[str]:
        """获取数据库中某个枚举字段的实际值"""
        try:
            cursor = conn.cursor()
            
            # 查询唯一值
            query = f"SELECT DISTINCT {column_name} FROM {table_name} WHERE {column_name} IS NOT NULL;"
            cursor.execute(query)
            
            results = cursor.fetchall()
            values = {str(row[0]) for row in results if row[0] is not None}
            
            cursor.close()
            return values
            
        except psycopg2.Error as e:
            print(f"❌ 查询表 {table_name}.{column_name} 失败: {e}")
            return set()

    def check_database_enum_consistency(self):
        """检查数据库枚举值一致性"""
        conn = self.connect_database()
        if not conn:
            return
        
        try:
            for table_name, columns in self.enum_field_mappings.items():
                for column_name, enum_class_name in columns.items():
                    print(f"🔍 检查 {table_name}.{column_name} (对应枚举: {enum_class_name})")
                    
                    # 获取数据库实际值
                    db_values = self.get_database_enum_values(conn, table_name, column_name)
                    
                    if not db_values:
                        print(f"  ℹ️ 表 {table_name} 中 {column_name} 字段无数据")
                        continue
                    
                    # 查找对应的枚举定义
                    code_enum_values = set()
                    enum_source = "未找到"
                    
                    # 在后端枚举中查找
                    if enum_class_name in self.backend_enums:
                        code_enum_values = set(self.backend_enums[enum_class_name]['values'].values())
                        enum_source = f"backend: {self.backend_enums[enum_class_name]['file']}"
                    
                    # 在前端枚举中查找（去掉Enum后缀）
                    frontend_enum_name = enum_class_name.replace('Enum', '')
                    if frontend_enum_name in self.frontend_enums:
                        frontend_values = set(self.frontend_enums[frontend_enum_name]['values'].values())
                        if code_enum_values:
                            # 检查前后端是否一致
                            if code_enum_values != frontend_values:
                                self.issues['database_enum_mismatch'].append({
                                    'type': 'frontend_backend_enum_mismatch',
                                    'table': table_name,
                                    'column': column_name,
                                    'enum_class': enum_class_name,
                                    'backend_values': sorted(code_enum_values),
                                    'frontend_values': sorted(frontend_values),
                                    'message': f"前后端枚举值不一致"
                                })
                        else:
                            code_enum_values = frontend_values
                            enum_source = f"frontend: {self.frontend_enums[frontend_enum_name]['file']}"
                    
                    if not code_enum_values:
                        self.issues['missing_enum_constraints'].append({
                            'type': 'enum_definition_not_found',
                            'table': table_name,
                            'column': column_name,
                            'enum_class': enum_class_name,
                            'database_values': sorted(db_values),
                            'message': f"找不到枚举 {enum_class_name} 的定义"
                        })
                        continue
                    
                    # 比较数据库值与代码定义
                    invalid_values = db_values - code_enum_values
                    missing_values = code_enum_values - db_values
                    
                    if invalid_values:
                        self.issues['invalid_enum_values'].append({
                            'type': 'invalid_database_enum_values',
                            'table': table_name,
                            'column': column_name,
                            'enum_class': enum_class_name,
                            'invalid_values': sorted(invalid_values),
                            'valid_values': sorted(code_enum_values),
                            'enum_source': enum_source,
                            'message': f"数据库中存在无效的枚举值: {', '.join(invalid_values)}"
                        })
                        
                        # 生成数据迁移建议
                        self.generate_migration_suggestions(table_name, column_name, invalid_values, code_enum_values)
                    
                    if missing_values:
                        print(f"  ℹ️ 代码定义的值在数据库中不存在: {', '.join(missing_values)}")
                    
                    if not invalid_values and not missing_values:
                        print(f"  ✅ {table_name}.{column_name} 枚举值一致")
                    else:
                        print(f"  ❌ {table_name}.{column_name} 发现不一致")
                        print(f"     数据库值: {sorted(db_values)}")
                        print(f"     代码定义: {sorted(code_enum_values)}")
                        if invalid_values:
                            print(f"     无效值: {sorted(invalid_values)}")
        
        finally:
            conn.close()

    def generate_migration_suggestions(self, table_name: str, column_name: str, invalid_values: Set[str], valid_values: Set[str]):
        """生成数据迁移建议"""
        suggestions = []
        
        # 尝试智能匹配
        value_mappings = {}
        for invalid_val in invalid_values:
            # 大小写转换匹配
            lower_val = invalid_val.lower()
            upper_val = invalid_val.upper()
            
            if lower_val in valid_values:
                value_mappings[invalid_val] = lower_val
            elif upper_val in valid_values:
                value_mappings[invalid_val] = upper_val
            else:
                # 模糊匹配
                best_match = self.find_best_match(invalid_val, valid_values)
                if best_match:
                    value_mappings[invalid_val] = best_match
        
        if value_mappings:
            # 生成SQL更新语句
            sql_statements = []
            for old_val, new_val in value_mappings.items():
                sql = f"UPDATE {table_name} SET {column_name} = '{new_val}' WHERE {column_name} = '{old_val}';"
                sql_statements.append(sql)
            
            self.issues['data_migration_needed'].append({
                'type': 'enum_value_migration',
                'table': table_name,
                'column': column_name,
                'value_mappings': value_mappings,
                'sql_statements': sql_statements,
                'message': f"需要数据迁移以修复枚举值不一致"
            })

    def find_best_match(self, invalid_value: str, valid_values: Set[str]) -> Optional[str]:
        """寻找最佳匹配的有效值"""
        invalid_lower = invalid_value.lower()
        
        # 完全匹配（忽略大小写）
        for valid_val in valid_values:
            if valid_val.lower() == invalid_lower:
                return valid_val
        
        # 部分匹配
        for valid_val in valid_values:
            if invalid_lower in valid_val.lower() or valid_val.lower() in invalid_lower:
                return valid_val
        
        return None

    def generate_migration_script(self) -> str:
        """生成数据库迁移脚本"""
        if not self.issues['data_migration_needed']:
            return ""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        migration_content = f'''"""
数据库枚举值修复迁移脚本
生成时间: {datetime.now().isoformat()}
修复数据库中不符合代码规范的枚举值

由 database_data_validator.py 自动生成
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '{timestamp}_fix_enum_data_consistency'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    """修复枚举值数据不一致"""
    # 获取数据库连接
    conn = op.get_bind()
    
'''
        
        for issue in self.issues['data_migration_needed']:
            if issue['type'] == 'enum_value_migration':
                migration_content += f'''
    # 修复 {issue['table']}.{issue['column']} 枚举值
    # 值映射: {issue['value_mappings']}
'''
                for sql in issue['sql_statements']:
                    migration_content += f"    conn.execute(\"{sql}\")\n"
        
        migration_content += '''

def downgrade():
    """回滚枚举值修复"""
    # 注意：这个回滚可能会导致数据丢失
    # 请根据实际情况手动实现回滚逻辑
    pass
'''
        
        return migration_content

    def print_summary(self):
        """打印检查摘要"""
        total_issues = sum(len(issues) for issues in self.issues.values())
        
        print(f"\n{'='*50}")
        print(f"📊 数据库数据验证检查报告")
        print(f"{'='*50}")
        print(f"📈 总体统计:")
        print(f"   总问题数: {total_issues}")
        
        for issue_type, issues in self.issues.items():
            if issues:
                print(f"   {issue_type}: {len(issues)} 个")
        
        # 详细问题报告
        if self.issues['invalid_enum_values']:
            print(f"\n❌ 无效枚举值问题 ({len(self.issues['invalid_enum_values'])} 个):")
            for issue in self.issues['invalid_enum_values']:
                print(f"   🔴 {issue['table']}.{issue['column']}: {issue['message']}")
                print(f"      无效值: {issue['invalid_values']}")
                print(f"      有效值: {issue['valid_values']}")
                print(f"      枚举源: {issue['enum_source']}")
        
        if self.issues['database_enum_mismatch']:
            print(f"\n⚠️ 前后端枚举不一致 ({len(self.issues['database_enum_mismatch'])} 个):")
            for issue in self.issues['database_enum_mismatch']:
                print(f"   🟡 {issue['enum_class']}: {issue['message']}")
                print(f"      后端值: {issue['backend_values']}")
                print(f"      前端值: {issue['frontend_values']}")
        
        if self.issues['data_migration_needed']:
            print(f"\n🔧 需要数据迁移 ({len(self.issues['data_migration_needed'])} 个):")
            for issue in self.issues['data_migration_needed']:
                print(f"   🔄 {issue['table']}.{issue['column']}: {issue['message']}")
                print(f"      建议映射: {issue['value_mappings']}")
        
        # 生成迁移脚本
        if self.issues['data_migration_needed']:
            migration_script = self.generate_migration_script()
            if migration_script:
                script_path = self.project_root / "backend" / "alembic" / "versions" / f"fix_enum_data_consistency_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
                
                print(f"\n📝 生成数据库迁移脚本:")
                print(f"   文件路径: {script_path}")
                print(f"   运行命令: cd backend && alembic upgrade head")

    def save_report(self, output_file: str):
        """保存详细报告到文件"""
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_issues': sum(len(issues) for issues in self.issues.values()),
                'backend_enums': len(self.backend_enums),
                'frontend_enums': len(self.frontend_enums),
            },
            'issues': self.issues,
            'backend_enums': self.backend_enums,
            'frontend_enums': self.frontend_enums
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"📄 详细报告已保存到: {output_file}")

    def run_validation(self, verbose: bool = False, save_report: bool = False):
        """运行完整的数据库数据验证"""
        print("🚀 Excel2Doc 数据库数据验证开始...")
        print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 解析枚举定义
        print("\n📂 解析后端Python枚举...")
        self.backend_enums = self.parse_python_enums()
        print(f"✅ 后端分析完成: 发现 {len(self.backend_enums)} 个枚举定义")
        if verbose and self.backend_enums:
            for name, info in self.backend_enums.items():
                print(f"   📋 {name}: {list(info['values'].values())}")
        
        print("\n📂 解析前端TypeScript枚举...")
        self.frontend_enums = self.parse_typescript_enums()
        print(f"✅ 前端分析完成: 发现 {len(self.frontend_enums)} 个枚举定义")
        if verbose and self.frontend_enums:
            for name, info in self.frontend_enums.items():
                print(f"   📋 {name}: {list(info['values'].values())}")
        
        print("\n🔍 检查数据库枚举值一致性...")
        self.check_database_enum_consistency()
        
        # 打印结果摘要
        self.print_summary()
        
        # 保存报告
        if save_report:
            report_file = self.project_root / f"database_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            self.save_report(str(report_file))
        
        print(f"\n🎉 数据库数据验证完成！")

def main():
    parser = argparse.ArgumentParser(
        description="Excel2Doc 数据库数据验证检查器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python database_data_validator.py                    # 基本检查
  python database_data_validator.py --verbose          # 显示详细信息
  python database_data_validator.py --report           # 生成详细报告文件
  python database_data_validator.py --verbose --report # 详细检查并生成报告
        """
    )
    
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')
    parser.add_argument('--report', '-r', action='store_true', help='生成详细报告文件')
    
    args = parser.parse_args()
    
    # 获取项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    
    # 创建验证器并运行
    validator = DatabaseDataValidator(str(project_root))
    validator.run_validation(verbose=args.verbose, save_report=args.report)

if __name__ == '__main__':
    main()