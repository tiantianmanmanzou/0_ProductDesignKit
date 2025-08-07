#!/usr/bin/env python3
"""
Excel2Doc 运行时API一致性检查脚本

用途:
- 启动前后端服务
- 执行实际API调用测试  
- 验证枚举值传递一致性
- 检查字段名转换正确性

使用方法:
    python scripts/runtime_api_consistency_check.py
    python scripts/runtime_api_consistency_check.py --report  # 生成详细报告
"""

import asyncio
import subprocess
import time
import json
import os
import signal
import sys
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import argparse

# 尝试导入aiohttp，如果不可用则使用标准库
try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

@dataclass
class TestResult:
    """测试结果记录"""
    test_name: str
    description: str
    passed: bool
    expected: Any = None
    actual: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    timestamp: str = ""

class RuntimeAPIChecker:
    """运行时API一致性检查器"""
    
    def __init__(self, generate_report: bool = False):
        self.base_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:3000"
        self.test_results: List[TestResult] = []
        self.generate_report = generate_report
        self.backend_process: Optional[subprocess.Popen] = None
        self.frontend_process: Optional[subprocess.Popen] = None
        self.use_aiohttp = AIOHTTP_AVAILABLE
        
        # 测试数据配置
        self.test_file_path = Path("测试项目数据表.xlsx")
        
        if not self.use_aiohttp:
            print("⚠️ aiohttp 未安装，使用标准库进行HTTP请求（功能有限）")
    
    def _make_sync_request(self, url: str, method: str = 'GET', data=None, headers=None) -> Tuple[int, str]:
        """使用标准库进行HTTP请求"""
        try:
            if headers is None:
                headers = {}
            
            if method == 'GET':
                req = urllib.request.Request(url, headers=headers)
            else:
                req = urllib.request.Request(url, data=data, headers=headers, method=method)
            
            with urllib.request.urlopen(req) as response:
                return response.status, response.read().decode('utf-8')
                
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode('utf-8') if e.fp else str(e)
        except Exception as e:
            return 0, str(e)
        
    async def run_full_check(self) -> bool:
        """运行完整的运行时检查"""
        print("🚀 Excel2Doc 运行时API一致性检查开始...")
        print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        try:
            # 1. 检查环境
            if not self._check_environment():
                return False
            
            # 2. 启动服务
            print("📦 启动后端和前端服务...")
            if not await self._start_services():
                print("❌ 服务启动失败")
                return False
            
            # 3. 等待服务就绪
            print("⏳ 等待服务就绪...")
            if not await self._wait_for_services():
                print("❌ 服务就绪检查失败")
                return False
            
            print("✅ 服务已启动，开始执行测试...")
            print()
            
            # 4. 执行各项测试
            await self._test_project_creation_enum_consistency()
            await self._test_field_name_consistency() 
            await self._test_api_response_format()
            await self._test_error_handling_consistency()
            
            # 5. 生成报告
            return self._generate_final_report()
            
        except KeyboardInterrupt:
            print("\n⚠️ 测试被用户中断")
            return False
        except Exception as e:
            print(f"❌ 测试执行出错: {str(e)}")
            return False
        finally:
            # 6. 清理服务
            await self._cleanup_services()
    
    def _check_environment(self) -> bool:
        """检查运行环境"""
        print("🔍 检查运行环境...")
        
        # 检查必要的目录
        required_dirs = ["backend", "frontend"]
        for dir_name in required_dirs:
            if not Path(dir_name).exists():
                print(f"❌ 缺少必要目录: {dir_name}")
                return False
        
        # 检查测试文件
        if not self.test_file_path.exists():
            print(f"⚠️ 测试文件不存在: {self.test_file_path}")
            print("   将使用虚拟数据进行测试")
        
        print("✅ 环境检查通过")
        return True
    
    async def _start_services(self) -> bool:
        """启动后端和前端服务"""
        try:
            # 启动后端服务
            backend_cmd = ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
            self.backend_process = subprocess.Popen(
                backend_cmd,
                cwd="backend",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid if os.name != 'nt' else None
            )
            
            # 启动前端服务（如果需要）
            # frontend_cmd = ["npm", "run", "dev"]
            # self.frontend_process = subprocess.Popen(
            #     frontend_cmd,
            #     cwd="frontend",
            #     stdout=subprocess.PIPE,
            #     stderr=subprocess.PIPE
            # )
            
            # 等待服务启动
            await asyncio.sleep(5)
            return True
            
        except Exception as e:
            print(f"启动服务失败: {str(e)}")
            return False
    
    async def _wait_for_services(self, timeout: int = 30) -> bool:
        """等待服务就绪"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                if self.use_aiohttp:
                    async with aiohttp.ClientSession() as session:
                        # 检查后端健康状态
                        async with session.get(f"{self.base_url}/health") as response:
                            if response.status == 200:
                                return True
                else:
                    # 使用标准库检查服务状态
                    status_code, response_text = self._make_sync_request(f"{self.base_url}/health")
                    if status_code == 200:
                        return True
            except:
                pass
            
            await asyncio.sleep(2)
        
        return False
    
    async def _test_project_creation_enum_consistency(self):
        """测试项目创建API的枚举值一致性"""
        print("📝 测试项目创建枚举值一致性...")
        
        test_cases = [
            {
                "name": "测试项目_枚举一致性",
                "description": "运行时枚举一致性检查",
                "expected_parse_status": "uploaded"  # 期望小写
            }
        ]
        
        for case in test_cases:
            start_time = time.time()
            
            try:
                async with aiohttp.ClientSession() as session:
                    # 准备表单数据
                    data = aiohttp.FormData()
                    data.add_field('name', case['name'])
                    data.add_field('description', case['description'])
                    
                    # 添加测试文件（如果存在）
                    if self.test_file_path.exists():
                        with open(self.test_file_path, 'rb') as f:
                            data.add_field('excel_file', f, filename='test.xlsx')
                    else:
                        # 创建虚拟文件数据
                        data.add_field('excel_file', b'dummy data', filename='test.xlsx')
                    
                    async with session.post(f"{self.base_url}/api/v1/projects/", data=data) as response:
                        execution_time = time.time() - start_time
                        
                        if response.status == 200 or response.status == 201:
                            result = await response.json()
                            actual_status = result.get('data', {}).get('parseStatus')
                            
                            # 检查枚举值格式
                            test_passed = actual_status == case['expected_parse_status']
                            
                            self.test_results.append(TestResult(
                                test_name="project_creation_enum_consistency",
                                description="项目创建返回正确的小写枚举值",
                                passed=test_passed,
                                expected=case['expected_parse_status'],
                                actual=actual_status,
                                execution_time=execution_time,
                                timestamp=datetime.now().isoformat()
                            ))
                            
                            if test_passed:
                                print(f"  ✅ 枚举值一致性检查通过: {actual_status}")
                            else:
                                print(f"  ❌ 枚举值不一致: 期望 '{case['expected_parse_status']}', 实际 '{actual_status}'")
                                
                        else:
                            error_text = await response.text()
                            self.test_results.append(TestResult(
                                test_name="project_creation_enum_consistency",
                                description="项目创建API调用",
                                passed=False,
                                error=f"HTTP {response.status}: {error_text}",
                                execution_time=execution_time,
                                timestamp=datetime.now().isoformat()
                            ))
                            print(f"  ❌ API调用失败: HTTP {response.status}")
                            
            except Exception as e:
                execution_time = time.time() - start_time
                self.test_results.append(TestResult(
                    test_name="project_creation_enum_consistency",
                    description="项目创建API调用",
                    passed=False,
                    error=str(e),
                    execution_time=execution_time,
                    timestamp=datetime.now().isoformat()
                ))
                print(f"  ❌ 测试执行异常: {str(e)}")
    
    async def _test_field_name_consistency(self):
        """测试字段名一致性（camelCase vs snake_case）"""
        print("🔤 测试字段名一致性...")
        
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                # 获取项目列表，检查字段名格式
                async with session.get(f"{self.base_url}/api/v1/projects/?page=1&limit=5") as response:
                    execution_time = time.time() - start_time
                    
                    if response.status == 200:
                        result = await response.json()
                        projects = result.get('data', [])
                        
                        if projects:
                            # 检查第一个项目的字段名
                            project = projects[0]
                            expected_camel_fields = ['createdAt', 'updatedAt', 'parseStatus', 'fileSize']
                            snake_case_fields = []
                            
                            for field in expected_camel_fields:
                                snake_version = self._camel_to_snake(field)
                                if snake_version in project and field not in project:
                                    snake_case_fields.append(snake_version)
                            
                            test_passed = len(snake_case_fields) == 0
                            
                            self.test_results.append(TestResult(
                                test_name="field_name_consistency",
                                description="API响应字段使用camelCase格式",
                                passed=test_passed,
                                expected="所有字段使用camelCase",
                                actual=f"发现snake_case字段: {snake_case_fields}" if snake_case_fields else "所有字段都是camelCase",
                                execution_time=execution_time,
                                timestamp=datetime.now().isoformat()
                            ))
                            
                            if test_passed:
                                print("  ✅ 字段名格式一致性检查通过")
                            else:
                                print(f"  ❌ 发现snake_case字段: {snake_case_fields}")
                        else:
                            print("  ⚠️ 没有项目数据可供检查")
                    else:
                        error_text = await response.text()
                        self.test_results.append(TestResult(
                            test_name="field_name_consistency",
                            description="获取项目列表检查字段名",
                            passed=False,
                            error=f"HTTP {response.status}: {error_text}",
                            execution_time=execution_time,
                            timestamp=datetime.now().isoformat()
                        ))
                        
        except Exception as e:
            execution_time = time.time() - start_time
            self.test_results.append(TestResult(
                test_name="field_name_consistency",
                description="字段名一致性检查",
                passed=False,
                error=str(e),
                execution_time=execution_time,
                timestamp=datetime.now().isoformat()
            ))
    
    async def _test_api_response_format(self):
        """测试API响应格式一致性"""
        print("📋 测试API响应格式一致性...")
        
        test_endpoints = [
            ("/api/v1/projects/", "项目列表API"),
            ("/api/v1/health", "健康检查API")
        ]
        
        for endpoint, description in test_endpoints:
            start_time = time.time()
            
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.base_url}{endpoint}") as response:
                        execution_time = time.time() - start_time
                        
                        if response.status == 200:
                            result = await response.json()
                            
                            # 检查统一响应格式 {code, message, data, timestamp}
                            expected_fields = ['code', 'message', 'data', 'timestamp']
                            missing_fields = [field for field in expected_fields if field not in result]
                            
                            test_passed = len(missing_fields) == 0
                            
                            self.test_results.append(TestResult(
                                test_name=f"api_response_format_{endpoint.replace('/', '_')}",
                                description=f"{description}响应格式标准化",
                                passed=test_passed,
                                expected=f"包含字段: {expected_fields}",
                                actual=f"缺少字段: {missing_fields}" if missing_fields else "格式正确",
                                execution_time=execution_time,
                                timestamp=datetime.now().isoformat()
                            ))
                            
                            if test_passed:
                                print(f"  ✅ {description} 响应格式正确")
                            else:
                                print(f"  ❌ {description} 缺少字段: {missing_fields}")
                                
            except Exception as e:
                execution_time = time.time() - start_time
                self.test_results.append(TestResult(
                    test_name=f"api_response_format_{endpoint.replace('/', '_')}",
                    description=f"{description}响应格式检查",
                    passed=False,
                    error=str(e),
                    execution_time=execution_time,
                    timestamp=datetime.now().isoformat()
                ))
    
    async def _test_error_handling_consistency(self):
        """测试错误处理一致性"""
        print("⚠️ 测试错误处理一致性...")
        
        # 测试无效请求的错误格式
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                # 发送无效的项目创建请求
                invalid_data = aiohttp.FormData()
                invalid_data.add_field('name', '')  # 空名称应该失败
                
                async with session.post(f"{self.base_url}/api/v1/projects/", data=invalid_data) as response:
                    execution_time = time.time() - start_time
                    
                    if response.status >= 400:  # 期望错误状态码
                        result = await response.json()
                        
                        # 检查错误响应格式
                        has_error_info = 'message' in result or 'error' in result
                        
                        self.test_results.append(TestResult(
                            test_name="error_handling_consistency",
                            description="错误响应格式标准化",
                            passed=has_error_info,
                            expected="包含错误信息字段",
                            actual=f"响应包含: {list(result.keys())}",
                            execution_time=execution_time,
                            timestamp=datetime.now().isoformat()
                        ))
                        
                        if has_error_info:
                            print("  ✅ 错误响应格式正确")
                        else:
                            print("  ❌ 错误响应缺少错误信息")
                    else:
                        print("  ⚠️ 预期的错误请求返回了成功状态")
                        
        except Exception as e:
            execution_time = time.time() - start_time
            self.test_results.append(TestResult(
                test_name="error_handling_consistency",
                description="错误处理一致性检查",
                passed=False,
                error=str(e),
                execution_time=execution_time,
                timestamp=datetime.now().isoformat()
            ))
    
    def _camel_to_snake(self, camel_str: str) -> str:
        """将camelCase转换为snake_case"""
        result = []
        for i, c in enumerate(camel_str):
            if c.isupper() and i > 0:
                result.append('_')
            result.append(c.lower())
        return ''.join(result)
    
    def _generate_final_report(self) -> bool:
        """生成最终测试报告"""
        print("\n" + "="*50)
        print("📊 运行时API一致性检查报告")
        print("="*50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.passed)
        failed_tests = total_tests - passed_tests
        
        print(f"\n📈 总体统计:")
        print(f"   总测试数: {total_tests}")
        print(f"   通过: {passed_tests} ✅")
        print(f"   失败: {failed_tests} ❌")
        print(f"   通过率: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ 失败的测试:")
            for result in self.test_results:
                if not result.passed:
                    print(f"   • {result.test_name}: {result.description}")
                    if result.error:
                        print(f"     错误: {result.error}")
                    else:
                        print(f"     期望: {result.expected}")
                        print(f"     实际: {result.actual}")
        
        # 生成JSON报告文件
        if self.generate_report:
            report_data = {
                'summary': {
                    'total_tests': total_tests,
                    'passed_tests': passed_tests,
                    'failed_tests': failed_tests,
                    'success_rate': passed_tests/total_tests*100 if total_tests > 0 else 0,
                    'execution_time': datetime.now().isoformat()
                },
                'test_results': [asdict(result) for result in self.test_results]
            }
            
            report_file = Path('runtime-check-report.json')
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n📄 详细报告已保存至: {report_file}")
        
        return failed_tests == 0
    
    async def _cleanup_services(self):
        """清理启动的服务"""
        print("\n🧹 清理服务...")
        
        if self.backend_process:
            try:
                if os.name != 'nt':
                    os.killpg(os.getpgid(self.backend_process.pid), signal.SIGTERM)
                else:
                    self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
            except:
                pass
        
        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
            except:
                pass
        
        print("✅ 服务清理完成")

async def main():
    parser = argparse.ArgumentParser(description='Excel2Doc运行时API一致性检查工具')
    parser.add_argument('--report', action='store_true', help='生成详细JSON报告文件')
    parser.add_argument('--timeout', type=int, default=30, help='服务启动超时时间（秒）')
    
    args = parser.parse_args()
    
    checker = RuntimeAPIChecker(generate_report=args.report)
    success = await checker.run_full_check()
    
    if success:
        print("\n🎉 所有运行时一致性检查通过！")
        sys.exit(0)
    else:
        print("\n💥 发现运行时一致性问题，请查看上述报告")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())