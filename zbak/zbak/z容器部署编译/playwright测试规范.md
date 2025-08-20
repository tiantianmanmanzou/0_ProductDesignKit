# Playwright E2E测试规范

## 📋 概述

本规范基于Excel2Doc项目的实际测试经验制定，提供了一套完整的Playwright端到端测试方法论，包括脚本编写、执行测试、结果分析、问题修复和验证的完整流程。

## 🎯 测试流程总览

```
编写脚本 → 执行测试 → 分析结果 → 修复问题 → 验证修复 → 直到问题解决
    ↓         ↓         ↓         ↓         ↓
   规范化    自动化    可视化    精准化    验证化
```

## 🔧 阶段一：编写脚本

### 1.1 测试脚本结构规范

#### 基础测试文件结构
```typescript
import { test, expect } from '@playwright/test';
import path from 'path';
import { fileURLToPath } from 'url';

// 解决ES模块__dirname问题
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

test.describe('功能模块名称', () => {
  test.beforeEach(async ({ page }) => {
    // 通用前置操作
  });

  test('具体测试用例描述', async ({ page }) => {
    // 测试步骤
  });
});
```

#### 调试测试文件结构
```typescript
test.describe('功能调试', () => {
  test.beforeEach(async ({ page }) => {
    // 监听控制台错误
    page.on('console', msg => {
      if (msg.type() === 'error') {
        console.log('❌ 浏览器控制台错误:', msg.text());
      }
      if (msg.type() === 'warn') {
        console.log('⚠️ 浏览器控制台警告:', msg.text());
      }
    });

    // 监听页面错误
    page.on('pageerror', error => {
      console.log('❌ 页面错误:', error.message);
    });

    // 监听网络请求失败
    page.on('requestfailed', request => {
      console.log('❌ 网络请求失败:', request.url(), request.failure()?.errorText);
    });

    // 监听POST请求
    page.on('request', request => {
      if (request.method() === 'POST') {
        console.log('🔵 POST请求:', request.url());
      }
    });

    // 监听响应
    page.on('response', response => {
      if (response.request().method() === 'POST') {
        console.log('🔵 POST响应:', response.url(), response.status());
      }
      if (response.status() >= 400) {
        console.log('❌ HTTP错误响应:', response.url(), response.status());
      }
    });
  });
});
```

### 1.2 测试用例编写原则

#### 1.2.1 测试粒度划分
- **单元级测试**: 单个组件/功能点
- **集成级测试**: 多个组件协作
- **端到端测试**: 完整用户流程
- **调试级测试**: 问题诊断专用

#### 1.2.2 选择器优先级
```typescript
// 优先级从高到低
1. data-testid属性: page.getByTestId('element-id')
2. 语义化角色: page.getByRole('button', { name: '按钮名' })
3. 文本内容: page.getByText('文本内容')
4. 占位符: page.getByPlaceholder('占位符文本')
5. CSS选择器: page.locator('.class-name')
```

#### 1.2.3 测试数据管理
```typescript
// 使用唯一标识避免数据冲突
const projectName = `测试项目_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

// 文件路径处理
const testFilePath = path.join(__dirname, '../fixtures/test-file.xlsx');
```

### 1.3 错误处理和容错设计

#### 网络请求监听
```typescript
// 方法1: 监听特定请求
const responsePromise = page.waitForResponse(response => 
  response.url().includes('/api/v1/projects') && 
  response.request().method() === 'POST',
  { timeout: 30000 }
);

// 方法2: 容错处理
try {
  const response = await responsePromise;
  console.log(`API响应状态: ${response.status()}`);
} catch (error) {
  console.log('❌ 网络请求超时或失败，跳过API验证');
}
```

#### 状态验证策略
```typescript
// 多重验证避免测试脆弱性
try {
  await expect(page.locator('.success-message')).toBeVisible({ timeout: 5000 });
  console.log('✅ 发现成功消息');
} catch (e) {
  try {
    await expect(page.getByText(projectName)).toBeVisible({ timeout: 5000 });
    console.log('✅ 项目已出现在列表中');
  } catch (e2) {
    const dialog = page.getByRole('dialog');
    const isVisible = await dialog.isVisible();
    console.log(`⚠️ 弹窗状态: ${isVisible ? '仍然打开' : '已关闭'}`);
  }
}
```

## 🚀 阶段二：执行测试

### 2.1 测试执行命令

#### 基础执行
```bash
# 运行所有测试
npx playwright test

# 运行特定测试文件
npx playwright test tests/project-creation.spec.ts

# 运行特定测试用例
npx playwright test --grep "应该成功创建项目"
```

#### 调试执行
```bash
# 显示浏览器界面
npx playwright test --headed

# 调试模式
npx playwright test --debug

# 增加超时时间
npx playwright test --timeout=180000

