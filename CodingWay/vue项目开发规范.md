---
description: Vue项目开发规范
globs: "*.vue"
alwaysApply: true
---

# Vue项目开发规范指南

## 技术栈与版本要求

**严格遵循以下版本进行开发和部署：**

```json
{
  "vue": "2.6.10",
  "element-ui": "2.13.2"
}
```

## 组件与样式规范目标

本规范旨在确保项目UI风格一致性和提高开发效率。**所有开发者必须严格遵循**以下规范进行新页面开发和现有页面维护。

## 核心设计原则

1. **组件复用优先**：必须使用已封装的通用组件，禁止重复开发相同功能组件
2. **样式统一管理**：所有组件样式已集中在样式模块文件中，禁止在页面组件中编写独立样式
3. **官方样式覆盖**：自定义样式必须基于Element UI官方样式进行覆盖，不允许引入新的类名
4. **变量驱动设计**：必须使用项目定义的变量控制颜色、间距、字体等，禁止使用硬编码值
5. **类名不重复**：对同一个对象的样式定义必须在一个类名中完成，禁止多个类名重复定义样式

## 开发规范详细说明

### 1. 组件引入规范

**禁止在页面中重复引入全局组件和样式：**

- 全局组件已在入口文件中注册（位置：`src/components`），直接使用无需导入
- 全局样式已在入口文件中引入（位置：`src/styles`），无需重复引入

✅ **正确示例：**

```vue
<template>
  <div>
    <!-- 直接使用全局注册的组件，无需导入 -->
    <TablePage
      :search-form="searchForm"
      :search-fields="searchFields"
      :action-buttons="actionButtons"
      :table-data="tableData"
      :table-columns="tableColumns"
      @search="handleSearch"
      @action="handleAction"
    />
  </div>
</template>

<script>
export default {
  // 无需import导入TablePage组件
  data() {
    return {
      searchForm: {},
      searchFields: [
        // 搜索字段配置...
      ],
      actionButtons: [
        // 按钮配置...
      ],
      tableData: [],
      tableColumns: [
        // 列配置...
      ]
    }
  },
  methods: {
    handleSearch(params) {
      // 搜索处理逻辑
    },
    handleAction(action, row) {
      // 按钮点击处理逻辑
    }
  }
}
</script>

<!-- 无需添加任何样式代码 -->
```

❌ **错误示例：**

```vue
<template>
  <div class="custom-page"><!-- 错误：创建了自定义页面类 -->
    <table-page></table-page>
  </div>
</template>

<script>
import TablePage from '@/components/TablePage' // 错误：不需要导入全局组件

export default {
  components: {
    TablePage // 错误：不需要注册全局组件
  }
}
</script>

<style scoped>
.custom-page {
  /* 错误：在页面中添加了自定义样式 */
  padding: 20px;
  background-color: #f5f5f5;
}
</style>
```

### 2. 样式管理规范

**样式修改必须遵循以下流程：**

1. **定位样式文件**：
   - 表格页面样式：`src/styles/modules/table-page.scss`
   - 页签样式：`src/styles/modules/page-tab.scss`
   - 页面标题样式：`src/styles/modules/page-title.scss`

2. **样式修改规则**：
   - 只允许在对应的样式模块文件中修改样式
   - 必须保持原有的类名结构和命名规范
   - 必须使用项目定义的scss变量（`src/styles/variables.scss`）

3. **禁止事项**：
   - 严禁在页面组件的 `<style>` 标签中添加样式
   - 严禁创建与现有样式功能重复的新样式

✅ **正确示例（修改表格样式）：**

在 `src/styles/modules/table-page.scss` 中：

```scss
// 使用项目变量
@import '../variables.scss';

.el-table {
  &__header {
    background-color: $table-header-bg;
    height: $table-header-height;
    
    th {
      font-weight: $font-weight-bold;
      color: $text-color-primary;
    }
  }
  
  &__row {
    height: $table-row-height;
    
    &:hover {
      background-color: $table-hover-color;
    }
  }
}
```

❌ **错误示例：**

在页面组件中：

```vue
<style scoped>
/* 错误：在页面组件中定义样式 */
.el-table__header {
  background-color: #f5f7fa; /* 错误：使用硬编码颜色值 */
}

/* 错误：创建新类名定义表格样式 */
.my-custom-table th {
  font-weight: bold;
}
</style>
```

