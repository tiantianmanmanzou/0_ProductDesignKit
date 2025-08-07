#!/usr/bin/env python3
"""
Excel2Doc 枚举使用场景静态分析器

用途:
- 分析所有枚举定义及其值
- 追踪枚举值在代码中的使用情况  
- 检查是否有硬编码字符串应该使用枚举
- 验证前后端枚举使用一致性

使用方法:
    python scripts/enum_usage_analyzer.py
    python scripts/enum_usage_analyzer.py --verbose      # 详细输出
    python scripts/enum_usage_analyzer.py --report       # 生成分析报告
"""

import ast
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict
from datetime import datetime
import argparse

@dataclass
class EnumDefinition:
    """枚举定义信息"""
    name: str
    file_path: str
    line_number: int
    values: Dict[str, str]  # key -> value
    base_classes: List[str]
    language: str  # 'python' or 'typescript'

@dataclass
class EnumUsage:
    """枚举使用信息"""
    enum_name: str
    usage_type: str  # 'direct', 'string_literal', 'hardcoded'
    file_path: str
    line_number: int
    context: str
    value: str
    language: str

@dataclass
class ConsistencyIssue:
    """一致性问题"""
    issue_type: str
    description: str
    frontend_item: Optional[str] = None
    backend_item: Optional[str] = None
    severity: str = 'warning'  # 'error', 'warning', 'info'

