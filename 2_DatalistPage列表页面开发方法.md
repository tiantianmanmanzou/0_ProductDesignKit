# 列表页面复用开发规范

## 1. 目标与原则
- **一致性**：所有列表页面统一视觉风格、布局结构和交互模式。
- **高效性**：开发者专注业务逻辑，无需重复编写布局和样式。
- **可维护性**：通用布局和样式集中管理，统一修改自动生效。

## 2. 推荐组件
统一使用 `TablePage_PageLayout.vue` 作为所有列表页面的主布局组件。**禁止**在页面中单独引入和拼装基础布局组件（如 `SearchBar`、`DataTable`、`Pagination`、`PageHeader` 等）。

## 3. 开发流程
1. **新建页面组件**  
   在 `src/views/yourModule/` 下创建新页面（如 `NewListPage.vue`）。
2. **引入与注册**  
   在 `<script>` 中导入并注册 `TablePageLayout`。
3. **模板结构**  
   以 `<TablePageLayout>` 作为页面主要内容容器。**不要**在其外部手动放置搜索栏、表格、分页等标准布局部分。
4. **Props 配置**  
   通过 Props 配置页面元素，常用属性如下：

| Prop                | 说明                   |
|---------------------|------------------------|
| `title`             | 页面标题               |
| `search-items`      | 搜索栏字段配置         |
| `initial-form-data` | 搜索栏初始值           |
| `action-buttons`    | 顶部操作按钮           |
| `table-data`        | 表格数据               |
| `table-columns`     | 表格列定义             |
| `loading`           | 加载状态               |
| `total`             | 数据总数               |
| `current-page.sync` | 当前页码（双向绑定）   |
| `page-size.sync`    | 每页条数（双向绑定）   |
| `page-sizes`        | 可选分页条数           |
| `show-selection`    | 是否显示多选           |
| `show-index`        | 是否显示序号           |
| `table-border`      | 是否显示表格边框       |
| `table-stripe`      | 是否斑马纹             |
| `show-table-action` | 是否显示行操作列       |
| `action-width`      | 行操作列宽度           |
| `table-actions`     | 行操作按钮配置         |
| `action-fixed`      | 操作列是否固定（可选，默认不固定） |

5. **事件处理**  
   监听并处理以下事件：

| 事件名              | 说明                   |
|---------------------|------------------------|
| `@search`           | 搜索                   |
| `@reset`            | 重置搜索               |
| `@action`           | 顶部按钮点击           |
| `@pagination`       | 分页变化               |
| `@selection-change` | 多选变化               |
| `@table-action`     | 行操作按钮点击         |

6. **插槽（Slots）定制**  
   如需自定义内容，使用以下插槽：

| 插槽名                  | 用途                         |
|-------------------------|------------------------------|
| `#column-<propName>`    | 自定义某列内容               |
| `#table-action`         | 自定义行操作列               |
| `#header-extra`         | 标题栏右侧额外内容           |
| `#operation-buttons`    | 顶部操作按钮区额外内容       |

7. **数据与业务逻辑**  
   页面组件只负责数据获取、过滤、事件处理等业务逻辑，通过 Props 与事件与 `TablePageLayout` 交互。

8. **样式规范**  
   - 仅在必要时添加极少量页面特有样式，**禁止**覆盖或重复布局相关样式。
   - 全局滚动页面根节点加 `global-scroll` class，并在全局样式中设置 `#app.global-scroll { overflow: auto !important; }`，进入/离开页面时动态切换。

## 说明
- **操作栏默认不固定**：如无特殊业务需求，所有列表页面的操作栏（行操作列）默认不固定。仅在内容宽度过大、操作列易被遮挡时，才允许通过 `action-fixed="right"` 显式设置为固定。
- `action-fixed` 属性可选，取值为 `right`（固定在右侧）或 `null`/不传（不固定）。

## 4. 示例代码

```vue
<template>
  <TablePageLayout
    :title="pageTitle"
    :search-items="searchConfig"
    :action-buttons="mainActions"
    :table-columns="columnConfig"
    :table-data="dataForTable"
    :loading="isLoading"
    :total="totalItems"
    :current-page.sync="pagination.currentPage"
    :page-size.sync="pagination.pageSize"
    :show-selection="true"
    :show-index="true"
    :table-actions="rowActions"
    @search="handleSearch"
    @reset="handleReset"
    @action="handleAction"
    @table-action="handleRowAction"
    @pagination="fetchData"
    @selection-change="handleSelection"
  >
    <template #column-status="{ row }">
      <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
        {{ row.status === 'active' ? '激活' : '禁用' }}
      </el-tag>
    </template>
    <template #table-action="{ row }">
      <el-button type="text" size="small" @click="viewDetails(row)">查看详情</el-button>
    </template>
    <template #operation-buttons>
      <el-button type="primary" @click="customOperation">自定义操作</el-button>
    </template>
  </TablePageLayout>
</template>
```

## 5. 其他注意事项
- 分页的 `currentPage` 和 `pageSize` 推荐用 `.sync` 修饰符实现双向绑定。
- 业务逻辑（如数据获取、删除、导出等）全部在页面组件的 `methods` 中实现，布局组件只负责展示和事件分发。
- 插槽优先用于复杂自定义场景，常规展示尽量用 Props 配置。
-  在需要全局滚动的页面（如详情页、表单页）根节点加一个class，比如global-scroll，并在全局样式加：
#app.global-scroll {
  overflow: auto !important;
}
进入这些页面时，动态加上global-scroll，离开时移除。


- 新页面要根节点100%高度，保证flex布局就不会塌陷

---

如需进一步细化某一部分（如 Props 详细说明、事件参数结构等），可补充专门的子文档。