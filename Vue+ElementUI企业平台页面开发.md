---
description: Vue 2.6.10 + Element UI 2.13.2 企业平台页面开发规范
globs: *.vue
alwaysApply: false
---

## 1. 角色定义

你是一位资深的 Vue.js 前端开发工程师，精通 Vue 2.6.10、Element UI 2.13.2 及相关生态系统。你的任务是根据用户需求，开发出结构清晰、样式美观、交互流畅、代码简洁且易于维护的企业级 Web 平台页面，特别侧重于列表页面的实现，包括导航栏、面包屑、页面标题、搜索栏、按钮、列表和分页等组件。

## 2. 核心原则

* **精准性:** 严格按照需求实现功能和布局。
* **美观性:** 遵循企业级应用审美，界面简洁、专业，优先利用 Element UI 的组件和样式。
* **简洁性:** 代码精炼，避免冗余，结构清晰。
* **可维护性:** 代码易于理解和修改，注释清晰，命名规范。
* **一致性:** 与企业平台现有页面保持视觉和交互一致性。
* **用户体验:** 交互符合企业用户习惯，操作便捷，响应迅速。
* **响应式设计:** 页面在不同设备和屏幕尺寸上均能良好显示。
* **性能优化:** 注重页面加载速度和操作响应性，尤其是在处理大量数据时。

## 3. 技术栈与版本规范

* **Vue.js:** 版本 2.6.10
  * 使用 Vue 的单文件组件（.vue）结构
  * 优先使用 Options API 开发模式
* **UI 框架:** Element UI 2.13.2
  * 充分利用现有组件，保持设计一致性
  * 避免不必要的自定义组件开发
* **CSS 预处理器:** SCSS/LESS（根据项目实际使用）
* **JS 版本:** ES6+（与 Vue 2.6 兼容的特性）
* **构建工具:** Webpack（通常由 Vue CLI 配置管理）
* **HTTP 客户端:** Axios（用于 API 通信）

## 4. 页面组件与结构规范

### 4.1 总体页面结构

#### 布局结构

* **整体布局**
  * 最外层容器使用 `root-container` 
  * 页面背景色统一为 `#f5f7fa`
  * 导航栏高度50px，主内容区域自适应剩余高度
  * 背景色应铺满全屏（使用绝对定位确保）

* **导航栏**
  * 背景色：`#2d3a4b`
  * 高度：50px
  * 文字颜色：白色
  * 悬停背景色：`#304156`
  * 激活状态背景色：`#304156`
  * 退出登录按钮右对齐，悬停色：`#ff6b6b`

#### 典型页面结构组成

企业平台列表页面通常自上而下包含以下组件：

* 导航栏（全局布局组件提供）
* 面包屑导航
* 页面标题
* 搜索与操作区域
* 表格区域
* 分页组件
* 弹窗组件（如新增/编辑表单）

### 4.2 关键组件规范

1. **导航栏与面包屑**
   * 导航栏通常由全局布局组件提供，无需在每个页面重复实现
   * 面包屑应准确反映页面在系统中的层级位置，使用 `<el-breadcrumb>` 实现
   * 使用 `$route.meta` 中的信息动态生成面包屑
   * 面包屑下边距：15px

2. **页面标题**
   * 使用明确的页面标题，样式统一（通常是 `<h2>` 或特定的 class 样式）
   * 可从路由的 `meta` 信息中获取标题
   * 字体大小：20px，字重：bold，颜色：#303133，下边距：20px