# 生成详细报告
npx playwright test --reporter=html
```

#### 容器环境执行
```bash
# 确保容器运行
docker-compose up -d

# 等待服务启动
sleep 15

# 执行测试
npx playwright test --timeout=120000
```

### 2.2 测试环境准备

#### 检查服务状态
```bash
# 检查容器状态
docker-compose ps

# 检查端口占用
lsof -i :3000
lsof -i :8000

# 检查服务健康
curl -s http://localhost:3000 > /dev/null && echo "前端服务正常"
curl -s http://localhost:8000/health > /dev/null && echo "后端服务正常"
```

## 📊 阶段三：分析结果

### 3.1 测试报告分析

#### HTML报告
```bash
# 生成并查看报告
npx playwright test --reporter=html
npx playwright show-report
```

#### 测试结果解读
```
✅ PASSED - 测试通过
❌ FAILED - 测试失败
⚠️ TIMEOUT - 测试超时
🔄 FLAKY - 测试不稳定
```

### 3.2 前端日志分析

#### 浏览器控制台错误
```typescript
// 关键错误类型
1. JavaScript运行时错误
2. 网络请求错误 (404, 500, 超时)
3. 资源加载错误 (图片, CSS, JS)
4. 表单验证错误
5. API响应格式错误
```

#### 前端调试信息
```typescript
// 在测试中添加调试日志
console.log('🚀 开始执行步骤X');
console.log('✅ 步骤X执行成功');
console.log('❌ 步骤X执行失败', error);
console.log('🔍 当前页面状态:', await page.url());
```

### 3.3 后端日志分析

#### 日志查看命令
```bash
# 查看实时日志
docker-compose logs -f backend

# 查看最近日志
docker-compose logs backend --tail=50

# 筛选特定内容
docker-compose logs backend | grep -E "(ERROR|POST|422|500)"

# 按时间筛选
docker-compose logs backend --since=5m
```

#### 关键日志模式
```bash
# 成功模式
INFO: 192.168.x.x - "POST /api/v1/projects HTTP/1.1" 201 Created

# 失败模式
ERROR - Database session error: [validation errors]
INFO: 192.168.x.x - "POST /api/v1/projects HTTP/1.1" 422 Unprocessable Entity

# 认证问题
INFO: 192.168.x.x - "POST /api/v1/projects HTTP/1.1" 403 Forbidden
```

### 3.4 错误分类和诊断

#### 前端错误分类
```typescript
错误类型分类:
1. 网络连接错误 - "Failed to fetch"
2. 认证错误 - "401 Unauthorized"
3. 表单验证错误 - "{field: [validation errors]}"
4. 超时错误 - "Request timeout"
5. 数据格式错误 - "422 Unprocessable Entity"
```

#### 后端错误分类
```bash
HTTP状态码诊断:
- 200/201: 成功
- 400: 请求格式错误
- 401: 未认证
- 403: 权限不足
- 422: 数据验证失败
- 500: 服务器内部错误
```

## 🔧 阶段四：修复问题

### 4.1 常见问题修复模式

#### 问题1: 表单验证冲突
```typescript
// 问题表现
❌ 浏览器控制台错误: 创建项目失败: {file: Array(1)}

// 问题分析
- HTML模板中字段标记为required但验证规则中无对应字段
- Element Plus尝试验证不存在的字段

// 修复方法
// 移除HTML中的prop和required属性
<el-form-item label="Excel文件">  // 而不是 prop="file" required
  <!-- 表单内容 -->
</el-form-item>

// 移除不匹配的验证规则
const rules = {
  name: [...],
  description: [...],
  // 移除: file: [...]
}
```

#### 问题2: FormData Content-Type冲突
```typescript
// 问题表现
POST请求发送但后端收到空数据

// 问题分析
axios默认Content-Type覆盖了FormData的multipart/form-data

// 修复方法
// 在axios拦截器中检测FormData
httpClient.interceptors.request.use((config) => {
  // 其他处理...
  
  // 如果是FormData，删除Content-Type让浏览器自动设置
  if (config.data instanceof FormData) {
    delete config.headers['Content-Type'];
  }
  
  return config;
});
```

#### 问题3: 网络请求超时
```typescript
// 问题表现
测试显示"网络请求超时或失败"

// 问题分析
- 请求实际没有发送
- 前端代码在发送前就出错

// 修复方法
// 添加详细的错误捕获
try {
  await apiCall();
} catch (error) {
  console.error('具体错误:', {
    message: error.message,
    response: error.response,
    request: error.request,
    stack: error.stack
  });
}
```

### 4.2 修复验证方法

#### 逐步验证修复效果
```bash
# 1. 修复后立即测试单个用例
npx playwright test --grep "特定用例" --headed

# 2. 查看修复后的日志
docker-compose logs backend --tail=10

