# React 列表页面复用开发规范

## 1. 目标与原则
- **一致性**：所有列表页面致力于实现统一的视觉风格、布局结构和交互模式。
- **高效性**：开发者应聚焦于业务逻辑实现，最大程度减少在布局和基础样式上的重复劳动。
- **可维护性**：通过通用布局组件和集中样式管理，实现一处修改、多处生效的便捷维护。

## 2. 核心布局组件与实现思路

### 2.1 推荐的核心布局组件
本项目推荐使用标准化的列表布局组件来构建列表页面。根据页面具体需求（例如，是否需要左侧筛选树或复杂的顶部筛选区域），可以选择：
- **`TablePageLayout`**: 通用列表页面布局，通常包含顶部搜索栏、操作按钮、数据表格和分页。
- **`FilterBarTablePageLayout`**: 带有侧边栏/顶部复杂筛选区域的列表页面布局，如资源管理页面所采用的布局。

**核心原则**：**禁止**在各个列表页面中手动、重复地引入和拼装基础UI组件（如 `SearchBar`、`DataTable`、`Pagination`、`PageHeader` 等）来构建整体布局。应优先使用项目封装好的核心列表布局组件。

### 2.2 总体实现思路
- **布局组件中心化**：由核心列表布局组件（如 `FilterBarTablePageLayout`）统一负责页面的主要结构，包括筛选区域、内容表格、操作按钮和分页等。
- **页面组件专注业务**：具体的列表页面组件则专注于：
    - 数据获取与管理（使用React Hooks）。
    - 业务逻辑处理（搜索、筛选、增删改查、弹窗交互等）。
    - 向布局组件传递配置（如搜索项、表格列定义、按钮配置）。
    - 通过render props定制布局组件的特定区域。
    - 响应布局组件发出的事件回调。

## 3. 页面组件实现详解

本节详细说明如何基于核心布局组件 `FilterBarTablePageLayout` 来实现一个功能完善的列表页面。

### 3.1 引入核心布局与页面模板结构

在React组件中，首先引入并使用 `FilterBarTablePageLayout` 组件。页面的主要结构由该布局组件构成。

```tsx
// UserManagement.tsx
import React, { useState, useEffect, useCallback } from 'react'
import FilterBarTablePageLayout from '@/components/layouts/FilterBarTablePageLayout'
import DialogWrapper from '@/components/common/DialogWrapper'
import FilterFields from '@/components/common/FilterFields'
import type { SearchItem, ActionButton as ActionButtonType, TableColumn } from '@/types'

const UserManagement: React.FC = () => {
  // State管理
  const [loading, setLoading] = useState(false)
  const [tableData, setTableData] = useState<any[]>([])
  const [filters, setFilters] = useState({
    searchText: '',
    selectedUserType: null,
    department: ''
  })
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: 0
  })
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([])
  const [dialogVisible, setDialogVisible] = useState(false)
  const [dialogData, setDialogData] = useState<any>({})

  // 页面配置
  const pageTitle = '用户管理'
  
  const searchConfig: SearchItem[] = [
    { type: 'input', label: '用户名', prop: 'searchText', placeholder: '输入用户名或邮箱' },
    { type: 'select', label: '部门', prop: 'department', placeholder: '请选择部门', 
      options: [
        { label: '技术部', value: 'tech' },
        { label: '市场部', value: 'marketing' },
        { label: '人事部', value: 'hr' }
      ]
    }
  ]

  const actionButtons: ActionButtonType[] = [
    { text: '新增用户', action: 'add', type: 'primary' },
    { text: '批量删除', action: 'batchDelete', type: 'danger' },
    { text: '导出', action: 'export', type: 'default' }
  ]

  const tableColumns: TableColumn[] = [
    { prop: 'userName', label: '用户名', minWidth: 120 },
    { prop: 'email', label: '邮箱', minWidth: 200 },
    { prop: 'department', label: '部门', width: 120 },
    { prop: 'status', label: '状态', width: 100, render: 'status' },
    { prop: 'createTime', label: '创建时间', minWidth: 180 }
  ]

  return (
    <div className="user-management-page">
      <FilterBarTablePageLayout
        title={pageTitle}
        searchItems={searchConfig}
        initialFormData={filters}
        actionButtons={actionButtons}
        tableColumns={tableColumns}
        tableData={tableData}
        loading={loading}
        total={pagination.total}
        current={pagination.current}
        pageSize={pagination.pageSize}
        showSelection={true}
        showIndex={true}
        showTableAction={true}
        actionWidth={120}
        onSearch={handleSearch}
        onReset={handleReset}
        onAction={handleAction}
        onTableAction={handleTableAction}
        onPagination={handlePagination}
        onSelectionChange={handleSelectionChange}
        filterContent={
          <FilterFields 
            fields={filterFieldsConfig}
            value={filters}
            onChange={handleFilterChange}
          />
        }
        renderColumns={{
          status: (value: string, row: any) => (
            <span className={`status-tag ${value === 'active' ? 'status-active' : 'status-inactive'}`}>
              {value === 'active' ? '启用' : '禁用'}
            </span>
          )
        }}
        renderActions={(row: any) => (
          <>
            <button className="action-btn" onClick={() => handleEdit(row)}>
              编辑
            </button>
            <button className="action-btn danger" onClick={() => handleDelete(row)}>
              删除
            </button>
          </>
        )}
      />

      {/* 弹窗组件 */}
      <DialogWrapper
        visible={dialogVisible}
        title="用户信息"
        onConfirm={handleDialogConfirm}
        onCancel={handleDialogCancel}
      >
        {/* 弹窗内容 */}
      </DialogWrapper>
    </div>
  )
}

export default UserManagement
```