class EnumUsageAnalyzer:
    """枚举使用场景分析器"""
    
    def __init__(self, verbose: bool = False, generate_report: bool = False):
        self.verbose = verbose
        self.generate_report = generate_report
        
        # 分析结果存储
        self.enum_definitions: Dict[str, EnumDefinition] = {}
        self.enum_usages: List[EnumUsage] = []
        self.hardcoded_strings: List[EnumUsage] = []
        self.consistency_issues: List[ConsistencyIssue] = []
        
        # 分类存储
        self.frontend_enums: Dict[str, Dict[str, str]] = {}
        self.backend_enums: Dict[str, Dict[str, str]] = {}
        
        # 已知的枚举值模式
        self.known_enum_patterns = {
            'parse_status': r'^(uploaded|parsing|completed|failed)$',
            'task_status': r'^(pending|running|completed|failed|cancelled)$',
            'user_status': r'^(active|inactive|pending|suspended)$',
            'log_level': r'^(debug|info|warning|error|fatal)$',
            'file_type': r'^(excel|csv|json|xml|pdf)$'
        }
        
    def analyze_project(self) -> Dict[str, Any]:
        """分析整个项目的枚举使用情况"""
        print("🔍 开始项目枚举使用场景分析...")
        print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # 1. 分析后端Python代码
        print("📂 分析后端Python枚举...")
        self._analyze_backend_enums()
        
        # 2. 分析前端TypeScript代码  
        print("📂 分析前端TypeScript枚举...")
        self._analyze_frontend_enums()
        
        # 3. 查找硬编码字符串
        print("🔍 查找硬编码枚举字符串...")
        self._find_hardcoded_enum_strings()
        
        # 4. 交叉验证前后端一致性
        print("🔄 检查前后端枚举一致性...")
        self._check_frontend_backend_consistency()
        
        # 5. 生成分析报告
        return self._generate_analysis_report()
    
    def _analyze_backend_enums(self):
        """分析后端Python枚举定义和使用"""
        backend_dir = Path("backend/app")
        if not backend_dir.exists():
            print("⚠️ 后端目录不存在，跳过后端分析")
            return
        
        python_files = list(backend_dir.rglob("*.py"))
        if self.verbose:
            print(f"   找到 {len(python_files)} 个Python文件")
        
        for py_file in python_files:
            if self.verbose:
                print(f"   分析文件: {py_file}")
            self._analyze_python_file(py_file)
        
        print(f"✅ 后端分析完成: 发现 {len(self.backend_enums)} 个枚举定义")
    
    def _analyze_python_file(self, file_path: Path):
        """分析单个Python文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, FileNotFoundError):
            return
        
        try:
            tree = ast.parse(content)
        except SyntaxError:
            if self.verbose:
                print(f"     语法错误，跳过文件: {file_path}")
            return
        
        # 使用AST分析枚举定义
        enum_visitor = EnumDefinitionVisitor(file_path, 'python')
        enum_visitor.visit(tree)
        
        for enum_def in enum_visitor.enums:
            self.enum_definitions[f"{enum_def.name}_backend"] = enum_def
            self.backend_enums[enum_def.name] = enum_def.values
        
        # 查找枚举使用
        usage_visitor = EnumUsageVisitor(file_path, self.enum_definitions, 'python')
        usage_visitor.visit(tree)
        self.enum_usages.extend(usage_visitor.usages)
        
        # 查找可能的硬编码字符串
        self._find_hardcoded_in_python_file(file_path, content)
    
    def _analyze_frontend_enums(self):
        """分析前端TypeScript枚举定义和使用"""
        frontend_dir = Path("frontend/src")
        if not frontend_dir.exists():
            print("⚠️ 前端目录不存在，跳过前端分析")
            return
        
        ts_files = list(frontend_dir.rglob("*.ts")) + list(frontend_dir.rglob("*.tsx"))
        if self.verbose:
            print(f"   找到 {len(ts_files)} 个TypeScript文件")
        
        for ts_file in ts_files:
            if self.verbose:
                print(f"   分析文件: {ts_file}")
            self._analyze_typescript_file(ts_file)
        
        print(f"✅ 前端分析完成: 发现 {len(self.frontend_enums)} 个枚举定义")
    
    def _analyze_typescript_file(self, file_path: Path):
        """分析单个TypeScript文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, FileNotFoundError):
            return
        
        # 使用正则表达式分析TypeScript枚举
        self._find_typescript_enums(file_path, content)
        self._find_hardcoded_in_typescript_file(file_path, content)
    
    def _find_typescript_enums(self, file_path: Path, content: str):
        """查找TypeScript枚举定义"""
        # 匹配enum定义
        enum_pattern = r'enum\s+(\w+)\s*\{([^}]*)\}'
        enums = re.finditer(enum_pattern, content, re.DOTALL)
        
        for match in enums:
            enum_name = match.group(1)
            enum_body = match.group(2)
            line_num = content[:match.start()].count('\n') + 1
            
            # 提取枚举值
            enum_values = {}
            value_pattern = r'(\w+)\s*=\s*[\'"]([^\'\"]*)[\'"]'
            values = re.finditer(value_pattern, enum_body)
            
            for value_match in values:
                key = value_match.group(1)
                value = value_match.group(2)
                enum_values[key] = value
            
            # 存储枚举定义
            enum_def = EnumDefinition(
                name=enum_name,
                file_path=str(file_path),
                line_number=line_num,
                values=enum_values,
                base_classes=[],
                language='typescript'
            )
            
            self.enum_definitions[f"{enum_name}_frontend"] = enum_def
            self.frontend_enums[enum_name] = enum_values
        
        # 匹配type联合类型（类似枚举）
        type_pattern = r'type\s+(\w+)\s*=\s*([^;]+);'
        types = re.finditer(type_pattern, content)
        
        for match in types:
            type_name = match.group(1)
            type_def = match.group(2).strip()
            
            # 检查是否是字符串联合类型
            if "'" in type_def or '"' in type_def:
                line_num = content[:match.start()].count('\n') + 1
                
                # 提取字符串值
                string_values = re.findall(r'[\'"]([^\'"]*)[\'"]', type_def)
                if string_values:
                    enum_values = {f"VALUE_{i}": value for i, value in enumerate(string_values)}
                    
                    enum_def = EnumDefinition(
                        name=type_name,
                        file_path=str(file_path),
                        line_number=line_num,
                        values=enum_values,
                        base_classes=[],
                        language='typescript'
                    )
                    
                    self.enum_definitions[f"{type_name}_frontend"] = enum_def
                    self.frontend_enums[type_name] = enum_values
    
    def _find_hardcoded_in_python_file(self, file_path: Path, content: str):
        """在Python文件中查找硬编码枚举字符串"""
        # 查找字符串字面量
        string_pattern = r'[\'"]([^\'"]+)[\'"]'
        matches = re.finditer(string_pattern, content)
        
        for match in matches:
            string_value = match.group(1)
            
            # 检查是否匹配已知枚举模式
            for enum_type, pattern in self.known_enum_patterns.items():
                if re.match(pattern, string_value.lower()):
                    line_num = content[:match.start()].count('\n') + 1
                    context = self._get_line_context(content, match.start())
                    
                    self.hardcoded_strings.append(EnumUsage(
                        enum_name=enum_type,
                        usage_type='hardcoded',
                        file_path=str(file_path),
                        line_number=line_num,
                        context=context,
                        value=string_value,
                        language='python'
                    ))
    
    def _find_hardcoded_in_typescript_file(self, file_path: Path, content: str):
        """在TypeScript文件中查找硬编码枚举字符串"""
        # 查找字符串字面量
        string_pattern = r'[\'"]([^\'"]+)[\'"]'
        matches = re.finditer(string_pattern, content)
        
        for match in matches:
            string_value = match.group(1)
            
            # 检查是否匹配已知枚举模式
            for enum_type, pattern in self.known_enum_patterns.items():
                if re.match(pattern, string_value.lower()):
                    line_num = content[:match.start()].count('\n') + 1
                    context = self._get_line_context(content, match.start())
                    
                    self.hardcoded_strings.append(EnumUsage(
                        enum_name=enum_type,
                        usage_type='hardcoded',
                        file_path=str(file_path),
                        line_number=line_num,
                        context=context,
                        value=string_value,
                        language='typescript'
                    ))
    
    def _find_hardcoded_enum_strings(self):
        """在所有文件中查找硬编码枚举字符串"""
        total_hardcoded = len(self.hardcoded_strings)
        
        if total_hardcoded > 0:
            print(f"⚠️ 发现 {total_hardcoded} 个可能的硬编码枚举字符串")
            
            if self.verbose:
                by_type = defaultdict(int)
                for usage in self.hardcoded_strings:
                    by_type[usage.enum_name] += 1
                
                for enum_type, count in by_type.items():
                    print(f"   {enum_type}: {count} 个")
        else:
            print("✅ 未发现明显的硬编码枚举字符串")
    
    def _check_frontend_backend_consistency(self):
        """检查前后端枚举一致性"""
        # 寻找可能对应的前后端枚举
        potential_matches = []
        
        for frontend_enum, frontend_values in self.frontend_enums.items():
            for backend_enum, backend_values in self.backend_enums.items():
                # 基于名称相似性匹配
                similarity_score = self._calculate_name_similarity(frontend_enum, backend_enum)
                if similarity_score > 0.6:  # 60%以上相似度
                    potential_matches.append((frontend_enum, backend_enum, similarity_score))
        
        # 对匹配结果进行分析
        for frontend_enum, backend_enum, score in potential_matches:
            frontend_values = set(self.frontend_enums[frontend_enum].values())
            backend_values = set(self.backend_enums[backend_enum].values())
            
            # 检查值的一致性
            missing_in_frontend = backend_values - frontend_values
            missing_in_backend = frontend_values - backend_values
            
            if missing_in_frontend:
                self.consistency_issues.append(ConsistencyIssue(
                    issue_type='missing_enum_values',
                    description=f'前端枚举 {frontend_enum} 缺少值: {missing_in_frontend}',
                    frontend_item=frontend_enum,
                    backend_item=backend_enum,
                    severity='warning'
                ))
            
            if missing_in_backend:
                self.consistency_issues.append(ConsistencyIssue(
                    issue_type='missing_enum_values', 
                    description=f'后端枚举 {backend_enum} 缺少值: {missing_in_backend}',
                    frontend_item=frontend_enum,
                    backend_item=backend_enum,
                    severity='warning'
                ))
        
        if self.consistency_issues:
            print(f"⚠️ 发现 {len(self.consistency_issues)} 个前后端一致性问题")
        else:
            print("✅ 前后端枚举一致性检查通过")
    
    def _calculate_name_similarity(self, name1: str, name2: str) -> float:
        """计算两个名称的相似度"""
        name1_lower = name1.lower()
        name2_lower = name2.lower()
        
        # 简单的相似度计算
        if name1_lower == name2_lower:
            return 1.0
        
        # 检查是否包含共同的关键词
        keywords1 = set(re.findall(r'\w+', name1_lower))
        keywords2 = set(re.findall(r'\w+', name2_lower))
        
        if not keywords1 or not keywords2:
            return 0.0
        
        intersection = keywords1 & keywords2
        union = keywords1 | keywords2
        
        return len(intersection) / len(union)
    
    def _get_line_context(self, content: str, position: int, context_lines: int = 1) -> str:
        """获取指定位置的代码上下文"""
        lines = content[:position].split('\n')
        line_num = len(lines) - 1
        all_lines = content.split('\n')
        
        start = max(0, line_num - context_lines)
        end = min(len(all_lines), line_num + context_lines + 1)
        
        context_lines_content = []
        for i in range(start, end):
            prefix = ">>> " if i == line_num else "    "
            context_lines_content.append(f"{prefix}{all_lines[i]}")
        
        return '\n'.join(context_lines_content)
    
    def _generate_analysis_report(self) -> Dict[str, Any]:
        """生成分析报告"""
        print("\n" + "="*50)
        print("📊 枚举使用场景分析报告")
        print("="*50)
        
        # 统计信息
        total_enums = len(self.enum_definitions)
        frontend_enum_count = len(self.frontend_enums)
        backend_enum_count = len(self.backend_enums)
        hardcoded_count = len(self.hardcoded_strings)
        consistency_issues_count = len(self.consistency_issues)
        
        print(f"\n📈 统计概览:")
        print(f"   枚举定义总数: {total_enums}")
        print(f"   前端枚举: {frontend_enum_count}")
        print(f"   后端枚举: {backend_enum_count}")
        print(f"   硬编码字符串: {hardcoded_count}")
        print(f"   一致性问题: {consistency_issues_count}")
        
        # 详细的枚举列表
        if self.verbose:
            if self.frontend_enums:
                print(f"\n📂 前端枚举详情:")
                for name, values in self.frontend_enums.items():
                    print(f"   • {name}: {list(values.values())}")
            
            if self.backend_enums:
                print(f"\n📂 后端枚举详情:")
                for name, values in self.backend_enums.items():
                    print(f"   • {name}: {list(values.values())}")
        
        # 硬编码字符串问题
        if hardcoded_count > 0:
            print(f"\n⚠️ 硬编码枚举字符串问题:")
            hardcoded_by_type = defaultdict(list)
            for usage in self.hardcoded_strings:
                hardcoded_by_type[usage.enum_name].append(usage)
            
            for enum_type, usages in hardcoded_by_type.items():
                print(f"   📋 {enum_type} ({len(usages)} 处):")
                for usage in usages[:3]:  # 只显示前3个
                    print(f"      • {usage.file_path}:{usage.line_number} - '{usage.value}'")
                if len(usages) > 3:
                    print(f"      • ... 还有 {len(usages) - 3} 处")
        
        # 一致性问题
        if consistency_issues_count > 0:
            print(f"\n🔄 前后端一致性问题:")
            for issue in self.consistency_issues:
                print(f"   • {issue.description}")
        
        # 生成报告数据
        report_data = {
            'summary': {
                'total_enums': total_enums,
                'frontend_enums': frontend_enum_count,
                'backend_enums': backend_enum_count,
                'hardcoded_strings': hardcoded_count,
                'consistency_issues': consistency_issues_count,
                'analysis_time': datetime.now().isoformat()
            },
            'enum_definitions': {k: asdict(v) for k, v in self.enum_definitions.items()},
            'hardcoded_strings': [asdict(usage) for usage in self.hardcoded_strings],
            'consistency_issues': [asdict(issue) for issue in self.consistency_issues]
        }
        
        # 保存报告文件
        if self.generate_report:
            report_file = Path('enum-usage-analysis-report.json')
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n📄 详细分析报告已保存至: {report_file}")
        
        # 生成改进建议
        self._generate_improvement_suggestions()
        
        return report_data
    
    def _generate_improvement_suggestions(self):
        """生成改进建议"""
        print(f"\n💡 改进建议:")
        
        suggestions = []
        
        if len(self.hardcoded_strings) > 0:
            suggestions.append("1. 将硬编码字符串替换为枚举值使用")
            suggestions.append("   - 创建或使用现有枚举定义")
            suggestions.append("   - 统一枚举值的命名格式（建议小写）")
        
        if len(self.consistency_issues) > 0:
            suggestions.append("2. 解决前后端枚举一致性问题")
            suggestions.append("   - 统一前后端枚举值定义")
            suggestions.append("   - 建立枚举值同步机制")
        
        if len(self.frontend_enums) == 0 or len(self.backend_enums) == 0:
            suggestions.append("3. 完善枚举定义")
            suggestions.append("   - 为状态值创建明确的枚举定义")
            suggestions.append("   - 避免在代码中直接使用字符串字面量")
        
        if not suggestions:
            suggestions.append("✅ 当前枚举使用符合最佳实践")
        
        for suggestion in suggestions:
            print(f"   {suggestion}")