### 3. 新增样式规范

**如需添加新样式，必须遵循：**

1. **基于Element UI官方样式**：
   - 必须使用Element UI提供的类名作为基础
   - 禁止创建与Element UI功能重复的新类名

2. **BEM命名规范**：
   - Block（块）：独立实体，如 `.el-table`
   - Element（元素）：Block的一部分，使用双下划线连接，如 `.el-table__header`
   - Modifier（修饰符）：Block或Element的状态，使用双连字符连接，如 `.el-table--striped`

✅ **正确示例（添加新样式）：**

在 `src/styles/modules/table-page.scss` 中：

```scss
// 基于Element UI的表格组件扩展样式
.el-table {
  // 已有样式...
  
  // 新增导出按钮样式（使用BEM命名规范）
  &__export-button {
    margin-left: $spacing-medium;
    
    &--disabled {
      opacity: 0.5;
    }
  }
}
```

❌ **错误示例：**

```scss
/* 错误：创建与Element UI无关的新类名 */
.custom-table {
  width: 100%;
  border: 1px solid #ddd;
}

/* 错误：不遵循BEM命名规范 */
.tableExportBtn {
  margin-left: 10px;
}
```

### 4. 组件库使用指南

**项目已封装以下组件，禁止重新开发相同功能组件：**

#### 表格页面组件体系

| 组件名 | 说明 | 主要属性/事件 |
|-------|------|-------------|
| **TablePage** | 完整表格页面容器 | `:search-form`, `:search-fields`, `:action-buttons`, `:table-data`, `:table-columns`, `@search`, `@action` |
| **SearchBar** | 搜索表单组件 | `:form`, `:fields`, `@search` |
| **ActionButtons** | 操作按钮组件 | `:buttons`, `@click` |
| **DataTable** | 数据表格组件 | `:data`, `:columns`, `@row-click`, `@selection-change` |
| **Pagination** | 分页组件 | `:current`, `:total`, `:page-size`, `@change` |

✅ **使用示例：**

```vue
<template>
  <TablePage
    :search-form="searchForm"
    :search-fields="[
      { label: '名称', prop: 'name', type: 'input' },
      { label: '状态', prop: 'status', type: 'select', options: statusOptions }
    ]"
    :action-buttons="[
      { label: '新增', type: 'primary', action: 'add' },
      { label: '批量操作', type: 'default', children: [
        { label: '导出', action: 'export' },
        { label: '删除', action: 'batchDelete' }
      ]}
    ]"
    :table-data="tableData"
    :table-columns="[
      { label: '名称', prop: 'name' },
      { label: '状态', prop: 'status', formatter: statusFormatter },
      { label: '操作', type: 'action', actions: [
        { label: '编辑', action: 'edit' },
        { label: '删除', action: 'delete' }
      ]}
    ]"
    @search="handleSearch"
    @action="handleAction"
  />
</template>
```

#### 其他通用组件

- **页签组件**：使用 `el-tabs` 和 `el-tab-pane`，样式已全局统一
- **页面标题组件**：使用 `page-title` 组件，支持标题文本和右侧操作按钮

## 禁止事项总结

为确保项目开发质量和一致性，严禁以下行为：

1. **❌ 禁止在页面中重复引入已全局注册的组件**
2. **❌ 禁止在页面组件中添加样式代码**
3. **❌ 禁止创建与现有组件功能重复的新组件**
4. **❌ 禁止使用硬编码的样式值（颜色、尺寸等）**
5. **❌ 禁止使用不符合BEM规范的类名**
6. **❌ 禁止创建与Element UI功能重复的样式类**

## 开发流程最佳实践

1. 首先查看现有组件和样式是否满足需求
2. 使用全局组件构建页面基本结构
3. 如需样式调整，仅在样式模块文件中进行修改
4. 严格遵循组件属性定义，不要添加未定义的属性
5. 使用Element UI官方文档作为参考，结合项目已有实现
项目实际使用的是Vue 2，它不支持Vue 3的语法v-model:property.
在Vue 2中，v-model不接受参数，所以我们需要改回使用.sync修饰符，尽管ESLint提示它被废弃，但在Vue 2项目中这是正确的用法。





