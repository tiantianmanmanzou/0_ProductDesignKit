#!/usr/bin/env python3
"""
数据库迁移脚本分析器

分析Alembic迁移脚本中的枚举定义和数据操作，检查是否与代码定义一致
这是检查数据库schema和数据一致性的重要工具

功能：
1. 解析Alembic迁移脚本
2. 提取枚举相关的DDL操作
3. 检查枚举值设置是否符合规范
4. 识别潜在的数据不一致风险
5. 生成迁移脚本改进建议
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

class MigrationScriptAnalyzer:
    """数据库迁移脚本分析器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.backend_root = self.project_root / "backend"
        self.alembic_versions_dir = self.backend_root / "alembic" / "versions"
        
        # 分析结果
        self.migration_files = []
        self.enum_operations = []
        self.data_operations = []
        self.potential_issues = []
        
        # 已知的枚举类型（从代码分析中获取）
        self.known_enums = {
            'ParseStatusEnum': ['uploaded', 'parsing', 'completed', 'failed'],
            'TaskStatusEnum': ['pending', 'running', 'completed', 'failed'],
            'TaskTypeEnum': ['data_extraction', 'summary_generation', 'module_extraction'],
            'GenerationStatusEnum': ['pending', 'generating', 'completed', 'failed'],
            'SummaryTypeEnum': ['l1_summary', 'l2_summary', 'l3_summary', 'combined_summary'],
            'UserStatusEnum': ['active', 'inactive', 'suspended'],
        }
        
        # 枚举相关的SQL模式
        self.enum_patterns = {
            'create_enum': r"op\.execute\(['\"]CREATE TYPE (\w+) AS ENUM \((.*?)\)['\"]",
            'alter_enum': r"op\.execute\(['\"]ALTER TYPE (\w+) (?:ADD VALUE|RENAME VALUE) (.*?)['\"]",
            'drop_enum': r"op\.execute\(['\"]DROP TYPE (?:IF EXISTS )?(\w+)['\"]",
            'enum_column': r"sa\.Column\(['\"](\w+)['\"], (\w+)(?:\(\))?",
            'update_enum_data': r"op\.execute\(['\"]UPDATE (\w+) SET (\w+) = ['\"]([^'\"]*)['\"] WHERE (\w+) = ['\"]([^'\"]*)['\"]['\"]"
        }

    def find_migration_files(self) -> List[Path]:
        """查找所有迁移文件"""
        if not self.alembic_versions_dir.exists():
            print(f"❌ Alembic版本目录不存在: {self.alembic_versions_dir}")
            return []
        
        migration_files = []
        for file_path in self.alembic_versions_dir.glob("*.py"):
            if not file_path.name.startswith("__"):
                migration_files.append(file_path)
        
        # 按创建时间排序
        migration_files.sort(key=lambda x: x.stat().st_mtime)
        return migration_files

    def parse_migration_file(self, file_path: Path) -> Dict[str, Any]:
        """解析单个迁移文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            migration_info = {
                'file_path': str(file_path.relative_to(self.project_root)),
                'file_name': file_path.name,
                'content': content,
                'revision': self._extract_revision(content),
                'down_revision': self._extract_down_revision(content),
                'enum_operations': [],
                'data_operations': [],
                'potential_issues': []
            }
            
            # 解析枚举相关操作
            migration_info['enum_operations'] = self._extract_enum_operations(content)
            migration_info['data_operations'] = self._extract_data_operations(content)
            migration_info['potential_issues'] = self._analyze_potential_issues(migration_info)
            
            return migration_info
            
        except Exception as e:
            print(f"❌ 解析迁移文件失败 {file_path}: {e}")
            return {
                'file_path': str(file_path.relative_to(self.project_root)),
                'error': str(e)
            }

    def _extract_revision(self, content: str) -> Optional[str]:
        """提取revision信息"""
        match = re.search(r"revision\s*=\s*['\"]([^'\"]+)['\"]", content)
        return match.group(1) if match else None

    def _extract_down_revision(self, content: str) -> Optional[str]:
        """提取down_revision信息"""
        match = re.search(r"down_revision\s*=\s*['\"]([^'\"]+)['\"]", content)
        return match.group(1) if match else None

    def _extract_enum_operations(self, content: str) -> List[Dict[str, Any]]:
        """提取枚举相关操作"""
        enum_ops = []
        
        # 创建枚举类型
        for match in re.finditer(self.enum_patterns['create_enum'], content, re.IGNORECASE | re.DOTALL):
            enum_name = match.group(1)
            enum_values_str = match.group(2)
            enum_values = [v.strip().strip("'\"") for v in enum_values_str.split(',')]
            
            enum_ops.append({
                'operation': 'CREATE_ENUM',
                'enum_name': enum_name,
                'enum_values': enum_values,
                'line': content[:match.start()].count('\n') + 1
            })
        
        # 修改枚举类型
        for match in re.finditer(self.enum_patterns['alter_enum'], content, re.IGNORECASE):
            enum_name = match.group(1)
            operation_detail = match.group(2)
            
            enum_ops.append({
                'operation': 'ALTER_ENUM',
                'enum_name': enum_name,
                'operation_detail': operation_detail,
                'line': content[:match.start()].count('\n') + 1
            })
        
        # 删除枚举类型
        for match in re.finditer(self.enum_patterns['drop_enum'], content, re.IGNORECASE):
            enum_name = match.group(1)
            
            enum_ops.append({
                'operation': 'DROP_ENUM',
                'enum_name': enum_name,
                'line': content[:match.start()].count('\n') + 1
            })
        
        # 使用枚举的列定义
        for match in re.finditer(self.enum_patterns['enum_column'], content, re.IGNORECASE):
            column_name = match.group(1)
            column_type = match.group(2)
            
            # 检查是否是已知的枚举类型
            if any(enum_name.lower() in column_type.lower() for enum_name in self.known_enums.keys()):
                enum_ops.append({
                    'operation': 'USE_ENUM_COLUMN',
                    'column_name': column_name,
                    'column_type': column_type,
                    'line': content[:match.start()].count('\n') + 1
                })
        
        return enum_ops

    def _extract_data_operations(self, content: str) -> List[Dict[str, Any]]:
        """提取数据操作"""
        data_ops = []
        
        # UPDATE语句（特别是枚举值更新）
        for match in re.finditer(self.enum_patterns['update_enum_data'], content, re.IGNORECASE):
            table_name = match.group(1)
            column_name = match.group(2)
            new_value = match.group(3)
            old_value = match.group(5)
            
            data_ops.append({
                'operation': 'UPDATE_ENUM_DATA',
                'table_name': table_name,
                'column_name': column_name,
                'old_value': old_value,
                'new_value': new_value,
                'line': content[:match.start()].count('\n') + 1
            })
        
        # 通用的op.execute操作
        execute_pattern = r"op\.execute\(['\"]([^'\"]*(?:UPDATE|INSERT|DELETE)[^'\"]*)['\"]"
        for match in re.finditer(execute_pattern, content, re.IGNORECASE | re.DOTALL):
            sql_statement = match.group(1)
            
            data_ops.append({
                'operation': 'EXECUTE_SQL',
                'sql_statement': sql_statement,
                'line': content[:match.start()].count('\n') + 1
            })
        
        return data_ops

    def _analyze_potential_issues(self, migration_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """分析潜在问题"""
        issues = []
        
        # 检查枚举值是否符合小写规范
        for enum_op in migration_info['enum_operations']:
            if enum_op['operation'] == 'CREATE_ENUM':
                enum_name = enum_op['enum_name']
                enum_values = enum_op['enum_values']
                
                # 检查是否有大写值
                uppercase_values = [v for v in enum_values if v != v.lower()]
                if uppercase_values:
                    issues.append({
                        'type': 'ENUM_CASE_VIOLATION',
                        'severity': 'ERROR',
                        'message': f"枚举 {enum_name} 包含大写值: {uppercase_values}",
                        'line': enum_op['line'],
                        'enum_name': enum_name,
                        'violating_values': uppercase_values,
                        'suggested_fix': f"将值改为小写: {[v.lower() for v in uppercase_values]}"
                    })
                
                # 检查是否与已知枚举定义一致
                if enum_name in self.known_enums:
                    expected_values = set(self.known_enums[enum_name])
                    actual_values = set(enum_values)
                    
                    missing_values = expected_values - actual_values
                    extra_values = actual_values - expected_values
                    
                    if missing_values or extra_values:
                        issues.append({
                            'type': 'ENUM_DEFINITION_MISMATCH',
                            'severity': 'WARNING',
                            'message': f"枚举 {enum_name} 定义与代码不一致",
                            'line': enum_op['line'],
                            'enum_name': enum_name,
                            'missing_values': list(missing_values),
                            'extra_values': list(extra_values),
                            'expected_values': list(expected_values),
                            'actual_values': list(actual_values)
                        })
        
        # 检查数据更新操作
        for data_op in migration_info['data_operations']:
            if data_op['operation'] == 'UPDATE_ENUM_DATA':
                old_value = data_op['old_value']
                new_value = data_op['new_value']
                
                # 检查是否是大小写转换
                if old_value.upper() == new_value.upper() and old_value != new_value:
                    issues.append({
                        'type': 'ENUM_CASE_FIX',
                        'severity': 'INFO',
                        'message': f"数据迁移修复了枚举大小写: {old_value} -> {new_value}",
                        'line': data_op['line'],
                        'table_name': data_op['table_name'],
                        'column_name': data_op['column_name'],
                        'old_value': old_value,
                        'new_value': new_value
                    })
        
        return issues

    def analyze_migration_consistency(self) -> Dict[str, Any]:
        """分析迁移一致性"""
        print("🔍 分析数据库迁移脚本...")
        
        # 查找迁移文件
        migration_files = self.find_migration_files()
        if not migration_files:
            print("❌ 未找到迁移文件")
            return {'migration_files': [], 'total_issues': 0}
        
        print(f"✅ 找到 {len(migration_files)} 个迁移文件")
        
        # 解析每个迁移文件
        all_issues = []
        all_enum_operations = []
        all_data_operations = []
        
        for file_path in migration_files:
            print(f"  📄 分析: {file_path.name}")
            
            migration_info = self.parse_migration_file(file_path)
            self.migration_files.append(migration_info)
            
            if 'error' not in migration_info:
                all_enum_operations.extend(migration_info['enum_operations'])
                all_data_operations.extend(migration_info['data_operations'])
                all_issues.extend(migration_info['potential_issues'])
        
        # 统计分析结果
        analysis_result = {
            'migration_files': self.migration_files,
            'total_migrations': len(self.migration_files),
            'total_enum_operations': len(all_enum_operations),
            'total_data_operations': len(all_data_operations),
            'total_issues': len(all_issues),
            'enum_operations': all_enum_operations,
            'data_operations': all_data_operations,
            'issues': all_issues
        }
        
        return analysis_result

    def generate_fix_suggestions(self, analysis_result: Dict[str, Any]) -> List[str]:
        """生成修复建议"""
        suggestions = []
        
        # 基于问题类型生成建议
        issues_by_type = {}
        for issue in analysis_result['issues']:
            issue_type = issue['type']
            if issue_type not in issues_by_type:
                issues_by_type[issue_type] = []
            issues_by_type[issue_type].append(issue)
        
        if 'ENUM_CASE_VIOLATION' in issues_by_type:
            suggestions.append("""