### 3.2 Props 配置详解

页面组件通过 Props 将数据和配置传递给 `FilterBarTablePageLayout` 组件，以驱动其渲染和行为。主要 Props 包括：

- **`title`**: 页面标题 (e.g., `"用户管理"`)
- **`searchItems`**: 顶部搜索栏的字段配置数组
- **`initialFormData`**: 筛选表单的初始数据对象
- **`actionButtons`**: 页面顶部操作按钮的配置数组
- **`tableColumns`**: 表格列定义的配置数组
- **`tableData`**: 当前页需要显示的表格数据数组
- **`loading`**: 控制表格加载状态的布尔值
- **`total`**: 数据总条目数，用于分页
- **`current` / `pageSize`**: 当前页码和每页条数
- **`showSelection` / `showIndex`**: 是否显示表格复选框和序号列
- **`showTableAction` / `actionWidth`**: 是否显示表格行操作列及其宽度

#### 3.2.1 表格列宽配置规范 (CRITICAL)

**重要**: 为确保表格列宽能够自适应并均匀分布，所有列配置必须遵循以下规范：

**✅ 推荐的列宽配置方式**：
```typescript
const tableColumns: TableColumn[] = [
  // ✅ 推荐：使用 minWidth 实现自适应列宽
  { prop: 'fieldName', label: '字段名称', minWidth: 120 },
  { prop: 'fieldComment', label: '中文名称', minWidth: 120 },
  { prop: 'dataType', label: '数据类型', minWidth: 100 },
  
  // ✅ 推荐：对于内容较长的列，可以设置更大的 minWidth
  { prop: 'description', label: '描述信息', minWidth: 200 },
  
  // ✅ 推荐：对于状态、操作等固定宽度列，可以使用 width
  { prop: 'status', label: '状态', width: 80 },
  { prop: 'action', label: '操作', width: 120 }
]
```

**❌ 避免的配置方式**：
```typescript
const tableColumns: TableColumn[] = [
  // ❌ 避免：所有列都使用固定 width，会导致列宽无法自适应
  { prop: 'fieldName', label: '字段名称', width: 180 },
  { prop: 'fieldComment', label: '中文名称', width: 180 },
  
  // ❌ 避免：minWidth 设置过大，在小屏幕上会导致水平滚动
  { prop: 'dataType', label: '数据类型', minWidth: 300 }
]
```

**配置原则**：
1. **优先使用 `minWidth`**：让列宽能够根据容器大小自适应调整
2. **合理设置最小宽度**：通常设置为 80-150px，确保内容可读性
3. **固定宽度仅用于特殊列**：如状态标签、操作按钮等内容固定的列
4. **启用溢出提示**：DataTable 组件已自动启用溢出省略和悬停提示
5. **内容长度适配**：根据预期内容长度合理设置 minWidth 值

#### 3.2.2 操作按钮配置规范

**重要**: 操作按钮配置必须严格按照以下格式，以确保与 `ActionButton` 组件兼容：

```typescript
const actionButtons: ActionButtonType[] = [
  { 
    text: '按钮显示文字',    // 必需：按钮显示的文字
    action: 'actionKey',     // 必需：点击时传递的动作标识
    type: 'primary',         // 可选：按钮类型 (primary, default, success, warning, danger, info, text)
    size: 'medium',          // 可选：按钮尺寸 (large, medium, small, mini)
    disabled: false          // 可选：是否禁用
  }
  // 注意：不要添加 icon 属性，操作按钮统一使用纯文字显示
]
```

**配置要点**：
- 使用 `text` 而不是 `label` 作为显示文字属性
- 使用 `action` 而不是 `key` 作为动作标识属性  
- **禁止使用 `icon` 属性**，所有操作按钮统一使用纯文字显示
- 事件处理方法接收的参数是 `action` 的值（字符串），而不是整个按钮对象

### 3.3 事件处理机制

页面组件监听由 `FilterBarTablePageLayout` 组件触发的回调事件，以执行相应的业务逻辑。主要事件处理包括：

```tsx
// 搜索事件处理
const handleSearch = useCallback((formData: Record<string, any>) => {
  setFilters(prev => ({ ...prev, ...formData }))
  setPagination(prev => ({ ...prev, current: 1 }))
  fetchData({ ...filters, ...formData, page: 1 })
}, [filters])

// 重置事件处理
const handleReset = useCallback(() => {
  const resetFilters = {
    searchText: '',
    selectedUserType: null,
    department: ''
  }
  setFilters(resetFilters)
  setPagination(prev => ({ ...prev, current: 1 }))
  fetchData({ ...resetFilters, page: 1 })
}, [])

// 操作按钮事件处理
const handleAction = useCallback((action: string) => {
  console.log('Page action:', action) // action 是字符串，如 'export', 'batchDelete'
  
  switch (action) {
    case 'add':
      setDialogData({})
      setDialogVisible(true)
      break
    case 'export':
      exportData()
      break
    case 'batchDelete':
      if (selectedRowKeys.length === 0) {
        // 显示警告消息
        return
      }
      batchDeleteUsers()
      break
    default:
      console.warn('Unknown action:', action)
  }
}, [selectedRowKeys])

// 表格行操作事件处理
const handleTableAction = useCallback((action: string, row: any) => {
  console.log('Table action:', action, row)
  // 通过 renderActions 自定义时，通常不会用到此回调
}, [])

// 分页事件处理
const handlePagination = useCallback((page: number, size: number) => {
  setPagination(prev => ({ ...prev, current: page, pageSize: size }))
  fetchData({ ...filters, page, pageSize: size })
}, [filters])

// 选择变化事件处理
const handleSelectionChange = useCallback((selectedKeys: React.Key[]) => {
  setSelectedRowKeys(selectedKeys)
}, [])
```

