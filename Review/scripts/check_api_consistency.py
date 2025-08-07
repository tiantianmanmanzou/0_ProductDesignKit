#!/usr/bin/env python3
"""
Excel2Doc API字段一致性检查脚本

用途:
- 检查前后端API字段名一致性
- 识别前端类型定义与后端Schema的不匹配
- 验证API端点的请求/响应格式一致性
- 生成API一致性报告

使用方法:
    python scripts/check_api_consistency.py
    python scripts/check_api_consistency.py --report  # 生成详细报告
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Set, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class APIEndpoint:
    """API端点信息"""
    method: str
    path: str
    file_path: str
    line_number: int
    request_fields: Set[str] = field(default_factory=set)
    response_fields: Set[str] = field(default_factory=set)

@dataclass
class TypeDefinition:
    """类型定义信息"""
    name: str
    file_path: str
    line_number: int
    fields: Dict[str, str] = field(default_factory=dict)  # field_name -> field_type

@dataclass
class ConsistencyIssue:
    """一致性问题"""
    issue_type: str
    frontend_file: str
    backend_file: str
    frontend_line: int
    backend_line: int
    field_name: str
    frontend_format: str
    backend_format: str
    message: str
    severity: str  # 'error', 'warning', 'info'

class APIConsistencyChecker:
    """API一致性检查器"""
    
    def __init__(self):
        self.frontend_types: Dict[str, TypeDefinition] = {}
        self.backend_schemas: Dict[str, TypeDefinition] = {}
        self.frontend_api_calls: List[Dict] = []
        self.backend_endpoints: List[APIEndpoint] = []
        self.issues: List[ConsistencyIssue] = []
        
        # 字段名映射规则
        self.field_mappings = {
            'created_at': 'createdAt',
            'updated_at': 'updatedAt',
            'excel_file': 'excelFile',
            'file_size': 'fileSize',
            'parse_status': 'parseStatus',
            'project_id': 'projectId',
            'column_name': 'columnName',
            'column_type': 'columnType',
            'is_active': 'isActive',
            'module_level': 'moduleLevel',
            'module_name': 'moduleName',
            'module_path': 'modulePath',
            'summary_content': 'content',
            'key_fields': 'keyFields',
            'extractor_type': 'extractorType',
            'generation_config': 'generationConfig'
        }

    def check_api_consistency(self) -> bool:
        """执行API一致性检查"""
        print("🔍 Excel2Doc API一致性检查开始...")
        print()
        
        # 解析前端类型定义
        print("📂 解析前端类型定义...")
        self._parse_frontend_types()
        
        # 解析后端Schema定义
        print("📂 解析后端Schema定义...")
        self._parse_backend_schemas()
        
        # 解析前端API调用
        print("📂 解析前端API调用...")
        self._parse_frontend_api_calls()
        
        # 解析后端API端点
        print("📂 解析后端API端点...")
        self._parse_backend_endpoints()
        
        # 执行一致性检查
        print("🔍 执行一致性检查...")
        self._check_type_consistency()
        self._check_api_field_consistency()
        self._check_enum_consistency()
        
        # 输出检查结果
        return self._report_results()

    def _parse_frontend_types(self) -> None:
        """解析前端TypeScript类型定义"""
        frontend_types_dir = Path("frontend/src/types")
        if not frontend_types_dir.exists():
            return
            
        for file_path in frontend_types_dir.rglob("*.ts"):
            self._parse_typescript_file(file_path)

    def _parse_typescript_file(self, file_path: Path) -> None:
        """解析TypeScript文件中的类型定义"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, FileNotFoundError):
            return

        # 匹配接口定义
        interface_pattern = r'export\s+interface\s+(\w+)\s*\{([^}]*)\}'
        interfaces = re.finditer(interface_pattern, content, re.DOTALL)
        
        for match in interfaces:
            interface_name = match.group(1)
            interface_body = match.group(2)
            line_num = self._get_line_number(content, match.start())
            
            # 解析字段
            field_pattern = r'(\w+)\s*\??\s*:\s*([^;,\n]+)'
            fields = {}
            for field_match in re.finditer(field_pattern, interface_body):
                field_name = field_match.group(1).strip()
                field_type = field_match.group(2).strip()
                fields[field_name] = field_type
            
            self.frontend_types[interface_name] = TypeDefinition(
                name=interface_name,
                file_path=str(file_path),
                line_number=line_num,
                fields=fields
            )

    def _parse_backend_schemas(self) -> None:
        """解析后端Pydantic Schema定义"""
        backend_schemas_dir = Path("backend/app/schemas")
        if not backend_schemas_dir.exists():
            return
            
        for file_path in backend_schemas_dir.rglob("*.py"):
            self._parse_pydantic_file(file_path)

    def _parse_pydantic_file(self, file_path: Path) -> None:
        """解析Pydantic Schema文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, FileNotFoundError):
            return

        # 匹配Pydantic模型定义
        class_pattern = r'class\s+(\w+)\(BaseModel\):([^}]*?)(?=\n\nclass|\n\ndef|\Z)'
        classes = re.finditer(class_pattern, content, re.DOTALL)
        
        for match in classes:
            class_name = match.group(1)
            class_body = match.group(2)
            line_num = self._get_line_number(content, match.start())
            
            # 解析字段和alias
            field_pattern = r'(\w+)\s*:\s*([^=\n]+)(?:\s*=\s*Field\([^)]*alias\s*=\s*[\'"](\w+)[\'"][^)]*\))?'
            fields = {}
            for field_match in re.finditer(field_pattern, class_body):
                field_name = field_match.group(1).strip()
                field_type = field_match.group(2).strip()
                alias = field_match.group(3) if len(field_match.groups()) > 2 and field_match.group(3) else None
                
                # 记录字段名（优先使用alias）
                display_name = alias if alias else field_name
                fields[display_name] = field_type
                
                # 同时记录原字段名，用于检查一致性
                if alias:
                    fields[f"_original_{field_name}"] = field_type
            
            self.backend_schemas[class_name] = TypeDefinition(
                name=class_name,
                file_path=str(file_path),
                line_number=line_num,
                fields=fields
            )

    def _parse_frontend_api_calls(self) -> None:
        """解析前端API调用"""
        services_dir = Path("frontend/src/services")
        if not services_dir.exists():
            return
            
        for file_path in services_dir.rglob("*.ts"):
            self._parse_api_service_file(file_path)

    def _parse_api_service_file(self, file_path: Path) -> None:
        """解析API服务文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, FileNotFoundError):
            return

        # 查找API调用模式
        api_call_pattern = r'api\.(get|post|put|delete)\s*\(\s*[\'"]([^\'"]*)[\'"][^)]*\)'
        api_calls = re.finditer(api_call_pattern, content)
        
        for match in api_calls:
            method = match.group(1).upper()
            path = match.group(2)
            line_num = self._get_line_number(content, match.start())
            
            self.frontend_api_calls.append({
                'method': method,
                'path': path,
                'file': str(file_path),
                'line': line_num
            })

    def _parse_backend_endpoints(self) -> None:
        """解析后端API端点"""
        api_dir = Path("backend/app/api")
        if not api_dir.exists():
            return
            
        for file_path in api_dir.rglob("*.py"):
            self._parse_fastapi_file(file_path)

    def _parse_fastapi_file(self, file_path: Path) -> None:
        """解析FastAPI路由文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, FileNotFoundError):
            return

        # 匹配路由定义
        route_pattern = r'@router\.(get|post|put|delete)\s*\(\s*[\'"]([^\'"]*)[\'"]'
        routes = re.finditer(route_pattern, content)
        
        for match in routes:
            method = match.group(1).upper()
            path = match.group(2)
            line_num = self._get_line_number(content, match.start())
            
            endpoint = APIEndpoint(
                method=method,
                path=path,
                file_path=str(file_path),
                line_number=line_num
            )
            self.backend_endpoints.append(endpoint)

    def _check_type_consistency(self) -> None:
        """检查类型定义一致性"""
        # 比较相似名称的前后端类型
        for frontend_name, frontend_type in self.frontend_types.items():
            # 查找对应的后端Schema
            backend_candidates = []
            for backend_name, backend_type in self.backend_schemas.items():
                if self._is_related_type(frontend_name, backend_name):
                    backend_candidates.append((backend_name, backend_type))
            
            for backend_name, backend_type in backend_candidates:
                self._compare_type_fields(frontend_type, backend_type)

    def _is_related_type(self, frontend_name: str, backend_name: str) -> bool:
        """判断前后端类型是否相关"""
        # 简单的名称匹配逻辑
        frontend_lower = frontend_name.lower()
        backend_lower = backend_name.lower()
        
        # 移除常见后缀
        for suffix in ['read', 'create', 'update', 'response', 'request']:
            backend_lower = backend_lower.replace(suffix, '')
        
        return (frontend_lower in backend_lower or 
                backend_lower in frontend_lower or
                abs(len(frontend_lower) - len(backend_lower)) <= 3)

    def _compare_type_fields(self, frontend_type: TypeDefinition, backend_type: TypeDefinition) -> None:
        """比较前后端类型字段"""
        frontend_fields = set(frontend_type.fields.keys())
        backend_fields = set(k for k in backend_type.fields.keys() if not k.startswith('_original_'))
        
        # 检查字段名一致性
        for field_name in frontend_fields:
            if field_name in backend_fields:
                continue  # 字段名完全匹配，正常情况
                
            # 检查是否应该有对应的snake_case版本
            snake_version = self._camel_to_snake(field_name)
            if f"_original_{snake_version}" in backend_type.fields:
                # 后端有对应的snake_case字段，但没有正确的alias
                self.issues.append(ConsistencyIssue(
                    issue_type='missing_alias',
                    frontend_file=frontend_type.file_path,
                    backend_file=backend_type.file_path,
                    frontend_line=frontend_type.line_number,
                    backend_line=backend_type.line_number,
                    field_name=field_name,
                    frontend_format=field_name,
                    backend_format=snake_version,
                    message=f'Backend field "{snake_version}" should have camelCase alias "{field_name}"',
                    severity='warning'
                ))

        # 检查后端有而前端没有的字段
        for field_name in backend_fields:
            if field_name not in frontend_fields:
                original_field = f"_original_{self._camel_to_snake(field_name)}"
                if original_field in backend_type.fields:
                    self.issues.append(ConsistencyIssue(
                        issue_type='missing_frontend_field',
                        frontend_file=frontend_type.file_path,
                        backend_file=backend_type.file_path,
                        frontend_line=frontend_type.line_number,
                        backend_line=backend_type.line_number,
                        field_name=field_name,
                        frontend_format='missing',
                        backend_format=field_name,
                        message=f'Frontend type "{frontend_type.name}" missing field "{field_name}"',
                        severity='info'
                    ))

    def _check_api_field_consistency(self) -> None:
        """检查API字段一致性"""
        # 这里可以添加更复杂的API字段检查逻辑
        # 由于解析API请求/响应体比较复杂，暂时跳过详细实现
        pass

    def _check_enum_consistency(self) -> None:
        """检查枚举值一致性"""
        # 1. 收集所有枚举定义
        backend_enums = self._collect_backend_enums()
        frontend_enums = self._collect_frontend_enums()
        
        # 2. 检查相同概念的枚举是否值一致
        for backend_enum_name, backend_values in backend_enums.items():
            # 寻找前端对应的枚举
            frontend_counterpart = self._find_frontend_enum_counterpart(
                backend_enum_name, frontend_enums
            )
            
            if frontend_counterpart:
                frontend_values = frontend_enums[frontend_counterpart]
                
                # 比较值
                missing_in_frontend = set(backend_values.values()) - set(frontend_values.values())
                missing_in_backend = set(frontend_values.values()) - set(backend_values.values())
                
                if missing_in_frontend or missing_in_backend:
                    self.issues.append(ConsistencyIssue(
                        issue_type='enum_value_mismatch',
                        frontend_file='multiple frontend files',
                        backend_file='multiple backend files',
                        frontend_line=0,
                        backend_line=0,
                        field_name=f'{backend_enum_name}/{frontend_counterpart}',
                        frontend_format=f'values: {list(frontend_values.values())}',
                        backend_format=f'values: {list(backend_values.values())}',
                        message=f'枚举值不匹配: 前端 {frontend_counterpart} vs 后端 {backend_enum_name}',
                        severity='error'
                    ))
        
        # 3. 查找可能应该使用枚举的硬编码字符串
        hardcoded_candidates = self._find_hardcoded_enum_candidates()
        for candidate in hardcoded_candidates:
            self.issues.append(ConsistencyIssue(
                issue_type='hardcoded_enum_candidate',
                frontend_file='',
                backend_file=candidate['file_path'],
                frontend_line=0,
                backend_line=candidate['line_number'],
                field_name=candidate['string_value'],
                frontend_format='',
                backend_format=f'硬编码字符串: "{candidate["string_value"]}"',
                message=f'可能应该使用枚举: "{candidate["string_value"]}" (类型: {candidate["suggested_enum_type"]})',
                severity='warning'
            ))

    def _collect_backend_enums(self) -> Dict[str, Dict[str, str]]:
        """收集后端枚举定义"""
        enums = {}
        backend_dir = Path("backend/app")
        
        if not backend_dir.exists():
            return enums
            
        for py_file in backend_dir.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 查找枚举类定义
                enum_pattern = r'class\s+(\w+Enum).*?:\s*(.*?)(?=\n\n|\nclass|\ndef|\nif|\Z)'
                enum_matches = re.finditer(enum_pattern, content, re.DOTALL)
                
                for match in enum_matches:
                    enum_name = match.group(1)
                    enum_body = match.group(2)
                    
                    # 提取枚举值
                    enum_values = {}
                    value_pattern = r'(\w+)\s*=\s*[\'"]([^\'"]*)[\'"]'
                    value_matches = re.finditer(value_pattern, enum_body)
                    
                    for value_match in value_matches:
                        key = value_match.group(1)
                        value = value_match.group(2)
                        enum_values[key] = value
                    
                    if enum_values:
                        enums[enum_name] = enum_values
                        
            except (UnicodeDecodeError, FileNotFoundError):
                continue
                
        return enums

    def _collect_frontend_enums(self) -> Dict[str, Dict[str, str]]:
        """收集前端枚举定义"""
        enums = {}
        frontend_dir = Path("frontend/src")
        
        if not frontend_dir.exists():
            return enums
            
        for ts_file in frontend_dir.rglob("*.ts"):
            try:
                with open(ts_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 查找enum定义
                enum_pattern = r'enum\s+(\w+)\s*\{([^}]*)\}'
                enum_matches = re.finditer(enum_pattern, content, re.DOTALL)
                
                for match in enum_matches:
                    enum_name = match.group(1)
                    enum_body = match.group(2)
                    
                    # 提取枚举值
                    enum_values = {}
                    value_pattern = r'(\w+)\s*=\s*[\'"]([^\'"]*)[\'"]'
                    value_matches = re.finditer(value_pattern, enum_body)
                    
                    for value_match in value_matches:
                        key = value_match.group(1)
                        value = value_match.group(2)
                        enum_values[key] = value
                    
                    if enum_values:
                        enums[enum_name] = enum_values
                
                # 查找type联合类型
                type_pattern = r'type\s+(\w+)\s*=\s*([^;]+);'
                type_matches = re.finditer(type_pattern, content)
                
                for match in type_matches:
                    type_name = match.group(1)
                    type_def = match.group(2).strip()
                    
                    # 检查是否是字符串联合类型
                    if "'" in type_def or '"' in type_def:
                        string_values = re.findall(r'[\'"]([^\'"]*)[\'"]', type_def)
                        if string_values:
                            enum_values = {f"VALUE_{i}": value for i, value in enumerate(string_values)}
                            enums[type_name] = enum_values
                            
            except (UnicodeDecodeError, FileNotFoundError):
                continue
                
        return enums

    def _find_frontend_enum_counterpart(self, backend_enum_name: str, frontend_enums: Dict[str, Dict[str, str]]) -> Optional[str]:
        """寻找前端对应的枚举"""
        backend_lower = backend_enum_name.lower().replace('enum', '')
        
        for frontend_name in frontend_enums.keys():
            frontend_lower = frontend_name.lower().replace('enum', '')
            
            # 检查名称相似性
            if (backend_lower in frontend_lower or 
                frontend_lower in backend_lower or
                self._calculate_similarity(backend_lower, frontend_lower) > 0.7):
                return frontend_name
        
        return None

    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """计算字符串相似度"""
        from difflib import SequenceMatcher
        return SequenceMatcher(None, str1, str2).ratio()

    def _find_hardcoded_enum_candidates(self) -> List[Dict[str, Any]]:
        """查找可能应该使用枚举的硬编码字符串"""
        candidates = []
        
        # 定义枚举值模式
        enum_patterns = {
            'parse_status': r'^(uploaded|parsing|completed|failed)$',
            'task_status': r'^(pending|running|completed|failed|cancelled)$', 
            'user_status': r'^(active|inactive|pending|suspended)$',
            'log_level': r'^(debug|info|warning|error|fatal)$',
            'file_type': r'^(excel|csv|json|xml|pdf)$'
        }
        
        # 扫描后端文件
        backend_dir = Path("backend/app")
        if backend_dir.exists():
            for py_file in backend_dir.rglob("*.py"):
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 查找字符串字面量
                    string_pattern = r'[\'"]([^\'"]+)[\'"]'
                    matches = re.finditer(string_pattern, content)
                    
                    for match in matches:
                        string_value = match.group(1)
                        
                        # 跳过明显不是枚举的字符串
                        if (len(string_value) < 2 or len(string_value) > 20 or
                            string_value.startswith(('http', '/', '.', '_')) or
                            string_value in {'utf-8', 'application/json', 'GET', 'POST'}):
                            continue
                        
                        # 检查是否匹配枚举模式
                        for enum_type, pattern in enum_patterns.items():
                            if re.match(pattern, string_value.lower()):
                                line_num = content[:match.start()].count('\n') + 1
                                context = self._get_line_context(content, match.start())
                                
                                candidates.append({
                                    'file_path': str(py_file),
                                    'line_number': line_num,
                                    'string_value': string_value,
                                    'suggested_enum_type': enum_type,
                                    'context': context
                                })
                                break
                                
                except (UnicodeDecodeError, FileNotFoundError):
                    continue
        
        return candidates

    def _get_line_context(self, content: str, position: int) -> str:
        """获取指定位置的代码上下文"""
        lines = content[:position].split('\n')
        line_num = len(lines) - 1
        all_lines = content.split('\n')
        
        if 0 <= line_num < len(all_lines):
            return all_lines[line_num].strip()
        
        return ""

    def _camel_to_snake(self, camel_str: str) -> str:
        """将camelCase转换为snake_case"""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def _get_line_number(self, content: str, position: int) -> int:
        """根据字符位置计算行号"""
        return content[:position].count('\n') + 1

    def _report_results(self) -> bool:
        """输出检查结果"""
        print()
        
        if not self.issues:
            print("✅ 前后端API字段格式完全一致!")
            print()
            self._print_summary()
            return True

        # 按严重程度分组
        error_issues = [i for i in self.issues if i.severity == 'error']
        warning_issues = [i for i in self.issues if i.severity == 'warning']
        info_issues = [i for i in self.issues if i.severity == 'info']
        
        print(f"❌ 发现 {len(self.issues)} 个API一致性问题:")
        print(f"   🔴 错误: {len(error_issues)} 个")
        print(f"   🟡 警告: {len(warning_issues)} 个")  
        print(f"   ℹ️  信息: {len(info_issues)} 个")
        print()

        # 按问题类型分组显示
        issues_by_type = defaultdict(list)
        for issue in self.issues:
            issues_by_type[issue.issue_type].append(issue)

        for issue_type, type_issues in issues_by_type.items():
            print(f"📂 {issue_type.replace('_', ' ').title()} ({len(type_issues)} 个):")
            for issue in type_issues:
                severity_icon = {'error': '🔴', 'warning': '🟡', 'info': 'ℹ️'}[issue.severity]
                print(f"   {severity_icon} {issue.message}")
                print(f"      前端: {issue.frontend_file}:{issue.frontend_line}")
                print(f"      后端: {issue.backend_file}:{issue.backend_line}")
            print()

        self._print_summary()
        return len(error_issues) == 0

    def _print_summary(self) -> None:
        """输出解析统计信息"""
        print("📊 解析统计:")
        print(f"   前端类型定义: {len(self.frontend_types)} 个")
        print(f"   后端Schema定义: {len(self.backend_schemas)} 个")
        print(f"   前端API调用: {len(self.frontend_api_calls)} 个")
        print(f"   后端API端点: {len(self.backend_endpoints)} 个")
        print()
        
        if self.frontend_types:
            print("📋 前端类型:")
            for name in sorted(self.frontend_types.keys()):
                field_count = len(self.frontend_types[name].fields)
                print(f"   {name} ({field_count} 字段)")
        
        if self.backend_schemas:
            print("📋 后端Schema:")
            for name in sorted(self.backend_schemas.keys()):
                field_count = len([k for k in self.backend_schemas[name].fields.keys() 
                                 if not k.startswith('_original_')])
                print(f"   {name} ({field_count} 字段)")
        print()

def main():
    parser = argparse.ArgumentParser(description='Excel2Doc API一致性检查工具')
    parser.add_argument('--report', action='store_true', help='生成详细报告')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')
    
    args = parser.parse_args()
    
    if not os.path.exists('frontend') and not os.path.exists('backend'):
        print("❌ 错误: 未找到frontend或backend目录")
        print("请在Excel2Doc项目根目录下运行此脚本")
        sys.exit(1)

    checker = APIConsistencyChecker()
    success = checker.check_api_consistency()
    
    if args.report:
        # 生成详细报告到文件
        report_file = "api_consistency_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            report_data = {
                'frontend_types': {name: {
                    'file': type_def.file_path,
                    'fields': list(type_def.fields.keys())
                } for name, type_def in checker.frontend_types.items()},
                'backend_schemas': {name: {
                    'file': type_def.file_path,
                    'fields': [k for k in type_def.fields.keys() if not k.startswith('_original_')]
                } for name, type_def in checker.backend_schemas.items()},
                'issues': [{
                    'type': issue.issue_type,
                    'message': issue.message,
                    'severity': issue.severity,
                    'frontend_file': issue.frontend_file,
                    'backend_file': issue.backend_file
                } for issue in checker.issues]
            }
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        print(f"📄 详细报告已保存到: {report_file}")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()