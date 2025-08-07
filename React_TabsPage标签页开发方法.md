# React 标签页开发规范（基于实际实现）

本规范基于项目中 `UserManagementTabs.tsx` 的实际实现，为开发者提供标准化的标签页开发指导。

## 1. 总体实现架构

### 1.1 技术选型
- **布局组件**: `VerticalTabsPageLayout` - 垂直图标标签页布局
- **图标库**: `@ant-design/icons` - Ant Design 图标
- **路由**: React Router v6 - 支持嵌套路由和Outlet
- **类型安全**: TypeScript + 严格类型定义

### 1.2 实现原理
```
父级路由容器 (UserManagementTabs)
├── VerticalTabsPageLayout (布局组件)
│   ├── VerticalIconMenu (左侧图标菜单)
│   └── Outlet (右侧内容区域)
│       ├── UserManagement-User.tsx
│       ├── UserManagement-Role.tsx
│       └── UserManagement-Permission.tsx
```

---

## 2. 标准实现模式

### 2.1 标签页容器组件实现

**文件位置**: `src/views/{模块名}/{模块名}Tabs.tsx`

```tsx
// src/views/UserManagement/UserManagementTabs.tsx
import React from 'react'
import { UserOutlined, SafetyOutlined, KeyOutlined } from '@ant-design/icons'
import VerticalTabsPageLayout from '../../components/layouts/VerticalTabsPageLayout'
import type { VerticalIconMenuItem } from '../../components/common/VerticalIconMenu'

const UserManagementTabs: React.FC = () => {
  // 标签页菜单配置
  const menuItems: VerticalIconMenuItem[] = [
    {
      key: '/user-management/user',
      icon: <UserOutlined />,
      label: '用户管理'
    },
    {
      key: '/user-management/role',
      icon: <SafetyOutlined />,
      label: '角色管理'
    },
    {
      key: '/user-management/permission',
      icon: <KeyOutlined />,
      label: '权限管理'
    }
  ]

  return (
    <VerticalTabsPageLayout 
      menuItems={menuItems}
      menuWidth={60}
      menuBackgroundColor="#fafafa"
      contentPadding="24px"
      contentMargin="16px 16px 16px 0"
      contentBorderRadius="0 6px 6px 0"
      contentBoxShadow="2px 2px 8px rgba(0,0,0,0.06)"
    />
  )
}

export default UserManagementTabs
```

### 2.2 路由配置实现

**文件位置**: `src/router/index.tsx`

```tsx
import { createBrowserRouter, Navigate } from 'react-router-dom'
import NavigationLayout from '../components/layouts/NavigationLayout'
import UserManagementTabs from '../views/UserManagement/UserManagementTabs'
import UserManagementUser from '../views/UserManagement/UserManagement-User'
import UserManagementRole from '../views/UserManagement/UserManagement-Role'
import UserManagementPermission from '../views/UserManagement/UserManagement-Permission'

const router = createBrowserRouter([
  {
    path: '/',
    element: <NavigationLayout pageName="企业数据管理平台" breadcrumbs={[]} />,
    children: [
      // 用户管理垂直标签页模块
      {
        path: 'user-management',
        element: <UserManagementTabs />,
        children: [
          {
            index: true,
            element: <Navigate to="/user-management/user" replace />
          },
          {
            path: 'user',
            element: <UserManagementUser />,
            handle: { 
              title: '用户管理', 
              breadcrumb: ['系统管理', '用户权限管理', '用户管理'] 
            }
          },
          {
            path: 'role',
            element: <UserManagementRole />,
            handle: { 
              title: '角色管理', 
              breadcrumb: ['系统管理', '用户权限管理', '角色管理'] 
            }
          },
          {
            path: 'permission',
            element: <UserManagementPermission />,
            handle: { 
              title: '权限管理', 
              breadcrumb: ['系统管理', '用户权限管理', '权限管理'] 
            }
          }
        ]
      }
    ]
  }
])
```

### 2.3 子页面内容实现

**文件位置**: `src/views/{模块名}/{模块名}-{子页面}.tsx`