class EnumDefinitionVisitor(ast.NodeVisitor):
    """AST访问器：查找Python枚举定义"""
    
    def __init__(self, file_path: Path, language: str):
        self.file_path = file_path
        self.language = language
        self.enums: List[EnumDefinition] = []
        
    def visit_ClassDef(self, node: ast.ClassDef):
        # 检查是否继承自Enum
        base_names = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_names.append(base.id)
            elif isinstance(base, ast.Attribute):
                base_names.append(f"{base.value.id}.{base.attr}" if isinstance(base.value, ast.Name) else base.attr)
        
        if any('Enum' in name for name in base_names):
            enum_values = {}
            
            for item in node.body:
                if isinstance(item, ast.Assign):
                    # 处理赋值语句 ENUM_KEY = "enum_value"
                    if len(item.targets) == 1 and isinstance(item.targets[0], ast.Name):
                        key = item.targets[0].id
                        if isinstance(item.value, ast.Constant):
                            enum_values[key] = str(item.value.value)
            
            self.enums.append(EnumDefinition(
                name=node.name,
                file_path=str(self.file_path),
                line_number=node.lineno,
                values=enum_values,
                base_classes=base_names,
                language=self.language
            ))
        
        self.generic_visit(node)

class EnumUsageVisitor(ast.NodeVisitor):
    """AST访问器：查找Python枚举使用"""
    
    def __init__(self, file_path: Path, enum_definitions: Dict[str, EnumDefinition], language: str):
        self.file_path = file_path
        self.enum_definitions = enum_definitions
        self.language = language
        self.usages: List[EnumUsage] = []
    
    def visit_Attribute(self, node: ast.Attribute):
        # 查找 EnumClass.VALUE 形式的使用
        if isinstance(node.value, ast.Name):
            enum_name = node.value.id
            # 检查是否是已知枚举
            for def_key, enum_def in self.enum_definitions.items():
                if enum_def.name == enum_name and enum_def.language == self.language:
                    self.usages.append(EnumUsage(
                        enum_name=enum_name,
                        usage_type='direct',
                        file_path=str(self.file_path),
                        line_number=node.lineno,
                        context=f"{enum_name}.{node.attr}",
                        value=node.attr,
                        language=self.language
                    ))
        
        self.generic_visit(node)

def main():
    parser = argparse.ArgumentParser(description='Excel2Doc枚举使用场景分析工具')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细输出')
    parser.add_argument('--report', '-r', action='store_true', help='生成详细JSON分析报告')
    
    args = parser.parse_args()
    
    if not Path('frontend').exists() and not Path('backend').exists():
        print("❌ 错误: 未找到frontend或backend目录")
        print("请在Excel2Doc项目根目录下运行此脚本")
        return 1
    
    analyzer = EnumUsageAnalyzer(verbose=args.verbose, generate_report=args.report)
    analyzer.analyze_project()
    
    print(f"\n🎉 枚举使用场景分析完成！")
    return 0

if __name__ == "__main__":
    exit(main())