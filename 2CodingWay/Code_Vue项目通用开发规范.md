# Vue 项目开发规范

阿迪

## 2. 技术栈版本

- Vue.js: v2.6.10
- Element UI: v2.13.2
- Vue Router: (根据 `router/index.js` 确认，通常为 v3.x for Vue 2)
- Vuex: (根据 `store/index.js` 确认，通常为 v3.x for Vue 2)
- Axios: (版本根据 `package.json` 或实际使用情况)

## 3. 目录结构规范

项目采用标准的 Vue CLI 生成的目录结构，并在此基础上进行组织。

```
1_ZJZTFrontProject/
├── public/                     # 静态资源，会被直接拷贝到输出目录
│   └── index.html              # HTML 入口文件
├── src/                        # 项目核心源码目录
│   ├── assets/                 # 模块静态资源 (会被 webpack 处理)
│   │   ├── fonts/
│   │   └── images/
│   ├── components/             # 全局/可复用组件
│   │   ├── common/             # 通用基础组件 (如 DataTable.vue, SearchBar.vue)
│   │   └── [业务模块名]/       # 按业务模块划分的组件 (可选，视项目复杂度)
│   ├── layouts/                # 布局组件 (如 PageLayout_TablePage.vue, TabLayout_VerticalTabs.vue)
│   ├── mock/                   # 模拟数据接口
│   ├── plugins/                # Vue 插件 (如 element.js)
│   ├── router/                 # 路由配置
│   │   └── index.js
│   ├── store/                  # Vuex 状态管理
│   │   ├── index.js            # Vuex 入口，组合模块
│   │   ├── getters.js          # 全局 Getters (若有)
│   │   └── modules/            # Vuex 模块 (如 user.js, workflow.js)
│   ├── styles/                 # 全局样式与变量
│   │   ├── index.scss          # 全局样式入口 (或按需引入)
│   │   ├── variables.scss      # 全局 SCSS 变量
│   │   ├── mixins.scss         # 全局 SCSS Mixins
│   │   └── [组件名].scss       # 特定组件或页面的独立样式 (较少使用)
│   ├── utils/                  # 工具函数模块
│   │   ├── request.js          # Axios 实例封装与拦截器
│   │   ├── auth.js             # 认证相关工具 (Token处理等)
│   │   ├── index.js            # 通用工具函数或导出其他工具模块
│   │   └── [功能名].js         # 特定功能的工具函数 (如 iframe.js, validate.js)
│   ├── views/                  # 页面视图组件
│   │   ├── [业务模块名]/       # 按业务模块/一级导航组织页面
│   │   │   ├── PageName.vue
│   │   │   └── ...
│   │   └── example/            # 示例页面
│   ├── App.vue                 # 根 Vue 组件
│   └── main.js                 # 应用入口文件
├── .env.[mode]               # 环境变量配置文件
├── babel.config.js             # Babel 配置
├── vue.config.js               # Vue CLI 配置文件 (webpack配置等)
└── package.json                # 项目依赖与脚本
```

**规范说明:**

*   **命名**:
    *   文件夹名：使用 `kebab-case` (短横线分隔) 或 `PascalCase` (如业务模块名)。建议统一为 `kebab-case` 以保持一致性。
    *   `.vue` 文件名：组件使用 `PascalCase` (如 `MyComponent.vue`)。视图也建议使用 `PascalCase` (如 `UserProfile.vue`)。
    *   `.js` 文件名：使用 `camelCase` (如 `utils/request.js`) 或 `kebab-case`。
*   `components/common/`: 存放与业务逻辑无关，可在多处复用的基础UI组件。
*   `layouts/`: 存放页面骨架组件，如包含头部、侧边栏、内容区的布局。
*   `views/`: 按照业务模块或功能进行子目录组织，使结构更清晰。
*   `utils/request.js`: 应封装 `axios` 实例，包括基础 URL、超时设置、请求/响应拦截器（如Token注入、统一错误处理）。

## 4. 编码规范

### 4.1 Vue 组件规范

*   **组件命名**:
    *   组件名应为多个单词，避免与HTML元素冲突。使用 `PascalCase`。
    *   在 `components` 目录中，组件文件名应与其 `name` 选项一致。
    *   全局注册的组件名也使用 `PascalCase` (如 `Vue.component('PageHeader', PageHeader)`).