#### 3.3.1 操作按钮事件处理示例

```typescript
// 正确的操作按钮事件处理方法
const handleAction = useCallback((action: string) => {
  console.log('Page action:', action) // action 是字符串，如 'export', 'batchClaim'
  
  if (action === 'export') {
    exportData()
  } else if (action === 'batchClaim') {
    batchClaimResources()
  } else if (action === 'delete') {
    deleteSelectedItems()
  }
}, [])
```

**注意事项**：
- 事件处理方法接收的参数是按钮的 `action` 属性值（字符串）
- 不要使用 `action.key` 或 `action.action` 的形式
- 直接对字符串进行比较即可

### 3.4 自定义渲染（Render Props）定制与应用

React 版本使用 render props 允许页面组件对核心布局组件的特定区域进行深度自定义：

- **`filterContent`**: 用于在 `FilterBarTablePageLayout` 中嵌入自定义的筛选逻辑和UI
  ```tsx
  filterContent={
    <FilterFields 
      fields={filterFieldsConfig}
      value={filters}
      onChange={handleFilterChange}
    />
  }
  ```

- **`renderColumns`**: 用于自定义特定列的渲染
  ```tsx
  renderColumns={{
    status: (value: string, row: any) => (
      <span className={`status-tag ${value === 'active' ? 'status-active' : 'status-inactive'}`}>
        {value === 'active' ? '启用' : '禁用'}
      </span>
    ),
    avatar: (value: string, row: any) => (
      <img src={value || '/default-avatar.png'} alt="头像" className="user-avatar" />
    )
  }}
  ```

- **`renderActions`**: 用于完全自定义表格的行操作列
  ```tsx
  renderActions={(row: any) => (
    <>
      <button className="action-btn" onClick={() => handleEdit(row)}>
        编辑
      </button>
      <button className="action-btn danger" onClick={() => handleDelete(row)}>
        删除
      </button>
    </>
  )}
  ```

- **其他渲染属性**: 如 `headerExtra`（标题栏右侧额外内容）、`operationButtons`（顶部操作按钮区额外内容）等

### 3.5 数据管理与业务逻辑实现

列表页面的核心业务逻辑、状态管理和数据获取均使用React Hooks在函数组件中实现。

```tsx
// 数据获取Hook
const fetchData = useCallback(async (params = {}) => {
  setLoading(true)
  try {
    const requestParams = {
      ...filters,
      ...params,
      page: pagination.current,
      pageSize: pagination.pageSize
    }
    
    // const response = await getUserList(requestParams)
    // setTableData(response.data.list)
    // setPagination(prev => ({ ...prev, total: response.data.total }))

    // 模拟数据
    const mockData = Array.from({ length: requestParams.pageSize }, (_, i) => ({
      id: (requestParams.page - 1) * requestParams.pageSize + i + 1,
      userName: `用户${(requestParams.page - 1) * requestParams.pageSize + i + 1}`,
      email: `user${i + 1}@example.com`,
      department: ['技术部', '市场部', '人事部'][i % 3],
      status: Math.random() > 0.5 ? 'active' : 'inactive',
      createTime: new Date().toLocaleString()
    }))
    
    setTableData(mockData)
    setPagination(prev => ({ ...prev, total: 100 }))
    
  } catch (error) {
    console.error('Failed to load data:', error)
    // 显示错误消息
  } finally {
    setLoading(false)
  }
}, [filters, pagination.current, pagination.pageSize])

// 组件初始化
useEffect(() => {
  fetchData()
}, [])

// 业务操作方法
const handleEdit = useCallback((row: any) => {
  setDialogData(row)
  setDialogVisible(true)
}, [])

const handleDelete = useCallback((row: any) => {
  // 显示确认对话框
  // 删除确认后调用API
  console.log('Delete user:', row.id)
}, [])

const exportData = useCallback(() => {
  console.log('Export data with filters:', filters)
  // 实现导出逻辑
}, [filters])

const batchDeleteUsers = useCallback(() => {
  console.log('Batch delete users:', selectedRowKeys)
  // 实现批量删除逻辑
}, [selectedRowKeys])
```

### 3.5.1 数据处理最佳实践

React Hook 中的常见最佳实践：

1. **使用 useState 管理组件状态**:
   ```tsx
   const [filters, setFilters] = useState({
     searchText: '',
     department: ''
   })
   ```

2. **使用 useCallback 优化事件处理函数**:
   ```tsx
   const handleSearch = useCallback((formData: Record<string, any>) => {
     setFilters(prev => ({ ...prev, ...formData }))
     fetchData(formData)
   }, [])
   ```

