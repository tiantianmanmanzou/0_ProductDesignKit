# Excel2Doc 开发规范检查工具集

> 🎯 **统一命名规范，确保前后端一致性** 

## 📁 目录结构

```
  0_ProductDesignKit/review/
  ├── README.md                           # 完整的工具集文档
  ├── Excel2Doc前后端开发规范.md          # 开发规范
  ├── scripts/                           # 增强的检查脚本
  │   ├── check_naming_convention.py     # 命名规范检查（增强版）
  │   ├── check_api_consistency.py       # API一致性检查（增强版）
  │   ├── runtime_api_consistency_check.py # 运行时检查（新）
  │   └── enum_usage_analyzer.py         # 枚举分析器（新）
  └── ci-cd-examples/                    # CI/CD集成配置（新）
      ├── README.md
      ├── github-actions-runtime-check.yml
      ├── pre-commit-config.yaml
      ├── docker-compose.check.yml
      └── nginx-reports.conf
```

## 🚀 快速开始

### 1. 安装依赖

确保您已安装以下工具：

```bash
# Python 3.9+ 和必要的包
pip install pre-commit black flake8 isort mypy

# Node.js 18+ (如果需要前端检查)
npm install -g markdownlint-cli
```

### 2. 配置 Git 钩子

```bash
# 从项目根目录运行
cd /Users/zhangxy/GenAI/Excel2Doc

# 复制 pre-commit 配置到项目根目录
cp 0_ProductDesignKit/review.pre-commit-config.yaml .

# 安装 pre-commit 钩子
pre-commit install

# 测试配置是否正常
pre-commit run --all-files
```

### 3. 运行检查工具

#### 🚀 一键运行所有检查（推荐）

```bash
# 运行所有必需检查（推荐）
python 0_ProductDesignKit/review/scripts/run_all_checks.py

# 跳过需要特殊依赖的可选检查
python 0_ProductDesignKit/review/scripts/run_all_checks.py --skip-optional

# 详细检查并生成报告
python 0_ProductDesignKit/review/scripts/run_all_checks.py --verbose --report
```

#### 🔍 单独运行检查工具

```bash
# 从项目根目录运行各项检查
# 1. 命名规范检查（包含硬编码字符串检查）
python 0_ProductDesignKit/review/scripts/check_naming_convention.py

# 2. API一致性检查（包含枚举值检查）
python 0_ProductDesignKit/review/scripts/check_api_consistency.py

# 3. 枚举使用场景分析
python 0_ProductDesignKit/review/scripts/enum_usage_analyzer.py

# 4. 数据库数据验证检查（需要数据库连接）
python 0_ProductDesignKit/review/scripts/database_data_validator.py

# 5. 运行时API一致性检查（可选，需要aiohttp）
python 0_ProductDesignKit/review/scripts/runtime_api_consistency_check.py

# 6. 数据库迁移脚本分析
python 0_ProductDesignKit/review/scripts/migration_script_analyzer.py

# 显示详细信息和生成报告
python 0_ProductDesignKit/review/scripts/check_naming_convention.py --verbose
python 0_ProductDesignKit/review/scripts/check_api_consistency.py --report
python 0_ProductDesignKit/review/scripts/enum_usage_analyzer.py --verbose --report
python 0_ProductDesignKit/review/scripts/runtime_api_consistency_check.py --report
```

## 🔍 工具说明

### 1. 命名规范检查器 (`check_naming_convention.py`) - 增强版

**新增功能**:
- ✅ 检查前端TypeScript接口字段命名规范
- ✅ 检查后端Python类、方法、枚举命名规范
- ✅ 识别snake_case和camelCase混用问题
- ✅ 验证组件文件命名规范
- 🆕 **检查硬编码字符串是否应该使用枚举**
- 🆕 **识别应该使用枚举值的字符串字面量**
- 🆕 **提供枚举使用建议**

**使用示例**:
```bash
# 基本检查（包含新的硬编码检查）
python 0_ProductDesignKit/review/scripts/check_naming_convention.py

# 显示详细信息
python 0_ProductDesignKit/review/scripts/check_naming_convention.py --verbose
```

