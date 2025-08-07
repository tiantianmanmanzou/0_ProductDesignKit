# Excel2Doc 前后端统一开发规范

> **版本**: v1.1  
> **创建日期**: 2025-08-07  
> **最后更新**: 2025-08-07  
> **适用范围**: Excel2Doc项目前后端开发团队  
> **目的**: 解决命名不一致问题，建立统一的开发标准，完善数据库迁移规范


## 🎯 核心原则

### 1. 统一性原则
**所有对外接口(API)统一使用camelCase命名**
- ✅ `{ "projectId": "123", "createdAt": "2024-01-01" }`
- ❌ `{ "project_id": "123", "created_at": "2024-01-01" }`

### 2. 一致性原则
**同类型数据在不同层次保持命名一致**
- 数据库: `created_at` (snake_case)
- 后端API: `createdAt` (camelCase)  
- 前端类型: `createdAt` (camelCase)

### 3. 可读性原则
**命名应该清晰表达含义，避免缩写**
- ✅ `columnMappingConfig`
- ❌ `colMapCfg`

---

## 🎨 前端开发规范

### 1. 文件命名规范
- **组件文件**: PascalCase (`ProjectList.tsx`)
- **页面文件**: kebab-case (`extraction-config.tsx`)
- **工具函数**: camelCase (`dateUtils.ts`)

### 2. TypeScript类型定义

#### **接口命名 (PascalCase)**
```typescript
interface Project {
  id: string;
  name: string;
  description?: string;
  status: ProjectStatus;
  excelFile?: ExcelFile;        // camelCase ✓
  createdAt: string;            // camelCase ✓
  updatedAt: string;            // camelCase ✓
}
```

#### **枚举定义 (PascalCase + 小写值)**
```typescript
enum ProjectStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  ARCHIVED = 'archived',
  DELETED = 'deleted'
}
```

### 3. API调用规范

#### **服务方法命名 (camelCase)**
```typescript
export const projectService = {
  getProjects: (params?: ProjectQuery) => api.get('/projects', { params }),
  createProject: (data: ProjectCreateData) => api.post('/projects', data),
  updateProject: (id: string, data: ProjectUpdateData) => 
    api.put(`/projects/${id}`, data),
  deleteProject: (id: string) => api.delete(`/projects/${id}`)
};
```

### 4. 组件开发规范

#### **React组件结构**
```typescript
export const ProjectList: React.FC<ProjectListProps> = ({ 
  projects,
  onProjectSelect,
  isLoading 
}) => {
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  
  return (
    <div className="project-list">
      {/* 组件内容 */}
    </div>
  );
};

interface ProjectListProps {
  projects: Project[];
  onProjectSelect: (project: Project) => void;
  isLoading?: boolean;
  className?: string;
}
```

### 5. 状态管理规范

#### **Redux/Zustand模式**
```typescript
// Action命名
export const fetchProjects = createAsyncThunk('project/fetchProjects', ...);

// State定义
interface ProjectState {
  projects: Project[];
  currentProject: Project | null;
  isLoading: boolean;
  error: string | null;
}
```

---

## 🖥️ 后端开发规范

### 1. 文件命名规范
- **Python文件**: snake_case (`project_service.py`)
- **类名**: PascalCase (`ProjectService`)

### 2. 数据库模型规范

```python
class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    status = Column(Enum(ProjectStatusEnum), default=ProjectStatusEnum.ACTIVE)
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    
    excel_file = relationship("ExcelFile", back_populates="projects")
```

### 3. 数据库迁移规范

#### **命名规范**
- 格式：`YYYYMMDD_HHMMSS_description.py`  
- revision ID与文件名保持一致
- 描述使用snake_case

#### **内容要求**
- **详细文档注释**：包含说明、影响范围、回滚说明
- **完整函数**：upgrade()和downgrade()都必须实现
- **分步执行**：添加NOT NULL字段时先允许NULL，设默认值，再改为NOT NULL
- **逆序回滚**：downgrade按upgrade的相反顺序执行

#### **安全实践**
- 添加字段：nullable=True → 设默认值 → nullable=False
- 删除字段：生产环境分两步（代码停用→删除字段）
- 枚举更新：使用临时字段策略避免锁表
- 大表处理：分批执行，避免长时间锁定

#### **执行流程**
```bash
# 生产环境标准流程
pg_dump excel2doc > backup_$(date +%Y%m%d_%H%M%S).sql
alembic upgrade head --sql  # 预览
alembic upgrade head        # 执行
alembic current            # 验证
```

### 4. Pydantic Schema规范