3. **正确的数据筛选方式**:
   ```tsx
   const filteredData = useMemo(() => {
     let result = originalData
     
     if (filters.category) {
       result = result.filter(item => item.category === filters.category)
     }
     
     if (filters.status) {
       result = result.filter(item => item.status === filters.status)
     }
     
     if (filters.searchText) {
       result = result.filter(item => 
         item.name.includes(filters.searchText)
       )
     }
     
     return result
   }, [originalData, filters])
   ```

4. **使用 useEffect 处理副作用**:
   ```tsx
   useEffect(() => {
     fetchData()
   }, [filters, pagination.current, pagination.pageSize])
   ```

遵循这些最佳实践可以提高代码的性能和可维护性。

## 4. 快速开发新列表页面的推荐流程

1. **创建页面组件**: 在 `src/views/yourModule/` 目录下创建新的 `.tsx` 文件 (e.g., `MyNewListPage.tsx`)。
2. **引入核心布局组件**: 引入项目推荐的核心列表布局组件 (e.g., `FilterBarTablePageLayout` 或 `TablePageLayout`)。
3. **搭建组件基本结构**: 使用引入的核心列表布局组件作为主要内容容器。
4. **定义状态和配置**: 使用 `useState` 初始化页面所需的状态，包括：
   - 筛选条件对象 (`filters`)
   - 表格数据数组 (`tableData`) 和总数 (`pagination.total`)
   - 分页对象 (`pagination`)
   - 加载状态 (`loading`)
   - 相关的配置数组 (搜索栏、操作按钮、表格列)
5. **配置Props**: 根据状态数据，为核心布局组件绑定必要的 Props。
6. **实现事件处理**: 
   - 编写 `fetchData` 函数用于获取和处理列表数据
   - 实现事件处理函数 (如 `onSearch`, `onAction`, `onPagination` 的回调)
   - 编写业务相关的操作处理函数
7. **(可选) 自定义渲染**: 如果布局组件提供的标准功能不满足需求，通过render props进行定制。
8. **调用初始加载**: 在 `useEffect` 钩子中调用 `fetchData()` 加载初始数据。
9. **编写样式**: 如有必要，在对应的 `.scss` 文件中添加页面特有的少量样式。

## 5. 结构与代码示例

以下代码片段展示了基于 `FilterBarTablePageLayout` 的完整列表页面示例：

### 5.1 完整页面组件示例