**输出示例**:
```
🔍 Excel2Doc 命名规范检查开始...

❌ 发现 12 个命名规范问题:
   🔴 错误: 5 个
   🟡 警告: 7 个

📁 frontend/src/types/project.ts:
  🔴 第12行: Interface "Project" field "created_at" should use camelCase: "createdAt"

📁 backend/app/models/project.py:
  🔴 第25行: Enum "ParseStatusEnum" value "UPLOADED" should be lowercase: "uploaded"

📁 backend/app/services/project_service.py:
  🟡 第135行: String "UPLOADED" should use enum: ParseStatusEnum.UPLOADED.value
  🟡 第142行: String "completed" should use enum: ParseStatusEnum.COMPLETED.value
```

### 2. API一致性检查器 (`check_api_consistency.py`) - 增强版

**新增功能**:
- ✅ 比较前端TypeScript类型与后端Pydantic Schema
- ✅ 检查API字段名前后端一致性
- ✅ 识别缺失的字段别名配置
- 🆕 **检查前后端枚举值一致性**
- 🆕 **识别应该使用枚举的硬编码字符串**
- 🆕 **自动匹配前后端对应的枚举定义**

**使用示例**:
```bash
# 基本检查（包含新的枚举检查）
python 0_ProductDesignKit/review/scripts/check_api_consistency.py

# 生成详细报告文件
python 0_ProductDesignKit/review/scripts/check_api_consistency.py --report

# 显示详细信息
python 0_ProductDesignKit/review/scripts/check_api_consistency.py --verbose
```

**输出示例**:
```
🔍 Excel2Doc API一致性检查开始...

❌ 发现 5 个API一致性问题:
   🔴 错误: 1 个
   🟡 警告: 3 个
   ℹ️  信息: 1 个

📂 Enum Value Mismatch (1 个):
   🔴 枚举值不匹配: 前端 ParseStatus vs 后端 ParseStatusEnum
      前端值: ['uploaded', 'parsing', 'completed', 'failed'] 
      后端值: ['UPLOADED', 'PARSING', 'COMPLETED', 'FAILED']

📂 Hardcoded Enum Candidate (2 个):
   🟡 可能应该使用枚举: "UPLOADED" (类型: parse_status)
      位置: backend/app/services/project_service.py:135

📊 解析统计:
   前端类型定义: 12 个
   后端Schema定义: 8 个
   前端枚举: 3 个
   后端枚举: 5 个
```

### 3. 枚举使用场景分析器 (`enum_usage_analyzer.py`) - 🆕 新工具

**功能**:
- 🆕 **分析所有枚举定义及其值**
- 🆕 **追踪枚举值在代码中的使用情况**
- 🆕 **检查硬编码字符串应该使用枚举的场景**
- 🆕 **验证前后端枚举使用一致性**
- 🆕 **生成枚举使用分析报告**

**使用示例**:
```bash
# 基本分析
python 0_ProductDesignKit/review/scripts/enum_usage_analyzer.py

# 详细分析
python 0_ProductDesignKit/review/scripts/enum_usage_analyzer.py --verbose

# 生成分析报告
python 0_ProductDesignKit/review/scripts/enum_usage_analyzer.py --report
```

**输出示例**:
```
🔍 开始项目枚举使用场景分析...

📂 分析后端Python枚举...
   找到 15 个Python文件
✅ 后端分析完成: 发现 5 个枚举定义

📂 分析前端TypeScript枚举...
   找到 8 个TypeScript文件  
✅ 前端分析完成: 发现 3 个枚举定义

🔍 查找硬编码枚举字符串...
⚠️ 发现 12 个可能的硬编码枚举字符串

🔄 检查前后端枚举一致性...
⚠️ 发现 2 个前后端一致性问题

📊 统计概览:
   枚举定义总数: 8
   前端枚举: 3
   后端枚举: 5
   硬编码字符串: 12
   一致性问题: 2
```

### 4. 数据库数据验证检查器 (`database_data_validator.py`) - 🆕 新工具

**功能**:
- 🆕 **连接数据库检查枚举字段的实际值**
- 🆕 **与代码定义的枚举值进行对比**
- 🆕 **识别数据不一致问题**
- 🆕 **生成数据修复建议和迁移脚本**
- 🆕 **检查前后端枚举定义一致性**

**使用示例**:
```bash
# 基本数据库验证
python 0_ProductDesignKit/review/scripts/database_data_validator.py

# 详细验证分析
python 0_ProductDesignKit/review/scripts/database_data_validator.py --verbose

# 生成验证报告和迁移脚本
python 0_ProductDesignKit/review/scripts/database_data_validator.py --report
```