#### **统一使用alias进行字段转换**
```python
class ProjectRead(BaseModel):
    id: str
    name: str
    created_at: datetime = Field(alias='createdAt')
    updated_at: datetime = Field(alias='updatedAt')
    excel_file: Optional['ExcelFileRead'] = Field(None, alias='excelFile')
    
    class Config:
        from_attributes = True
        populate_by_name = True  # 支持双向转换
```

### 5. 枚举定义规范

```python
class ProjectStatusEnum(str, Enum):
    ACTIVE = "active"       # 统一使用小写值
    INACTIVE = "inactive"  
    ARCHIVED = "archived"
    DELETED = "deleted"
```

### 6. API路由规范

#### **RESTful + kebab-case**
```python
# 资源操作
@router.get("/projects")
@router.post("/projects") 
@router.get("/projects/{project_id}")

# 复杂操作
@router.post("/projects/batch-delete")
@router.get("/projects/{project_id}/excel-preview")
```

### 7. 服务层规范

```python
class ProjectService:
    @staticmethod
    def get_projects(db: Session, page: int = 1, limit: int = 20) -> Tuple[List[Project], int]:
        """获取项目列表"""
        # 实现逻辑
        
    @staticmethod
    def create_project(db: Session, project_data: ProjectCreateRequest) -> Project:
        """创建新项目"""
        # 实现逻辑
```

---

## 🔗 API设计规范

### 1. 统一响应格式

#### **标准响应结构**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    // 具体数据，全部使用camelCase
  },
  "timestamp": "2024-01-07T10:30:00Z"
}
```

#### **列表响应格式**
```json
{
  "code": 200,
  "message": "success", 
  "data": {
    "items": [...],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100,
      "totalPages": 5
    }
  }
}
```

#### **错误响应格式**
```json
{
  "code": 400,
  "message": "Validation failed",
  "data": null,
  "errors": [
    {
      "field": "projectName",
      "message": "项目名称不能为空"
    }
  ]
}
```

### 2. 字段转换规则

- **后端到前端**: 使用Pydantic alias自动转换 (snake_case → camelCase)
- **前端到后端**: 使用populate_by_name支持双向转换

---

## 🛠️ 自动化检查工具

### 1. ESLint配置 (.eslintrc.js)
```javascript
module.exports = {
  extends: ['@typescript-eslint/recommended'],
  rules: {
    '@typescript-eslint/naming-convention': [
      'error',
      { 'selector': 'variableLike', 'format': ['camelCase'] },
      { 'selector': 'typeLike', 'format': ['PascalCase'] }
    ],
    'react/jsx-pascal-case': 'error'
  }
};
```

### 2. Python工具配置

#### **flake8配置 (.flake8)**
```ini
[flake8]
max-line-length = 120
exclude = .git, __pycache__, .venv, migrations
```

#### **black配置 (pyproject.toml)**
```toml
[tool.black]
line-length = 120
target-version = ['py39']
```

### 3. Pre-commit配置

```yaml
repos:
  - repo: local
    hooks:
      - id: eslint
        name: ESLint Check
        entry: cd frontend && npm run lint
        files: ^frontend/.*\.(ts|tsx)$
        
      - id: migration-check
        name: Migration Validation
        entry: python scripts/check_migration.py
        files: ^backend/alembic/versions/.*\.py$
```

---

## 📝 代码审查清单

### 前端审查要点
- [ ] 组件文件使用PascalCase (`ProjectList.tsx`)
- [ ] 页面文件使用kebab-case (`module-summary.tsx`)
- [ ] 接口字段使用camelCase
- [ ] 枚举值使用小写字符串
- [ ] API调用错误处理完整

### 后端审查要点
- [ ] 数据库字段使用snake_case
- [ ] 类名使用PascalCase
- [ ] Schema使用alias进行字段转换
- [ ] API路径使用kebab-case
- [ ] 枚举值使用小写字符串

### 数据库迁移审查要点
- [ ] 文件命名：`YYYYMMDD_HHMMSS_description.py`
- [ ] 包含详细文档注释
- [ ] upgrade和downgrade函数完整实现
- [ ] NOT NULL字段分步执行
- [ ] 开发环境测试通过

---

## 🔄 执行流程

### 1. 开发阶段
1. 参考规范确定命名方式
2. 使用IDE插件实时检查
3. 提交前运行pre-commit检查
4. 自测功能完整性

### 2. 代码审查
1. 使用审查清单逐项检查
2. 重点关注命名一致性
3. 验证API接口标准化
4. 确认错误处理完整性

### 3. 部署验证
1. 运行完整测试套件
2. 执行命名规范检查
3. 验证API文档一致性
4. 监控系统稳定性
