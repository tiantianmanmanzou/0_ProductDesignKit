<template>
  <div class="root-container">
    <!-- 顶部导航栏 -->
    <div class="nav-header">
      <div class="nav-menu">
        <router-link to="/" class="nav-item">首页</router-link>
        <router-link to="/data-publish" class="nav-item">数据发布</router-link>
        <router-link to="/data-subscribe" class="nav-item">数据订阅</router-link>
        <router-link to="/data-consume" class="nav-item">数据消费</router-link>
        <router-link to="/data-analysis" class="nav-item">数据分析</router-link>
        <router-link to="/data-manage" class="nav-item">数据管理</router-link>
        <router-link to="/system-manage" class="nav-item">系统管理</router-link>
        <router-link to="/help" class="nav-item">帮助文档</router-link>
        <a href="javascript:;" class="nav-item logout" @click="handleLogout">退出登录</a>
      </div>
    </div>

    <div class="page-container">
      <!-- 面包屑导航 -->
      <el-breadcrumb class="breadcrumb" separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>用户管理</el-breadcrumb-item>
        <el-breadcrumb-item>用户列表</el-breadcrumb-item>
      </el-breadcrumb>
      
      <!-- 页面标题 -->
      <div class="page-title">用户列表</div>
      
      <!-- 搜索与操作区域 -->
      <div class="search-area">
        <el-form :inline="true" :model="searchForm" class="search-form" ref="searchForm">
          <el-form-item label="关键词">
            <el-input v-model="searchForm.keyword" placeholder="请输入用户名/手机号" clearable></el-input>
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
              <el-option label="全部" value=""></el-option>
              <el-option label="启用" value="1"></el-option>
              <el-option label="禁用" value="0"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch" :loading="loading">查询</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
        
        <!-- 操作按钮区 -->
        <div class="operation-buttons">
          <el-button type="primary" @click="handleAdd" icon="el-icon-plus">新增用户</el-button>
          <el-button type="primary" plain @click="handleExport" :loading="downloadLoading" icon="el-icon-download">导出</el-button>
        </div>
      </div>
      
      <!-- 表格区域 -->
      <div class="table-container">
        <div class="table-viewport">
          <el-table
            :data="tableData"
            border
            v-loading="loading"
            stripe
            style="width: 100%"
            :cell-style="{ 'white-space': 'nowrap' }"
            :header-cell-style="{ backgroundColor: '#e4e7ed', color: '#606266', 'white-space': 'nowrap' }">
            <el-table-column type="selection" width="45"></el-table-column>
            <el-table-column prop="id" label="ID" min-width="60" show-overflow-tooltip></el-table-column>
            <el-table-column prop="username" label="用户名" min-width="90" show-overflow-tooltip></el-table-column>
            <el-table-column prop="phone" label="手机号" min-width="110" show-overflow-tooltip></el-table-column>
            <el-table-column prop="email" label="邮箱" min-width="140" show-overflow-tooltip></el-table-column>
            <el-table-column prop="department" label="部门" min-width="120" show-overflow-tooltip></el-table-column>
            <el-table-column prop="position" label="职位" min-width="100" show-overflow-tooltip></el-table-column>
            <el-table-column prop="entryDate" label="入职日期" min-width="100" show-overflow-tooltip></el-table-column>
            <el-table-column prop="role" label="角色" min-width="90">
              <template slot-scope="scope">
                <el-tag :type="scope.row.role === 'admin' ? 'danger' : scope.row.role === 'user' ? 'primary' : 'info'">
                  {{ scope.row.role === 'admin' ? '管理员' : scope.row.role === 'user' ? '普通用户' : '访客' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" min-width="70">
              <template slot-scope="scope">
                <el-tag :type="scope.row.status === '1' ? 'success' : 'info'">
                  {{ scope.row.status === '1' ? '启用' : '禁用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="createTime" label="创建时间" min-width="140" show-overflow-tooltip></el-table-column>
            <el-table-column label="操作" min-width="160" fixed="right">
              <template slot-scope="scope">
                <el-button type="text" @click="handleView(scope.row)" icon="el-icon-view">查看</el-button>
                <el-button type="text" @click="handleEdit(scope.row)" icon="el-icon-edit">编辑</el-button>
                <el-button type="text" class="delete-btn" @click="handleDelete(scope.row)" icon="el-icon-delete">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          
          <!-- 分页组件 -->
          <div class="pagination-container">
            <el-pagination
              background
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              :current-page="pagination.currentPage"
              :page-sizes="[10, 20, 50, 100]"
              :page-size="pagination.pageSize"
              layout="total, sizes, prev, pager, next, jumper"
              :total="pagination.total">
            </el-pagination>
          </div>
        </div>
      </div>
      
      <!-- 新增/编辑弹窗 -->
      <el-dialog
        :title="dialogTitle"
        :visible.sync="dialogVisible"
        width="800px"
        :close-on-click-modal="false"
        custom-class="user-dialog"
        @close="handleDialogClose">
        <el-form :model="form" :rules="rules" ref="form" label-width="80px" v-loading="dialogLoading">
          <div class="form-row">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="form.username" placeholder="请输入用户名"></el-input>
            </el-form-item>
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="form.phone" placeholder="请输入手机号"></el-input>
            </el-form-item>
          </div>
          <div class="form-row">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="form.email" placeholder="请输入邮箱"></el-input>
            </el-form-item>
            <el-form-item label="部门" prop="department">
              <el-input v-model="form.department" placeholder="请输入所属部门"></el-input>
            </el-form-item>
          </div>
          <div class="form-row">
            <el-form-item label="职位" prop="position">
              <el-input v-model="form.position" placeholder="请输入职位"></el-input>
            </el-form-item>
            <el-form-item label="入职日期" prop="entryDate">
              <el-date-picker
                v-model="form.entryDate"
                type="date"
                placeholder="请选择入职日期"
                value-format="yyyy-MM-dd"
                style="width: 100%">
              </el-date-picker>
            </el-form-item>
          </div>
          <div class="form-row">
            <el-form-item label="角色" prop="role">
              <el-select v-model="form.role" placeholder="请选择角色" style="width: 100%">
                <el-option label="管理员" value="admin"></el-option>
                <el-option label="普通用户" value="user"></el-option>
                <el-option label="访客" value="guest"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="状态" prop="status">
              <el-radio-group v-model="form.status">
                <el-radio label="1">启用</el-radio>
                <el-radio label="0">禁用</el-radio>
              </el-radio-group>
            </el-form-item>
          </div>
          <el-form-item label="备注" prop="remark">
            <el-input
              type="textarea"
              v-model="form.remark"
              placeholder="请输入备注信息"
              :rows="3">
            </el-input>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="cancelForm">取 消</el-button>
          <el-button type="primary" @click="submitForm" :loading="dialogLoading">确 定</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
/**
 * 用户列表管理组件
 * @description 实现用户的增删改查、导出等功能
 */
export default {
  name: 'UserList',
  data() {
    // 自定义表单验证规则
    const validatePhone = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入手机号'))
      } else if (!/^1[3-9]\d{9}$/.test(value)) {
        callback(new Error('请输入正确的手机号'))
      } else {
        callback()
      }
    }

    return {
      // 搜索表单数据
      searchForm: {
        keyword: '',
        status: ''
      },
      
      // 表格数据和加载状态
      tableData: [],
      mockData: [
        {
          id: '1',
          username: '张三',
          phone: '13800138000',
          email: 'zhangsan@example.com',
          department: '研发部',
          position: '高级工程师',
          entryDate: '2023-01-15',
          role: 'admin',
          status: '1',
          createTime: '2024-04-01 10:00:00'
        },
        {
          id: '2',
          username: '李四',
          phone: '13800138001',
          email: 'lisi@example.com',
          department: '产品部',
          position: '产品经理',
          entryDate: '2023-02-20',
          role: 'user',
          status: '0',
          createTime: '2024-04-01 11:00:00'
        },
        {
          id: '3',
          username: '王五',
          phone: '13800138002',
          email: 'wangwu@example.com',
          department: '测试部',
          position: '测试工程师',
          entryDate: '2023-03-10',
          role: 'user',
          status: '1',
          createTime: '2024-04-01 12:00:00'
        },
        {
          id: '4',
          username: '赵六',
          phone: '13800138003',
          email: 'zhaoliu@example.com',
          department: '运维部',
          position: '运维工程师',
          entryDate: '2023-04-05',
          role: 'user',
          status: '1',
          createTime: '2024-04-01 13:00:00'
        },
        {
          id: '5',
          username: '钱七',
          phone: '13800138004',
          email: 'qianqi@example.com',
          department: '研发部',
          position: '前端工程师',
          entryDate: '2023-05-12',
          role: 'user',
          status: '0',
          createTime: '2024-04-01 14:00:00'
        },
        {
          id: '6',
          username: '孙八',
          phone: '13800138005',
          email: 'sunba@example.com',
          department: '研发部',
          position: '后端工程师',
          entryDate: '2023-06-18',
          role: 'admin',
          status: '1',
          createTime: '2024-04-01 15:00:00'
        },
        {
          id: '7',
          username: '周九',
          phone: '13800138006',
          email: 'zhoujiu@example.com',
          department: '产品部',
          position: '产品专员',
          entryDate: '2023-07-22',
          role: 'user',
          status: '1',
          createTime: '2024-04-01 16:00:00'
        },
        {
          id: '8',
          username: '吴十',
          phone: '13800138007',
          email: 'wushi@example.com',
          department: '测试部',
          position: '自动化测试',
          entryDate: '2023-08-30',
          role: 'user',
          status: '0',
          createTime: '2024-04-01 17:00:00'
        },
        {
          id: '9',
          username: '郑十一',
          phone: '13800138008',
          email: 'zheng11@example.com',
          department: '运维部',
          position: '系统工程师',
          entryDate: '2023-09-15',
          role: 'user',
          status: '1',
          createTime: '2024-04-02 09:00:00'
        },
        {
          id: '10',
          username: '王十二',
          phone: '13800138009',
          email: 'wang12@example.com',
          department: '研发部',
          position: '架构师',
          entryDate: '2023-10-20',
          role: 'admin',
          status: '1',
          createTime: '2024-04-02 10:00:00'
        },
        {
          id: '11',
          username: '李十三',
          phone: '13800138010',
          email: 'li13@example.com',
          department: '产品部',
          position: '高级产品经理',
          entryDate: '2023-11-25',
          role: 'user',
          status: '0',
          createTime: '2024-04-02 11:00:00'
        },
        {
          id: '12',
          username: '赵十四',
          phone: '13800138011',
          email: 'zhao14@example.com',
          department: '测试部',
          position: '测试主管',
          entryDate: '2023-12-30',
          role: 'admin',
          status: '1',
          createTime: '2024-04-02 12:00:00'
        },
        {
          id: '13',
          username: '张十五',
          phone: '13800138012',
          email: 'zhang15@example.com',
          department: '运维部',
          position: '运维主管',
          entryDate: '2024-01-05',
          role: 'admin',
          status: '1',
          createTime: '2024-04-02 13:00:00'
        },
        {
          id: '14',
          username: '刘十六',
          phone: '13800138013',
          email: 'liu16@example.com',
          department: '研发部',
          position: '技术总监',
          entryDate: '2024-02-10',
          role: 'admin',
          status: '0',
          createTime: '2024-04-02 14:00:00'
        },
        {
          id: '15',
          username: '陈十七',
          phone: '13800138014',
          email: 'chen17@example.com',
          department: '产品部',
          position: '产品总监',
          entryDate: '2024-03-15',
          role: 'admin',
          status: '1',
          createTime: '2024-04-02 15:00:00'
        }
      ],
      loading: false,
      downloadLoading: false,
      
      // 分页配置
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      
      // 弹窗控制和表单数据
      dialogVisible: false,
      dialogLoading: false,
      dialogType: 'add', // 'add' 或 'edit'
      form: this.getInitialFormData(),
      
      // 表单验证规则
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        phone: [
          { required: true, validator: validatePhone, trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ],
        department: [
          { required: true, message: '请输入所属部门', trigger: 'blur' }
        ],
        position: [
          { required: true, message: '请输入职位', trigger: 'blur' }
        ],
        entryDate: [
          { required: true, message: '请选择入职日期', trigger: 'change' }
        ],
        role: [
          { required: true, message: '请选择角色', trigger: 'change' }
        ],
        status: [
          { required: true, message: '请选择状态', trigger: 'change' }
        ]
      }
    }
  },
  
  computed: {
    dialogTitle() {
      return this.dialogType === 'add' ? '新增用户' : '编辑用户'
    }
  },
  
  created() {
    this.fetchList()
  },
  
  methods: {
    // 获取初始表单数据
    getInitialFormData() {
      return {
        id: '',
        username: '',
        phone: '',
        email: '',
        department: '',
        position: '',
        entryDate: '',
        role: 'user',
        remark: '',
        status: '1'
      }
    },

    /**
     * 获取用户列表数据
     * @description 根据搜索条件和分页信息获取用户列表
     */
    fetchList() {
      this.loading = true
      // 构建请求参数
      const params = {
        page: this.pagination.currentPage,
        pageSize: this.pagination.pageSize,
        ...this.searchForm
      }
      
      // 模拟API调用
      setTimeout(() => {
        try {
          // 模拟搜索和分页逻辑
          let filteredData = [...this.mockData]
          
          // 关键词搜索
          if (params.keyword) {
            const keyword = params.keyword.toLowerCase()
            filteredData = filteredData.filter(item => 
              item.username.toLowerCase().includes(keyword) ||
              item.phone.includes(keyword)
            )
          }
          
          // 状态筛选
          if (params.status !== '') {
            filteredData = filteredData.filter(item => item.status === params.status)
          }
          
          // 计算总数
          this.pagination.total = filteredData.length
          
          // 分页处理
          const start = (params.page - 1) * params.pageSize
          const end = start + params.pageSize
          this.tableData = filteredData.slice(start, end)
          
        } catch (error) {
          this.$message.error('获取用户列表失败：' + error.message)
        } finally {
          this.loading = false
        }
      }, 500)
    },
    
    /**
     * 搜索处理
     * @description 处理搜索表单提交，重置分页并刷新列表
     */
    handleSearch() {
      this.pagination.currentPage = 1
      this.fetchList()
    },
    
    /**
     * 重置搜索
     * @description 重置搜索表单并刷新列表
     */
    resetSearch() {
      this.$refs.searchForm.resetFields()
      this.handleSearch()
    },
    
    // 分页处理
    handleSizeChange(size) {
      this.pagination.pageSize = size
      this.fetchList()
    },
    
    handleCurrentChange(current) {
      this.pagination.currentPage = current
      this.fetchList()
    },
    
    /**
     * 新增用户
     * @description 打开新增用户弹窗并重置表单
     */
    handleAdd() {
      this.dialogType = 'add'
      this.form = this.getInitialFormData()
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.form && this.$refs.form.clearValidate()
      })
    },
    
    /**
     * 编辑用户
     * @description 打开编辑用户弹窗并填充表单数据
     * @param {Object} row 当前行数据
     */
    handleEdit(row) {
      this.dialogType = 'edit'
      this.form = JSON.parse(JSON.stringify(row))
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.form && this.$refs.form.clearValidate()
      })
    },
    
    /**
     * 查看用户
     * @description 查看用户详情
     * @param {Object} row 当前行数据
     */
    handleView(row) {
      this.$message.info('查看用户：' + row.username)
    },
    
    /**
     * 删除用户
     * @description 删除指定用户
     * @param {Object} row 当前行数据
     */
    handleDelete(row) {
      this.$confirm('确认删除该用户吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 这里应该调用删除API
        this.$message.success(`删除用户"${row.username}"成功`)
        this.fetchList()
      }).catch(() => {
        // 用户取消删除，不做处理
      })
    },
    
    /**
     * 取消表单
     * @description 关闭弹窗并重置表单
     */
    cancelForm() {
      this.dialogVisible = false
      this.$nextTick(() => {
        this.$refs.form && this.$refs.form.resetFields()
      })
    },

    /**
     * 提交表单
     * @description 提交新增或编辑表单
     */
    submitForm() {
      this.$refs.form.validate(valid => {
        if (!valid) return
        
        const isAdd = this.dialogType === 'add'
        this.dialogLoading = true
        
        // 这里应该调用新增或编辑API
        setTimeout(() => {
          try {
            this.$message.success(isAdd ? '添加成功' : '修改成功')
            this.dialogVisible = false
            this.fetchList()
          } catch (error) {
            this.$message.error((isAdd ? '添加' : '修改') + '失败：' + error.message)
          } finally {
            this.dialogLoading = false
          }
        }, 500)
      })
    },
    
    /**
     * 导出数据
     * @description 导出用户列表数据
     */
    handleExport() {
      this.$confirm('是否确认导出所有数据?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.downloadLoading = true
        try {
          // 这里应该调用导出API
          this.$message.success('导出成功')
        } catch (error) {
          this.$message.error('导出失败：' + error.message)
        } finally {
          this.downloadLoading = false
        }
      }).catch(() => {
        // 用户取消导出，不做处理
      })
    },

    // 添加退出登录方法
    handleLogout() {
      this.$confirm('确认退出登录?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message.success('退出登录成功')
        // 这里应该调用退出登录API，然后跳转到登录页
      }).catch(() => {
        // 用户取消退出，不做处理
      })
    },
  }
}
</script>

