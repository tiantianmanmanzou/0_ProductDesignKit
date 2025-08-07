# E2E功能测试规范

## 概述

本文档基于 `frontend/tests/e2e/column-mapping-edit.spec.ts` 测试文件的分析，提供了一套完整的E2E功能测试规范，用于指导后续类似功能的测试文件开发。

## 1. 测试架构设计

### 1.1 测试文件结构
```typescript
import { test, expect, Page } from '@playwright/test';

test.describe('功能模块名称测试', () => {
  // 测试常量定义
  // 测试用例实现
});
```

### 1.2 测试常量定义
```typescript
const TEST_PROJECT_ID = '17edf317-fd6b-4b38-8bfe-451423865232';
const TEST_SESSION_ID = `mapping_edit_test_${Date.now()}`;
```

**规范要求：**
- 使用唯一的测试会话ID，便于追踪和调试
- 预定义测试用的项目ID和配置ID
- 常量命名使用大写下划线格式

## 2. 测试监控机制

### 2.1 控制台日志监控
```typescript
let consoleMessages: string[] = [];

page.on('console', msg => {
  const message = `[${msg.type()}] ${msg.text()}`;
  consoleMessages.push(message);
  
  // 过滤重复的Excel数据日志
  if (message.includes('Cell[') || message.includes('Row ')) {
    return;
  }
  
  console.log(`🔍 Console: ${message}`);
});
```

**规范要求：**
- 记录所有控制台消息
- 过滤重复或无关的日志信息
- 使用表情符号增强日志可读性

### 2.2 网络请求监控
```typescript
let apiRequests: any[] = [];
let apiResponses: any[] = [];

page.on('request', request => {
  if (request.url().includes('/api/v1/data-processing/')) {
    const requestData = {
      url: request.url(),
      method: request.method(),
      headers: request.headers(),
      timestamp: new Date().toISOString()
    };
    
    if (request.method() === 'POST' || request.method() === 'PUT') {
      try {
        requestData.postData = request.postData();
      } catch (e) {
        requestData.postData = 'Failed to capture post data';
      }
    }
    
    apiRequests.push(requestData);
    console.log(`📤 API Request: ${request.method()} ${request.url()}`);
  }
});

page.on('response', response => {
  if (response.url().includes('/api/v1/data-processing/')) {
    const responseData = {
      url: response.url(),
      status: response.status(),
      headers: response.headers(),
      timestamp: new Date().toISOString()
    };
    
    apiResponses.push(responseData);
    console.log(`📥 API Response: ${response.status()} ${response.url()}`);
  }
});
```

**规范要求：**
- 监控关键API的请求和响应
- 记录请求方法、URL、状态码和时间戳
- 捕获POST/PUT请求的数据
- 处理异常情况避免测试中断

## 3. 测试步骤执行标准

### 3.1 步骤划分和日志输出
```typescript
console.log('\\n=== 步骤1: 导航到配置页面并进入编辑模式 ===');
console.log('\\n=== 步骤2: 验证进入编辑配置界面并完成基本配置 ===');
console.log('\\n=== 步骤3: 配置列映射关系 ===');
```

**规范要求：**
- 使用层次化的步骤编号（步骤1、步骤2.1、步骤2.2等）
- 每个主要步骤有明确的分隔线和描述
- 子步骤使用缩进和详细说明

### 3.2 页面导航和等待策略
```typescript
// 1. 导航到页面
await page.goto('http://localhost:3000/data-processing/extraction-config');
await page.waitForLoadState('networkidle');

// 2. 等待页面加载
await page.waitForTimeout(3000);

// 3. 等待特定元素出现
const configTable = page.locator('table tbody');
await configTable.waitFor({ timeout: 10000 });
```

**规范要求：**
- 使用 `networkidle` 确保页面完全加载
- 合理设置超时时间（一般操作3秒，重要操作10秒）
- 优先使用元素等待而非固定时间等待

### 3.3 元素定位策略
```typescript
// 多种选择器策略
const projectSelectors = [
  editConfigDialog.locator('select:has(option:has-text("项目"))'),
  editConfigDialog.locator('[data-radix-select-trigger]:has-text("项目")'),
  editConfigDialog.locator('button[role="combobox"]:has-text("项目")')
];

let projectSelector = null;
for (const selector of projectSelectors) {
  if (await selector.count() > 0 && await selector.first().isVisible()) {
    projectSelector = selector.first();
    break;
  }
}
```

**规范要求：**
- 提供多种备选的元素选择器
- 优先使用语义化的选择器
- 检查元素的可见性和可用性
- 处理动态加载的UI组件