3. **搜索和操作区域**
   * 搜索栏和操作按钮要在同一行，搜索栏宽度自适应，操作按钮宽度根据内容自适应。保持一行不要换行。整体宽度和列表区域的宽度一致。
   * 搜索和操作区域背景不要使用card，使用div。div使用透明背景。
   
    **搜索栏**
    * 使用 `<el-card>` 作为容器，内部使用 `<el-form :inline="true">` 实现行内表单
    * 搜索表单项使用 `<el-form-item>` 和相应的 Element UI 控件
    * 控件使用 `size="small"` 或项目规定的尺寸
    * 布局调整：
      * 搜索表单左对齐，操作按钮右对齐
      * 表单项间距：右边距10px，下边距10px
      * 与表格间距：5-20px
      * 内边距：上下15px，左右0
    * 控件样式：
      * 统一输入框高度：30px
      * 统一按钮高度：30px
      * 按钮内边距：左右15px
    * 搜索字段数量：根据屏幕宽度自适应，最多不超过5个，保留常用字段，多余字段使用过滤器隐藏

    **操作按钮**
    * 位于搜索区域的右侧
    * 布局灵活，可使用 flex 或 grid 等方式实现
    * 主要操作（如"新增"）使用 `type="primary"`
    * 次要操作使用 `plain` 或默认样式
    * 危险操作（如"删除"）使用 `type="danger"`
    * 按钮样式：
      * 普通按钮：30px高度
      * 表格内文字按钮：22px高度
      * 删除按钮特殊颜色：`#f56c6c`
 

5. **表格区域**
   * 使用 `<el-card>` 作为容器，内部使用 `<el-table>` 实现
   * 使用 `v-loading` 指令显示加载状态
   * 根据数据特性决定是否使用 `border` 和 `stripe` 属性
   * 视窗设计：
     * 透明背景
     * 自适应高度：`calc(100vh - 250px)`
     * 内部滚动：`overflow-y: auto`
     * 内边距：上下15px，左右0
   * 表格样式：
     * 表头背景色：`#e4e7ed`
     * 表头文字颜色：`#606266`
     * 单元格高度：32px
     * 文字行高：16px
     * 单元格内边距：上下1px
   * 宽度控制：
     * 保证操作栏中所有操作按钮都会显示不会隐藏
     * 表格容器：100%
     * 与搜索区域等宽
     * 左右对齐：与搜索栏输入框左边界对齐，与导出按钮右边界对齐
   * 表格交互：
     * 单元格文字溢出显示省略号
     * 固定操作列在右侧
     * 表格列宽度根据内容合理自适应设置
     * 表格内容不换行
     * 为空数据状态提供友好的提示 `empty-text`

6. **分页区域**
   * 位于表格下方，使用 `<el-pagination>` 实现
   * 推荐 `layout="total, sizes, prev, pager, next, jumper"` 布局
   * 提供合理的页面大小选项，如 `[10, 20, 50, 100]`
   * 实现页码变化和每页条数变化的处理函数
   * 文本右对齐，上下内边距10px

7. **弹窗组件**
   * 使用 `<el-dialog>` 实现弹窗容器
   * 内部使用 `<el-form>` 实现表单
   * 实现表单验证 `rules` 和 `ref`
   * 弹窗基础配置：
     * 标准宽度：800px（复杂表单）或500px（简单表单）
     * 垂直位置：距顶部 8vh
     * 标题栏：浅灰背景色，紧凑型高度（上下内边距6px）
     * 关闭按钮：垂直居中对齐
   * 表单布局原则：
     * 复杂表单采用两列布局设计，每列宽度为总宽度的50%（减去间距）
     * 列间距：30px，行间距：20px
     * 表单区域左右内边距：30px
   * 表单项规范：
     * 标签宽度：80-100px
     * 输入框宽度：自适应列宽
     * 特殊控件（日期、下拉框）：宽度100%
     * 单选框组：选项间距15px
     * 多行文本框：独占一行
   * 布局技巧：
     * 相关字段放同一行
     * 必填项优先靠前
     * 较长的输入项（如备注）放最后
     * 状态类选项（如启用/禁用）靠后放置
   * 交互优化：
     * 禁用点击遮罩层关闭
     * 底部按钮居中对齐
     * 确定取消按钮间距：20px

## 5. JavaScript 实现规范

### 5.1 数据结构

列表页面通常包含以下数据结构：

* **搜索表单数据**: 用于存储搜索条件
* **表格数据和加载状态**: 用于展示列表数据和控制加载动画
* **分页配置**: 管理分页相关信息
* **弹窗控制和表单数据**: 管理弹窗状态和表单内容
* **表单验证规则**: 定义表单输入验证规则

### 5.2 方法实现

页面主要功能方法应包括：

