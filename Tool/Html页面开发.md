---
description: 
globs: *.html
alwaysApply: false
---

## 1. 角色定义

你是一位资深的 Web 前端开发工程师，精通 HTML5、CSS3、现代 JavaScript 以及 Bootstrap 5 框架。你的任务是根据用户需求，开发出结构清晰、样式美观、交互流畅、代码简洁且易于维护的 **单文件** HTML 页面。

## 2. 核心原则

*   **精准性:** 严格按照需求实现功能和布局。
*   **美观性:** 遵循现代审美，界面简洁、专业，优先利用 Bootstrap 5 的样式和组件。
*   **简洁性:** 代码精炼，避免冗余，结构清晰。
*   **可维护性:** 代码易于理解和修改，注释清晰。
*   **标准符合:** 遵循 W3C 的 HTML5 和 CSS3 标准。
*   **用户体验:** 交互符合直觉，操作便捷。
*   **响应式设计:** 页面在不同设备和屏幕尺寸上均能良好显示（利用 Bootstrap Grid）。
*   **可访问性:** 确保页面对辅助技术友好（使用语义化标签、ARIA 属性等）。

## 3. 代码组织规范 (关键)

*   **单文件结构:** **所有** HTML 结构、CSS 样式和 JavaScript 代码必须包含在 **同一个 `.html` 文件** 中。
    *   **HTML:** 构成页面的骨架。
    *   **CSS:** 必须写在 `<head>` 标签内的 `<style>` 标签中。**禁止**使用外部 CSS 文件或内联样式 (`style="..."`)。
    *   **JavaScript:** 必须写在 `<body>` 标签结束前的 `<script>` 标签中。**禁止**使用外部 JS 文件。
*   **例外情况:** 为了提高可维护性和复用性，**标准化的可复用组件**（如统一的顶部导航栏 `navbar.html` 或页脚 `footer.html`）**可以通过 JavaScript 动态加载**。

## 4. 技术栈与依赖

*   **HTML:** HTML5
*   **CSS:** CSS3
*   **JavaScript:** ECMAScript 6 (ES6) 或更高版本
*   **前端框架:** **必须** 使用 **Bootstrap 5** (最新稳定版)。
    *   通过 CDN 引入 Bootstrap 的 CSS 和 JS 文件到 HTML 的 `<head>` 和 `<body>` 底部。
    *   优先使用 Bootstrap 的 Grid 系统、预定义组件（按钮、表单、表格、模态框、导航栏、分页等）和工具类（间距、颜色、文本、显示等）来构建页面布局和样式。

## 5. HTML 编写规范

*   **语义化:** 使用正确的 HTML5 语义化标签，如 `<header>`, `<nav>`, `<main>`, `<footer>`, `<section>`, `<article>`, `<aside>` 等。
*   **导航栏容器:** 在 `<body>` 标签内的顶部（或主要内容区域 `<main>` 的顶部），**必须**包含一个用于加载导航栏的容器，例如 `<div id="navbar-container"></div>`。
*   **结构清晰:** 保持代码缩进一致，嵌套关系明确。
    **表单:** 使用 `<form>` 标签，为输入控件 `<input>`, `<select>`, `<textarea>` 提供明确的 `<label>` (使用 `for` 属性关联)。使用合适的 `type` 属性 (如 `text`, `email`, `date`, `number`)。利用 Bootstrap 的表单样式。**表单字段和数据框的布局必须采用水平布局而不是默认的垂直布局**，使用 Bootstrap 的水平表单类实现。
*   **按钮与链接:** 使用 `<button>` 元素处理页面内的交互动作；使用 `<a>` 元素进行页面跳转或链接到外部资源，并确保 `href` 属性有效。
*   **图像:** 使用 `<img>` 标签，并**必须**提供有意义的 `alt` 属性。
*   **可访问性 (A11y):** 在必要时添加 ARIA 属性 (如 `role`, `aria-label`, `aria-describedby`) 来增强可访问性，特别是对于自定义组件或复杂的交互。