```tsx
// src/views/UserManagement/UserManagement-User.tsx
import React, { useState, useCallback } from 'react'
import FilterBarTablePageLayout from '../../components/layouts/FilterBarTablePageLayout'
import type { SearchItem, ActionButton, TableColumn } from '../../types'

const UserManagementUser: React.FC = () => {
  const [loading, setLoading] = useState(false)
  const [tableData, setTableData] = useState<any[]>([])

  // 搜索配置
  const searchItems: SearchItem[] = [
    { type: 'input', label: '用户名', prop: 'username', placeholder: '请输入用户名' },
    { 
      type: 'select', 
      label: '状态', 
      prop: 'status', 
      placeholder: '请选择状态',
      options: [
        { label: '启用', value: 'active' },
        { label: '禁用', value: 'inactive' }
      ]
    }
  ]

  // 操作按钮配置
  const actionButtons: ActionButton[] = [
    { name: 'add', label: '新增用户', type: 'primary' },
    { name: 'export', label: '导出数据', type: 'default' }
  ]

  // 表格列配置
  const tableColumns: TableColumn[] = [
    { prop: 'username', label: '用户名', minWidth: 150 },
    { prop: 'realName', label: '真实姓名', width: 120 },
    { prop: 'department', label: '部门', width: 150 },
    { prop: 'role', label: '角色', width: 120 },
    { prop: 'status', label: '状态', width: 100 },
    { prop: 'createTime', label: '创建时间', width: 180 }
  ]

  // 事件处理
  const handleSearch = useCallback((formData: Record<string, any>) => {
    console.log('搜索参数:', formData)
    // 执行搜索逻辑
  }, [])

  const handleAction = useCallback((action: string) => {
    console.log('操作:', action)
    // 执行对应操作
  }, [])

  return (
    <FilterBarTablePageLayout
      searchItems={searchItems}
      actionButtons={actionButtons}
      tableColumns={tableColumns}
      tableData={tableData}
      loading={loading}
      onSearch={handleSearch}
      onAction={handleAction}
      showSelection={true}
      showIndex={true}
      showTableAction={true}
    />
  )
}

export default UserManagementUser
```

---

## 3. 关键配置说明

### 3.1 VerticalIconMenuItem 接口定义

```tsx
interface VerticalIconMenuItem {
  key: string        // 路由路径，用于导航和当前标签识别
  icon: React.ReactNode  // Ant Design 图标组件
  label: string      // 标签显示文本（用于tooltip）
  tooltip?: string   // 可选的自定义tooltip文本
}
```

### 3.2 VerticalTabsPageLayout 配置项

```tsx
interface VerticalTabsPageLayoutProps {
  menuItems: VerticalIconMenuItem[]    // 必需：菜单项配置
  menuWidth?: number                   // 可选：菜单宽度，默认60px
  menuBackgroundColor?: string         // 可选：菜单背景色，默认#fafafa
  contentPadding?: string             // 可选：内容区域内边距，默认24px
  contentMargin?: string              // 可选：内容区域外边距
  contentBorderRadius?: string        // 可选：内容区域圆角
  contentBoxShadow?: string           // 可选：内容区域阴影
}
```

### 3.3 标准配置值参考

```tsx
// 推荐的标准配置
const standardConfig = {
  menuWidth: 60,
  menuBackgroundColor: "#fafafa",
  contentPadding: "24px",
  contentMargin: "16px 16px 16px 0",
  contentBorderRadius: "0 6px 6px 0",
  contentBoxShadow: "2px 2px 8px rgba(0,0,0,0.06)"
}
```

---

## 4. 开发步骤指导

### 4.1 创建新标签页模块的完整步骤

**步骤1：创建标签页容器组件**
```bash
# 在对应模块目录创建Tabs组件
touch src/views/{ModuleName}/{ModuleName}Tabs.tsx
```

**步骤2：配置菜单项**
```tsx
const menuItems: VerticalIconMenuItem[] = [
  {
    key: '/{module-path}/page1',
    icon: <IconComponent1 />,
    label: '页面1名称'
  },
  {
    key: '/{module-path}/page2', 
    icon: <IconComponent2 />,
    label: '页面2名称'
  }
  // ... 更多标签页
]
```

**步骤3：创建子页面组件**
```bash
# 为每个标签页创建对应的内容组件
touch src/views/{ModuleName}/{ModuleName}-Page1.tsx
touch src/views/{ModuleName}/{ModuleName}-Page2.tsx
```

**步骤4：配置路由**
```tsx
// 在 router/index.tsx 中添加路由配置
{
  path: '{module-path}',
  element: <{ModuleName}Tabs />,
  children: [
    {
      index: true,
      element: <Navigate to="/{module-path}/page1" replace />
    },
    {
      path: 'page1',
      element: <{ModuleName}Page1 />,
      handle: { title: '页面1', breadcrumb: ['模块', '页面1'] }
    }
    // ... 更多子路由
  ]
}
```