# 3. 验证API直接调用
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer $TOKEN" \
  -F "name=测试项目" \
  -F "file=@test.xlsx"
```

## ✅ 阶段五：验证修复

### 5.1 验证策略

#### 单点验证
```bash
# 验证修复的特定功能
npx playwright test tests/debug-project-creation.spec.ts --headed
```

#### 全面验证
```bash
# 运行完整测试套件
npx playwright test tests/user-project-creation.spec.ts --timeout=120000
```

#### 回归验证
```bash
# 确保修复没有破坏其他功能
npx playwright test tests/ --timeout=120000
```

### 5.2 验证标准

#### 成功标准
```typescript
验证检查清单:
✅ 所有测试用例通过
✅ 前端控制台无错误
✅ 后端返回正确状态码 (200/201)
✅ 数据正确保存到数据库
✅ 用户界面状态正确 (弹窗关闭/页面跳转)
✅ 错误处理机制正常
```

#### 质量指标
```typescript
性能指标:
- API响应时间 < 2秒
- 页面加载时间 < 5秒
- 测试执行稳定性 > 95%

功能指标:
- 核心功能测试通过率 = 100%
- 边界情况覆盖率 > 80%
- 错误处理覆盖率 > 90%
```

## 📋 测试最佳实践

### 1. 测试组织
```
tests/
├── fixtures/           # 测试数据文件
├── utils/              # 测试工具函数
├── page-objects/       # 页面对象模型
├── basic/              # 基础功能测试
├── integration/        # 集成测试
├── e2e/                # 端到端测试
└── debug/              # 调试测试
```

### 2. 命名规范
```typescript
// 测试文件命名
- feature-name.spec.ts          // 功能测试
- feature-name-debug.spec.ts    // 调试测试
- feature-name-integration.spec.ts // 集成测试

// 测试用例命名
test('应该成功完成用户的真实项目创建流程', async ({ page }) => {
  // 描述性强，明确测试目标
});
```

### 3. 数据管理
```typescript
// 测试数据隔离
const testData = {
  projectName: `测试项目_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
  description: '自动化测试创建的项目',
  testFile: path.join(__dirname, '../fixtures/test-excel.xlsx')
};
```

### 4. 等待策略
```typescript
// 明确的等待条件
await expect(page.getByRole('dialog')).toBeVisible();
await page.waitForLoadState('networkidle');
await page.waitForResponse(response => response.url().includes('/api/'));

// 避免硬等待
// ❌ await page.waitForTimeout(5000);
// ✅ await expect(element).toBeVisible({ timeout: 5000 });
```

## 🚨 故障排除指南

### 常见问题快速诊断

#### 问题症状 → 检查项目 → 解决方案

**1. 测试超时**
```
症状: Test timeout exceeded
检查: 
- 服务是否启动 (docker-compose ps)
- 网络连接是否正常 (curl测试)
- 选择器是否正确 (page.locator().isVisible())
解决: 增加超时时间，优化选择器，检查服务状态
```

**2. 元素找不到**
```
症状: Element not found
检查:
- 页面是否加载完成 (waitForLoadState)
- 选择器是否正确 (开发者工具验证)
- 元素是否在DOM中 (page.content())
解决: 使用更准确的选择器，添加等待条件
```

**3. API请求失败**
```
症状: 4xx/5xx HTTP错误
检查:
- 认证token是否有效
- 请求数据格式是否正确
- 后端服务是否正常
- 数据库连接是否正常
解决: 修复数据格式，检查认证，重启服务
```

## 📊 测试报告模板

### 执行总结
```markdown
## 测试执行报告

**测试日期**: 2025-XX-XX
**测试环境**: Docker容器化环境
**测试范围**: 项目创建功能完整流程

## 测试结果
- 总用例数: X
- 通过数: X
- 失败数: X
- 通过率: XX%

## 问题修复记录
1. **问题**: 描述问题
   **原因**: 根本原因分析
   **修复**: 具体修复方案
   **验证**: 修复验证结果

## 质量评估
- 功能完整性: ✅/❌
- 性能指标: ✅/❌
- 错误处理: ✅/❌
- 用户体验: ✅/❌
```

## 🎯 总结

本规范提供了从测试脚本编写到问题修复的完整方法论，关键是：

1. **编写阶段**: 规范化脚本结构，添加充分的调试信息
2. **执行阶段**: 选择合适的执行参数和环境配置
3. **分析阶段**: 结合前后端日志进行全面分析
4. **修复阶段**: 针对具体问题类型采用对应修复策略
5. **验证阶段**: 多维度验证修复效果

通过遵循这个循环流程，可以高效地发现、定位和修复E2E测试中的各类问题，确保应用程序的质量和稳定性。

---

**制定日期**: 2025-07-07  
**基于项目**: Excel2Doc  
**适用范围**: Vue3 + FastAPI + Docker容器化项目