```tsx
// UserManagement.tsx
import React, { useState, useEffect, useCallback, useMemo } from 'react'
import FilterBarTablePageLayout from '@/components/layouts/FilterBarTablePageLayout'
import DialogWrapper from '@/components/common/DialogWrapper'
import FilterFields from '@/components/common/FilterFields'
import type { SearchItem, ActionButton as ActionButtonType, TableColumn } from '@/types'
import './UserManagement.scss'

const UserManagement: React.FC = () => {
  // 状态管理
  const [loading, setLoading] = useState(false)
  const [tableData, setTableData] = useState<any[]>([])
  const [filters, setFilters] = useState({
    searchText: '',
    selectedUserType: null,
    department: ''
  })
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: 0
  })
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([])
  const [dialogState, setDialogState] = useState({
    visible: false,
    title: '',
    loading: false,
    formData: {} as any,
    currentRow: null as any
  })

  // 页面配置
  const pageTitle = '用户管理'
  
  const searchConfig: SearchItem[] = useMemo(() => [
    { type: 'input', label: '关键字', prop: 'searchText', placeholder: '输入用户名或邮箱' },
    { 
      type: 'select', 
      label: '部门', 
      prop: 'department', 
      placeholder: '请选择部门',
      options: [
        { label: '技术部', value: 'tech' },
        { label: '市场部', value: 'marketing' },
        { label: '人事部', value: 'hr' }
      ]
    }
  ], [])

  const actionButtons: ActionButtonType[] = useMemo(() => [
    { text: '新增用户', action: 'add', type: 'primary' },
    { text: '批量删除', action: 'batchDelete', type: 'danger' },
    { text: '导出', action: 'export', type: 'default' }
  ], [])

  const tableColumns: TableColumn[] = useMemo(() => [
    { prop: 'userName', label: '用户名', minWidth: 120 },
    { prop: 'email', label: '邮箱', minWidth: 200 },
    { prop: 'department', label: '部门', width: 120 },
    { prop: 'status', label: '状态', width: 100, render: 'status' },
    { prop: 'createTime', label: '创建时间', minWidth: 180 }
  ], [])

  const filterFieldsConfig = useMemo(() => ({
    treeData: [
      {
        label: '用户类型',
        value: 'userType',
        children: [
          { label: '管理员', value: 'admin' },
          { label: '普通用户', value: 'user' },
          { label: '访客', value: 'guest' }
        ]
      }
    ]
  }), [])

  // 数据获取
  const fetchData = useCallback(async (params = {}) => {
    setLoading(true)
    try {
      const requestParams = {
        ...filters,
        ...params,
        page: pagination.current,
        pageSize: pagination.pageSize
      }
      
      // const response = await getUserList(requestParams)
      // setTableData(response.data.list)
      // setPagination(prev => ({ ...prev, total: response.data.total }))

      // 模拟数据
      await new Promise(resolve => setTimeout(resolve, 500)) // 模拟加载延迟
      const mockData = Array.from({ length: requestParams.pageSize }, (_, i) => {
        const index = (requestParams.page - 1) * requestParams.pageSize + i + 1
        return {
          id: index,
          userName: `用户${index}`,
          email: `user${index}@example.com`,
          department: ['技术部', '市场部', '人事部'][i % 3],
          status: Math.random() > 0.5 ? 'active' : 'inactive',
          createTime: new Date(Date.now() - Math.random() * 10000000000).toLocaleString(),
          canDelete: Math.random() > 0.7
        }
      })
      
      setTableData(mockData)
      setPagination(prev => ({ ...prev, total: 100 }))
      
    } catch (error) {
      console.error('Failed to load data:', error)
      // 这里应该显示错误消息，实际项目中可使用 message 组件
    } finally {
      setLoading(false)
    }
  }, [filters, pagination.current, pagination.pageSize])

  // 事件处理
  const handleSearch = useCallback((formData: Record<string, any>) => {
    setFilters(prev => ({ ...prev, ...formData }))
    setPagination(prev => ({ ...prev, current: 1 }))
    // fetchData 会在 useEffect 中被调用
  }, [])

  const handleReset = useCallback(() => {
    const resetFilters = {
      searchText: '',
      selectedUserType: null,
      department: ''
    }
    setFilters(resetFilters)
    setPagination(prev => ({ ...prev, current: 1 }))
  }, [])

  const handleFilterChange = useCallback((selectedFilterValues: any) => {
    setFilters(prev => ({ 
      ...prev, 
      selectedUserType: selectedFilterValues.userType 
    }))
    setPagination(prev => ({ ...prev, current: 1 }))
  }, [])

  const handleAction = useCallback((action: string) => {
    console.log('Page action:', action)
    
    switch (action) {
      case 'add':
        setDialogState({
          visible: true,
          title: '新增用户',
          loading: false,
          formData: {},
          currentRow: null
        })
        break
      case 'export':
        exportData()
        break
      case 'batchDelete':
        if (selectedRowKeys.length === 0) {
          alert('请至少选择一项进行批量删除')
          return
        }
        batchDeleteUsers()
        break
      default:
        console.warn('Unknown action:', action)
    }
  }, [selectedRowKeys])

  const handleTableAction = useCallback((action: string, row: any) => {
    console.log('Table action:', action, row)
    // 通过 renderActions 自定义时，通常不会用到此回调
  }, [])

  const handlePagination = useCallback((page: number, size: number) => {
    setPagination(prev => ({ ...prev, current: page, pageSize: size }))
  }, [])

  const handleSelectionChange = useCallback((selectedKeys: React.Key[]) => {
    setSelectedRowKeys(selectedKeys)
  }, [])

  // 业务操作
  const handleEdit = useCallback((row: any) => {
    setDialogState({
      visible: true,
      title: '编辑用户',
      loading: false,
      formData: { ...row },
      currentRow: row
    })
  }, [])

  const handleDelete = useCallback((row: any) => {
    if (window.confirm(`确认删除用户 "${row.userName}"?`)) {
      console.log('Delete user:', row.id)
      // await deleteUser(row.id)
      // 重新加载数据
      fetchData()
    }
  }, [fetchData])

  const exportData = useCallback(() => {
    console.log('Export data with filters:', filters)
    alert('导出功能执行中...')
  }, [filters])

  const batchDeleteUsers = useCallback(() => {
    console.log('Batch delete users:', selectedRowKeys)
    alert(`批量删除 ${selectedRowKeys.length} 个用户`)
  }, [selectedRowKeys])

  const handleDialogConfirm = useCallback(async () => {
    setDialogState(prev => ({ ...prev, loading: true }))
    try {
      // 表单验证和提交逻辑
      console.log('Save user data:', dialogState.formData)
      // await saveUser(dialogState.formData)
      
      setDialogState(prev => ({ ...prev, visible: false, loading: false }))
      fetchData() // 重新加载数据
    } catch (error) {
      console.error('Save failed:', error)
    } finally {
      setDialogState(prev => ({ ...prev, loading: false }))
    }
  }, [dialogState.formData, fetchData])

  const handleDialogCancel = useCallback(() => {
    setDialogState(prev => ({ ...prev, visible: false }))
  }, [])

  // 副作用
  useEffect(() => {
    fetchData()
  }, [filters, pagination.current, pagination.pageSize])

  return (
    <div className="user-management-page">
      <FilterBarTablePageLayout
        title={pageTitle}
        searchItems={searchConfig}
        initialFormData={filters}
        actionButtons={actionButtons}
        tableColumns={tableColumns}
        tableData={tableData}
        loading={loading}
        total={pagination.total}
        current={pagination.current}
        pageSize={pagination.pageSize}
        showSelection={true}
        showIndex={true}
        showTableAction={true}
        actionWidth={120}
        onSearch={handleSearch}
        onReset={handleReset}
        onAction={handleAction}
        onTableAction={handleTableAction}
        onPagination={handlePagination}
        onSelectionChange={handleSelectionChange}
        filterContent={
          <FilterFields 
            fields={filterFieldsConfig}
            value={filters}
            onChange={handleFilterChange}
          />
        }
        renderColumns={{
          status: (value: string, row: any) => (
            <span className={`status-tag ${value === 'active' ? 'status-active' : 'status-inactive'}`}>
              {value === 'active' ? '启用' : '禁用'}
            </span>
          )
        }}
        renderActions={(row: any) => (
          <>
            <button className="action-btn" onClick={() => handleEdit(row)}>
              编辑
            </button>
            {row.canDelete && (
              <button className="action-btn danger" onClick={() => handleDelete(row)}>
                删除
              </button>
            )}
          </>
        )}
      />

      {/* 弹窗组件 */}
      <DialogWrapper
        visible={dialogState.visible}
        title={dialogState.title}
        loading={dialogState.loading}
        onConfirm={handleDialogConfirm}
        onCancel={handleDialogCancel}
      >
        <div className="user-form">
          <div className="form-item">
            <label>用户名：</label>
            <input 
              type="text" 
              value={dialogState.formData.userName || ''} 
              onChange={(e) => setDialogState(prev => ({
                ...prev,
                formData: { ...prev.formData, userName: e.target.value }
              }))}
            />
          </div>
          <div className="form-item">
            <label>邮箱：</label>
            <input 
              type="email" 
              value={dialogState.formData.email || ''} 
              onChange={(e) => setDialogState(prev => ({
                ...prev,
                formData: { ...prev.formData, email: e.target.value }
              }))}
            />
          </div>
        </div>
      </DialogWrapper>
    </div>
  )
}

export default UserManagement
```