*   **组件 `name` 选项**: 所有组件都必须有 `name` 选项，方便调试和组件递归。
*   **Props**:
    *   明确声明 Props 类型、默认值和是否必需。
    *   Prop 命名：HTML attribute 使用 `kebab-case`，JavaScript 中使用 `camelCase`。
    ```javascript
    props: {
      myProp: {
        type: String,
        required: true,
        default: 'default value'
      },
      anotherProp: {
        type: [Boolean, String],
        default: false
      }
    }
    ```
*   **`v-for` 指令**: 必须带上 `:key`，且 `key` 值应保证唯一和稳定。避免使用 `index`作为 `key`，除非列表是纯静态且不会改变顺序。
*   **组件结构顺序**: 推荐组件内选项的书写顺序：
    1.  `name`
    2.  `components`
    3.  `mixins`
    4.  `props`
    5.  `data`
    6.  `computed`
    7.  `watch`
    8.  生命周期钩子 (按执行顺序: `beforeCreate`, `created`, `beforeMount`, `mounted`, `beforeUpdate`, `updated`, `beforeDestroy`, `destroyed`)
    9.  `methods`
    10. 模板 (`<template>`)
    11. 样式 (`<style>`)
*   **`scoped` 样式**: 默认情况下，组件的 `<style>` 标签应添加 `scoped` 属性，以避免样式全局污染。
    ```html
    <style scoped>
    .button {
      color: red;
    }
    </style>
    ```
    若需修改子组件深层样式且不方便通过 prop 控制，可使用深度作用选择器 `>>>` 或 `/deep/` (Sass/Less 中用 `::v-deep`)，但应谨慎使用。
*   **模板简洁性**:
    *   避免在模板中写入过于复杂的表达式，应将其移至 `computed` 属性或 `methods`。
    *   善用计算属性缓存计算结果。
*   **组件通信**:
    *   父到子：Props。
    *   子到父：`$emit` 事件。事件名使用 `kebab-case`。
    *   兄弟/跨级：Vuex 或 Event Bus (慎用 Event Bus，易造成维护困难，优先考虑 Vuex)。

### 4.2 JavaScript 规范

*   **ESLint**: 项目应配置 ESLint，并遵循预设的规则 (如 Vue 官方推荐规则 `plugin:vue/recommended` 或 `plugin:vue/essential` 结合 Prettier)。
*   **变量声明**: 优先使用 `const`，其次是 `let`，避免使用 `var`。
*   **模块导入**:
    *   路径别名：使用 `@` 代表 `src` 目录 (如 `import MyComponent from '@/components/MyComponent.vue'`)。
    *   导入顺序：
        1.  第三方库 (如 `import Vue from 'vue'`)
        2.  Vue 插件
        3.  项目工具函数/服务 (如 `import { fetchData } from '@/utils/request'`)
        4.  Vuex store 相关
        5.  组件 (布局组件、父组件、子组件、通用组件)
        6.  样式文件
    *   每个导入组之间可以空一行。
*   **函数**:
    *   优先使用箭头函数处理回调，以正确绑定 `this` 上下文。
    *   方法名使用 `camelCase`。
*   **注释**:
    *   对复杂逻辑、重要函数、难以理解的代码段添加必要的注释。
    *   组件的 `props`、`events`、主要功能也建议添加注释。
*   **条件渲染**: `v-if` vs `v-show`
    *   `v-if`：真实的条件渲染，切换时会销毁和重建元素/组件。适用于条件不常改变的场景。
    *   `v-show`：通过 CSS `display` 控制显隐，元素/组件始终被渲染。适用于频繁切换的场景。

## 5. 路由规范 (`vue-router`)

*   **路由定义 (`src/router/index.js`)**:
    *   **懒加载**: 页面组件应使用动态 `import()` 实现懒加载，并使用 `webpackChunkName` 对代码块进行命名，便于调试和分析。
      ```javascript
      const UserProfile = () => import(/* webpackChunkName: "user" */ '@/views/User/UserProfile.vue');
      ```
    *   **命名路由**: 为重要路由添加 `name` 属性，方便编程式导航和 `router-link` 的使用。`name` 应使用 `PascalCase` 并与组件名对应。
    *   **`meta` 字段**: 合理使用 `meta` 字段存储路由元信息，如页面标题、是否需要认证、布局信息等。
      ```javascript
      {
        path: '/profile',
        name: 'UserProfile',
        component: UserProfile,
        meta: { title: '用户中心', requiresAuth: true }
      }
      ```
    *   **布局嵌套**: 通过路由配置实现页面布局的嵌套，如项目中的 `VerticalTabsPageLayout`。