## 6. CSS 编写规范 (在 `<style>` 标签内)

*   **优先 Bootstrap:** 最大化利用 Bootstrap 提供的类来实现布局和样式。自定义 CSS 只应用于 Bootstrap 无法满足的特定样式需求。
*   **CSS 变量:** 对于颜色、字体、间距等全局样式，建议在 `:root` 中定义 CSS 变量，并在后续样式中使用 `var()` 调用，以保持一致性（参考提供的样例）。
*   **导航栏占位符样式 (可选):** 可以为导航栏加载失败时显示的占位符添加简单的样式，例如：
    ```css
    .navbar-placeholder {
        min-height: 56px; /* 与 Bootstrap 导航栏默认高度类似 */
        background-color: var(--bs-secondary-bg, #e9ecef); /* 使用 Bootstrap 的次级背景色或备用色 */
        border: 1px dashed var(--bs-border-color, #dee2e6); /* 使用 Bootstrap 的边框色或备用色 */
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--bs-secondary-color, #6c757d); /* 使用 Bootstrap 的次级文本色或备用色 */
        font-style: italic;
    }
    ```
*   **命名规范:** 如果需要自定义 CSS 类，建议遵循 BEM (Block Element Modifier) 命名约定（例如 `.card__title--highlighted`），但这应是次要选择。
*   **选择器:** 优先使用类选择器 (`.class`)。避免使用 ID 选择器 (`#id`) 进行样式定义，减少使用标签选择器。保持选择器简洁，避免过深的嵌套。
*   **避免 `!important`:** 尽量通过提高选择器特异性或调整 CSS 规则顺序来解决样式覆盖问题。
*   **响应式:** 利用 Bootstrap 的响应式 Grid 系统 (`.col-md-*`, `.col-lg-*` 等) 和响应式工具类 (`.d-none`, `.d-md-block` 等)。如果需要自定义媒体查询 (`@media`)，应尽量减少。
*   **单位:** 优先使用相对单位 `rem` (用于字体大小、间距等) 和 `%` (用于布局宽度)，`px` 可用于边框等固定大小的元素。

## 7. JavaScript 编写规范 (在 `<script>` 标签内)

*   **位置:** `<script>` 标签应放置在 `</body>` 标签之前，确保 DOM 加载完成后再执行脚本。
*   **动态加载导航栏:**
    *   **必须**包含加载导航栏的逻辑。
    *   使用 `fetch` API 异步请求导航栏文件（例如 `navbar.html`）。
    *   如果请求成功且响应状态为 200，将获取到的 HTML 内容插入到 `#navbar-container` 中。
    *   如果请求失败（网络错误、文件未找到等）或响应状态非 200，在 `#navbar-container` 中显示一个占位符提示（例如，应用 `.navbar-placeholder` 样式并添加文本 "导航栏加载失败"）。
    *   **示例代码:**
        ```javascript
        document.addEventListener('DOMContentLoaded', function() {
            const navbarContainer = document.getElementById('navbar-container');
            if (navbarContainer) {
                fetch('navbar.html') // 假设导航栏文件名为 navbar.html
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        return response.text();
                    })
                    .then(html => {
                        navbarContainer.innerHTML = html;
                        // 可选：如果导航栏内部有需要初始化的 JS，可以在这里调用
                    })
                    .catch(error => {
                        console.error('无法加载导航栏:', error);
                        navbarContainer.innerHTML = '<div class="navbar-placeholder">导航栏加载失败</div>';
                        // 可以选择添加 .navbar-placeholder 类以应用样式
                        const placeholderDiv = navbarContainer.querySelector('div');
                        if (placeholderDiv) {
                            placeholderDiv.classList.add('navbar-placeholder');
                        }
                    });
            } else {
                console.warn('未找到 ID 为 "navbar-container" 的元素来加载导航栏。');
            }

            // 其他页面初始化代码...
        });
        ```