<style lang="scss" scoped>
// 添加全局样式
::v-deep {
  html, body {
    margin: 0;
    padding: 0;
    height: 100%;
    background-color: #f5f7fa;
  }
}

.root-container {
  min-height: 100vh;
  background-color: #f5f7fa;
  margin: 0;
  padding: 0;
  width: 100%;
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
}

.nav-header {
  height: 50px;
  background-color: #2d3a4b;
  color: #fff;
  
  .nav-menu {
    height: 100%;
    display: flex;
    align-items: center;
    padding: 0 20px;
    
    .nav-item {
      color: #fff;
      text-decoration: none;
      padding: 0 15px;
      font-size: 14px;
      height: 50px;
      line-height: 50px;
      transition: all 0.3s;
      
      &:hover {
        background-color: #304156;
      }
      
      &.router-link-active {
        background-color: #304156;
      }
      
      &.logout {
        margin-left: auto;
        cursor: pointer;
        
        &:hover {
          color: #ff6b6b;
        }
      }
    }
  }
}

.page-container {
  padding: 20px;
  min-height: calc(100vh - 50px);
  background-color: #f5f7fa;
  
  ::v-deep {
    // 统一设置输入框和按钮高度
    .el-input__inner {
      height: 30px;
      line-height: 30px;
    }
    
    .el-button {
      height: 30px;
      line-height: 28px;
      padding: 0 15px;
    }
    
    // 表格中的按钮保持原样
    .el-table .el-button--text {
      height: 22px;
      line-height: 22px;
      padding: 0 3px;
    }
  }

  .breadcrumb {
    margin-bottom: 15px;
  }
  
  .page-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 15px;
    color: #303133;
  }
  
  .search-area {
    position: relative;
    margin-bottom: 5px;
    padding: 15px 0;
    width: 100%;
    max-width: 100%;
    
    .search-form {
      display: flex;
      flex-wrap: wrap;
      margin-right: 150px;
      width: 100%;
      
      .el-form-item {
        margin-right: 10px;
        margin-bottom: 0;
      }
    }
    
    .operation-buttons {
      position: absolute;
      right: 0;
      top: 15px;
      
      .el-button {
        margin-left: 8px;
      }
    }
  }
  
  .table-container {
    margin-bottom: 20px;
    width: 100%;
    max-width: 100%;
    
    .table-viewport {
      background-color: transparent;
      border-radius: 4px;
      padding: 15px 0;
      height: calc(100vh - 250px);
      overflow-y: auto;
      width: 100%;
    }
    
    .el-table {
      margin-bottom: 20px;
      width: 100% !important;
      
      ::v-deep {
        .el-table__row {
          height: 32px;
        }
        
        .cell {
          line-height: 16px;
          padding-top: 1px;
          padding-bottom: 1px;
          white-space: nowrap;
        }
        
        .el-table__header {
          th {
            background-color: #eef1f6 !important;
            border-right: 1px solid #dfe6ec !important;
            border-bottom: 1px solid #dfe6ec !important;
            .cell {
              line-height: 20px;
              font-weight: bold;
            }
          }
          th:last-child {
            border-right: none !important;
          }
        }

        // 调整表格内部的tag样式
        .el-tag {
          height: 22px;
          line-height: 20px;
          padding: 0 8px;
        }

        // 调整操作按钮的样式
        .el-button--text {
          padding: 0 3px;
          height: 22px;
          line-height: 22px;
        }

        // 固定列样式
        .el-table__fixed-right {
          height: 100% !important;
          background-color: #fff;
          th {
            border-right: 1px solid #dfe6ec !important;
          }
        }
      }
      
      .delete-btn {
        color: #f56c6c;
      }
    }
    
    .pagination-container {
      padding: 15px 0 0;
      text-align: right;
    }
  }
}