### 4.2 文件命名规范

```
src/views/{ModuleName}/
├── {ModuleName}Tabs.tsx          // 标签页容器组件
├── {ModuleName}-{SubPage}.tsx    // 子页面组件
├── {ModuleName}-{SubPage}.tsx    // 更多子页面
└── index.ts                      // 可选的导出文件
```

**命名示例**:
- `UserManagementTabs.tsx` - 用户管理标签页容器
- `UserManagement-User.tsx` - 用户管理子页面
- `UserManagement-Role.tsx` - 角色管理子页面

---

## 5. 最佳实践与规范

### 5.1 代码规范

**1. 组件导入顺序**
```tsx
// 1. React相关
import React from 'react'

// 2. 第三方库
import { UserOutlined } from '@ant-design/icons'

// 3. 项目内组件
import VerticalTabsPageLayout from '../../components/layouts/VerticalTabsPageLayout'

// 4. 类型定义
import type { VerticalIconMenuItem } from '../../components/common/VerticalIconMenu'
```

**2. 配置对象提取**
```tsx
// ✅ 推荐：将配置提取为常量
const MENU_ITEMS: VerticalIconMenuItem[] = [
  // 配置项...
]

const LAYOUT_CONFIG = {
  menuWidth: 60,
  menuBackgroundColor: "#fafafa",
  // 其他配置...
}

// ❌ 避免：直接在JSX中写配置
<VerticalTabsPageLayout 
  menuItems={[{key: '...', icon: <UserOutlined />, label: '...'}]}
/>
```

**3. TypeScript类型安全**
```tsx
// ✅ 使用严格的类型定义
const menuItems: VerticalIconMenuItem[] = [...]

// ✅ 为组件定义明确的Props类型
interface ModuleTabsProps {
  // props定义
}

const ModuleTabs: React.FC<ModuleTabsProps> = (props) => {
  // 组件实现
}
```

### 5.2 性能优化

**1. 使用React.memo优化**
```tsx
const UserManagementTabs = React.memo(() => {
  // 组件实现
})

export default UserManagementTabs
```

**2. 菜单配置缓存**
```tsx
// ✅ 使用useMemo缓存配置
const menuItems = useMemo(() => [
  {
    key: '/user-management/user',
    icon: <UserOutlined />,
    label: '用户管理'
  }
  // ...
], [])
```

### 5.3 错误处理

**1. 路由守卫**
```tsx
// 在路由配置中添加错误边界
{
  path: 'user-management',
  element: <UserManagementTabs />,
  errorElement: <ErrorBoundary />,
  children: [
    // 子路由配置
  ]
}
```

**2. 默认路由处理**
```tsx
// 确保有默认的重定向路由
{
  index: true,
  element: <Navigate to="/user-management/user" replace />
}
```

---

## 6. 样式定制指导

### 6.1 标准样式配置

项目提供了标准的样式配置，通常无需自定义。如需定制，可以通过props调整：

```tsx
<VerticalTabsPageLayout 
  menuItems={menuItems}
  menuWidth={80}                    // 调整菜单宽度
  menuBackgroundColor="#f0f0f0"     // 调整背景色
  contentPadding="32px"             // 调整内容边距
  contentBorderRadius="8px"         // 调整圆角
/>
```

### 6.2 图标使用规范

**1. 图标选择原则**
- 使用Ant Design图标库中的语义化图标
- 保持同一模块内图标风格一致
- 图标含义要与功能相符

**2. 常用图标参考**
```tsx
import { 
  UserOutlined,      // 用户相关
  SafetyOutlined,    // 安全/角色相关
  KeyOutlined,       // 权限相关
  DatabaseOutlined,  // 数据相关
  SettingOutlined,   // 设置相关
  FileOutlined,      // 文件相关
  DashboardOutlined  // 仪表板
} from '@ant-design/icons'
```

---

## 7. 故障排查指南

### 7.1 常见问题

**问题1: 标签页切换无反应**
```tsx
// 检查key是否与路由路径匹配
const menuItems: VerticalIconMenuItem[] = [
  {
    key: '/user-management/user',  // ✅ 必须与路由路径完全一致
    icon: <UserOutlined />,
    label: '用户管理'
  }
]
```

**问题2: 页面内容不显示**
```tsx
// 检查是否正确配置了子路由和Outlet
{
  path: 'user-management',
  element: <UserManagementTabs />,  // ✅ 包含<Outlet />的容器组件
  children: [
    {
      path: 'user',
      element: <UserManagementUser />  // ✅ 实际内容组件
    }
  ]
}
```

