# Vue项目静态文件打包配置文档

## 概述
本文档介绍如何配置Vue项目，使打包后的静态文件在浏览器中打开时自动跳转到指定页面，而不是默认首页。

## 配置方法

### 1. 修改 vue.config.js

在项目根目录的 `vue.config.js` 文件中添加以下配置：

```javascript
module.exports = {
  publicPath: './',
  chainWebpack: (config) => {
    config
      .plugin('html')
      .tap(args => {
        // 修改HTML模板的minify选项以避免删除我们添加的脚本
        if (args[0].minify) {
          args[0].minify.removeComments = false;
          args[0].minify.minifyJS = false;
        }
        return args;
      });
  },
  configureWebpack: (config) => {
    // 添加一个简单的webpack插件来修改HTML
    config.plugins.push({
      apply: (compiler) => {
        compiler.hooks.emit.tapAsync('AddAutoRedirect', (compilation, callback) => {
          if (compilation.assets['index.html']) {
            let html = compilation.assets['index.html'].source();
            html = html.replace(
              '</body>',
              `<script>
                // 强制跳转到指定页面
                function forceRedirect() {
                  if (window.location.hash === '' || window.location.hash === '#/' || window.location.hash === '#/portal') {
                    window.location.hash = '#/governance/datastandard/management/data-element';
                  }
                }
                // 页面加载时立即执行
                forceRedirect();
                // DOM加载完成后再次执行
                window.addEventListener('DOMContentLoaded', forceRedirect);
                // 页面完全加载后再次执行
                window.addEventListener('load', forceRedirect);
                // 监听hash变化，防止被重定向回portal
                window.addEventListener('hashchange', function() {
                  setTimeout(function() {
                    if (window.location.hash === '#/portal') {
                      window.location.hash = '#/governance/datastandard/management/data-element';
                    }
                  }, 100);
                });
              </script></body>`
            );
            compilation.assets['index.html'] = {
              source: () => html,
              size: () => html.length
            };
          }
          callback();
        });
      }
    });
  }
};
```

### 2. 自定义目标页面

要跳转到不同的页面，只需修改配置中的目标路由：

```javascript
// 将此行中的路由路径替换为你想要的目标页面
window.location.hash = '#/你的目标路由路径';
```

**常见目标路由示例：**
- 数据元标准：`#/governance/datastandard/management/data-element`
- 用户管理：`#/user-management/user`
- 日志管理：`#/log-management`
- 数据建模：`#/governance/datamodel/catalog`

### 3. 构建和分享

#### 构建静态文件
```bash
npm run build
```

#### 分享方法
1. 构建完成后，压缩整个 `dist` 文件夹
2. 发送给其他人
3. 接收方解压后，双击 `index.html` 即可在浏览器中直接查看指定页面

## 配置特点

### 强制跳转逻辑
- **立即执行**：页面加载时立即检查并跳转
- **多重检测**：在DOMContentLoaded和load事件中再次检查
- **防回退**：监听hash变化，防止被Vue路由重定向回默认页面
- **兼容性好**：支持直接用浏览器打开HTML文件

### 检测条件
跳转会在以下情况触发：
- URL hash为空
- URL hash为 `#/`
- URL hash为 `#/portal`（可根据项目调整）

## 注意事项

1. **路由确认**：确保目标路由在项目中存在且配置正确
2. **相对路径**：`publicPath: './'` 确保静态文件使用相对路径，支持离线查看
3. **一次配置**：配置完成后，每次 `npm run build` 都会自动应用
4. **备份原文件**：建议在修改前备份原始的 `vue.config.js`

## 使用场景

- **演示分享**：将特定功能页面直接分享给他人查看
- **离线预览**：无需服务器环境，直接在浏览器中查看
- **功能展示**：快速展示项目中的特定模块或页面
- **测试部署**：验证特定页面的静态构建效果

## 扩展配置

### 多条件跳转
可以根据不同条件跳转到不同页面：

```javascript
function forceRedirect() {
  const hash = window.location.hash;
  if (hash === '' || hash === '#/') {
    window.location.hash = '#/governance/datastandard/management/data-element';
  } else if (hash === '#/portal') {
    window.location.hash = '#/governance/datastandard/management/data-element';
  }
  // 可以添加更多条件
}
```

### 延迟跳转
如果需要延迟跳转：

```javascript
setTimeout(function() {
  forceRedirect();
}, 500); // 延迟500ms
```

这个配置方法可以复用到其他Vue项目中，只需要修改目标路由路径即可。