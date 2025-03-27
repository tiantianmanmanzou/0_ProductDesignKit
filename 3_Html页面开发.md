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
*   **表单:** 使用 `<form>` 标签，为输入控件 `<input>`, `<select>`, `<textarea>` 提供明确的 `<label>` (使用 `for` 属性关联)。使用合适的 `type` 属性 (如 `text`, `email`, `date`, `number`)。利用 Bootstrap 的表单样式。
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

## 8. 特定页面布局规范 (参考样例)

*   **顶部内容区域 (包含搜索与操作):**
    *   通常位于页面标题下方（或导航栏下方），在主要内容（如表格）上方。
    *   **强制要求:** 搜索区域 (`.search-area`) 和页面级操作按钮区域 (`.top-actions`) **必须** 放置在 **同一个容器** 内（例如 `<div class="card p-3 top-content-area">`）。
    *   **布局实现:**
        *   **推荐:** 在父容器内使用 **Bootstrap Grid (`row` 和 `col-*`)**。这是最稳定可靠的方式。
        *   **方法:** 使用 `<div class="row">` 包裹搜索区和按钮区。将搜索区放入一个 `col-*`（如 `col-md-8`），将按钮区放入另一个 `col-*`（如 `col-md-4`）。在按钮区的 `col-*` 上添加 `d-flex justify-content-end` 使按钮在该列内右对齐。
    *   **目标:** 确保搜索区域和操作按钮区域在 **同一行显示，避免换行**，且搜索区居左，按钮区居右。
    *   **示例 (Grid 布局):**
        ```html
        <div class="card p-3 top-content-area mb-4">
            <div class="row w-100 align-items-end">
                <div class="col-md-8 col-lg-9 search-area">
                    <!-- 搜索表单 -->
                    <form class="filter-form">
                        <!-- ... form content ... -->
                    </form>
                </div>
                <div class="col-md-4 col-lg-3 top-actions d-flex justify-content-end">
                    <!-- 页面级按钮 -->
                    <button class="btn btn-primary ms-2">新增</button>
                    <button class="btn btn-secondary ms-2">导出</button>
                </div>
            </div>
        </div>
        ```
*   **搜索区域 (`.search-area`):**
    *   位于顶部内容区域的左侧（由 Grid 列定义）。
    *   包含表单元素（输入框、下拉选择、日期选择器等）和搜索/重置按钮。
    *   使用 Bootstrap 的表单和按钮组件。
    *   **注意:** 为了保持单行布局，应合理控制搜索条件的数量。如果搜索条件过多，考虑使用更紧凑的布局或允许用户在请求时指定所需的搜索字段数量（例如，明确说明需要几个输入框）。
*   **页面级操作按钮区域 (`.top-actions`):**
    *   位于顶部内容区域的右侧。
    *   包含页面级别的主要操作按钮（如 新增、批量删除、导入、导出等）。
    *   使用 Bootstrap 按钮组件。
*   **表格区域 (`.table-container`):**
    *   位于搜索和操作区域下方。
    *   使用 Bootstrap 的表格样式 (`.table`, `.table-hover` 等)。
    *   包含表头 (`<thead>`) 和表体 (`<tbody>`)。
    *   操作列（如 查看、编辑、删除）通常放在表格最右侧。
*   **分页区域 (`.pagination-container`):**
    *   位于表格下方。
    *   包含分页信息（总条数、每页显示数量）和分页控件。
    *   使用 Bootstrap 的分页组件 (`.pagination`)。
    *   通常右对齐。

## 9. 其他

*   **注释:** 对非显而易见的 HTML 结构、复杂的 CSS 规则或 JavaScript 函数添加注释。
*   **性能:** 虽然是单文件，但仍需注意避免非常大的图片或不必要的复杂计算。
*   **测试:** 在主流浏览器（Chrome, Firefox, Edge, Safari）和不同屏幕尺寸下测试页面显示和功能。

## 10. 推荐样式风格 (基于 tablepage.html 样例)

以下样式规范总结自 `tablepage.html` 样例，推荐在开发数据密集型后台管理页面时参考，以保持视觉风格统一和专业性。

**1. 整体风格与理念**