## 枚举大小写规范修复

发现迁移脚本中定义的枚举值不符合小写规范。

建议：
1. 修改迁移脚本，将枚举值改为小写
2. 添加数据迁移步骤，更新已有数据
3. 确保新建表时使用正确的枚举值

示例修复：
```python
# 错误
op.execute("CREATE TYPE parse_status_enum AS ENUM ('UPLOADED', 'PARSING', 'COMPLETED')")

# 正确  
op.execute("CREATE TYPE parse_status_enum AS ENUM ('uploaded', 'parsing', 'completed')")

# 添加数据修复
op.execute("UPDATE projects SET parse_status = 'uploaded' WHERE parse_status = 'UPLOADED'")
```
""")
        
        if 'ENUM_DEFINITION_MISMATCH' in issues_by_type:
            suggestions.append("""
## 枚举定义一致性修复

发现迁移脚本中的枚举定义与代码定义不一致。

建议：
1. 检查代码中的枚举定义
2. 确保迁移脚本与代码保持同步
3. 考虑是否需要添加或删除枚举值

修复步骤：
1. 比对代码中的枚举定义
2. 更新迁移脚本以匹配代码
3. 测试数据兼容性
""")
        
        return suggestions

    def print_analysis_report(self, analysis_result: Dict[str, Any]):
        """打印分析报告"""
        print(f"\n{'='*60}")
        print(f"📊 数据库迁移脚本分析报告")
        print(f"{'='*60}")
        
        # 总体统计
        print(f"📈 总体统计:")
        print(f"   迁移文件数: {analysis_result['total_migrations']}")
        print(f"   枚举操作数: {analysis_result['total_enum_operations']}")
        print(f"   数据操作数: {analysis_result['total_data_operations']}")
        print(f"   发现问题数: {analysis_result['total_issues']}")
        
        # 枚举操作详情
        if analysis_result['enum_operations']:
            print(f"\n📋 枚举操作详情:")
            enum_ops_by_type = {}
            for op in analysis_result['enum_operations']:
                op_type = op['operation']
                if op_type not in enum_ops_by_type:
                    enum_ops_by_type[op_type] = []
                enum_ops_by_type[op_type].append(op)
            
            for op_type, ops in enum_ops_by_type.items():
                print(f"   {op_type}: {len(ops)} 个")
        
        # 问题详情
        if analysis_result['issues']:
            print(f"\n❌ 发现的问题:")
            issues_by_severity = {'ERROR': [], 'WARNING': [], 'INFO': []}
            
            for issue in analysis_result['issues']:
                severity = issue.get('severity', 'WARNING')
                issues_by_severity[severity].append(issue)
            
            for severity, issues in issues_by_severity.items():
                if issues:
                    severity_icon = {'ERROR': '🔴', 'WARNING': '🟡', 'INFO': 'ℹ️'}[severity]
                    print(f"\n   {severity_icon} {severity} ({len(issues)} 个):")
                    
                    for issue in issues:
                        print(f"      • {issue['message']}")
                        if 'suggested_fix' in issue:
                            print(f"        建议: {issue['suggested_fix']}")
        
        # 修复建议
        suggestions = self.generate_fix_suggestions(analysis_result)
        if suggestions:
            print(f"\n💡 修复建议:")
            for suggestion in suggestions:
                print(suggestion)

    def save_analysis_report(self, analysis_result: Dict[str, Any], output_file: str):
        """保存分析报告"""
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'analysis_result': analysis_result,
            'suggestions': self.generate_fix_suggestions(analysis_result)
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"📄 详细报告已保存到: {output_file}")

    def run_analysis(self, verbose: bool = False, save_report: bool = False):
        """运行完整分析"""
        print("🚀 Excel2Doc 数据库迁移脚本分析开始...")
        print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 执行分析
        analysis_result = self.analyze_migration_consistency()
        
        # 打印报告
        self.print_analysis_report(analysis_result)
        
        # 保存报告
        if save_report:
            report_file = self.project_root / f"migration_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            self.save_analysis_report(analysis_result, str(report_file))
        
        print(f"\n🎉 数据库迁移脚本分析完成！")
        
        return analysis_result['total_issues'] == 0

def main():
    parser = argparse.ArgumentParser(
        description="Excel2Doc 数据库迁移脚本分析器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python migration_script_analyzer.py                    # 基本分析
  python migration_script_analyzer.py --verbose          # 显示详细信息
  python migration_script_analyzer.py --report           # 生成详细报告文件
        """
    )
    
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')
    parser.add_argument('--report', '-r', action='store_true', help='生成详细报告文件')
    
    args = parser.parse_args()
    
    # 获取项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    
    # 创建分析器并运行
    analyzer = MigrationScriptAnalyzer(str(project_root))
    success = analyzer.run_analysis(verbose=args.verbose, save_report=args.report)
    
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()