**问题3: 默认标签页未激活**
```tsx
// 确保设置了正确的默认重定向
{
  index: true,
  element: <Navigate to="/user-management/user" replace />  // ✅ 重定向到第一个标签页
}
```

### 7.2 调试技巧

**1. 路由调试**
```tsx
// 在组件中添加路由信息打印
import { useLocation } from 'react-router-dom'

const UserManagementTabs: React.FC = () => {
  const location = useLocation()
  console.log('当前路由:', location.pathname)  // 调试当前路由
  
  // ...组件实现
}
```

**2. 菜单项调试**
```tsx
const menuItems: VerticalIconMenuItem[] = [
  {
    key: '/user-management/user',
    icon: <UserOutlined />,
    label: '用户管理'
  }
]

console.log('菜单配置:', menuItems)  // 调试菜单配置
```

---

## 8. 开发检查清单

### 8.1 代码实现检查
- [ ] 标签页容器组件创建完成
- [ ] 菜单项配置正确（key、icon、label）
- [ ] 子页面组件创建完成
- [ ] 路由配置正确（嵌套路由结构）
- [ ] 默认重定向设置
- [ ] TypeScript类型定义完整

### 8.2 功能测试检查
- [ ] 标签页切换正常
- [ ] 页面内容正确显示
- [ ] 刷新页面后标签页状态保持
- [ ] 面包屑导航正确
- [ ] URL路径与页面匹配

### 8.3 代码质量检查
- [ ] 组件命名规范
- [ ] 文件组织结构清晰
- [ ] 导入语句顺序正确
- [ ] 配置对象提取合理
- [ ] 错误处理完善

---

## 9. 扩展开发示例

### 9.1 数据资产管理标签页

```tsx
// src/views/AssetManagement/AssetManagementTabs.tsx
import React from 'react'
import { DatabaseOutlined, FileOutlined, BarChartOutlined } from '@ant-design/icons'
import VerticalTabsPageLayout from '../../components/layouts/VerticalTabsPageLayout'
import type { VerticalIconMenuItem } from '../../components/common/VerticalIconMenu'

const AssetManagementTabs: React.FC = () => {
  const menuItems: VerticalIconMenuItem[] = [
    {
      key: '/asset-management/database',
      icon: <DatabaseOutlined />,
      label: '数据库清单'
    },
    {
      key: '/asset-management/table',
      icon: <FileOutlined />,
      label: '数据表清单'
    },
    {
      key: '/asset-management/api',
      icon: <BarChartOutlined />,
      label: 'API清单'
    }
  ]

  return (
    <VerticalTabsPageLayout 
      menuItems={menuItems}
      menuWidth={60}
      menuBackgroundColor="#fafafa"
      contentPadding="24px"
      contentMargin="16px 16px 16px 0"
      contentBorderRadius="0 6px 6px 0"
      contentBoxShadow="2px 2px 8px rgba(0,0,0,0.06)"
    />
  )
}

export default AssetManagementTabs
```

### 9.2 对应的路由配置

```tsx
// router/index.tsx 中添加
{
  path: 'asset-management',
  element: <AssetManagementTabs />,
  children: [
    {
      index: true,
      element: <Navigate to="/asset-management/database" replace />
    },
    {
      path: 'database',
      element: <AssetManagementDatabase />,
      handle: { 
        title: '数据库清单', 
        breadcrumb: ['数据资产', '数据清单', '数据库清单'] 
      }
    },
    {
      path: 'table',
      element: <AssetManagementTable />,
      handle: { 
        title: '数据表清单', 
        breadcrumb: ['数据资产', '数据清单', '数据表清单'] 
      }
    },
    {
      path: 'api',
      element: <AssetManagementApi />,
      handle: { 
        title: 'API清单', 
        breadcrumb: ['数据资产', '数据清单', 'API清单'] 
      }
    }
  ]
}
```

---

## 10. 总结

基于 `UserManagementTabs.tsx` 的实际实现，本规范提供了完整的React标签页开发指导。核心要点：

1. **统一架构**: 使用 `VerticalTabsPageLayout` + `Outlet` 模式
2. **配置驱动**: 通过 `VerticalIconMenuItem[]` 配置标签页
3. **路由嵌套**: 利用React Router v6的嵌套路由特性
4. **类型安全**: 严格的TypeScript类型定义
5. **标准化**: 统一的文件命名和组织结构

遵循此规范可以确保项目中所有标签页功能的一致性、可维护性和开发效率。 