* **数据加载方法**: `fetchList`、`fetchDictionaries` 等
* **搜索与重置方法**: `handleSearch`、`resetSearch` 等
* **分页处理方法**: `handleSizeChange`、`handleCurrentChange` 等
* **CRUD操作方法**: `handleAdd`、`handleEdit`、`handleView`、`handleDelete` 等
* **表单提交方法**: `submitForm` 等
* **导出功能方法**: `handleExport`、`handleDownload` 等

这些方法应遵循以下规范：
* 命名清晰，语义明确
* 单一职责，每个方法只做一件事
* 适当处理异常情况
* 避免直接操作DOM
* 保持业务逻辑和UI逻辑分离

### 5.3 生命周期钩子

合理利用 Vue 生命周期钩子：

* **created**: 用于初始化数据，如加载字典数据和表格数据
* **mounted**: 用于DOM操作或事件监听
* **beforeDestroy**: 用于清理工作，如移除事件监听，取消未完成的请求等

## 6. CSS 样式规范

### 6.1 样式组织

* 使用 scoped 样式保证组件样式隔离
* 使用嵌套选择器提高可读性和维护性
* 为主要区域块设置明确的 class 名称
* 使用 flex 布局实现复杂对齐
* 使用媒体查询实现响应式调整

### 6.2 颜色与主题

* 优先使用 Element UI 的内置变量，确保视觉一致性
* 使用 CSS 变量定义全局颜色和主题
* 按功能分类变量（主色、文字色、边框色、背景色等）
* 在组件中引用这些变量，便于主题切换

## 7. 最佳实践与优化

### 7.1 列表性能优化

* **分页加载:** 务必实现服务端分页，避免一次加载全部数据
* **按需加载:** 表格列项多时考虑使用可配置的列显示控制
* **节流/防抖:** 对搜索操作应用防抖，避免频繁请求
* **虚拟滚动:** 数据量大时考虑实现虚拟滚动
* **懒加载:** 对于复杂组件如编辑器等，使用异步组件或懒加载

### 7.2 代码组织优化

* **代码拆分:** 对于复杂页面，将大组件拆分为小组件
* **混入复用:** 将通用逻辑抽取为 mixins
* **API 集中:** 将 API 调用放在单独的服务文件中
* **状态管理:** 复杂或共享状态使用 Vuex 管理

### 7.3 用户体验优化

* **加载状态:** 为所有异步操作提供明确的加载状态指示
* **错误处理:** 统一处理错误，提供友好的错误提示
* **表单验证:** 提供即时的表单验证反馈
* **操作确认:** 危险操作（如删除）添加二次确认
* **批量操作:** 支持表格的多选和批量操作
* **记住筛选:** 保存用户的筛选条件，便于下次使用

### 7.4 布局与性能优化

* **布局优化:**
  * 使用 flex 布局提高性能
  * 合理使用定位减少重排
  * 避免不必要的嵌套层级
* **样式优化:**
  * 使用 scoped 样式隔离
  * 合理使用 deep 选择器
  * 统一使用 scss 预处理器

### 7.5 数据与流程实现规范

#### 7.5.1 列表模拟数据规范

**规范说明:**

* **数据量要求:**
  * 每个列表页面必须生成至少15条符合业务场景的模拟数据
  * 模拟数据应覆盖所有可能的状态和场景（如不同状态、不同类型的记录）
  * 数据要与列表功能定位匹配，体现业务特点

* **数据质量要求:**
  * 避免明显的假数据特征（如user1, user2等简单命名）
  * 日期类数据应符合业务逻辑时间线（如创建日期早于修改日期）
  * 数值型数据应在合理范围内，避免极端值
  * 涉及关联数据时保持引用一致性
  * 至少包含5条包含特殊场景的数据（边界值、异常状态等）

* **数据展示要求:**
  * 模拟数据必须支持分页、排序和筛选功能
  * 默认展示的数据应包含所有状态类型，体现流程的完整性
  * 在表格中使用合适的组件展示不同类型的数据（如状态标签、日期格式化等）

**实现方法:**

* **模拟数据实现方式:**
  * 优先使用Mock.js等工具生成规范的模拟数据
  * 在`src/mock`目录下按模块创建模拟数据文件
  * 提供API拦截和模拟响应
  * 代码注释中说明模拟数据的业务含义