*   **专业简洁:** 整体界面追求干净、专业的外观，适合数据密集型的后台管理系统。
*   **数据中心:** 布局和样式优先考虑数据的清晰展示和高效操作。
*   **一致性:** 通过 CSS 变量和统一的组件样式，确保视觉元素的一致性。
*   **现代感:** 使用适度的圆角、阴影和过渡效果，提升现代感和用户体验。

**2. 核心配色方案 (通过 CSS 变量定义)**

*   **主色调 (Primary):**
    *   `--primary-color: #3b82f6` / `#477BE3` (蓝色，用于按钮、链接、激活状态、焦点指示)
    *   `--primary-hover: #2563eb` (主色悬停/加深)
    *   `--primary-light-color: #E7F0FF` (浅蓝色，用于悬停背景或辅助元素)
*   **功能色:**
    *   `--success-color: #10b981` / `#00B86B` (绿色，用于成功状态、已处理徽章)
    *   `--danger-color: #ef4444` / `#F54E4E` (红色，用于错误、严重告警、删除操作)
    *   `--warning-color: #f59e0b` / `#FF9900` (橙色，用于警告状态/告警)
    *   `--info-color: #6b7280` (灰色，用于提示信息、次要状态)
*   **背景色:**
    *   `--background-color: #f8fafc` / `#F4F6F8` (页面整体背景，浅灰色)
    *   `--card-background: #ffffff` (卡片、表格、输入框、弹窗等内容区域背景，白色)
    *   `--table-header-background: #FAFAFA` (表头背景，极浅灰色)
    *   `--table-row-hover-background: #F0F5FF` (表格行悬停背景，浅蓝色)
*   **文本色:**
    *   `--text-primary: #1e293b` / `#333333` (主要文字，深灰色/黑色)
    *   `--text-secondary: #64748b` / `#666666` (次要文字、标签、表头文字，灰色)
    *   `--text-placeholder: #999999` (输入框占位文字，浅灰色)
*   **边框色:**
    *   `--border-color: #e2e8f0` / `#E0E0E0` (用于卡片、表格、输入框、分隔线等)
*   **阴影:**
    *   `--shadow-sm`, `--shadow`, `--shadow-md` (定义不同层级的阴影，用于卡片、导航栏、弹窗等提升层次感)
*   **圆角:**
    *   `--radius-sm: 0.375rem` / `4px` (小圆角，用于按钮、输入框、徽章等)
    *   `--radius: 0.5rem` / `4px` (中等圆角，用于卡片等)

**3. 布局规范**

*   **整体布局:**
    *   主要内容区域 (`.content-container` 或直接在 `<body>` 上应用样式) 使用左右内边距 (如 `padding: 0 24px` 或 `px-4`)，上下外边距 (如 `margin: 24px 0` 或 `mt-3`)。
*   **页面标题 (`.page-title`):** 字体较大 (如 `20px`)，加粗，位于内容区顶部。
*   **搜索与操作区 (`.top-content-area`):**
    *   使用 `display: flex`，`justify-content: space-between` 将搜索区和页面级操作按钮区分开。
    *   整体放置在一个白色背景、带阴影的卡片式容器中 (`.card`)。
    *   **搜索区 (`.search-area`):** 占据主要宽度，内部搜索表单 (`.search-form`) 也使用 `display: flex`，`flex-wrap: wrap` (允许换行)，`align-items: flex-end` (使标签和输入框底部对齐)，并通过 `gap` 控制间距。
    *   **页面操作区 (`.top-actions`):** 放置页面级别按钮（如新建、批量操作、导出），使用 `display: flex` 和 `gap` 控制按钮间距，通常与搜索区底部对齐 (`align-self: flex-end`)。
*   **表格区域 (`.table-container`):**
    *   使用白色背景 (`--card-background`)、圆角 (`--radius`)、阴影 (`--shadow-sm`) 和边框 (`--border-color`) 的卡片式容器 (`.card`)。
    *   容器内使用 `overflow: auto` 或 `.table-responsive` 处理表格内容的水平滚动。
    *   表格 (`.table`) 宽度 `100%`。
    *   **操作列:** 通常位于表格最右侧，可考虑使用 `position: sticky` 固定。
*   **分页区域 (`.pagination-container`):**
    *   使用 `display: flex`，`justify-content: flex-end` (右对齐)，`align-items: center`。
    *   包含总条数信息 (`.page-info`)、每页显示数量选择 (`.form-select`)、页码导航 (`.pagination`) 和可选的页面跳转功能 (`.pagination-jump`)。
    *   通过 `gap` 或 `margin` 控制各元素间距。