### 5.2 配套样式文件示例

```scss
// UserManagement.scss
.user-management-page {
  height: 100%;
  
  .status-tag {
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 12px;
    
    &.status-active {
      background-color: #f0f9ff;
      color: #1e40af;
      border: 1px solid #3b82f6;
    }
    
    &.status-inactive {
      background-color: #fef2f2;
      color: #dc2626;
      border: 1px solid #ef4444;
    }
  }
  
  .action-btn {
    padding: 4px 8px;
    margin-right: 8px;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    background: white;
    color: #374151;
    cursor: pointer;
    font-size: 12px;
    
    &:hover {
      background-color: #f9fafb;
    }
    
    &.danger {
      color: #dc2626;
      border-color: #ef4444;
      
      &:hover {
        background-color: #fef2f2;
      }
    }
  }
  
  .user-form {
    .form-item {
      margin-bottom: 16px;
      
      label {
        display: inline-block;
        width: 80px;
        font-weight: 500;
      }
      
      input {
        width: 200px;
        padding: 8px;
        border: 1px solid #d1d5db;
        border-radius: 4px;
        
        &:focus {
          outline: none;
          border-color: #3b82f6;
          box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
        }
      }
    }
  }
}
```

### 5.3 整体结构示意图

```
应用顶层布局 (可选, 如项目统一导航栏 NavigationLayout)
  └── 路由容器 (React Router)
      └── 列表页面组件 (e.g., UserManagement.tsx)
          ├── 核心列表布局组件 (e.g., FilterBarTablePageLayout)
          │   ├── 筛选区域 (由布局组件管理, 可通过 filterContent 属性自定义)
          │   │   └── (若自定义: e.g., FilterFields 组件 / 或布局内建 SearchBar)
          │   ├── 顶部操作按钮区域 (通过 actionButtons 属性配置)
          │   ├── 数据表格区域 (由布局组件内 DataTable 实现)
          │   │   ├── 表格列 (通过 tableColumns 属性配置)
          │   │   └── (单元格内容可通过 renderColumns 自定义)
          │   ├── 行操作列 (通过 showTableAction 属性控制, 内容通过 renderActions 自定义)
          │   └── 分页组件 (由布局组件内 Pagination 实现, 通过分页相关属性绑定)
          │
          └── 页面级辅助组件 (e.g., DialogWrapper 用于弹窗)
              └── (弹窗内部表单等业务组件)
```

**多Tab页面的扁平化结构示意图**：

```
应用顶层布局 (可选, 如项目统一导航栏 NavigationLayout)
  └── 路由容器 (React Router)
      └── Tab布局组件 (e.g., HorizontalTabsPageLayout / VerticalTabsPageLayout)
          ├── Tab导航区域 (根据路由配置自动生成)
          └── Tab内容区域 (React Router Outlet)
              └── 各Tab页面组件 (各自独立的React组件)
                  └── 核心列表布局组件 (e.g., TablePageLayout)
                      ├── 搜索栏
                      ├── 操作按钮
                      ├── 数据表格
                      └── 分页
```

## 6. 样式规范
- **模块化样式**: 页面特有的样式应写在对应的 `.scss` 文件中，通过CSS Modules或者类名前缀避免全局污染。
- **最小化原则**: 仅在核心布局组件无法满足需求，且确实需要微调时，才添加少量页面特有样式。**严禁**大范围覆盖或重写核心布局组件的基础样式。
- **Class 命名**: 遵循项目统一的 BEM 或其他 CSS 命名规范。
- **响应式设计**: 确保页面在不同屏幕尺寸下都有良好的显示效果。
- **高度与布局**: 确保列表页面及其布局组件能正确撑开高度，通常要求根节点有 `height: 100%` 或使用 Flex 布局来避免内容塌陷。

## 7. 统一列表页面的优点
- **开发效率高**: 开发者聚焦于业务逻辑，无需重复搭建列表页的常见结构。
- **代码一致性强**: 所有列表页面遵循相似的结构和交互模式，降低学习成本，便于团队协作。
- **易于维护和升级**: 核心布局和样式集中管理，修改一处即可影响所有使用该布局的页面。
- **用户体验统一**: 用户在不同列表页面间切换时，能获得一致的操作体验。
- **代码复用性好**: 标准化的布局组件和开发模式促进了代码复用。
- **类型安全**: TypeScript提供的类型检查确保了代码的健壮性。