**输出示例**:
```
🚀 Excel2Doc 数据库数据验证开始...

📂 解析后端Python枚举...
✅ 后端分析完成: 发现 9 个枚举定义

📂 解析前端TypeScript枚举...
✅ 前端分析完成: 发现 9 个枚举定义

🔍 检查数据库枚举值一致性...
  🔍 检查 projects.parse_status (对应枚举: ParseStatusEnum)
  ❌ projects.parse_status 发现不一致
     数据库值: ['UPLOADED', 'parsing', 'completed']
     代码定义: ['uploaded', 'parsing', 'completed', 'failed']
     无效值: ['UPLOADED']

📊 数据库数据验证检查报告
==================================================
❌ 无效枚举值问题 (1 个):
   🔴 projects.parse_status: 数据库中存在无效的枚举值: ['UPLOADED']
      无效值: ['UPLOADED']
      有效值: ['uploaded', 'parsing', 'completed', 'failed']

🔧 需要数据迁移 (1 个):
   🔄 projects.parse_status: 需要数据迁移以修复枚举值不一致
      建议映射: {'UPLOADED': 'uploaded'}

📝 生成数据库迁移脚本:
   文件路径: backend/alembic/versions/fix_enum_data_consistency_20250107_143052.py
   运行命令: cd backend && alembic upgrade head
```

### 5. 运行时API一致性检查器 (`runtime_api_consistency_check.py`) - 🆕 增强工具

**功能**:
- 🆕 **启动前后端服务进行实际测试**
- 🆕 **验证API调用的枚举值传递一致性**
- 🆕 **检查字段名转换的正确性**
- 🆕 **测试API响应格式标准化**
- 🆕 **验证错误处理一致性**
- 🆕 **支持无aiohttp依赖运行**（使用标准库）

**使用示例**:
```bash
# 运行实际API测试
python 0_ProductDesignKit/review/scripts/runtime_api_consistency_check.py

# 生成详细测试报告
python 0_ProductDesignKit/review/scripts/runtime_api_consistency_check.py --report
```

**输出示例**:
```
🚀 Excel2Doc 运行时API一致性检查开始...

📦 启动后端和前端服务...
⏳ 等待服务就绪...
✅ 服务已启动，开始执行测试...

📝 测试项目创建枚举值一致性...
  ❌ 枚举值不一致: 期望 'uploaded', 实际 'UPLOADED'

🔤 测试字段名一致性...
  ✅ 字段名格式一致性检查通过

📋 测试API响应格式一致性...
  ✅ 项目列表API 响应格式正确

⚠️ 测试错误处理一致性...
  ✅ 错误响应格式正确

📊 运行时API一致性检查报告
==================================================
📈 总体统计:
   总测试数: 5
   通过: 4 ✅
   失败: 1 ❌
   通过率: 80.0%

❌ 失败的测试:
   • project_creation_enum_consistency: 项目创建返回正确的小写枚举值
     期望: uploaded
     实际: UPLOADED
```

### 6. 数据库迁移脚本分析器 (`migration_script_analyzer.py`) - 🆕 新工具

**功能**:
- 🆕 **解析Alembic迁移脚本中的枚举相关操作**
- 🆕 **检查枚举值设置是否符合规范**
- 🆕 **识别迁移脚本中的数据不一致风险**
- 🆕 **验证迁移脚本与代码定义的一致性**
- 🆕 **生成迁移脚本改进建议**

**使用示例**:
```bash
# 基本迁移脚本分析
python 0_ProductDesignKit/review/scripts/migration_script_analyzer.py

# 详细分析
python 0_ProductDesignKit/review/scripts/migration_script_analyzer.py --verbose

# 生成分析报告
python 0_ProductDesignKit/review/scripts/migration_script_analyzer.py --report
```

