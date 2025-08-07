#!/usr/bin/env python3
"""
Excel2Doc 完整检查脚本集成器

运行所有检查工具的集成脚本，提供统一的接口和综合报告

功能：
1. 按顺序运行所有检查工具
2. 收集所有检查结果
3. 生成综合分析报告
4. 提供修复建议优先级排序
"""

import os
import sys
import subprocess
import json
import argparse
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

class IntegratedChecker:
    """集成检查器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.scripts_dir = self.project_root / "0_ProductDesignKit" / "review" / "scripts"
        
        # 检查工具配置
        self.check_tools = {
            'naming_convention': {
                'script': 'check_naming_convention.py',
                'description': '命名规范检查',
                'priority': 1,
                'required': True
            },
            'api_consistency': {
                'script': 'check_api_consistency.py',
                'description': 'API一致性检查',
                'priority': 2,
                'required': True
            },
            'enum_usage': {
                'script': 'enum_usage_analyzer.py',
                'description': '枚举使用场景分析',
                'priority': 3,
                'required': True
            },
            'migration_analysis': {
                'script': 'migration_script_analyzer.py',
                'description': '数据库迁移脚本分析',
                'priority': 4,
                'required': True
            },
            'database_validation': {
                'script': 'database_data_validator.py',
                'description': '数据库数据验证',
                'priority': 5,
                'required': False,  # 需要数据库连接
                'dependencies': ['psycopg2-binary']
            },
            'runtime_api_check': {
                'script': 'runtime_api_consistency_check.py',
                'description': '运行时API一致性检查',
                'priority': 6,
                'required': False,  # 需要启动服务
                'dependencies': ['aiohttp']
            }
        }
        
        # 检查结果
        self.results = {}
        self.summary = {
            'total_checks': 0,
            'successful_checks': 0,
            'failed_checks': 0,
            'skipped_checks': 0,
            'total_issues': 0,
            'critical_issues': 0,
            'warnings': 0,
            'info_items': 0
        }

    def check_dependencies(self, tool_name: str, tool_config: Dict[str, Any]) -> bool:
        """检查工具依赖"""
        if 'dependencies' not in tool_config:
            return True
        
        missing_deps = []
        for dep in tool_config['dependencies']:
            try:
                __import__(dep.replace('-', '_'))
            except ImportError:
                missing_deps.append(dep)
        
        if missing_deps:
            print(f"  ⚠️ {tool_config['description']} 缺少依赖: {', '.join(missing_deps)}")
            if tool_config.get('required', False):
                print(f"     这是必需的检查，请安装依赖后重试")
                return False
            else:
                print(f"     这是可选检查，将跳过")
                return False
        
        return True

    def run_single_check(self, tool_name: str, tool_config: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
        """运行单个检查工具"""
        script_path = self.scripts_dir / tool_config['script']
        
        if not script_path.exists():
            return {
                'tool_name': tool_name,
                'success': False,
                'error': f"脚本文件不存在: {script_path}",
                'execution_time': 0
            }
        
        print(f"🔍 运行 {tool_config['description']}...")
        
        start_time = datetime.now()
        try:
            # 构建命令
            cmd = [sys.executable, str(script_path)]
            if verbose:
                cmd.append('--verbose')
            
            # 运行脚本
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=300  # 5分钟超时
            )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                'tool_name': tool_name,
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode,
                'execution_time': execution_time
            }
            
        except subprocess.TimeoutExpired:
            execution_time = (datetime.now() - start_time).total_seconds()
            return {
                'tool_name': tool_name,
                'success': False,
                'error': '检查超时（超过5分钟）',
                'execution_time': execution_time
            }
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return {
                'tool_name': tool_name,
                'success': False,
                'error': str(e),
                'execution_time': execution_time
            }

    def parse_check_results(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """解析检查结果，提取问题统计"""
        parsed = {
            'issues': 0,
            'critical': 0,
            'warnings': 0,
            'info': 0,
            'details': []
        }
        
        if not result['success']:
            parsed['critical'] += 1
            parsed['issues'] += 1
            parsed['details'].append({
                'type': 'EXECUTION_ERROR',
                'severity': 'CRITICAL',
                'message': result.get('error', '检查执行失败')
            })
            return parsed
        
        stdout = result.get('stdout', '')
        
        # 解析不同类型的输出
        lines = stdout.split('\n')
        for line in lines:
            line = line.strip()
            
            # 解析错误和警告
            if '❌' in line or 'ERROR' in line.upper() or '🔴' in line:
                parsed['critical'] += 1
                parsed['issues'] += 1
                parsed['details'].append({
                    'type': 'ERROR',
                    'severity': 'CRITICAL',
                    'message': line.replace('❌', '').replace('🔴', '').strip()
                })
            elif '⚠️' in line or 'WARNING' in line.upper() or '🟡' in line:
                parsed['warnings'] += 1
                parsed['issues'] += 1
                parsed['details'].append({
                    'type': 'WARNING',
                    'severity': 'WARNING',
                    'message': line.replace('⚠️', '').replace('🟡', '').strip()
                })
            elif 'ℹ️' in line or 'INFO' in line.upper():
                parsed['info'] += 1
                parsed['details'].append({
                    'type': 'INFO',
                    'severity': 'INFO',
                    'message': line.replace('ℹ️', '').strip()
                })
        
        return parsed

    def run_all_checks(self, skip_optional: bool = False, verbose: bool = False) -> bool:
        """运行所有检查"""
        print("🚀 Excel2Doc 完整检查开始...")
        print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # 按优先级排序
        sorted_tools = sorted(
            self.check_tools.items(),
            key=lambda x: x[1]['priority']
        )
        
        for tool_name, tool_config in sorted_tools:
            self.summary['total_checks'] += 1
            
            # 检查是否跳过可选检查
            if skip_optional and not tool_config.get('required', True):
                print(f"⏭️ 跳过可选检查: {tool_config['description']}")
                self.summary['skipped_checks'] += 1
                continue
            
            # 检查依赖
            if not self.check_dependencies(tool_name, tool_config):
                if tool_config.get('required', False):
                    print(f"❌ 必需检查失败: {tool_config['description']}")
                    self.summary['failed_checks'] += 1
                    return False
                else:
                    self.summary['skipped_checks'] += 1
                    continue
            
            # 运行检查
            result = self.run_single_check(tool_name, tool_config, verbose)
            self.results[tool_name] = result
            
            # 解析结果
            parsed = self.parse_check_results(result)
            result['parsed'] = parsed
            
            # 更新统计
            if result['success']:
                self.summary['successful_checks'] += 1
                print(f"  ✅ {tool_config['description']} 完成")
            else:
                self.summary['failed_checks'] += 1
                print(f"  ❌ {tool_config['description']} 失败")
            
            self.summary['total_issues'] += parsed['issues']
            self.summary['critical_issues'] += parsed['critical']
            self.summary['warnings'] += parsed['warnings']
            self.summary['info_items'] += parsed['info']
            
            if parsed['issues'] > 0:
                print(f"     发现问题: {parsed['issues']} 个 (严重: {parsed['critical']}, 警告: {parsed['warnings']})")
        
        return True

    def generate_summary_report(self) -> str:
        """生成综合报告"""
        report = f"""
{'='*80}
📊 Excel2Doc 完整检查报告
{'='*80}