**4. 组件样式规范**

*   **表单控件 (`.form-control`, `.form-select`):**
    *   统一高度 (如 `32px`)。
    *   统一圆角 (`--radius-sm` / `4px`)。
    *   统一边框 (`1px solid --border-color`)。
    *   白色背景 (`--card-background`)。
    *   获取焦点时 (`:focus`)，边框变为主色 (`--primary-color`)，并带有浅色阴影 (`box-shadow`)。
    *   悬停时 (`:hover`)，边框颜色可轻微加深或变为主色。
    *   标签 (`.form-label`) 位于控件上方，使用次要文字颜色 (`--text-secondary`)，字体略小 (如 `13px`)。
*   **按钮 (`.btn`):**
    *   统一圆角 (`--radius-sm` / `4px`)。
    *   统一基础内边距 (`padding`) 和字体大小 (如 `14px`)。
    *   **主按钮 (`.btn-primary`):** 主色背景，白色文字。
    *   **次按钮 (`.btn-secondary`):** 白色背景，灰色文字，灰色边框。
    *   **其他功能按钮 (`.btn-success`, `.btn-danger`, `.btn-warning`):** 使用对应的功能色背景。
    *   **轮廓按钮 (`.btn-outline-*`):** 透明背景，对应颜色边框和文字，悬停时背景变浅色。
    *   **表格内操作按钮 (`.action-buttons a`):**
        *   使用链接 (`<a>`) 样式。
        *   使用主色文字 (`--primary-color`)。
        *   悬停时 (`:hover`) 显示下划线或文字颜色加深。
        *   删除/驳回等危险操作使用危险色文字 (`.text-danger`)。
        *   停止等警告操作使用警告色文字 (`.text-warning`)。
        *   可包含图标 (`<i>`) 以增强识别性。
*   **表格 (`.table`, `th`, `td`):**
    *   表头 (`th`) 使用浅灰色背景 (`--table-header-background`)，次要文字颜色 (`--text-secondary`)，加粗。
    *   单元格 (`td`) 使用白色背景，主要文字颜色 (`--text-primary`)，细边框分隔 (`border-bottom`)。
    *   表格行悬停 (`tr:hover`) 时有浅蓝色背景 (`--table-row-hover-background`)。
    *   复选框列 (`th:first-child`, `td:first-child`) 宽度固定且居中。
    *   内容过长时使用 `white-space: nowrap`, `overflow: hidden`, `text-overflow: ellipsis`，并可通过 `title` 属性显示完整内容。
*   **徽章/标签 (`.badge`):**
    *   使用圆角 (`--radius-sm` / `4px`)。
    *   内边距适中 (`padding`)。
    *   字体略小 (如 `12px`)，加粗。
    *   背景色和文字颜色根据状态使用对应的功能色或主色/次要色。对于浅色背景，确保文字颜色有足够对比度。
*   **分页器 (`.pagination`, `.page-link`):**
    *   页码链接 (`.page-link`) 使用白色背景，灰色边框和文字。
    *   当前页 (`.active .page-link`) 使用主色背景和白色文字。
    *   禁用状态 (`.disabled .page-link`) 使用更浅的背景和文字颜色。
    *   悬停时 (`:hover`) 背景变浅蓝，文字变主色。
*   **弹窗 (`.modal-*`):**
    *   内容区 (`.modal-content`) 使用白色背景、圆角和阴影。
    *   头部 (`.modal-header`) 和脚部 (`.modal-footer`) 可使用浅灰色背景 (`--table-header-background`) 和分隔线。
    *   标题 (`.modal-title`) 字体加粗 (如 `16px`)。

**5. 交互与细节**

*   **悬停 (Hover):** 按钮、链接、表格行、可交互元素有明确的悬停效果。
*   **焦点 (Focus):** 输入框、下拉框等表单控件有清晰的焦点指示。
*   **激活 (Active):** 按钮点击时可有轻微位移效果。
*   **滚动条:** 可选使用 `::-webkit-scrollbar-*` 美化滚动条。
*   **响应式:** 使用 `@media` 查询调整布局（如搜索区换行、表格列堆叠 - 需配合 JS 或 `data-label`）。