*   **导航守卫**:
    *   `beforeEach`: 用于全局权限校验、登录状态检查、页面访问控制等。
    *   `afterEach`: 用于设置页面标题 (如项目中已实现的逻辑)、上报分析数据等。
*   **路径**: 使用 `kebab-case` (如 `/user-management/user-list`)。

## 6. 状态管理规范 (Vuex)

*   **模块化**: 当应用状态复杂时，应使用 Vuex Modules 将 store 分割成模块。每个模块拥有自己的 `state`, `mutations`, `actions`, `getters`。
    *   在模块中启用命名空间: `namespaced: true`。
*   **State**:
    *   State 应该是唯一数据源。
    *   避免在组件内部直接修改 store 中的 state，应通过 mutations。
*   **Getters**:
    *   用于从 state 派生出一些状态，类似计算属性。
    *   Getter 的结果会被缓存，只有当其依赖的 state 变化时才会重新计算。
*   **Mutations**:
    *   更改 Vuex 的 store 中的状态的唯一方法是提交 mutation。
    *   Mutation 必须是同步函数。
    *   Mutation 名称建议使用大写常量风格 (如 `SET_USER_INFO`)。
*   **Actions**:
    *   Action 类似于 mutation，不同在于：
        *   Action 提交的是 mutation，而不是直接变更状态。
        *   Action 可以包含任意异步操作。
    *   Action 名称建议使用 `camelCase` (如 `fetchUserProfile`)。
    *   在 Action 中处理 API 请求和复杂的业务逻辑。
*   **辅助函数**: 善用 `mapState`, `mapGetters`, `mapMutations`, `mapActions` 辅助函数将 store 中的成员映射到组件的局部计算属性或方法中。

## 7. API 请求规范 (Axios)

*   **封装 Axios**:
    *   在 `src/utils/request.js` (或类似文件) 中创建和配置 Axios 实例。
    *   设置 `baseURL`、`timeout`。
    *   **请求拦截器**: 用于统一处理请求，如：
        *   在请求头中添加 `Authorization` Token。
        *   添加通用请求参数。
        *   显示全局 loading 状态。
    *   **响应拦截器**: 用于统一处理响应，如：
        *   根据后端返回的 code 做统一的错误提示 (如 `this.$message.error`)。
        *   处理 Token 失效，跳转登录页。
        *   数据转换。
        *   隐藏全局 loading 状态。
    *   项目中已实现的404错误返回模拟数据的方式，在开发阶段可保留，但生产环境需有更明确的错误上报和用户提示。
*   **API 维护**:
    *   建议创建 `src/api/` 目录，按业务模块组织 API 请求函数。
      ```javascript
      // src/api/user.js
      import request from '@/utils/request';

      export function getUserInfo(id) {
        return request({
          url: `/users/${id}`,
          method: 'get'
        });
      }

      export function updateUserProfile(data) {
        return request({
          url: '/users/profile',
          method: 'post',
          data
        });
      }
      ```
    *   组件中通过导入这些函数来调用 API，而不是直接使用 `this.$http.get(...)`。
*   **Loading 状态**: 对于耗时操作，应在界面上显示明确的 Loading 状态，提升用户体验。

## 8. 样式规范 (SCSS/CSS)

*   **预处理器**: 项目使用 SCSS。
*   **全局样式与变量**:
    *   `src/styles/variables.scss`: 定义全局颜色、字体大小、间距等 SCSS 变量。
    *   `src/styles/mixins.scss`: 定义可复用的 SCSS Mixins。
    *   `src/styles/index.scss` (或类似文件): 引入全局基础样式、重置样式、Element UI 主题覆盖等。
*   **BEM 命名规范 (推荐)**: 对于组件内部的复杂 CSS 结构，推荐使用 BEM (Block, Element, Modifier) 命名约定，以提高 CSS 的可读性和可维护性，并减少样式冲突。
    ```css
    /* Block */
    .card {}
    /* Element */
    .card__title {}
    .card__content {}
    /* Modifier */
    .card--highlighted {}
    .card__title--small {}
    ```
