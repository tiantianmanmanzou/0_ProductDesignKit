# CI/CD 集成配置示例

本目录包含了将 Excel2Doc 开发规范检查工具集成到 CI/CD 流水线的配置示例。

## 📁 文件说明

### 1. GitHub Actions 配置
- **`github-actions-runtime-check.yml`** - GitHub Actions 工作流配置
  - 运行所有静态检查和运行时检查
  - 自动上传检查报告
  - 在发现严重问题时使构建失败

### 2. Pre-commit 配置
- **`pre-commit-config.yaml`** - Git 提交前自动检查配置
  - 代码格式化（Black, Prettier）
  - 代码质量检查（flake8, ESLint）
  - 自定义规范检查

### 3. Docker 检查环境
- **`docker-compose.check.yml`** - Docker Compose 配置
  - 独立的检查环境，包含数据库和后端服务
  - 自动运行所有一致性检查
  - 生成和收集检查报告

- **`nginx-reports.conf`** - Nginx 配置用于报告展示
  - 提供 Web 界面查看检查报告
  - 支持 JSON 报告文件浏览

## 🚀 快速开始

### 方式1：GitHub Actions

1. 复制配置文件到项目：
```bash
mkdir -p .github/workflows
cp 0_ProductDesignKit/review/ci-cd-examples/github-actions-runtime-check.yml .github/workflows/
```

2. 推送代码，自动触发检查：
```bash
git add .github/workflows/github-actions-runtime-check.yml
git commit -m "Add runtime consistency check workflow"
git push
```

3. 在 GitHub Actions 页面查看检查结果和报告。

### 方式2：Pre-commit 钩子

1. 安装 pre-commit：
```bash
pip install pre-commit
```

2. 复制配置文件：
```bash
cp 0_ProductDesignKit/review/ci-cd-examples/pre-commit-config.yaml .pre-commit-config.yaml
```

3. 安装 Git 钩子：
```bash
pre-commit install
```

4. 手动测试（可选）：
```bash
pre-commit run --all-files
```

现在每次 `git commit` 时都会自动运行检查。

### 方式3：Docker 检查环境

1. 启动检查环境：
```bash
docker-compose -f 0_ProductDesignKit/review/ci-cd-examples/docker-compose.check.yml up
```

2. 查看检查结果：
```bash
# 查看一致性检查日志
docker-compose -f 0_ProductDesignKit/review/ci-cd-examples/docker-compose.check.yml logs consistency-checker

# 启动报告服务器（可选）
docker-compose -f 0_ProductDesignKit/review/ci-cd-examples/docker-compose.check.yml --profile reports up report-collector
```

3. 访问报告界面：
   - 打开浏览器访问 http://localhost:8080
   - 查看生成的 JSON 报告文件

## 📊 检查报告说明

### 生成的报告文件

1. **`api_consistency_report.json`** - API 一致性检查报告
2. **`enum-usage-analysis-report.json`** - 枚举使用分析报告  
3. **`runtime-check-report.json`** - 运行时 API 一致性检查报告

### 报告结构示例

```json
{
  "summary": {
    "total_tests": 5,
    "passed_tests": 4,
    "failed_tests": 1,
    "success_rate": 80.0,
    "execution_time": "2025-01-07T10:30:00"
  },
  "test_results": [
    {
      "test_name": "project_creation_enum_consistency",
      "description": "项目创建返回正确的小写枚举值",
      "passed": false,
      "expected": "uploaded",
      "actual": "UPLOADED",
      "execution_time": 1.25,
      "timestamp": "2025-01-07T10:30:01.123Z"
    }
  ]
}
```

## 🔧 自定义配置

### 修改检查级别

在 GitHub Actions 配置中修改失败条件：

```yaml
# 严格模式：任何警告都导致失败
- name: Strict consistency check
  run: |
    python 0_ProductDesignKit/review/scripts/check_naming_convention.py
    if [ $? -ne 0 ]; then exit 1; fi

# 宽松模式：仅严重错误导致失败  
- name: Lenient consistency check
  run: |
    python 0_ProductDesignKit/review/scripts/check_naming_convention.py || true
```

### 跳过特定检查

在 pre-commit 配置中：

```yaml
# 跳过枚举检查
- repo: local
  hooks:
    - id: naming-convention-check
      args: [0_ProductDesignKit/review/scripts/check_naming_convention.py, --skip-enum-check]
```

### 添加通知

在 GitHub Actions 中添加 Slack/Teams 通知：

```yaml
- name: Notify on failure
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: failure
    text: "❌ 一致性检查失败，请查看详细报告"
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

## 🛠️ 故障排除

### 常见问题

1. **权限问题**
```bash
chmod +x 0_ProductDesignKit/review/scripts/*.py
```

2. **依赖缺失**
```bash
pip install -r backend/requirements.txt
pip install aiohttp  # 运行时检查需要
```

3. **数据库连接问题**
```bash
# 确保数据库服务启动
docker-compose -f docker-compose.check.yml up postgres-check -d
```

4. **网络访问问题**
```bash
# 检查服务健康状态
curl -f http://localhost:8001/health
```

### 调试模式

启用详细日志：
```bash
# 运行时检查详细模式
python 0_ProductDesignKit/review/scripts/runtime_api_consistency_check.py --verbose --report

# Docker 调试模式
docker-compose -f docker-compose.check.yml up --verbose
```

## 📝 最佳实践

1. **渐进集成**
   - 先在本地使用 pre-commit
   - 再集成到 CI/CD 流水线
   - 最后添加运行时检查

2. **报告管理**
   - 定期清理旧的报告文件
   - 设置报告文件保留期限
   - 建立问题跟踪机制

3. **团队协作**
   - 共享检查配置
   - 建立修复优先级
   - 定期 Review 检查结果

4. **持续改进**
   - 根据项目发展调整检查规则
   - 优化检查性能
   - 完善错误处理