**输出示例**:
```
🚀 Excel2Doc 数据库迁移脚本分析开始...

🔍 分析数据库迁移脚本...
✅ 找到 15 个迁移文件
  📄 分析: 23412f575bf3_add_module_extraction_to_extract_type_.py
  📄 分析: add_enum_constraints_to_project_models.py

📊 数据库迁移脚本分析报告
============================================================
📈 总体统计:
   迁移文件数: 15
   枚举操作数: 8
   数据操作数: 3
   发现问题数: 2

📋 枚举操作详情:
   CREATE_ENUM: 5 个
   ALTER_ENUM: 2 个
   USE_ENUM_COLUMN: 1 个

❌ 发现的问题:
   🔴 ERROR (1 个):
      • 枚举 parse_status_enum 包含大写值: ['UPLOADED', 'PARSING']
        建议: 将值改为小写: ['uploaded', 'parsing']

   🟡 WARNING (1 个):
      • 枚举 ParseStatusEnum 定义与代码不一致
        缺少值: ['failed']
        多余值: ['PENDING']

💡 修复建议:
## 枚举大小写规范修复
建议修改迁移脚本，将枚举值改为小写...
```

### 7. 集成检查器 (`run_all_checks.py`) - 🆕 新工具

**功能**:
- 🆕 **按顺序运行所有检查工具**
- 🆕 **收集所有检查结果并生成综合报告**
- 🆕 **提供修复建议优先级排序**
- 🆕 **自动处理依赖检查和可选工具**
- 🆕 **统一的接口和错误处理**

**使用示例**:
```bash
# 运行所有必需检查
python 0_ProductDesignKit/review/scripts/run_all_checks.py

# 跳过可选检查（需要特殊依赖）
python 0_ProductDesignKit/review/scripts/run_all_checks.py --skip-optional

# 详细检查并生成报告文件
python 0_ProductDesignKit/review/scripts/run_all_checks.py --verbose --report
```

**输出示例**:
```
🚀 Excel2Doc 完整检查开始...
⏰ 开始时间: 2025-01-07 14:30:52

🔍 运行 命名规范检查...
  ✅ 命名规范检查 完成
     发现问题: 5 个 (严重: 2, 警告: 3)

🔍 运行 API一致性检查...
  ✅ API一致性检查 完成
     发现问题: 1 个 (严重: 0, 警告: 1)

🔍 运行 枚举使用场景分析...
  ✅ 枚举使用场景分析 完成

🔍 运行 数据库迁移脚本分析...
  ✅ 数据库迁移脚本分析 完成
     发现问题: 3 个 (严重: 3, 警告: 0)

  ⚠️ 数据库数据验证 缺少依赖: psycopg2-binary
     这是可选检查，将跳过

================================================================================
📊 Excel2Doc 完整检查报告
================================================================================

⏰ 检查时间: 2025-01-07 14:31:15

📈 总体统计:
   总检查数: 6
   成功检查: 4 ✅
   失败检查: 0 ❌  
   跳过检查: 2 ⏭️
   
   总问题数: 9
   严重问题: 5 🔴
   警告问题: 4 🟡
   信息提示: 0 ℹ️

🔍 详细问题分析:

📋 命名规范检查:
   🔴 后端Python类、方法、枚举命名规范违规
   🟡 硬编码字符串应该使用枚举

📋 数据库迁移脚本分析:
   🔴 枚举 parse_status_enum 包含大写值: ['UPLOADED', 'PARSING']
   🔴 枚举 summary_status_enum 包含大写值: ['PENDING', 'COMPLETED']

💡 优先修复建议:

1. 🔴 严重问题优先处理:
   - 枚举值大小写不一致问题
   - 数据库中存在无效枚举值
   - API接口命名规范违规

⚠️ 发现 5 个严重问题需要立即修复。

📄 详细报告已保存到: complete_check_report_20250107_143115.json
```

### 8. Pre-commit 钩子配置

自动在每次Git提交前运行以下检查：

- ✅ 代码格式化 (Black, Prettier)
- ✅ 代码质量检查 (flake8, ESLint)  
- ✅ 命名规范验证
- ✅ API一致性检查
- ✅ TypeScript类型检查

## 📋 常见问题和解决方案

### 问题1: 前端接口使用snake_case字段

```typescript
❌ 错误
interface Project {
  created_at: string;  // snake_case
  updated_at: string;  // snake_case
}

✅ 正确
interface Project {
  createdAt: string;   // camelCase
  updatedAt: string;   // camelCase
}
```

### 问题2: 后端枚举值大小写不一致

```python
❌ 错误
class StatusEnum(str, Enum):
    ACTIVE = "ACTIVE"      # 大写
    PENDING = "pending"    # 混用
    
✅ 正确
class StatusEnum(str, Enum):
    ACTIVE = "active"      # 统一小写
    PENDING = "pending"    # 统一小写
```

