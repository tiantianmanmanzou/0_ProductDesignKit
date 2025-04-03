#!/usr/bin/env python3
import os
import subprocess
import shutil
import sys
import argparse
import json
from pathlib import Path
import zipfile
import time
from datetime import datetime

class StaticPageBuilder:
    def __init__(self, config):
        """
        初始化构建器
        :param config: 配置字典，包含所有用户定义的参数
        """
        print("\n=== 初始化构建环境 ===")
        self.source_component = os.path.abspath(config['source_component'])
        self.base_output_dir = os.path.abspath(config['output_dir'])
        
        # 获取组件名称
        self.component_name = self._get_component_name()
        
        # 创建时间戳文件夹
        timestamp = datetime.now().strftime('Export_%m-%d_%H-%M-%S')
        self.output_dir = os.path.join(self.base_output_dir, timestamp)
        
        print(f"源组件路径: {self.source_component}")
        print(f"组件名称: {self.component_name}")
        print(f"输出目录: {self.output_dir}")
        
        # 获取源项目根目录
        self.source_project_root = self._find_project_root()
        print(f"源项目根目录: {self.source_project_root}")
        
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        print("输出目录已准备就绪")

    def _find_project_root(self):
        """查找项目根目录（包含package.json的目录）"""
        current_dir = os.path.dirname(self.source_component)
        while current_dir != '/':
            if os.path.exists(os.path.join(current_dir, 'package.json')):
                return current_dir
            current_dir = os.path.dirname(current_dir)
        return os.path.dirname(os.path.dirname(os.path.dirname(self.source_component)))

    def _backup_vue_config(self):
        """备份原有的vue.config.js文件"""
        vue_config_path = os.path.join(self.source_project_root, 'vue.config.js')
        backup_path = os.path.join(self.source_project_root, 'vue.config.js.bak')
        if os.path.exists(vue_config_path):
            print(f"\n=== 备份配置文件 ===")
            print(f"备份 {vue_config_path} -> {backup_path}")
            shutil.copy2(vue_config_path, backup_path)
            return True
        return False

    def _restore_vue_config(self):
        """恢复原有的vue.config.js文件"""
        vue_config_path = os.path.join(self.source_project_root, 'vue.config.js')
        backup_path = os.path.join(self.source_project_root, 'vue.config.js.bak')
        if os.path.exists(backup_path):
            print(f"\n=== 恢复配置文件 ===")
            print(f"恢复 {backup_path} -> {vue_config_path}")
            shutil.move(backup_path, vue_config_path)
            print("原有配置已恢复")

    def _create_temp_vue_config(self):
        """创建临时的vue.config.js文件，使用绝对路径配置"""
        print(f"\n=== 创建临时构建配置 ===")
        config_content = """const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  publicPath: '',
  productionSourceMap: false,
  filenameHashing: false,
  pages: {
    index: {
      entry: 'src/monitoring-entry.js',
      template: 'public/index.html',
      filename: 'index.html',
      title: '监控管理'
    }
  },
  css: {
    extract: {
      filename: 'css/[name].css',
      chunkFilename: 'css/[name].css'
    }
  },
  configureWebpack: {
    output: {
      filename: 'js/[name].js',
      chunkFilename: 'js/[name].js'
    }
  }
})"""
        vue_config_path = os.path.join(self.source_project_root, 'vue.config.js')
        print(f"创建临时配置文件: {vue_config_path}")
        with open(vue_config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        print("临时配置文件已创建")

    def run_command(self, command, cwd=None):
        """执行shell命令并打印输出"""
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=cwd
            )
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
            
            if process.poll() != 0:
                error = process.stderr.read()
                print(f"错误: {error}")
                return False
            return True
        except Exception as e:
            print(f"执行命令时出错: {e}")
            return False

    def _process_html_file(self, html_path):
        """处理HTML文件，修改资源引用路径"""
        print(f"\n=== 处理HTML文件 ===")
        print(f"正在处理: {html_path}")
        
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print("已读取HTML文件内容")
        
        # 修改资源引用路径
        original_content = content
        content = content.replace('src="/', 'src="')
        content = content.replace('href="/', 'href="')
        
        if content != original_content:
            print("已修改资源引用路径：")
            print("- 移除绝对路径前缀")
            print("- 使用相对路径引用")
        else:
            print("无需修改资源引用路径")
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("HTML文件处理完成")

    def _copy_dist_files(self, source_dist, dist_output):
        """复制dist目录，排除不需要的文件"""
        print(f"复制构建结果: {source_dist} -> {dist_output}")
        
        # 创建目标目录
        os.makedirs(dist_output, exist_ok=True)
        
        # 要排除的文件列表
        exclude_files = ['index.template.html']
        
        # 复制文件，排除不需要的文件
        for root, dirs, files in os.walk(source_dist):
            # 计算相对路径
            rel_path = os.path.relpath(root, source_dist)
            
            # 创建目标子目录
            if rel_path != '.':
                os.makedirs(os.path.join(dist_output, rel_path), exist_ok=True)
            
            # 复制文件
            for file in files:
                if file not in exclude_files:
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(dist_output, rel_path, file)
                    shutil.copy2(src_file, dst_file)
                    print(f"复制文件: {os.path.join(rel_path, file)}")

    def _get_component_name(self):
        """从源文件路径中提取组件名称"""
        # 获取文件名（不含路径和扩展名）
        base_name = os.path.splitext(os.path.basename(self.source_component))[0]
        return base_name

    def build(self):
        """在原项目中构建并复制结果"""
        print("\n=== 开始构建流程 ===")
        start_time = time.time()
        
        # 备份原有配置
        has_backup = self._backup_vue_config()
        
        try:
            # 创建临时配置
            self._create_temp_vue_config()
            
            # 在原项目目录中执行构建
            print("\n=== 执行Vue项目构建 ===")
            if not self.run_command("npm run build", cwd=self.source_project_root):
                print("构建失败")
                return False
            
            # 复制构建结果
            print("\n=== 处理构建结果 ===")
            source_dist = os.path.join(self.source_project_root, 'dist')
            if not os.path.exists(source_dist):
                print("构建后的dist目录不存在")
                return False
            
            # 复制到输出目录
            dist_output = os.path.join(self.output_dir, 'dist')
            if os.path.exists(dist_output):
                print(f"清理已存在的输出目录: {dist_output}")
                shutil.rmtree(dist_output)
            
            # 使用新的复制方法
            self._copy_dist_files(source_dist, dist_output)
            
            # 处理HTML文件中的资源引用路径
            html_file = os.path.join(dist_output, 'index.html')
            if os.path.exists(html_file):
                self._process_html_file(html_file)
            
            # 创建zip文件
            print("\n=== 创建ZIP压缩包 ===")
            timestamp = datetime.now().strftime('%m-%d_%H-%M-%S')
            zip_filename = f"{self.component_name}_{timestamp}.zip"
            zip_path = os.path.join(self.output_dir, zip_filename)
            if os.path.exists(zip_path):
                print(f"删除已存在的ZIP文件: {zip_path}")
                os.remove(zip_path)
            
            print(f"创建新的ZIP文件: {zip_path}")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                file_count = 0
                for root, dirs, files in os.walk(dist_output):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, dist_output)
                        zipf.write(file_path, arcname)
                        file_count += 1
                print(f"已添加 {file_count} 个文件到ZIP压缩包")
            
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            
            print(f"\n=== 构建完成 [耗时: {duration}秒] ===")
            print(f"输出目录: {self.output_dir}")
            print(f"静态文件: {dist_output}")
            print(f"Zip文件: {zip_path}")
            print("\n您可以：")
            print("1. 直接在浏览器中打开 dist/index.html 进行预览")
            print("2. 或解压 static-build.zip 后打开其中的 index.html")
            return True
            
        finally:
            # 恢复原有配置
            if has_backup:
                self._restore_vue_config()

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='构建Vue组件的静态页面')
    parser.add_argument('source', help='源组件文件路径')
    parser.add_argument('output', help='输出目录路径')
    
    args = parser.parse_args()
    
    config = {
        'source_component': args.source,
        'output_dir': args.output
    }
    
    try:
        builder = StaticPageBuilder(config)
        if builder.build():
            print("\n构建成功!")
        else:
            print("\n构建失败!")
            sys.exit(1)
    except Exception as e:
        print(f"\n构建过程中出错: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 