## 8. 结论
本规范旨在通过推广使用标准化的核心列表布局组件（如 `TablePageLayout` 或 `FilterBarTablePageLayout`），并结合清晰的React函数组件实现模式，来提升列表页面的开发效率、代码质量和可维护性。开发者应严格遵循本规范，充分利用布局组件提供的 Props、回调函数和 render props，将业务逻辑与视图结构有效分离。

## 9. 开发检查清单

为了避免常见错误，在开发列表页面时请使用以下检查清单：

### 9.1 操作按钮配置检查
- [ ] 使用 `text` 属性而不是 `label`
- [ ] 使用 `action` 属性而不是 `key` 
- [ ] **没有**添加 `icon` 属性（操作按钮统一使用纯文字）
- [ ] 事件处理方法直接比较 `action` 字符串，不使用 `action.key`
- [ ] 优先使用标准布局组件的 `actionButtons` 配置，避免内联按钮

### 9.2 React组件最佳实践检查  
- [ ] 使用 `useCallback` 优化事件处理函数
- [ ] 使用 `useMemo` 优化配置数组的创建
- [ ] 正确使用 `useEffect` 处理数据加载副作用
- [ ] 确保状态更新的不可变性原则

### 9.3 TypeScript类型检查
- [ ] 为所有Props定义正确的TypeScript类型
- [ ] 使用项目提供的类型定义（如 `SearchItem`, `ActionButton`, `TableColumn`）
- [ ] 确保事件处理函数的参数类型正确

### 9.4 性能优化检查
- [ ] 避免在render方法中创建新的对象或数组
- [ ] 合理使用 `React.memo` 包装子组件（如果需要）
- [ ] 确保列表的key属性使用稳定的唯一标识

## 10. 特殊布局处理

### 10.1 非标准表格布局
对于不使用标准表格布局的页面，仍需遵循按钮文字显示原则：

```tsx
{/* 推荐：即使是内联按钮也使用纯文字 */}
<button className="btn-primary" onClick={handleAddRole}>新增角色</button>

{/* 避免：不要添加图标 */}
<button className="btn-primary" onClick={handleAddRole}>
  <Icon name="plus" /> 新增角色
</button>
```

### 10.2 布局选择原则
- **标准列表页面**：优先使用 `TablePageLayout` 或 `FilterBarTablePageLayout`
- **特殊布局需求**：可以自定义布局，但仍需遵循按钮文字显示规范
- **按钮一致性**：无论使用哪种布局，所有操作按钮都应使用纯文字显示

## 11. 多Tab页面开发规范（扁平化方式）

### 11.1 扁平化多Tab页面概述

对于需要包含多个子Tab的功能模块，本项目采用**扁平化路由配置方式**实现，而非创建额外的主容器页面。这种方式能够降低文件维护成本，使代码结构更加清晰。

**核心优势**：
- 文件结构扁平化，无需额外维护主容器文件
- 各Tab页面代码解耦，便于独立开发和维护
- 支持按需加载，提高应用性能
- 简化代码复杂度，降低嵌套层级

### 11.2 实现方式

#### 11.2.1 路由配置示例

在路由配置中，通过嵌套路由配置实现多Tab页面：

```tsx
// router/index.tsx
import { createBrowserRouter } from 'react-router-dom'
import HorizontalTabsPageLayout from '@/components/layouts/HorizontalTabsPageLayout'

export const router = createBrowserRouter([
  {
    path: '/governance/data-standards',
    element: <HorizontalTabsPageLayout />, // 或 VerticalTabsPageLayout
    children: [
      {
        index: true,
        element: <Navigate to="/governance/data-standards/basic" replace />
      },
      {
        path: 'basic',
        element: <BasicDataStandards />,
        handle: {
          title: '基础数据标准',
          activeTab: 'basic'
        }
      },
      {
        path: 'dictionary',
        element: <DataDictionary />,
        handle: {
          title: '数据字典',
          activeTab: 'dictionary'
        }
      },
      // 更多Tab路由...
    ]
  }
])
```

#### 11.2.2 Tab布局组件调整

为了支持扁平化路由方式，Tab布局组件需要：

1. 从路由配置中读取Tab信息
2. 根据当前路由自动激活对应Tab
3. 处理Tab切换时的路由导航

Tab布局组件示例结构：

```tsx
// HorizontalTabsPageLayout.tsx
import React from 'react'
import { Outlet, useNavigate, useLocation, useMatches } from 'react-router-dom'

const HorizontalTabsPageLayout: React.FC = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const matches = useMatches()

  // 从路由配置中获取所有Tab
  const tabs = useMemo(() => {
    const parentMatch = matches.find(match => 
      match.pathname === location.pathname.split('/').slice(0, 3).join('/')
    )
    return parentMatch?.handle?.children || []
  }, [matches, location.pathname])

  // 当前激活的Tab
  const activeTabName = useMemo(() => {
    return location.pathname.split('/').pop()
  }, [location.pathname])

  // 判断Tab是否激活
  const isActive = (tabPath: string) => {
    return tabPath === activeTabName
  }

  // 切换Tab
  const switchTab = (tabPath: string) => {
    if (!isActive(tabPath)) {
      navigate(tabPath)
    }
  }

  return (
    <div className="tab-layout">
      <div className="tabs-header">
        {tabs.map((tab: any) => (
          <div 
            key={tab.path}
            className={`tab-item ${isActive(tab.path) ? 'active' : ''}`}
            onClick={() => switchTab(tab.path)}
          >
            {tab.handle.title}
          </div>
        ))}
      </div>
      <div className="tab-content">
        <Outlet />
      </div>
    </div>
  )
}

export default HorizontalTabsPageLayout
```