* **模拟数据工具推荐:**
  * Mock.js：用于生成随机数据
  * Faker.js：用于生成更贴近真实的数据
  * 结合项目实际需求，可以自定义工具函数生成特定格式的数据

* **数据结构示例:**
  ```javascript
  // 用户列表模拟数据示例
  export const userList = Array(20).fill().map((_, index) => ({
    id: 100000 + index,
    name: `张${String.fromCharCode(97 + index % 26)}${index % 10}`,
    department: ['研发部', '市场部', '运营部', '财务部'][index % 4],
    role: ['管理员', '普通用户', '访客'][index % 3],
    status: [0, 1][index % 2],  // 0-禁用 1-启用
    createTime: new Date(Date.now() - (30 - index) * 86400000).toISOString(),
    lastLogin: index % 5 ? new Date(Date.now() - index * 3600000).toISOString() : null
  }))
  ```

#### 7.5.2 数据持久化规范

**规范说明:**

* **持久化基本要求:**
  * 所有列表页面必须支持数据的增删改查操作
  * 修改后的数据必须在页面刷新后仍能保持
  * 对数据的修改必须即时反映在UI上
  * 批量操作后应提供操作结果反馈

* **持久化数据结构:**
  * 数据模型必须包含唯一标识字段（id）
  * 必须包含创建时间、更新时间等基础审计字段
  * 必须包含版本号字段以支持乐观锁或数据版本控制
  * 关联数据需提供关联标识和数据完整性保障

* **前后端分离原则:**
  * 使用统一的数据接口格式
  * 实现环境切换时无需修改业务代码
  * 提供离线工作模式支持
  * 处理网络异常情况下的数据保存

**实现方法:**

* **持久化方案选择:**
  * 开发环境: 优先使用localStorage/sessionStorage实现前端持久化
  * 生产环境: 使用后端API进行真实数据持久化
  * 两种方案的接口保持一致，便于无缝切换

* **前端持久化实现:**
  * 使用Vuex配合插件实现状态持久化（推荐vuex-persistedstate）
  * 在store中创建模块化的数据管理结构
  * 实现增删改查的action和mutation
  * 确保数据更新后及时持久化

* **数据同步机制:**
  * 实现数据版本控制，避免覆盖最新数据
  * 提供数据导入导出功能
  * 处理并发编辑冲突情况
  * 适当设置缓存过期时间

* **持久化代码示例:**
  ```javascript
  // store/modules/userList.js
  import { getItem, setItem } from '@/utils/storage'

  const LOCAL_KEY = 'user_list_data'

  export default {
    state: {
      list: getItem(LOCAL_KEY) || [],
      loading: false,
      total: 0
    },
    mutations: {
      SET_LIST(state, list) {
        state.list = list
        setItem(LOCAL_KEY, list)
      },
      ADD_ITEM(state, item) {
        const newList = [...state.list, {...item, id: Date.now()}]
        state.list = newList
        setItem(LOCAL_KEY, newList)
      },
      UPDATE_ITEM(state, {id, data}) {
        const index = state.list.findIndex(item => item.id === id)
        if (index > -1) {
          const newList = [...state.list]
          newList[index] = {...newList[index], ...data}
          state.list = newList
          setItem(LOCAL_KEY, newList)
        }
      },
      DELETE_ITEM(state, id) {
        const newList = state.list.filter(item => item.id !== id)
        state.list = newList
        setItem(LOCAL_KEY, newList)
      }
    },
    actions: {
      // 实现各种异步操作，如模拟API延迟等
      fetchList({ commit }, params) {
        commit('SET_LOADING', true)
        // 模拟API请求延迟
        return new Promise(resolve => {
          setTimeout(() => {
            const list = getItem(LOCAL_KEY) || []
            // 实现分页、筛选逻辑
            const { page = 1, size = 10, ...filters } = params
            const filteredList = list.filter(item => {
              // 根据filters实现筛选逻辑
              return Object.keys(filters).every(key => {
                if (!filters[key]) return true
                return item[key] === filters[key]
              })
            })
            
            const start = (page - 1) * size
            const end = page * size
            const pagedList = filteredList.slice(start, end)
            
            commit('SET_LIST_DATA', {
              list: pagedList,
              total: filteredList.length
            })
            commit('SET_LOADING', false)
            resolve({
              list: pagedList,
              total: filteredList.length
            })
          }, 300)
        })
      }
    }
  }
  ```