### 问题3: 后端Schema缺少camelCase别名

```python
❌ 错误
class ProjectRead(BaseModel):
    created_at: datetime  # 缺少alias

✅ 正确
class ProjectRead(BaseModel):
    created_at: datetime = Field(alias='createdAt')  # 添加alias
    
    class Config:
        populate_by_name = True  # 支持双向转换
```

## 🎯 最佳实践

### 开发工作流

1. **开发前**: 阅读 `开发规范快速使用指南.md`
2. **开发中**: 使用IDE插件实时检查命名规范
3. **提交前**: 运行 `python 0_ProductDesignKit/reviewscripts/check_naming_convention.py`
4. **Code Review**: 重点检查命名一致性
5. **部署前**: 运行完整的验证脚本

### 团队协作

1. **新人入职**: 
   - 配置开发环境和Git钩子
   - 学习开发规范文档
   - 运行检查工具了解项目现状

2. **定期Review**:
   - 每周检查规范执行情况
   - 每月更新工具和规范
   - 每季度全面评估改进效果

### CI/CD 集成 - 🆕 完整解决方案

提供了完整的 CI/CD 集成配置，包括：

- 🆕 **GitHub Actions 工作流** - 完整的运行时检查流水线
- 🆕 **Pre-commit 钩子** - Git 提交前自动检查
- 🆕 **Docker 检查环境** - 独立的检查和报告环境

```bash
# 快速设置 GitHub Actions
cp 0_ProductDesignKit/review/ci-cd-examples/github-actions-runtime-check.yml .github/workflows/

# 快速设置 Pre-commit  
cp 0_ProductDesignKit/review/ci-cd-examples/pre-commit-config.yaml .pre-commit-config.yaml
pre-commit install

# 快速设置 Docker 检查环境
docker-compose -f 0_ProductDesignKit/review/ci-cd-examples/docker-compose.check.yml up
```

**详细配置说明请查看**: `0_ProductDesignKit/review/ci-cd-examples/README.md`

## 📊 规范执行监控

### 度量指标

| 指标 | 目标值 | 当前值 | 状态 |
|------|--------|--------|------|
| 命名规范违规数量 | < 5个/月 | - | 待测量 |
| API字段不匹配错误 | 0个/月 | - | 待测量 |
| 代码审查时间 | 减少30% | - | 待测量 |
| 新功能开发效率 | 提升20% | - | 待测量 |

### 持续改进

1. **数据收集**: 每周运行检查工具统计问题数量
2. **趋势分析**: 分析问题类型和减少趋势  
3. **工具优化**: 根据实际使用情况完善检查逻辑
4. **规范更新**: 根据项目发展调整规范要求

## 🔧 自定义配置

### 修改检查规则

编辑脚本中的配置变量：

```python
# check_naming_convention.py 中的配置
self.allowed_snake_case_fields = {
    'created_at', 'updated_at', 'excel_file',
    # 添加您的例外字段
    'your_custom_field'
}

self.allowed_uppercase_enum_values = {
    'UUID', 'URL', 'API',
    # 添加您的例外枚举值
    'YOUR_CONSTANT'
}
```

### 扩展检查功能

1. **添加新的检查规则**: 在相应的检查方法中添加逻辑
2. **支持新的文件类型**: 扩展文件解析方法
3. **增加检查项目**: 在检查主流程中添加新的验证步骤

## 📞 获取帮助

### 问题排查

1. **检查工具无法运行**:
   - 确认Python版本 >= 3.9
   - 检查依赖包是否完整安装
   - 验证文件路径是否正确

2. **检查结果异常**:
   - 使用 `--verbose` 参数查看详细信息
   - 检查文件编码是否为UTF-8
   - 验证正则表达式匹配是否正确

3. **Pre-commit钩子问题**:
   - 运行 `pre-commit install` 重新安装
   - 使用 `pre-commit run --all-files` 测试配置
   - 检查 `.pre-commit-config.yaml` 文件路径

### 联系支持

- 📧 **技术支持**: 项目开发团队
- 📋 **问题反馈**: 通过项目内部协作平台
- 📖 **文档问题**: 提交改进建议

---

**版本**: v1.0  
**创建日期**: 2025-01-07  
**维护团队**: Excel2Doc开发团队  
**最后更新**: 2025-01-07