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
import VerticalTabsPageLayout from '@/layouts/TabLayout_VerticalTabs.vue' // 标签栏布局
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

在 `TabLayout_VerticalTabs.vue` 中，最外层包裹导航栏布局，并通过 `props` 接收标签页配置：

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
3. **无需在内容页引入导航栏或标签栏布局**，布局已由路由和 `TabLayout_VerticalTabs.vue` 统一处理。

---

## 5.1 更具体的内嵌页面示例 (以资产清单API列表页为例)

本节将以一个更具体的例子——资产清单模块下的API列表页 (`ApiTab.vue`)——来说明标签页内容页的实现。该页面自身也可能包含复杂的布局和组件，通常会使用如 `TablePageLayout` 这样的标准布局来构建其核心内容区。

**页面层级结构回顾:**

一个典型的复杂标签页（如 `ApiTab.vue`），当它被渲染时，其在整个应用中的页面嵌套结构可能如下所示（参考 `AssetCodingstructure.md` 的分析）：

```
顶级导航布局 (例如项目统一的 GovernanceCenterHeaderLayout 或通用的 NavigationHeaderLayout)
  └── 标签页布局 (VerticalTabsPageLayout / 即本文档中的 TabLayout_VerticalTabs.vue)
      ├── 左侧垂直标签栏 (由 el-menu 实现，根据 tabList prop 生成)
      └── 右侧内容区域 (<router-view />)
          └── 当前激活的标签内容页 (例如 ApiTab.vue)
              └── 页面特定布局 (例如 TablePageLayout)
                  ├── 页面头部 (PageHeader)
                  ├── 搜索栏 (SearchBar)
                  ├── 操作按钮区 (ActionButton)
                  ├── 数据表格 (DataTable)
                  └── 分页组件 (Pagination)
```
这个结构强调了各层布局的职责分离：顶级导航负责全局导航和面包屑，标签页布局负责标签切换，而具体的内容页（如`ApiTab.vue`）则专注于业务展示和交互，并可利用如`TablePageLayout`的组件来快速搭建标准化界面。

**`ApiTab.vue` 作为内容页的实现要点 (概念示例):**

下面的代码片段展示了 `ApiTab.vue` 可能的结构。关键在于它如何使用 `TablePageLayout` 并管理自身的业务逻辑，而不需要关心外部的标签页或顶级导航布局。