## 4. 用户交互模拟

### 4.1 表单填写和选择
```typescript
// 输入框填写
const configNameInput = editConfigDialog.locator('input[placeholder*="配置名称"]');
if (hasConfigName) {
  const currentName = await configNameInput.inputValue();
  if (!currentName || currentName.trim() === '') {
    await configNameInput.fill(`测试配置_${Date.now()}`);
  }
}

// 下拉选择
await projectSelector.click();
await page.waitForTimeout(2000);
const projectOptions = page.locator('[role="option"]');
if (await projectOptions.count() > 0) {
  await projectOptions.first().click();
}
```

**规范要求：**
- 检查输入框的当前值，避免重复输入
- 下拉选择需要等待选项加载
- 使用时间戳确保测试数据唯一性

### 4.2 复杂交互处理
```typescript
// 动态列表操作（删除现有映射）
const deleteButtons = editConfigDialog.locator('button:has(svg[class*="lucide-x"])');
const deleteCount = await deleteButtons.count();

if (deleteCount > 0) {
  // 从后往前删除，避免索引变化问题
  for (let i = deleteCount - 1; i >= 0; i--) {
    const deleteBtn = deleteButtons.nth(i);
    if (await deleteBtn.isVisible() && await deleteBtn.isEnabled()) {
      await deleteBtn.click();
      await page.waitForTimeout(500);
    }
  }
}
```

**规范要求：**
- 动态列表操作要考虑索引变化
- 从后往前删除或重新获取元素列表
- 每次操作后适当等待UI更新

## 5. 数据验证方法

### 5.1 前端验证
```typescript
// 验证界面状态
const editConfigDialog = page.locator('[role="dialog"]:has-text("编辑数据映射配置")');
const isInEditMode = await editConfigDialog.isVisible();

if (!isInEditMode) {
  throw new Error('未成功进入编辑配置界面');
}

// 验证表单数据
const afterText = await selector.textContent();
console.log(`✓ 修改后状态: "${afterText}"`);
```

### 5.2 API数据验证
```typescript
// 监控API请求
const saveRequestPromise = page.waitForRequest(request => 
  request.url().includes('/api/v1/data-processing/mapping-configs') && 
  (request.method() === 'POST' || request.method() === 'PUT')
, { timeout: 10000 }).catch(() => null);

// 验证请求数据
const saveRequest = await saveRequestPromise;
if (saveRequest) {
  const requestData = JSON.parse(saveRequest.postData() || '{}');
  console.log(`📊 保存请求数据:`);
  console.log(`  - 配置名称: ${requestData.config_name}`);
  console.log(`  - 映射项数量: ${requestData.column_mappings?.length || 0}`);
}
```

### 5.3 数据库验证
```typescript
// 直接API验证数据保存
const verificationResult = await page.evaluate(async (configId) => {
  try {
    const response = await fetch(`http://localhost:8000/api/v1/data-processing/mapping-configs/${configId}`);
    
    if (!response.ok) {
      return { success: false, error: `HTTP ${response.status}` };
    }
    
    const data = await response.json();
    return { success: true, data: data };
  } catch (error) {
    return { success: false, error: error.message };
  }
}, configId);

// 验证关键数据
const validationChecks = [];
if (savedData.extract_type === 'l1_l3_mapping') {
  validationChecks.push('✅ 映射类型正确保存');
} else {
  validationChecks.push(`❌ 映射类型保存错误`);
}
```

**规范要求：**
- 三层验证：前端UI、API请求、数据库存储
- 验证关键业务数据的完整性和正确性
- 提供详细的验证日志输出

## 6. 错误处理策略

### 6.1 异常捕获
```typescript
try {
  await smartMatchButton.click({ force: true });
  console.log('✅ 已执行智能匹配');
} catch (clickError) {
  console.log('⚠️ 智能匹配按钮点击失败，继续手动配置:', clickError.message);
  // 继续执行而不中断测试
}
```

### 6.2 重试机制
```typescript
// 第一次尝试失败后的重试逻辑
if (retryCount > 0) {
  const firstRetryProject = retryOptions.first();
  await firstRetryProject.click();
  console.log(`✅ 重试成功，已选择项目`);
} else {
  console.log('⚠️ 重试后仍然没有项目选项，跳过项目选择');
  // 不抛出错误，让测试继续
}
```

### 6.3 兜底处理
```typescript
// 备选方案处理
if (!targetCard || await targetCard.count() === 0) {
  if (cardCount > 1) {
    const secondCard = mappingTypeCards.nth(1);
    await secondCard.click();
    console.log(`✅ 已选择备用映射类型`);
  }
}
```

**规范要求：**
- 对关键操作提供重试机制
- 非关键操作失败时继续执行
- 提供兜底的备选方案
- 详细记录异常信息和处理结果

## 7. 测试报告和分析

### 7.1 测试过程分析
```typescript
// 错误消息分析
const errorMessages = consoleMessages.filter(msg => 
  msg.includes('[error]') || msg.includes('Error')
);

