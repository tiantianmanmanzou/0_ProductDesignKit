#!/usr/bin/env python3
"""
Excel2Doc 命名规范检查脚本

用途:
- 检查前后端代码是否符合命名规范
- 识别snake_case和camelCase混用问题
- 验证枚举值格式一致性
- 检查API字段名规范

使用方法:
    python scripts/check_naming_convention.py
    python scripts/check_naming_convention.py --fix  # 自动修复部分问题
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class NamingViolation:
    """命名规范违规记录"""
    file_path: str
    line_number: int
    violation_type: str
    current_name: str
    suggested_name: str
    message: str
    severity: str  # 'error', 'warning', 'info'

class NamingConventionChecker:
    """命名规范检查器"""
    
    def __init__(self, fix_mode: bool = False):
        self.violations: List[NamingViolation] = []
        self.fix_mode = fix_mode
        self.stats = defaultdict(int)
        
        # 允许的例外情况
        self.allowed_snake_case_fields = {
            'created_at', 'updated_at', 'excel_file', 'file_path', 'file_size',
            'parse_status', 'project_id', 'column_name', 'column_type',
            'is_active', 'module_level', 'summary_content', 'module_name',
            'module_path', 'key_fields', 'extractor_type', 'generation_config'
        }
        
        # 允许的大写枚举值
        self.allowed_uppercase_enum_values = {
            'UUID', 'URL', 'API', 'HTTP', 'HTTPS', 'JSON', 'XML'
        }
        
        # 新增：已知枚举值模式配置
        self.enum_value_patterns = {
            'status': ['uploaded', 'parsing', 'completed', 'failed'],
            'state': ['active', 'inactive', 'pending'],
            'level': ['info', 'warning', 'error', 'debug'],
            'type': ['excel', 'csv', 'json', 'xml']
        }
        
        # 新增：忽略的硬编码字符串
        self.ignored_hardcoded_strings = {
            'utf-8', 'application/json', 'text/html', 
            'GET', 'POST', 'PUT', 'DELETE', 'PATCH',
            'localhost', '127.0.0.1', 'http', 'https'
        }

    def check_all_files(self) -> bool:
        """检查所有相关文件"""
        print("🔍 Excel2Doc 命名规范检查开始...")
        print()
        
        # 检查前端文件
        frontend_dir = Path("frontend/src")
        if frontend_dir.exists():
            print("📂 检查前端文件...")
            self._check_frontend_directory(frontend_dir)
            
        # 检查后端文件
        backend_dir = Path("backend/app")
        if backend_dir.exists():
            print("📂 检查后端文件...")
            self._check_backend_directory(backend_dir)
            
        # 输出检查结果
        return self._report_results()

    def _check_frontend_directory(self, frontend_dir: Path) -> None:
        """检查前端目录"""
        for file_path in frontend_dir.rglob("*.ts"):
            if not any(part in str(file_path) for part in ['node_modules', 'dist', '.next']):
                self._check_frontend_file(file_path)
                
        for file_path in frontend_dir.rglob("*.tsx"):
            if not any(part in str(file_path) for part in ['node_modules', 'dist', '.next']):
                self._check_frontend_file(file_path)

    def _check_backend_directory(self, backend_dir: Path) -> None:
        """检查后端目录"""
        for file_path in backend_dir.rglob("*.py"):
            if not any(part in str(file_path) for part in ['__pycache__', 'migrations', '.venv']):
                self._check_backend_file(file_path)

    def _check_frontend_file(self, file_path: Path) -> None:
        """检查前端TypeScript文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, FileNotFoundError):
            return

        lines = content.split('\n')
        
        # 检查接口定义中的字段命名
        self._check_interface_fields(file_path, content, lines)
        
        # 检查变量命名
        self._check_variable_naming(file_path, content, lines)
        
        # 检查组件文件命名
        self._check_component_file_naming(file_path)
        
        # 检查枚举定义
        self._check_frontend_enum_values(file_path, content, lines)

    def _check_backend_file(self, file_path: Path) -> None:
        """检查后端Python文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, FileNotFoundError):
            return

        lines = content.split('\n')
        
        # 检查类命名
        self._check_class_naming(file_path, content, lines)
        
        # 检查枚举值格式
        self._check_backend_enum_values(file_path, content, lines)
        
        # 检查Pydantic Schema字段
        self._check_schema_fields(file_path, content, lines)
        
        # 检查API响应字段
        self._check_api_response_fields(file_path, content, lines)
        
        # 新增：检查硬编码枚举字符串
        self._check_hardcoded_enum_strings(file_path, content, lines)

    def _check_interface_fields(self, file_path: Path, content: str, lines: List[str]) -> None:
        """检查TypeScript接口字段命名"""
        # 匹配接口定义
        interface_pattern = r'interface\s+(\w+)\s*\{([^}]*)\}'
        interfaces = re.finditer(interface_pattern, content, re.DOTALL)
        
        for match in interfaces:
            interface_name = match.group(1)
            interface_body = match.group(2)
            
            # 查找snake_case字段
            field_pattern = r'(\w+_\w+)\s*[?:]'
            snake_fields = re.finditer(field_pattern, interface_body)
            
            for field_match in snake_fields:
                field_name = field_match.group(1)
                
                # 跳过允许的例外
                if field_name in self.allowed_snake_case_fields:
                    continue
                
                line_num = self._get_line_number(content, field_match.start())
                suggested_name = self._snake_to_camel(field_name)
                
                self.violations.append(NamingViolation(
                    file_path=str(file_path),
                    line_number=line_num,
                    violation_type='frontend_interface_snake_case',
                    current_name=field_name,
                    suggested_name=suggested_name,
                    message=f'Interface "{interface_name}" field "{field_name}" should use camelCase: "{suggested_name}"',
                    severity='error'
                ))
                self.stats['frontend_snake_case_fields'] += 1

    def _check_variable_naming(self, file_path: Path, content: str, lines: List[str]) -> None:
        """检查变量命名规范"""
        # 检查const和let声明
        var_pattern = r'(const|let|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[=:]'
        variables = re.finditer(var_pattern, content)
        
        for match in variables:
            var_type = match.group(1)
            var_name = match.group(2)
            
            # 跳过合理的命名
            if var_name.startswith('_') or var_name.upper() == var_name:
                continue
                
            if '_' in var_name and not var_name.upper() == var_name:
                line_num = self._get_line_number(content, match.start())
                suggested_name = self._snake_to_camel(var_name)
                
                self.violations.append(NamingViolation(
                    file_path=str(file_path),
                    line_number=line_num,
                    violation_type='frontend_variable_snake_case',
                    current_name=var_name,
                    suggested_name=suggested_name,
                    message=f'Variable "{var_name}" should use camelCase: "{suggested_name}"',
                    severity='warning'
                ))
                self.stats['frontend_snake_case_variables'] += 1

    def _check_component_file_naming(self, file_path: Path) -> None:
        """检查组件文件命名"""
        file_name = file_path.stem
        
        # 组件文件应该使用PascalCase
        if file_path.parent.name in ['components', 'pages'] and file_name != 'index':
            if not self._is_pascal_case(file_name):
                self.violations.append(NamingViolation(
                    file_path=str(file_path),
                    line_number=1,
                    violation_type='frontend_component_file_naming',
                    current_name=file_name,
                    suggested_name=self._to_pascal_case(file_name),
                    message=f'Component file "{file_name}" should use PascalCase',
                    severity='warning'
                ))
                self.stats['frontend_file_naming'] += 1

    def _check_frontend_enum_values(self, file_path: Path, content: str, lines: List[str]) -> None:
        """检查前端枚举值"""
        # 匹配TypeScript枚举
        enum_pattern = r'enum\s+(\w+)\s*\{([^}]*)\}'
        enums = re.finditer(enum_pattern, content, re.DOTALL)
        
        for match in enums:
            enum_name = match.group(1)
            enum_body = match.group(2)
            
            # 查找枚举值
            value_pattern = r'(\w+)\s*=\s*[\'"]([^\'"]*)[\'"]'
            enum_values = re.finditer(value_pattern, enum_body)
            
            for value_match in enum_values:
                enum_key = value_match.group(1)
                enum_value = value_match.group(2)
                
                # 检查枚举值是否为小写
                if enum_value.isupper() and enum_value not in self.allowed_uppercase_enum_values:
                    line_num = self._get_line_number(content, value_match.start())
                    suggested_value = enum_value.lower()
                    
                    self.violations.append(NamingViolation(
                        file_path=str(file_path),
                        line_number=line_num,
                        violation_type='frontend_enum_uppercase',
                        current_name=enum_value,
                        suggested_name=suggested_value,
                        message=f'Enum "{enum_name}" value "{enum_value}" should be lowercase: "{suggested_value}"',
                        severity='error'
                    ))
                    self.stats['frontend_enum_values'] += 1

    def _check_class_naming(self, file_path: Path, content: str, lines: List[str]) -> None:
        """检查Python类命名"""
        class_pattern = r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        classes = re.finditer(class_pattern, content)
        
        for match in classes:
            class_name = match.group(1)
            
            if not self._is_pascal_case(class_name):
                line_num = self._get_line_number(content, match.start())
                suggested_name = self._to_pascal_case(class_name)
                
                self.violations.append(NamingViolation(
                    file_path=str(file_path),
                    line_number=line_num,
                    violation_type='backend_class_naming',
                    current_name=class_name,
                    suggested_name=suggested_name,
                    message=f'Class "{class_name}" should use PascalCase: "{suggested_name}"',
                    severity='error'
                ))
                self.stats['backend_class_naming'] += 1

    def _check_backend_enum_values(self, file_path: Path, content: str, lines: List[str]) -> None:
        """检查Python枚举值格式"""
        # 匹配枚举类定义和其内容
        enum_pattern = r'class\s+(\w+Enum).*?:\s*(.*?)(?=\n\n|\nclass|\ndef|\nif|\Z)'
        enums = re.finditer(enum_pattern, content, re.DOTALL)
        
        for match in enums:
            enum_name = match.group(1)
            enum_body = match.group(2)
            
            # 查找枚举值赋值
            value_pattern = r'(\w+)\s*=\s*[\'"]([^\'"]*)[\'"]'
            enum_values = re.finditer(value_pattern, enum_body)
            
            for value_match in enum_values:
                enum_key = value_match.group(1)
                enum_value = value_match.group(2)
                
                # 检查是否为大写值（应该改为小写）
                if enum_value.isupper() and enum_value not in self.allowed_uppercase_enum_values:
                    line_num = self._get_line_number(content, match.start() + value_match.start())
                    suggested_value = enum_value.lower()
                    
                    self.violations.append(NamingViolation(
                        file_path=str(file_path),
                        line_number=line_num,
                        violation_type='backend_enum_uppercase',
                        current_name=enum_value,
                        suggested_name=suggested_value,
                        message=f'Enum "{enum_name}" value "{enum_value}" should be lowercase: "{suggested_value}"',
                        severity='error'
                    ))
                    self.stats['backend_enum_values'] += 1

    def _check_schema_fields(self, file_path: Path, content: str, lines: List[str]) -> None:
        """检查Pydantic Schema字段alias使用"""
        if 'schemas' not in str(file_path):
            return
            
        # 查找没有使用alias的snake_case字段
        field_pattern = r'(\w+_\w+)\s*:\s*.*?(?:Field\([^)]*alias\s*=\s*[\'"](\w+)[\'"]|Field\([^)]*\)|=\s*Field\([^)]*\)|$)'
        fields = re.finditer(field_pattern, content)
        
        for match in fields:
            field_name = match.group(1)
            alias = match.group(2) if len(match.groups()) > 1 else None
            
            if field_name in self.allowed_snake_case_fields and not alias:
                line_num = self._get_line_number(content, match.start())
                suggested_alias = self._snake_to_camel(field_name)
                
                self.violations.append(NamingViolation(
                    file_path=str(file_path),
                    line_number=line_num,
                    violation_type='backend_schema_missing_alias',
                    current_name=field_name,
                    suggested_name=f'{field_name} = Field(..., alias="{suggested_alias}")',
                    message=f'Schema field "{field_name}" should have camelCase alias: "{suggested_alias}"',
                    severity='warning'
                ))
                self.stats['backend_schema_fields'] += 1

    def _check_api_response_fields(self, file_path: Path, content: str, lines: List[str]) -> None:
        """检查API响应字段格式"""
        if 'api' not in str(file_path):
            return
            
        # 查找字典构造中的snake_case键
        dict_pattern = r'[\'"]([a-zA-Z_][a-zA-Z0-9_]*)[\'"]:\s*[^,}]+'
        dict_keys = re.finditer(dict_pattern, content)
        
        for match in dict_keys:
            key_name = match.group(1)
            
            if '_' in key_name and key_name not in self.allowed_snake_case_fields:
                line_num = self._get_line_number(content, match.start())
                suggested_key = self._snake_to_camel(key_name)
                
                self.violations.append(NamingViolation(
                    file_path=str(file_path),
                    line_number=line_num,
                    violation_type='backend_api_snake_case_key',
                    current_name=key_name,
                    suggested_name=suggested_key,
                    message=f'API response key "{key_name}" should use camelCase: "{suggested_key}"',
                    severity='error'
                ))
                self.stats['backend_api_keys'] += 1

    def _check_hardcoded_enum_strings(self, file_path: Path, content: str, lines: List[str]) -> None:
        """检查硬编码字符串是否应该使用枚举值"""
        
        # 1. 先收集所有枚举定义
        enum_values = self._collect_enum_values(content)
        
        # 2. 检查字符串赋值语句
        string_assignments = [
            r'(\w+)\s*=\s*[\'"]([^\'"]*)[\'"]',  # variable = "string"
            r'[\'"](\w+)[\'"]:\s*[\'"]([^\'"]*)[\'"]',  # "key": "value"  
            r'\.append\([\'"]([^\'"]*)[\'"]',  # .append("string")
            r'Field\([^)]*default\s*=\s*[\'"]([^\'"]*)[\'"]'  # Field(default="string")
        ]
        
        for pattern in string_assignments:
            matches = re.finditer(pattern, content)
            for match in matches:
                # 获取最后一个捕获组
                string_value = match.group(match.lastindex) if match.lastindex else ""
                
                # 检查是否应该使用枚举
                if self._should_use_enum(string_value, enum_values):
                    line_num = self._get_line_number(content, match.start())
                    enum_suggestion = self._get_enum_suggestion(string_value, enum_values)
                    
                    self.violations.append(NamingViolation(
                        file_path=str(file_path),
                        line_number=line_num,
                        violation_type='hardcoded_enum_string',
                        current_name=f'"{string_value}"',
                        suggested_name=enum_suggestion,
                        message=f'String "{string_value}" should use enum: {enum_suggestion}',
                        severity='warning'
                    ))
                    self.stats['hardcoded_enum_strings'] += 1

    def _collect_enum_values(self, content: str) -> Dict[str, str]:
        """收集所有枚举值映射"""
        enum_values = {}
        
        # Python 枚举
        enum_pattern = r'class\s+(\w+Enum).*?:\s*(.*?)(?=\n\n|\nclass|\ndef|\nif|\Z)'
        enums = re.finditer(enum_pattern, content, re.DOTALL)
        
        for match in enums:
            enum_name = match.group(1)
            enum_body = match.group(2)
            
            # 提取枚举值
            value_pattern = r'(\w+)\s*=\s*[\'"]([^\'"]*)[\'"]'
            values = re.finditer(value_pattern, enum_body)
            
            for value_match in values:
                enum_key = value_match.group(1)
                enum_value = value_match.group(2)
                enum_values[enum_value] = f'{enum_name}.{enum_key}.value'
                # 也检查大小写变体
                enum_values[enum_value.upper()] = f'{enum_name}.{enum_key}.value'
                enum_values[enum_value.lower()] = f'{enum_name}.{enum_key}.value'
        
        return enum_values

    def _should_use_enum(self, string_value: str, enum_values: Dict[str, str]) -> bool:
        """判断字符串是否应该使用枚举"""
        # 跳过忽略列表中的字符串
        if string_value in self.ignored_hardcoded_strings:
            return False
        
        # 检查已知的枚举值模式
        known_enum_patterns = [
            r'^(uploaded|parsing|completed|failed)$',
            r'^(active|inactive|pending)$', 
            r'^(success|error|warning|info)$',
            r'^(draft|published|archived)$'
        ]
        
        for pattern in known_enum_patterns:
            if re.match(pattern, string_value.lower()):
                return True
        
        # 检查是否在已收集的枚举值中
        return (string_value in enum_values or 
                string_value.upper() in enum_values or 
                string_value.lower() in enum_values)

    def _get_enum_suggestion(self, string_value: str, enum_values: Dict[str, str]) -> str:
        """获取枚举使用建议"""
        # 直接匹配
        if string_value in enum_values:
            return enum_values[string_value]
        
        # 大小写匹配
        if string_value.upper() in enum_values:
            return enum_values[string_value.upper()]
        
        if string_value.lower() in enum_values:
            return enum_values[string_value.lower()]
        
        # 根据模式推荐
        if re.match(r'^(uploaded|parsing|completed|failed)$', string_value.lower()):
            return f'ParseStatusEnum.{string_value.upper()}.value'
        
        return f'SomeEnum.{string_value.upper()}.value'

    def _get_line_number(self, content: str, position: int) -> int:
        """根据字符位置计算行号"""
        return content[:position].count('\n') + 1

    def _snake_to_camel(self, snake_str: str) -> str:
        """将snake_case转换为camelCase"""
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    def _is_pascal_case(self, name: str) -> bool:
        """检查是否为PascalCase格式"""
        return name[0].isupper() and '_' not in name

    def _to_pascal_case(self, name: str) -> str:
        """转换为PascalCase格式"""
        if '_' in name:
            components = name.split('_')
            return ''.join(x.title() for x in components)
        else:
            return name.title()

    def _report_results(self) -> bool:
        """输出检查结果"""
        print()
        
        if not self.violations:
            print("✅ 所有文件都符合命名规范!")
            print()
            return True

        # 按严重程度分组
        error_violations = [v for v in self.violations if v.severity == 'error']
        warning_violations = [v for v in self.violations if v.severity == 'warning']
        
        print(f"❌ 发现 {len(self.violations)} 个命名规范问题:")
        print(f"   🔴 错误: {len(error_violations)} 个")  
        print(f"   🟡 警告: {len(warning_violations)} 个")
        print()

        # 按文件分组显示
        violations_by_file = defaultdict(list)
        for violation in self.violations:
            violations_by_file[violation.file_path].append(violation)

        for file_path, file_violations in violations_by_file.items():
            print(f"📁 {file_path}")
            for violation in sorted(file_violations, key=lambda x: x.line_number):
                severity_icon = '🔴' if violation.severity == 'error' else '🟡'
                print(f"   {severity_icon} 第{violation.line_number}行: {violation.message}")
            print()

        # 统计信息
        if self.stats:
            print("📊 问题统计:")
            for category, count in self.stats.items():
                print(f"   {category}: {count}")
            print()

        # 修复建议
        if error_violations:
            print("🔧 修复建议:")
            print("   1. 优先修复错误级别的问题")
            print("   2. 统一API响应字段为camelCase格式")
            print("   3. 统一枚举值为小写格式")
            print("   4. 为Pydantic字段添加camelCase别名")
            print()

        return len(error_violations) == 0

def main():
    parser = argparse.ArgumentParser(description='Excel2Doc命名规范检查工具')
    parser.add_argument('--fix', action='store_true', help='自动修复部分问题（暂未实现）')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')
    
    args = parser.parse_args()
    
    if not os.path.exists('frontend') and not os.path.exists('backend'):
        print("❌ 错误: 未找到frontend或backend目录")
        print("请在Excel2Doc项目根目录下运行此脚本")
        sys.exit(1)

    checker = NamingConventionChecker(fix_mode=args.fix)
    success = checker.check_all_files()
    
    if args.fix:
        print("⚠️  自动修复功能正在开发中...")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()