⏰ 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📈 总体统计:
   总检查数: {self.summary['total_checks']}
   成功检查: {self.summary['successful_checks']} ✅
   失败检查: {self.summary['failed_checks']} ❌  
   跳过检查: {self.summary['skipped_checks']} ⏭️
   
   总问题数: {self.summary['total_issues']}
   严重问题: {self.summary['critical_issues']} 🔴
   警告问题: {self.summary['warnings']} 🟡
   信息提示: {self.summary['info_items']} ℹ️

"""
        
        if self.summary['total_issues'] > 0:
            report += "🔍 详细问题分析:\n\n"
            
            # 按优先级显示问题
            for tool_name, result in self.results.items():
                if result.get('parsed', {}).get('issues', 0) > 0:
                    tool_config = self.check_tools[tool_name]
                    report += f"📋 {tool_config['description']}:\n"
                    
                    for detail in result['parsed']['details']:
                        severity_icon = {'CRITICAL': '🔴', 'WARNING': '🟡', 'INFO': 'ℹ️'}.get(detail['severity'], '•')
                        report += f"   {severity_icon} {detail['message']}\n"
                    
                    report += "\n"
        
        # 修复建议
        if self.summary['critical_issues'] > 0:
            report += """
💡 优先修复建议:

1. 🔴 严重问题优先处理:
   - 枚举值大小写不一致问题
   - 数据库中存在无效枚举值
   - API接口命名规范违规

2. 🟡 警告问题择期处理:
   - 硬编码字符串建议使用枚举
   - 前后端类型定义不完全匹配

3. ℹ️ 信息提示作为改进参考:
   - 代码结构优化建议
   - 性能改进提示
"""
        
        success_rate = (self.summary['successful_checks'] / self.summary['total_checks'] * 100) if self.summary['total_checks'] > 0 else 0
        
        if success_rate >= 80 and self.summary['critical_issues'] == 0:
            report += "\n🎉 恭喜！项目前后端一致性检查基本通过！"
        elif self.summary['critical_issues'] == 0:
            report += "\n✅ 项目前后端一致性检查通过，有少量警告需要关注。"
        else:
            report += f"\n⚠️ 发现 {self.summary['critical_issues']} 个严重问题需要立即修复。"
        
        return report

    def save_detailed_report(self, output_file: str):
        """保存详细报告"""
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': self.summary,
            'tool_results': self.results,
            'project_root': str(self.project_root)
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"📄 详细报告已保存到: {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Excel2Doc 完整检查脚本集成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python run_all_checks.py                      # 运行所有必需检查
  python run_all_checks.py --skip-optional      # 跳过可选检查
  python run_all_checks.py --verbose --report   # 详细检查并生成报告
        """
    )
    
    parser.add_argument('--skip-optional', action='store_true', help='跳过可选检查（需要特殊依赖的检查）')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')
    parser.add_argument('--report', '-r', action='store_true', help='生成详细报告文件')
    
    args = parser.parse_args()
    
    # 获取项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    
    # 创建集成检查器并运行
    checker = IntegratedChecker(str(project_root))
    success = checker.run_all_checks(
        skip_optional=args.skip_optional,
        verbose=args.verbose
    )
    
    # 生成并显示报告
    print(checker.generate_summary_report())
    
    # 保存详细报告
    if args.report:
        report_file = project_root / f"complete_check_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        checker.save_detailed_report(str(report_file))
    
    # 根据结果设置退出码
    if checker.summary['critical_issues'] > 0:
        sys.exit(1)
    elif not success:
        sys.exit(2)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()