*   **Scoped CSS**: 优先使用 `<style scoped>`。
*   **避免使用 ID 选择器**: 除非有非常特殊的需求，否则应避免在 CSS 中使用 ID 选择器，以降低其特异性。
*   **避免使用 `!important`**: 尽量通过提高选择器特异性或调整样式加载顺序来解决样式覆盖问题，避免滥用 `!important`。
*   **样式调整的可复用性**: 当进行界面样式调整时，应优先考虑修改可复用的组件内部样式或项目共享的 `.scss` 样式文件（如 `variables.scss`, `mixins.scss` 或特定功能的 `*.scss` 文件）。这样做的好处是，相关的调整能够自动应用到所有使用该组件或共享样式的新旧页面，从而提高开发效率，确保视觉风格的统一性，并减少在多个页面单独进行重复样式调整的工作量。避免直接在单个页面视图（`.vue` 文件）中针对通用组件或布局进行一次性的样式覆盖，除非该调整确实是该页面独有的、不具备通用性的特殊情况。

## 9. 通用组件开发规范

参考 `components/common/DataTable.vue` 和 `layouts/PageLayout_TablePage.vue` 的设计：

*   **高内聚、低耦合**: 组件应专注于自身功能。
*   **Props**: 精心设计 Props，使其易于理解和使用。提供必要的默认值和类型校验。
*   **Slots**: 灵活运用插槽 (默认插槽、具名插槽、作用域插槽) 提高组件的扩展性和灵活性。例如 `DataTable.vue` 通过插槽允许父组件自定义列的渲染。
*   **Events**: 清晰定义组件对外触发的事件，并携带必要的参数。
*   **文档**: 为通用组件编写清晰的使用说明和 Props/Events/Slots API 文档 (可在组件文件顶部注释或单独文档中)。

## 10. 最佳实践与建议

*   **代码复用**:
    *   抽离可复用的业务逻辑到 `utils` 或 Vuex actions/getters。
    *   创建可复用的 UI 组件到 `components/common/`。
    *   使用 Mixins 共享组件间的通用逻辑 (谨慎使用，可能导致数据来源不清晰)。
*   **性能优化**:
    *   路由懒加载。
    *   组件按需引入 (对于非全局大型组件)。
    *   `v-show` 和 `v-if` 的合理使用。
    *   图片资源压缩和优化，使用雪碧图或 SVG 图标。
    *   长列表性能优化 (虚拟滚动，如果 Element UI 未提供或不满足需求)。
    *   合理使用 `keep-alive` 缓存组件状态。
    *   `debounce` 和 `throttle` 处理高频事件。
*   **错误处理**:
    *   组件内部应有自己的错误捕获和用户提示。
    *   Vue 全局错误处理 (`Vue.config.errorHandler`)。
    *   Axios 响应拦截器中统一处理 API 错误。
*   **可访问性 (a11y)**: 关注 Web 可访问性，确保应用对所有用户友好 (如为表单元素关联 `label`，为图标按钮提供文本提示等)。
*   **代码审查 (Code Review)**: 定期进行代码审查，有助于知识共享、发现潜在问题、统一编码风格。
*   **版本控制 (Git)**:
    *   遵循清晰的 Git 分支模型 (如 Git Flow 或 GitHub Flow)。
    *   编写有意义的 Commit Message (如遵循 Conventional Commits 规范)。
*   **持续集成/持续部署 (CI/CD)**: 如果条件允许，配置 CI/CD 流程自动化测试和部署。
*   **删除无用代码**: 定期清理项目中不再使用的组件、变量、函数、注释掉的代码块，保持代码库整洁。
*   **环境变量**: 使用 `.env` 文件管理不同环境 (开发、测试、生产) 的配置，如 API 基地址。

## 11. 现有项目特定实践总结

*   **`TablePageLayout.vue` 和 `VerticalTabsPageLayout.vue`**: 项目中广泛使用这些布局组件来统一页面结构，是很好的实践，应继续沿用。新页面开发时优先考虑是否能复用现有布局。
*   **全局组件注册**: `main.js` 中注册的 `PageHeader`, `SearchBar`, `ActionButton`, `DataTable` 等通用组件，方便了开发，可以继续维护和扩展这个列表。
*   **模拟数据**: 项目初始化和 API 错误时使用了模拟数据，这在开发阶段非常有用。需要明确区分开发和生产环境的数据处理逻辑。
*   **Iframe 集成**: 项目考虑了 iframe 嵌入的场景，相关工具函数和逻辑应妥善维护。

通过遵循以上规范，希望能帮助团队更高效地进行协作，并构建出高质量、易维护的 Vue 应用。本文档会根据项目进展和团队反馈持续更新。 