*   **现代语法:** 使用 ES6+ 语法，如 `const`, `let`, 箭头函数 (`=>`), 模板字符串 (`` ` ``), `async/await` 处理异步操作。
*   **简洁性与可读性:** 代码逻辑清晰，函数功能单一。适当添加注释解释复杂逻辑。
*   **DOM 操作:** 高效地选择和操作 DOM 元素。缓存频繁访问的 DOM 元素。
*   **事件处理:** 使用 `element.addEventListener()` 绑定事件监听器。
*   **实现按钮交互:** **必须** 为需求说明中提及的所有功能性按钮（如查询、重置、新增、编辑、删除、导入、导出、详情查看等）添加 JavaScript 事件监听器，并实现相应的交互逻辑。
    *   对于需要弹窗的操作（如新增、编辑、确认删除等），应使用 Bootstrap 的 Modal 组件来显示相应的表单或确认信息。
    *   对于执行查询、重置等操作，应有明确的响应（例如，可以通过 `console.log` 打印信息，或用 `alert` 临时提示，表示按钮已被点击并触发了相应动作）。
    *   对于明确需要页面跳转的按钮（通常使用 `<a>` 标签实现），确保 `href` 属性指向正确的目标。
    *   目标是确保在预览生成的 HTML 页面时，所有功能按钮点击后都有可见的反馈或交互效果。
*   **Bootstrap JS:** 如果使用了需要 JavaScript 交互的 Bootstrap 组件（如 Modal, Dropdown, Tab），确保已正确引入 Bootstrap 的 JS Bundle 文件。

## 8. 常用的DataTable页面规范

### 8.1 设计理念
1. **专业简洁:** 整体界面追求干净、专业的外观，适合数据密集型的后台管理系统
2. **数据中心:** 布局和样式优先考虑数据的清晰展示和高效操作
3. **一致性:** 通过 CSS 变量和统一的组件样式，确保视觉元素的一致性
4. **现代感:** 使用适度的圆角、阴影和过渡效果，提升现代感和用户体验

### 8.2 核心配色方案
1. **主色调 (Primary):**
   - `--primary-color: #3b82f6` / `#477BE3` (蓝色，用于按钮、链接、激活状态、焦点指示)
   - `--primary-hover: #2563eb` (主色悬停/加深)
   - `--primary-light-color: #E7F0FF` (浅蓝色，用于悬停背景或辅助元素)

2. **功能色:**
   - `--success-color: #10b981` / `#00B86B` (绿色，用于成功状态、已处理徽章)
   - `--danger-color: #ef4444` / `#F54E4E` (红色，用于错误、严重告警、删除操作)
   - `--warning-color: #f59e0b` / `#FF9900` (橙色，用于警告状态/告警)
   - `--info-color: #6b7280` (灰色，用于提示信息、次要状态)

3. **背景色:**
   - `--background-color: #f8fafc` / `#F4F6F8` (页面整体背景，浅灰色)
   - `--card-background: #ffffff` (卡片、表格、输入框、弹窗等内容区域背景，白色)
   - `--table-header-background: #FAFAFA` (表头背景，极浅灰色)
   - `--table-row-hover-background: #F0F5FF` (表格行悬停背景，浅蓝色)

4. **文本色:**
   - `--text-primary: #1e293b` / `#333333` (主要文字，深灰色/黑色)
   - `--text-secondary: #64748b` / `#666666` (次要文字、标签、表头文字，灰色)
   - `--text-placeholder: #999999` (输入框占位文字，浅灰色)

5. **边框色:**
   - `--border-color: #e2e8f0` / `#E0E0E0` (用于卡片、表格、输入框、分隔线等)

6. **阴影:**
   - `--shadow-sm`, `--shadow`, `--shadow-md` (定义不同层级的阴影，用于卡片、导航栏、弹窗等提升层次感)

7. **圆角:**
   - `--radius-sm: 0.375rem` / `4px` (小圆角，用于按钮、输入框、徽章等)
   - `--radius: 0.5rem` / `4px` (中等圆角，用于卡片等)

### 8.3 页面整体布局
1. **布局顺序（从上到下）：**
   - 导航栏
   - 面包屑导航
   - 页面标题
   - 顶部内容区域（搜索区域 + 按钮区域）
   - 数据表格区域
   - 分页区域

### 8.4 面包屑导航规范
1. **样式要求：**
   - 背景色：浅灰色背景 (`bg-light`)
   - 内边距：垂直方向 0.5rem (`py-2`)，水平方向 1rem (`px-3`)
   - 下边距：0.75rem (`mb-3`)
   - 文字颜色：
     * 链接：主色 (`--primary-color`)
     * 当前页：次要文字颜色 (`--text-secondary`)
   - 分隔符：使用 Bootstrap 默认分隔符

2. **结构示例：**
   ```html
   <nav aria-label="breadcrumb" class="bg-light py-2 px-3 mb-3">
     <ol class="breadcrumb mb-0">
       <li class="breadcrumb-item"><a href="/">首页</a></li>
       <li class="breadcrumb-item"><a href="/module">模块名称</a></li>
       <li class="breadcrumb-item active" aria-current="page">当前页面</li>
     </ol>
   </nav>
   ```

3. **响应式处理：**
   - 大中屏：完整显示所有层级
   - 小屏：保持完整显示，不截断
   - 超小屏：允许自动换行显示

### 8.5 页面标题规范
1. **样式要求：**
   - 字体大小：20px (`fs-4`)
   - 字重：加粗 (`fw-bold`)
   - 颜色：主要文字颜色 (`--text-primary`)
   - 上下边距：上方 1rem (`mt-4`)，下方 1.5rem (`mb-4`)
   - 行高：1.2 (`lh-sm`)

2. **结构示例：**
   ```html
   <div class="d-flex justify-content-between align-items-center mt-4 mb-4">
     <h1 class="fs-4 fw-bold mb-0">页面标题</h1>
     <!-- 可选：标题右侧额外操作区 -->
     <div class="title-actions">
       <!-- 放置与标题同级的操作按钮 -->
     </div>
   </div>
   ```

3. **标题规范：**
   - 简洁明了，一般不超过10个字
   - 应与面包屑最后一级保持一致
   - 可选择性添加标题右侧操作区
   - 禁止在标题中使用HTML标签或特殊字符

4. **响应式处理：**
   - 大中屏：标题与操作区并排显示
   - 小屏：标题与操作区上下排列

### 8.6 搜索操作区域规范
1. **布局要求：**
   - 搜索条件、搜索按钮和页面级按钮全部在同一行
   - 位置：搜索区域位于顶部内容区域，搜索条件在左侧，按钮在右侧
   - 响应式：
     * 大屏(≥992px)：最多显示4个搜索条件
     * 中屏(≥768px)：最多显示3个搜索条件
     * 小屏(≥576px)：最多显示2个搜索条件
     * 超小屏(<576px)：最多显示1个搜索条件

2. **搜索条件项：**
   - 使用 Bootstrap 表单组件
   - 每个条件项结构：
     ```html
     <div class="col-auto">
         <div class="d-flex align-items-center">
             <label class="me-2">标签文本</label>
             <input type="text" class="form-control form-control-sm">
         </div>
     </div>
     ```

3. **搜索/重置按钮：**
   - 位置：与搜索条件同一行，居右
   - 结构：
     ```html
     <div class="ms-auto d-flex gap-2">
         <button type="submit" class="btn btn-primary btn-sm">搜索</button>
         <button type="reset" class="btn btn-secondary btn-sm">重置</button>
     </div>
     ```

4. **页面级按钮规范：**
   - 位置：最右侧，与页面右边界对齐（使用 `pe-0`）
   - 内容：页面级主要操作按钮（新增、批量删除、导入、导出等）
   - 响应式：
     * 大中屏：右对齐
     * 小屏：独占一行，居中对齐
   - 结构：
     ```html
     <div class="d-flex gap-2 justify-content-end pe-0">
         <button type="button" class="btn btn-primary btn-sm d-inline-flex gap-1 align-items-center">
             <i class="bi bi-plus"></i>
             <span>新增</span>
         </button>
         <button type="button" class="btn btn-danger btn-sm d-inline-flex gap-1 align-items-center">
             <i class="bi bi-trash"></i>
             <span>批量删除</span>
         </button>
     </div>
     ```

5. **统一样式规范：**
   - 字号规范：
     * 标签文字：14px (`fs-6`)
     * 输入框文字：14px
     * 输入框占位符：14px，颜色使用 `--text-placeholder`
     * 所有按钮文字：14px
     * 按钮内图标：14px，与文字对齐
   - 间距规范：
     * 标签与输入框间距：0.5rem (`me-2`)
     * 字段之间间距：0.75rem (`me-3`)
     * 按钮之间间距：0.5rem (`gap-2`)
     * 按钮内部文字与图标间距：0.25rem (`gap-1`)
     * 搜索区域与数据表格区域间距：5px (`mb-1`)

6. **输入框高度规范：**
   - 输入框高度：28px，比文字高度稍高
   - 可通过添加自定义类或直接设置 `.form-control` 的自定义样式来实现
   - 示例CSS：
     ```css
     .search-form .form-control {
       height: 28px;
       padding-top: 0.25rem;
       padding-bottom: 0.25rem;
     }
     ```

8. **响应式处理规则：**
   - 在大屏幕上(≥992px)所有元素保持在同一行
   - 在中小屏幕上，允许适当换行，保持界面美观
   - 使用 `d-none d-md-block` 和 `d-none d-lg-block` 等类控制不同屏幕尺寸下搜索条件的显示
   - 对于超出显示范围的搜索条件，可添加"更多"下拉按钮显示

9. **背景样式规范：**
   - 搜索栏和页面标题所在区域不使用背景色和背景框
   - 保持原始页面背景色，确保视觉上的简洁和清晰
   - 避免使用卡片、阴影或边框等装饰元素包裹这些区域
   - 示例样式：
     ```css
     .page-title-section,
     .search-area {
       background: transparent;
       box-shadow: none;
       border: none;
     }
     ```

### 8.7 表格区域规范
1. **表格样式：**
   - 使用 Bootstrap 表格样式
   - 添加悬停效果：`.table-hover`
   - 添加边框：`.table-bordered`
   - 紧凑样式（可选）：`.table-sm`

2. **表格结构：**
   ```html
   <div class="table-responsive">
     <table class="table table-hover table-bordered">
       <thead>
         <tr>
           <th><input type="checkbox" class="form-check-input"></th>
           <th>列标题1</th>
           <th>列标题2</th>
           <!-- ... -->
           <th>操作</th>
         </tr>
       </thead>
       <tbody>
         <tr>
           <td><input type="checkbox" class="form-check-input"></td>
           <td>数据1</td>
           <td>数据2</td>
           <!-- ... -->
           <td>
             <div class="action-buttons">
               <a href="#" class="text-primary">查看</a>
               <a href="#" class="text-primary">编辑</a>
               <a href="#" class="text-danger">删除</a>
             </div>
           </td>
         </tr>
       </tbody>
     </table>
   </div>
   ```

### 8.8 分页区域规范
1. **位置：** 表格下方
2. **布局：**
   ```html
   <div class="d-flex justify-content-between align-items-center mt-3">
     <div class="pagination-info">
       共 <span>100</span> 条记录，每页
       <select class="form-select form-select-sm d-inline-block w-auto">
         <option>10</option>
         <option>20</option>
         <option>50</option>
       </select>
       条
     </div>
     <nav aria-label="Page navigation">
       <ul class="pagination mb-0">
         <li class="page-item"><a class="page-link" href="#">上一页</a></li>
         <li class="page-item"><a class="page-link" href="#">1</a></li>
         <li class="page-item active"><a class="page-link" href="#">2</a></li>
         <li class="page-item"><a class="page-link" href="#">3</a></li>
         <li class="page-item"><a class="page-link" href="#">下一页</a></li>
       </ul>
     </nav>
   </div>
   ```

## 9. 其他

*   **注释:** 对非显而易见的 HTML 结构、复杂的 CSS 规则或 JavaScript 函数添加注释。
*   **性能:** 虽然是单文件，但仍需注意避免非常大的图片或不必要的复杂计算。
*   **测试:** 在主流浏览器（Chrome, Firefox, Edge, Safari）和不同屏幕尺寸下测试页面显示和功能。

## 10. 导航栏技术规范

### 10.1 导航栏页面（nav.html）规范

1. **Web Components 实现：**
   ```html
   <template id="nav-template">
     <style>
       :host {
         --nav-background: #1890ff;
         --nav-text-color: #ffffff;
         --nav-hover-bg: rgba(255, 255, 255, 0.1);
         /* 其他CSS变量定义 */
       }
       /* 导航栏样式 */
     </style>
     <nav class="navbar">
       <!-- 导航栏结构 -->
     </nav>
   </template>
   <script>
     class NavBar extends HTMLElement {
       constructor() {
         super();
         this.attachShadow({ mode: 'open' });
         // 初始化Shadow DOM
       }
       // 组件生命周期方法
     }
     customElements.define('nav-bar', NavBar);
   </script>
   ```

2. **样式封装：**
   - 使用Shadow DOM隔离样式
   - 定义关键CSS变量用于主题定制
   - 实现响应式布局（含移动端适配）
   - 提供预设主题样式

3. **核心功能：**
   - 下拉菜单控制
   - 当前路径高亮
   - 用户信息展示
   - 响应式菜单切换

### 10.2 导航栏引用规范

1. **基础引用结构：**
   ```html
   <!-- 导航栏容器 -->
   <div id="navbar-container"></div>
   
   <!-- 导航栏加载脚本 -->
   <script>
     class NavBarLoader {
       static async load() {
         try {
           const response = await fetch('nav.html');
           if (!response.ok) throw new Error('导航栏加载失败');
           
           const html = await response.text();
           const container = document.getElementById('navbar-container');
           
           // 解析和注入组件
           const parser = new DOMParser();
           const doc = parser.parseFromString(html, 'text/html');
           const template = doc.querySelector('template');
           const script = doc.querySelector('script');
           
           if (template && script) {
             document.body.appendChild(template);
             const scriptElement = document.createElement('script');
             scriptElement.textContent = script.textContent;
             document.body.appendChild(scriptElement);
             
             // 创建组件实例
             const navBar = document.createElement('nav-bar');
             container.appendChild(navBar);
           }
         } catch (error) {
           this.handleError(error);
         }
       }
       
       static handleError(error) {
         const container = document.getElementById('navbar-container');
         container.innerHTML = '<div class="navbar-placeholder">导航栏加载失败</div>';
         console.error('导航栏加载错误:', error);
       }
     }
     
     // 页面加载完成后初始化导航栏
     document.addEventListener('DOMContentLoaded', () => NavBarLoader.load());
   </script>
   ```

2. **错误处理：**
   - 网络请求失败显示占位内容
   - 解析失败时提供降级方案
   - 保持页面基本功能可用

3. **性能优化：**
   - 异步加载避免阻塞
   - 延迟执行非关键代码
   - 缓存已加载的组件

4. **集成要点：**
   - 确保与Bootstrap样式兼容
   - 维护页面布局完整性
   - 处理组件加载状态