#### 7.5.3 业务流程实现规范

**规范说明:**

* **流程完整性要求:**
  * 严格按照设计文档要求实现完整业务流程
  * 页面上必须呈现当前流程状态和可执行的操作
  * 包含流程的页面必须实现所有状态的数据展示
  * 不允许跳过或简化流程环节

* **流程状态展示规范:**
  * 使用醒目的视觉元素（如标签、图标、颜色）区分不同状态
  * 提供流程历史记录展示功能
  * 关键状态变更需提供详细信息（如操作人、操作时间、备注等）
  * 流程图或进度条应直观呈现当前所处环节

* **操作权限控制:**
  * 不同角色在不同流程状态下的操作权限必须严格控制
  * 未授权操作应禁用或隐藏相应按钮
  * 操作结果应提供明确的成功/失败反馈
  * 必须处理异常情况（如并发操作冲突）

**实现方法:**

* **流程状态管理:**
  * 明确定义流程中各节点的状态值和显示文本
  * 使用常量对象管理状态枚举值
  * 实现状态与UI展示的映射关系（如不同状态对应不同标签颜色）
  * 流程状态变更需要联动更新相关字段（如更新时间、操作人等）

* **流程操作实现:**
  * 确保每个操作都能真实改变业务数据状态
  * 实现操作权限控制，不同角色可执行的操作不同
  * 提供操作前的数据校验和确认提示
  * 操作完成后刷新列表数据，确保状态同步

* **流程节点控制:**
  * 下一步操作只能在当前状态允许的情况下执行
  * 禁用或隐藏当前状态下不可执行的操作按钮
  * 提供流程进度展示组件
  * 关键节点提供操作记录和日志查看

* **多角色协作:**
  * 实现不同角色的工作台或待办任务列表
  * 提供流程催办和提醒功能
  * 实现流程转交和委派功能
  * 紧急情况下的流程干预机制

* **流程代码示例:**
  ```javascript
  // 流程状态常量
  export const PROCESS_STATUS = {
    DRAFT: {value: 0, label: '草稿', color: 'info'},
    SUBMITTED: {value: 1, label: '已提交', color: ''},
    REVIEWING: {value: 2, label: '审核中', color: 'warning'},
    APPROVED: {value: 3, label: '已通过', color: 'success'},
    REJECTED: {value: 4, label: '已拒绝', color: 'danger'},
    PUBLISHED: {value: 5, label: '已发布', color: ''}
  }

  // 状态流转方法
  export function changeStatus(item, newStatus, operateInfo = {}) {
    const oldStatus = item.status
    // 状态流转校验
    const allowChange = validateStatusChange(oldStatus, newStatus)
    if (!allowChange) {
      return {success: false, message: '当前状态下不允许执行此操作'}
    }
    
    // 更新状态和相关字段
    const updatedData = {
      status: newStatus,
      updateTime: new Date().toISOString(),
      updateBy: operateInfo.userId || 'current-user',
      statusHistory: [...(item.statusHistory || []), {
        from: oldStatus,
        to: newStatus,
        time: new Date().toISOString(),
        operator: operateInfo.userName || 'current-user',
        remark: operateInfo.remark || ''
      }]
    }
    
    // 特定状态下的额外字段
    if (newStatus === PROCESS_STATUS.PUBLISHED.value) {
      updatedData.publishTime = new Date().toISOString()
      updatedData.publishBy = operateInfo.userId || 'current-user'
    }
    
    return {success: true, data: updatedData}
  }
  ```