### 11.3 Tab页面间数据共享

在扁平化路由方式下，各Tab页面是独立组件，如需共享数据，推荐以下方案：

1. **使用Redux状态管理**：
   - 为功能模块创建专用的Redux slice
   - 将共享状态存储在Redux中
   - 各Tab页面通过Redux hooks访问共享数据

2. **使用URL参数**：
   - 将关键参数存储在URL中
   - Tab切换时保留这些参数
   - 适用于需要在页面刷新后保持的状态

3. **使用浏览器存储**：
   - 对于临时性共享数据，可使用sessionStorage
   - 对于需要持久化的数据，可使用localStorage

4. **使用React Context**：
   - 在Tab布局组件层级提供Context
   - 各Tab页面通过useContext访问共享状态

### 11.4 Tab页面组件实现

各Tab页面仍按照本文档前述章节的列表页面开发规范实现，使用核心布局组件：

```tsx
// BasicDataStandards.tsx
import React, { useState, useEffect, useCallback } from 'react'
import TablePageLayout from '@/components/layouts/TablePageLayout'

const BasicDataStandards: React.FC = () => {
  const [loading, setLoading] = useState(false)
  const [tableData, setTableData] = useState<any[]>([])
  // ... 其他状态

  // ... 配置和事件处理

  return (
    <div className="basic-standards-page">
      <TablePageLayout
        title="基础数据标准"
        searchItems={searchConfig}
        initialFormData={filters}
        actionButtons={actionButtons}
        tableColumns={tableColumns}
        tableData={tableData}
        loading={loading}
        total={pagination.total}
        current={pagination.current}
        pageSize={pagination.pageSize}
        onSearch={handleSearch}
        onReset={handleReset}
        onAction={handleAction}
        onPagination={handlePagination}
      />
    </div>
  )
}

export default BasicDataStandards
```

### 11.5 开发流程与注意事项

1. **开发流程**：
   - 在路由配置中定义多Tab结构
   - 为每个Tab创建单独的React组件，使用核心布局组件
   - 根据需求选择数据共享方式（Redux/URL参数/Context/存储）
   - 确保各Tab页面样式保持一致

2. **注意事项**：
   - 合理设计路由路径，确保URL结构清晰、语义化
   - 合理使用React.lazy实现路由懒加载，避免首次加载所有Tab内容
   - 可能需要在路由守卫中处理Tab切换的特殊逻辑
   - 确保页面刷新时正确恢复Tab状态和共享数据
   - 避免Tab切换时重复发起相同的API请求

### 11.6 扁平化方式与主容器方式的对比

| 方面 | 扁平化路由方式（推荐） | 主容器页面方式 |
|------|-----------------|--------------|
| 文件数量 | 少（无需主容器文件） | 多（需要额外的主容器文件） |
| 代码耦合度 | 低（各Tab独立） | 较高（主容器与子Tab间存在依赖） |
| 状态共享 | 通过Redux/Context/URL/存储 | 通过容器组件Props和回调 |
| 页面切换 | 触发路由变化 | 组件内部切换（不改变URL） |
| 用户体验 | URL反映当前Tab（可收藏/分享） | 需额外处理URL状态保持 |
| 代码复杂度 | 较低 | 较高（需处理组件嵌套关系） |
| 性能影响 | 支持按需加载各Tab | 可能需一次性加载所有Tab |

本项目推荐使用扁平化路由方式实现多Tab页面，以简化文件维护，提高代码清晰度和可维护性。

## 12. 其他注意事项与说明
- **操作栏固定**: `FilterBarTablePageLayout` 或 `TablePageLayout` 可能提供 `actionFixed` 属性来固定行操作列。应仅在表格内容宽度确实很大，导致操作列易被遮挡时才启用固定。默认情况下，操作列不固定，以获得更好的响应式表现。
- **分页数据绑定**: 分页相关的 `current` 和 `pageSize` 通过回调函数实现数据传递，确保状态管理的清晰性。
- **Props 与 Render Props 的选择**: 优先使用 Props 进行配置。当 Props 无法满足复杂的UI定制或逻辑嵌入需求时，再考虑使用 render props。
- **API 调用位置**: 所有与后端交互的API调用（数据获取、提交等）均应在页面组件的 hooks 中发起和处理，核心布局组件不直接参与API交互。
- **组件拆分**: 对于列表页面中复杂的、可复用的部分（例如弹窗内的表单），可以将其拆分为独立的子组件，再由页面组件引入和管理。
- **错误处理**: 建议在数据获取和操作中添加适当的错误处理逻辑，提升用户体验。

如需进一步细化核心列表布局组件（如 `TablePageLayout` 或 `FilterBarTablePageLayout`）的详细API文档，应查阅其各自的组件设计说明或源码注释。 