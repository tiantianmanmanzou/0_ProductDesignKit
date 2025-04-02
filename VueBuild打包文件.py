#!/usr/bin/env python3
import os
import subprocess
import shutil
import sys
from pathlib import Path

class StaticPageBuilder:
    def __init__(self):
        self.project_name = "my-static-datapublish"
        self.source_component = "9_实时消费服务/vue_shihsi/src/components/DataPublish.vue"
        self.current_dir = os.getcwd()
        
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

    def check_requirements(self):
        """检查必要的工具是否安装"""
        print("检查环境要求...")
        
        # 检查 node 和 npm
        if not self.run_command("node --version"):
            print("请先安装 Node.js")
            return False
        
        # 检查 vue-cli
        if not self.run_command("vue --version"):
            print("正在安装 Vue CLI...")
            if not self.run_command("npm install -g @vue/cli"):
                return False
        
        return True

    def create_vue_project(self):
        """创建 Vue 项目"""
        print("\n1. 创建 Vue 2 项目...")
        
        # 如果目录已存在，先删除
        if os.path.exists(self.project_name):
            shutil.rmtree(self.project_name)
        
        # 创建新项目
        if not self.run_command(f"vue create {self.project_name} -p default -m npm"):
            return False
        
        return True

    def install_dependencies(self):
        """安装项目依赖"""
        print("\n2. 安装 Element UI...")
        return self.run_command("npm install element-ui", cwd=self.project_name)

    def copy_component(self):
        """复制组件文件"""
        print("\n3. 复制组件文件...")
        try:
            # 创建组件目录
            components_dir = os.path.join(self.project_name, "src", "components")
            os.makedirs(components_dir, exist_ok=True)
            
            # 复制组件文件
            shutil.copy2(self.source_component, components_dir)
            return True
        except Exception as e:
            print(f"复制组件文件时出错: {e}")
            return False

    def update_main_js(self):
        """更新 main.js 文件"""
        print("\n4. 更新 main.js...")
        main_js_content = '''import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

Vue.config.productionTip = false
Vue.use(ElementUI)

new Vue({
  render: h => h(App),
}).$mount('#app')
'''
        try:
            with open(os.path.join(self.project_name, "src", "main.js"), "w") as f:
                f.write(main_js_content)
            return True
        except Exception as e:
            print(f"更新 main.js 时出错: {e}")
            return False

    def update_app_vue(self):
        """更新 App.vue 文件"""
        print("\n5. 更新 App.vue...")
        app_vue_content = '''<template>
  <div id="app">
    <DataPublish />
  </div>
</template>

<script>
import DataPublish from './components/DataPublish.vue'

export default {
  name: 'App',
  components: {
    DataPublish
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  padding: 0;
  margin: 0;
}
</style>
'''
        try:
            with open(os.path.join(self.project_name, "src", "App.vue"), "w") as f:
                f.write(app_vue_content)
            return True
        except Exception as e:
            print(f"更新 App.vue 时出错: {e}")
            return False

    def create_vue_config(self):
        """创建 vue.config.js 文件"""
        print("\n6. 创建 vue.config.js...")
        config_content = '''const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: './'
})
'''
        try:
            with open(os.path.join(self.project_name, "vue.config.js"), "w") as f:
                f.write(config_content)
            return True
        except Exception as e:
            print(f"创建 vue.config.js 时出错: {e}")
            return False

    def build_project(self):
        """构建项目"""
        print("\n7. 构建项目...")
        return self.run_command("npm run build", cwd=self.project_name)

    def create_zip(self):
        """创建 zip 文件"""
        print("\n8. 创建 zip 文件...")
        dist_dir = os.path.join(self.project_name, "dist")
        if not os.path.exists(dist_dir):
            print("dist 目录不存在，构建可能失败")
            return False
            
        return self.run_command(
            "zip -r ../static-datapublish.zip *",
            cwd=dist_dir
        )

    def build(self):
        """执行完整的构建过程"""
        steps = [
            (self.check_requirements, "环境检查"),
            (self.create_vue_project, "创建 Vue 项目"),
            (self.install_dependencies, "安装依赖"),
            (self.copy_component, "复制组件"),
            (self.update_main_js, "更新 main.js"),
            (self.update_app_vue, "更新 App.vue"),
            (self.create_vue_config, "创建配置文件"),
            (self.build_project, "构建项目"),
            (self.create_zip, "创建 zip 文件")
        ]
        
        for step_func, step_name in steps:
            print(f"\n{'='*20} {step_name} {'='*20}")
            if not step_func():
                print(f"\n❌ {step_name}失败")
                return False
            print(f"✅ {step_name}完成")
        
        print(f"\n🎉 构建成功！")
        print(f"静态文件位于: {os.path.join(self.current_dir, self.project_name, 'dist')}")
        print(f"压缩包位于: {os.path.join(self.current_dir, self.project_name, 'static-datapublish.zip')}")
        return True

def main():
    builder = StaticPageBuilder()
    builder.build()

if __name__ == "__main__":
    main() 