```vue
// ApiTab.vue (概念示例 - 位于 views/AssetList/ApiTab.vue 或类似路径)
<template>
  <TablePageLayout
    title="API列表" <!-- 此标题通常由 TablePageLayout 内部的 PageHeader 显示 -->
    :search-items="searchItems"
    :table-columns="tableColumnsConfig"
    :table-data="pageData"
    :total="totalEntries"
    :action-buttons="pageActionButtons"
    :table-actions="entryActionButtons"
    @search="triggerSearch"
    @page-change="handlePagination"
    @action="handlePageAction"
    @row-action="handleEntryAction"
  >
    <!-- 
      ApiTab.vue 利用 TablePageLayout 来构建其主要的列表展示和操作界面。
      它主要负责定义与"API列表"这一具体业务相关的：
      1. 搜索表单的配置 (searchItems)
      2. 表格列的配置 (tableColumnsConfig), 包括可能的多级表头和通过插槽实现的自定义单元格渲染。
      3. 数据的获取、处理和管理逻辑 (通常在 <script> 部分实现)。
      4. 对接 TablePageLayout 提供的分页逻辑。
      5. 配置页面级别的操作按钮 (如导入、导出) (pageActionButtons)。
      6. 配置表格中每一行的操作按钮 (如编辑、删除) (entryActionButtons)。
      7. 通过插槽自定义 TablePageLayout 内部的某些部分，例如特定列的显示方式。
    -->

    <!-- 示例：为 DataTable 的特定列提供自定义渲染 (通过命名插槽) -->
    <!-- 假设 'attributes' 是数据中的一个字段，需要在表格中特殊显示 -->
    <template #attributes="scope">
      <el-tag v-for="attr in scope.row.attributes" :key="attr" style="margin-right: 5px;">{{ attr }}</el-tag>
    </template>

    <!-- 示例：为可编辑的单元格提供输入组件，例如人工稽核的敏感分类选择 -->
    <!-- 假设 'req_manual_classification_editable' 是绑定到 el-select 的数据模型 -->
    <template #req_manual_classification="scope">
      <el-select 
        v-model="scope.row.req_manual_classification_editable" 
        placeholder="选择分类..."
        @change="(value) => handleCellEdit(scope.row, 'req_manual_classification', value)"
      >
        <el-option label="个人敏感信息" value="个人敏感信息"></el-option>
        <el-option label="重要数据" value="重要数据"></el-option>
        <el-option label="核心数据" value="核心数据"></el-option>
        <!-- 更多选项 -->
      </el-select>
    </template>
    <!-- 更多自定义列插槽可以根据 tableColumnsConfig 中的 slotName 定义 -->

  </TablePageLayout>
</template>

<script>
// 假设的API服务路径，根据实际项目结构调整
// import { getApiListData, updateApiEntry, deleteApiEntry, importApiList, exportApiList } from '@/api/assetList'; 
// 假设的配置文件路径，例如下拉选项
// import { classificationOptions, sensitivityLevelOptions } from './config/options';

export default {
  name: 'ApiTab',
  // components: { TablePageLayout }, // 如果 TablePageLayout 不是全局注册的
  data() {
    return {
      searchItems: [
        { type: 'input', label: 'API端点', prop: 'apiEndpoint' },
        { type: 'select', label: '所属应用', prop: 'applicationName', options: [/* 应用列表 */] } 
        // ...更多搜索项
      ],
      tableColumnsConfig: [ // 表格列配置
        { prop: 'apiEndpoint', label: 'API端点', width: 250 },
        { prop: 'applicationName', label: '所属应用', width: 180 },
        { prop: 'attributes', label: '接口属性', slotName: 'attributes', width: 200 }, // 使用上面定义的插槽
        { 
          label: '请求数据-人工稽核', // 多级表头示例
          children: [
            { prop: 'req_manual_classification_editable', label: '敏感分类', slotName: 'req_manual_classification', width: 180 },
            // ...更多人工稽核相关的子列
          ]
        },
        // ...更多列定义
      ],
      pageData: [], // 表格当前页数据
      totalEntries: 0, // 总条目数
      currentSearchParams: {}, // 当前搜索参数
      currentPageNum: 1, // 当前页码
      pageSizeNum: 10, // 每页条数
      pageActionButtons: [ // 页面级操作按钮
        { label: '导入API', key: 'import', type: 'primary', icon: 'el-icon-upload2' },
        { label: '导出列表', key: 'export', type: 'default', icon: 'el-icon-download' },
      ],
      entryActionButtons: [ // 行级操作按钮
        { label: '编辑', key: 'edit', type: 'text' },
        { label: '删除', key: 'delete', type: 'text', style: 'color: red;' },
      ]
    };
  },
  created() {
    this.loadData(); // 组件创建时加载初始数据
  },
  methods: {
    loadData() {
      const params = {
        ...this.currentSearchParams,
        page: this.currentPageNum,
        size: this.pageSizeNum
      };
      console.log('ApiTab: Fetching data with params:', params);
      // 模拟API调用
      // getApiListData(params).then(response => {
      //   this.pageData = response.data.list;
      //   this.totalEntries = response.data.total;
      // }).catch(error => {
      //   console.error('Error fetching API list:', error);
      // });

      // 模拟数据填充
      const mockData = Array.from({ length: this.pageSizeNum }, (_, i) => ({
        id: `api_${Date.now()}_${i}`,
        apiEndpoint: `/api/v1/item/${i}`,
        applicationName: i % 2 === 0 ? '核心服务A' : '业务支撑B',
        attributes: i % 3 === 0 ? ['公开', '需鉴权'] : ['内部'],
        req_manual_classification_editable: null,
      }));
      this.pageData = mockData;
      this.totalEntries = 50; // 假设总共50条
    },
    triggerSearch(params) {
      this.currentSearchParams = params;
      this.currentPageNum = 1; // 搜索后回到第一页
      this.loadData();
    },
    handlePagination({ page, limit }) {
      this.currentPageNum = page;
      this.pageSizeNum = limit;
      this.loadData();
    },
    handlePageAction({key}) { // 从 TablePageLayout emit 的事件中解构出 key
      console.log(`ApiTab: Page action '${key}' triggered.`);
      if (key === 'import') {
        // 执行导入逻辑，例如打开弹窗
        alert('触发导入操作');
      } else if (key === 'export') {
        // 执行导出逻辑
        alert('触发导出操作');
      }
    },
    handleEntryAction({key, row}) { // 从 TablePageLayout emit 的事件中解构出 key 和 row
      console.log(`ApiTab: Entry action '${key}' for row ID '${row.id}' triggered.`);
      if (key === 'edit') {
        // 执行编辑逻辑，例如打开编辑弹窗，并传入 row 数据
        alert(`编辑API: ${row.apiEndpoint}`);
      } else if (key === 'delete') {
        // 执行删除逻辑，通常需要用户确认
        confirm(`确认删除API: ${row.apiEndpoint}?`);
        // deleteApiEntry(row.id).then(() => this.loadData());
      },
    handleCellEdit(row, fieldKey, newValue) {
        console.log(`ApiTab: Cell edit on row ID '${row.id}', field '${fieldKey}', new value '${newValue}'.`);
        // 实际应用中，这里会调用API保存更改
        // updateApiEntry(row.id, { [fieldKey]: newValue }).then(...);
        // 为了演示，直接修改行数据 (在实际项目中，通常在API成功回调后更新或重新加载)
        const item = this.pageData.find(d => d.id === row.id);
        if (item) {
            item[fieldKey] = newValue; // 注意：Vue2 可能需要 $set 来确保响应性，取决于数据结构
        }
    }
  }
}
</script>

<style scoped>
/* ApiTab.vue 特有的局部样式 */
.el-tag + .el-tag {
  margin-left: 5px;
}
/* 可以在这里添加更多针对 ApiTab 内容的特定样式 */
</style>
```

