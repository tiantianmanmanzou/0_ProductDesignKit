# 标签页页面开发规范

本规范适用于所有需要"标签栏+导航栏"布局的页面模块，帮助开发者高效、规范地开发各类标签页类型页面。

## 1. 总体实现思路

- **导航栏布局**：作为页面级顶层布局，统一负责顶部导航栏和面包屑，保证全局一致。
- **标签栏布局**：作为二级布局，负责左侧垂直标签页（Tab）切换。
- **内容页**：只负责具体业务内容（如表格、表单等），无需关心导航栏和标签栏。

---

## 2. 路由配置实现

在 `src/router/index.js` 中，采用如下嵌套路由结构：

```js
import NavigationHeaderLayout from '@/layouts/NavigationHeaderLayout.vue' // 导航栏布局（示例名）
import VerticalTabsPageLayout from '@/layouts/VerticalTabs-PageLayout.vue' // 标签栏布局
import TabPageA from '@/views/TabModule/TabPageA.vue'
import TabPageB from '@/views/TabModule/TabPageB.vue'
import TabPageC from '@/views/TabModule/TabPageC.vue'

const tabList = [
  { path: '/tab-module/tabA', label: '标签A', icon: 'el-icon-document' },
  { path: '/tab-module/tabB', label: '标签B', icon: 'el-icon-user' },
  { path: '/tab-module/tabC', label: '标签C', icon: 'el-icon-setting' }
]

{
  path: '/tab-module',
  component: VerticalTabsPageLayout, // 统一用标签栏布局
  props: { tabList },
  children: [
    { path: 'tabA', name: 'TabPageA', component: TabPageA },
    { path: 'tabB', name: 'TabPageB', component: TabPageB },
    { path: 'tabC', name: 'TabPageC', component: TabPageC }
  ]
}
```

---

## 3. 标签栏布局组件实现

在 `VerticalTabs-PageLayout.vue` 中，最外层包裹导航栏布局，并通过 `props` 接收标签页配置：

```vue
<template>
  <NavigationHeaderLayout pageName="标签页模块">
    <div class="vertical-tabs-container">
      <div class="vertical-tabs-page">
        <el-aside width="60px" class="vtp-aside">
          <el-menu :default-active="$route.path" router unique-opened class="vtp-menu">
            <el-menu-item
              v-for="item in tabList"
              :key="item.path"
              :index="item.path"
              class="vtp-menu-item"
            >
              <i v-if="item.icon" :class="item.icon"></i>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <div class="vtp-content">
          <router-view/>
        </div>
      </div>
    </div>
  </NavigationHeaderLayout>
</template>

<script>
import NavigationHeaderLayout from '@/layouts/NavigationHeaderLayout.vue'
export default {
  name: 'VerticalTabsPageLayout',
  components: { NavigationHeaderLayout },
  props: {
    tabList: { type: Array, required: true }
  }
}
</script>
```

---

## 4. 内容页实现

每个标签页对应的内容页面（如 `TabPageA.vue`、`TabPageB.vue` 等），**只需专注业务内容**，无需引入导航栏或标签栏布局。例如：

```vue
<template>
  <TablePageLayout
    title="标签A内容"
    :show-search="true"
    :search-items="searchItems"
    ... // 其余props和事件
  >
    <!-- 插槽自定义表格操作按钮等 -->
  </TablePageLayout>
</template>
```

---

## 5. 快速开发新标签页页面的流程

1. **在 `views/` 下新建业务内容页面**，如 `TabPageX.vue`，只写内容。
2. **在 `router/index.js` 的对应模块路由下添加子路由**，并在 `tabList` 中补充对应 tab 配置。
3. **无需在内容页引入导航栏或标签栏布局**，布局已由路由和 `VerticalTabs-PageLayout.vue` 统一处理。

---

## 6. 结构示意

```
路由配置：
/tab-module (VerticalTabs-PageLayout)
  ├─ /tabA (TabPageA.vue)
  ├─ /tabB (TabPageB.vue)
  └─ /tabC (TabPageC.vue)

布局渲染：
NavigationHeaderLayout
  └─ VerticalTabs-PageLayout
      ├─ 左侧标签栏（tabList）
      └─ <router-view/>（渲染业务内容页）
```

---

## 7. 优点

- 内容页代码极为简洁，专注业务逻辑。
- 布局风格统一，维护简单。
- 新增标签页开发效率高，只需关注内容和路由配置。
- 支持灵活扩展标签页数量和内容。

---

## 8. 结论

> 采用本规范开发的所有标签页页面，内容页面无需关心布局，布局由父级统一包裹。只需专注业务内容和路由配置，即可实现高效、规范、可维护的标签页页面开发。