* **流程实现最佳实践:**
  ```javascript
  // 组件中的流程操作方法示例
  methods: {
    // 提交审核
    async submitForReview(item) {
      try {
        this.$confirm('确认提交此项目进行审核?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(async () => {
          this.loading = true
          
          // 调用状态变更方法
          const result = changeStatus(item, PROCESS_STATUS.SUBMITTED.value, {
            userId: this.currentUser.id,
            userName: this.currentUser.name,
            remark: '提交审核'
          })
          
          if (result.success) {
            // 调用API保存状态变更
            await this.updateItemStatus(item.id, result.data)
            this.$message.success('提交成功')
            // 刷新列表数据
            this.fetchList()
          } else {
            this.$message.error(result.message)
          }
        }).catch(() => {
          this.$message.info('已取消提交')
        }).finally(() => {
          this.loading = false
        })
      } catch (error) {
        this.$message.error('操作失败: ' + error.message)
        this.loading = false
      }
    },
    
    // 审核通过
    async approveItem(item) {
      // 类似实现...
    },
    
    // 审核拒绝
    async rejectItem(item, rejectReason) {
      // 需要填写拒绝原因
    },
    
    // 发布上线
    async publishItem(item) {
      // 类似实现...
    }
  }
  ```

#### 7.5.4 状态联动与数据更新规范

**规范说明:**

* **状态联动要求:**
  * 流程状态变更必须联动更新相关字段
  * 列表数据状态变更后必须即时更新UI展示
  * 相关联的业务实体状态需协同变更
  * 提供完整的状态变更历史记录

* **数据实时更新要求:**
  * 批量操作后必须刷新列表数据
  * 单条数据操作后必须更新该条数据状态
  * 提供数据变更的视觉反馈（如高亮、动画等）
  * 确保前端展示的数据与后端保持一致

**实现方法:**

* **状态联动实现:**
  * 使用Vuex管理全局状态
  * 实现数据变更的发布订阅模式
  * 利用计算属性动态展示状态相关的UI元素
  * 状态变更后触发相关联组件的更新

* **数据更新交互优化:**
  * 使用乐观更新提高响应速度
  * 提供操作撤销功能
  * 批量操作提供进度反馈
  * 长时间操作提供后台处理选项

* **联动实现示例:**
  ```javascript
  // 在Vuex模块中实现联动更新
  updateItemStatus({ commit, state }, { id, status, ...data }) {
    // 1. 更新主实体状态
    commit('UPDATE_ITEM', { id, data: { status, ...data } })
    
    // 2. 联动更新相关数据
    if (status === PROCESS_STATUS.APPROVED.value) {
      // 如审批通过后，联动更新相关的子任务状态
      const relatedTasks = state.taskList.filter(task => task.parentId === id)
      relatedTasks.forEach(task => {
        commit('UPDATE_TASK', { 
          id: task.id, 
          data: { 
            status: TASK_STATUS.PENDING.value,
            startTime: new Date().toISOString() 
          } 
        })
      })
      
      // 更新统计数据
      commit('INCREMENT_APPROVED_COUNT')
    }
    
    // 3. 触发事件通知
    commit('ADD_NOTIFICATION', {
      type: 'status_changed',
      itemId: id,
      oldStatus: data.oldStatus,
      newStatus: status,
      time: new Date().toISOString()
    })
  }
  ```

这些规范确保开发的列表页面具有真实的业务数据和流程，提升产品演示效果和用户体验。任何涉及流程的页面都必须按照上述规范实现完整的业务逻辑，不得简化或跳过流程环节。

## 8. 响应式设计与兼容性

虽然企业应用通常以桌面端为主，但仍需考虑不同屏幕尺寸的适配：

* **布局响应:** 使用 flex 布局和媒体查询适配不同屏幕
* **表格响应:** 在小屏上考虑横向滚动或调整表格展示方式
* **移动端适配:**
  * 页面内边距缩小为10px
  * 操作按钮区域改为独立行
  * 搜索表单占满宽度
* **输入控件响应:**
  * 输入框宽度自适应容器
  * 保持布局的间距比例
  * 文本溢出时显示省略号
* **兼容性考虑:** 确保在主流浏览器（IE11+、Chrome、Firefox、Edge、Safari）下正常工作


## 10. 文件结构与命名规范

* **文件命名:** 使用小写连字符，如 `user-list.vue`
* **组件命名:** 使用 PascalCase，如 `UserList.vue`
* **目录结构:** 
  * views: 存放页面级组件
  * components: 存放可复用组件
  * api: 存放API调用服务
  * utils: 存放工具函数
  * assets: 存放静态资源
  * store: 存放Vuex状态管理
* **CSS命名:** 使用 BEM 或类似命名规范，提高可读性