**路由配置回顾 (与本文档第2节 "路由配置实现" 对应):**

在 `src/router/index.js` 中，`ApiTab.vue` (或其他类似的具体业务标签页) 会作为 `VerticalTabsPageLayout` 的一个子路由出现。下面是一个示例，展示了如何将包含 `ApiTab` 的资产清单模块配置到路由中：

```js
// 引入顶级导航布局 (如果您的项目有统一的顶级导航)
// import NavigationHeaderLayout from '@/layouts/NavigationHeaderLayout.vue'; // 或 GovernanceCenterHeaderLayout

// 引入标签页布局组件
import VerticalTabsPageLayout from '@/layouts/TabLayout_VerticalTabs.vue'; 

// 引入各个标签页对应的具体内容组件
import DbTab from '@/views/AssetList/DbTab.vue';        // 示例：数据库列表页
import TableTab from '@/views/AssetList/TableTab.vue';  // 示例：数据表列表页
import ApiTab from '@/views/AssetList/ApiTab.vue';      // 我们的示例：API列表页
// ... 其他具体业务标签页组件

// 为资产清单模块定义标签列表
const assetListTabsConfig = [
  { path: '/asset/list/db', label: '全量库', icon: 'el-icon-coin', name: 'DbTab' }, // name 用于 keep-alive (如果需要)
  { path: '/asset/list/table', label: '全量表', icon: 'el-icon-notebook-2', name: 'TableTab' },
  { path: '/asset/list/api', label: 'API列表', icon: 'el-icon-s-promotion', name: 'ApiTab' },
  // ...可以根据实际需求添加更多标签页
];

// 路由配置中的一部分 (假设 '/asset' 是资产管理模块的根路径)
const assetRoutes = {
  path: '/asset', // 资产管理模块的顶级路径
  // component: NavigationHeaderLayout, // 如果资产管理模块整体包裹在某个顶级导航下
  // redirect: '/asset/list', // 可以重定向到默认的子模块
  meta: { title: '资产管理' }, 
  children: [
    {
      path: 'list', // 路径为 /asset/list
      component: VerticalTabsPageLayout, // 使用标准标签页布局组件
      props: { 
        tabList: assetListTabsConfig, // 将标签配置传递给布局组件
        pageTitle: '全量资产清单', // （可选）传递给布局组件，用于显示在面包屑或标题区域
        defaultTabPath: '/asset/list/api' // （可选）指定默认激活的标签页路径
      },
      // redirect: '/asset/list/api', // 或者通过 redirect 指定默认子路由 (更推荐此方式)
      children: [ // 定义各个标签页对应的路由
        { path: 'db', name: 'DbTab', component: DbTab, meta: { title: '全量库' } },
        { path: 'table', name: 'TableTab', component: TableTab, meta: { title: '全量表' } },
        { path: 'api', name: 'ApiTab', component: ApiTab, meta: { title: 'API列表' } },
        // 如果希望 /asset/list 默认显示 ApiTab, 可以在父路由使用 redirect: '/asset/list/api'
        // 或者将ApiTab的路径设置为空 '' 或 '*' (不推荐*), 并确保它是第一个子路由或有明确的 redirect
        // 例如： { path: '', redirect: 'api' } 或者 { path: 'api', alias:''}
      ]
    },
    // ... 资产管理模块下的其他非标签页布局的页面
  ]
};

// 这个 assetRoutes 对象最终会整合到主路由配置数组中。
```


---

## 6. 结构示意

```
路由配置：
/tab-module (VerticalTabsPageLayout)
  ├─ /tabA (TabPageA.vue)
  ├─ /tabB (TabPageB.vue)
  └─ /tabC (TabPageC.vue)

布局渲染 (以一个使用了 TablePageLayout 的内容页为例):

NavigationHeaderLayout (或项目级顶层导航布局, 如 GovernanceCenterHeaderLayout)
  └── VerticalTabsPageLayout (即 TabLayout_VerticalTabs.vue)
      ├── 左侧垂直标签栏 (el-menu, 根据 tabList prop 生成)
      └── <router-view/> (渲染右侧业务内容页)
          └── TabPageA.vue (或其他具体内容页, 例如 ApiTab.vue)
              └── TablePageLayout (如果内容页使用此标准布局)
                  ├── PageHeader (页面标题)
                  ├── SearchBar (搜索区域)
                  ├── ActionButton (操作按钮区域, 可能包含导入、导出等)
                  ├── DataTable (数据表格区域)
                  │   └── (内部可能包含复杂的列定义、多级表头、自定义插槽渲染)
                  └── Pagination (分页组件)
```