if (errorMessages.length > 0) {
  console.log(`❌ 发现 ${errorMessages.length} 个错误消息:`);
  errorMessages.forEach((msg, index) => {
    console.log(`${index + 1}. ${msg}`);
  });
}

// API请求分析
const mappingRequests = apiRequests.filter(req => 
  req.url.includes('mapping-configs') && (req.method === 'POST' || req.method === 'PUT')
);
console.log(`✓ 映射配置保存请求: ${mappingRequests.length} 个`);
```

### 7.2 测试总结报告
```typescript
console.log(`\\n📊 测试总结:`);
console.log(`✓ 测试会话ID: ${TEST_SESSION_ID}`);
console.log(`✓ 选择的配置: ${selectedConfigName}`);
console.log(`✓ 控制台消息: ${consoleMessages.length} 条`);
console.log(`✓ API请求: ${apiRequests.length} 个`);
console.log(`✓ 错误消息: ${errorMessages.length} 条`);

if (errorMessages.length > 0 || failedRequests.length > 0) {
  console.log(`❌ 测试发现问题，需要进一步调查`);
} else {
  console.log(`✅ 功能测试基本正常`);
}
```

## 8. 最佳实践总结

### 8.1 代码规范
- 使用TypeScript提供类型安全
- 变量命名语义化，使用驼峰命名法
- 常量使用大写下划线格式
- 适当的代码注释和文档

### 8.2 测试设计原则
- **可重复性**：每次测试结果应该一致
- **独立性**：测试用例之间不应相互依赖
- **可维护性**：测试代码易于理解和修改
- **全面性**：覆盖主要功能路径和边界情况

### 8.3 调试和维护
- 详细的日志输出便于问题定位
- 测试会话ID便于追踪特定的测试执行
- 分步骤验证便于定位失败点
- 提供多种备选方案提高测试稳定性

### 8.4 性能考虑
- 合理设置超时时间
- 避免不必要的等待
- 优化元素定位策略
- 及时清理测试数据

## 9. 测试模板

基于以上规范，提供一个通用的E2E测试模板：

```typescript
import { test, expect, Page } from '@playwright/test';

test.describe('【功能模块】测试', () => {
  const TEST_SESSION_ID = `test_${Date.now()}`;
  
  test('【具体功能】测试', async ({ page }) => {
    let consoleMessages: string[] = [];
    let apiRequests: any[] = [];
    let apiResponses: any[] = [];
    
    // 设置监控
    setupMonitoring(page, consoleMessages, apiRequests, apiResponses);
    
    console.log(`🚀 【功能】测试开始: ${TEST_SESSION_ID}`);
    
    try {
      // 步骤1: 页面导航
      console.log('\\n=== 步骤1: 页面导航 ===');
      await navigateToPage(page);
      
      // 步骤2: 用户交互
      console.log('\\n=== 步骤2: 用户交互 ===');
      await performUserInteractions(page);
      
      // 步骤3: 数据验证
      console.log('\\n=== 步骤3: 数据验证 ===');
      await validateResults(page);
      
    } catch (error) {
      console.error(`❌ 测试执行失败: ${error.message}`);
      throw error;
    } finally {
      // 测试分析和清理
      analyzeTestResults(consoleMessages, apiRequests, apiResponses);
    }
  });
});

function setupMonitoring(page: Page, messages: string[], requests: any[], responses: any[]) {
  // 监控设置实现
}

async function navigateToPage(page: Page) {
  // 页面导航实现
}

async function performUserInteractions(page: Page) {
  // 用户交互实现
}

async function validateResults(page: Page) {
  // 结果验证实现
}

function analyzeTestResults(messages: string[], requests: any[], responses: any[]) {
  // 测试分析实现
}
```

## 10. 结论

本规范基于实际的E2E测试实践，提供了完整的测试开发指导。遵循这些规范可以确保：

1. **测试质量**：全面的验证和错误处理
2. **可维护性**：清晰的结构和详细的日志
3. **可靠性**：稳健的重试机制和兜底方案
4. **可调试性**：详细的监控和分析机制

建议所有E2E测试开发都参考此规范，确保测试的一致性和质量。