@media screen and (max-width: 768px) {
  .page-container {
    padding: 10px;
    
    .search-area {
      .operation-buttons {
        position: static;
        margin-top: 10px;
        text-align: right;
      }
      
      .search-form {
        margin-right: 0;
      }
    }
  }
}

// 弹窗样式
::v-deep .user-dialog {
  .el-dialog {
    margin-top: 8vh !important;
  }

  .el-dialog__body {
    padding: 20px 30px 0 30px;

    .form-row {
      display: flex;
      margin: 0 -15px;
      justify-content: space-between;
      
      .el-form-item {
        width: calc(50% - 30px);
        margin: 0 15px 20px;
        flex: none;
        
        &:last-child {
          margin-bottom: 20px;
        }

        // 调整日期选择器和下拉框的宽度
        .el-date-editor.el-input,
        .el-select {
          width: 100%;
        }

        // 调整单选框组的间距
        .el-radio-group {
          .el-radio {
            margin-right: 15px;
            &:last-child {
              margin-right: 0;
            }
          }
        }
      }
    }

    .el-form-item__label {
      padding-right: 5px;
    }

    // 备注文本框样式
    .el-form-item--textarea {
      width: calc(100% - 30px);
      margin: 0 15px 20px;
    }
  }

  .el-dialog__footer {
    padding: 15px 30px 20px;
    text-align: center;
  }
}

// 修复表单验证样式
::v-deep .el-form-item {
  &.is-error {
    .el-input__inner {
      &:focus {
        border-color: #409eff;
      }
    }
  }
}
</style> 