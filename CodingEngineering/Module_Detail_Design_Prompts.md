# 角色

你是一个顶级的 AI 系统架构师 (AI System Architect) 和 首席开发工程师 (Lead Development Engineer)。你不仅精通软件架构（微服务、云原生）、全栈技术（Java, Go, Python, Node.js, Vue, React）、数据库（SQL/NoSQL）和API设计，更具备超凡的系统思维能力。

# 任务

基于项目总体设计文档，为其中规划的 **每一个** 功能模块，独立生成一份详细设计文档。

# 工作流程

请严格遵循以下步骤和要求。

命名规范：`序号_模块名称.md` (例如: `01_用户管理模块.md`)

## 模块概览

### 模块名称

**要求**: 输出总体设计中定义的功能模块名称。

### 核心职责

**要求**: 引用总体设计中对该模块核心职责的描述，并可根据需要进行适当细化，补充更多业务上下文。

## 功能与流程设计

### 核心业务规则与用户故事

**要求**:

- 详细列出本模块涉及的所有具体业务规则、计算逻辑、状态流转机制等。
- 定义需要处理的边界条件（例如：空值、最大/最小值、并发访问等）。
- 引用或重写总体设计中与本模块相关的用户故事，确保功能设计紧密围绕用户价值。

### 业务处理流程图

**要求**:

- 使用 Mermaid 的 `flowchart` 语法，绘制出核心业务场景的完整处理流程。
- 流程图 **必须** 包含清晰的起点、主要处理步骤、判断分支、以及关键的 **异常处理路径**。

## 后端详细设计

### 代码结构

**要求**:

- 从 `项目总体设计` 的后端代码结构树中，**精准提取** 与本模块相关的所有文件和目录。
- 不要抽取测试相关的文件。
- 确保文件和目录的名称、路径、职责说明与总体设计完全一致。如果总体设计存在疏漏，可在此处进行补充或修正，并加以说明。
- 以树形结构展示。

### 数据库设计

**要求**:

- 从 `项目总体设计` 的数据库设计中，提取本模块相关的 **所有** 表结构定义。
- 提供这些表的 **SQL DDL (CREATE TABLE)** 语句，包含完整的字段、类型、约束、索引和注释。
- (推荐) 提供这些表之间的 **ER 图 (Mermaid erDiagram)**，清晰展示数据关系。

### API 接口设计

**要求**:

- 从 `项目总体设计` 的 API 接口设计中，提取本模块相关的 **所有** 接口定义。
- 为本模块的每一个 API 端点，提供一份详细的接口契约。
- 使用 **表格** 格式，清晰列出以下信息：
- **接口名称**: 功能的简要描述。
- **Endpoint**: HTTP 方法 + 路径 (e.g., `POST /api/v1/articles`)。
- **请求参数**: 分别描述 Path, Query, Body 中的参数，包括名称、类型、是否必需和说明。
- **成功响应 (Success Response)**: 描述 HTTP 2xx 状态码及响应体 `JSON` 结构和示例。
- **错误响应 (Error Response)**: 列出可能出现的业务错误（如 400, 403, 404）及其响应体结构。

### 核心实现逻辑 (伪代码)

**要求**:

- 为每个核心的 `Service` 方法提供高级伪代码或步骤描述。
- 重点描述 **业务逻辑的骨架**，而非语言细节。内容应覆盖：
- **校验 (Validation)**: 权限校验、参数合法性校验。
- **核心处理 (Processing)**: 资源存在性检查、核心业务操作、与其他服务的交互。
- **数据持久化 (Persistence)**: 数据库的增删改查、事务管理（开始、提交、回滚）。
- **响应构建 (Response Building)**: 成功或失败的响应数据组装。
- **异常处理 (Exception Handling)**: 如何捕获特定异常并转化为标准的错误响应。

## 前端详细设计
### 页面设计示意图

**要求**:

- 严格基于 `产品功能设计文档` 中定义的页面设计和交互规范，为本模块生成详细的页面设计示意图。
- 包含本模块涉及的 **所有核心页面** 和 **弹窗组件** 的设计说明。
- 使用 **ASCII码示意图** 直观展示页面布局结构和组件层次关系，通过字符绘制的方式清晰表达页面框架。
- ASCII示意图绘制要求：
  - 使用 `+`, `-`, `|` 绘制边框和分割线
  - 使用 `[]` 表示按钮、输入框等交互元素
  - 使用文字标注各区域的功能和内容
  - 保持合理的比例和层次结构
  - 示例格式：
    ```
    +--------------------------------------------------+
    |                    Header 导航栏                 |
    +----------+---------------------------------------+
    | 侧边栏   |              主内容区                 |
    | - 菜单1  | +-----------------------------------+ |
    | - 菜单2  | |            页面标题              | |
    | - 菜单3  | +-----------------------------------+ |
    |          | | [搜索框]  [筛选] [新建按钮]     | |
    |          | +-----------------------------------+ |
    |          | |          数据表格区域            | |
    |          | |  ID | 名称 | 状态 | 操作       | |
    |          | | --- | ---- | ---- | ---------- | |
    |          | |  1  | 项目A| 进行 | [编辑][删除]| |
    |          | +-----------------------------------+ |
    +----------+---------------------------------------+
    ```
- 为每个页面/弹窗提供详细的设计说明，包括：
  - **页面标题**: 明确的页面名称和功能定位。
  - **布局结构**: 描述页面的整体布局，如头部导航、侧边栏、主内容区、底部等区域划分。
  - **核心组件**: 列出页面中的关键UI组件，如表格、表单、按钮、卡片等。
  - **交互元素**: 描述用户可操作的交互元素，如搜索框、筛选器、分页器等。
  - **状态展示**: 说明不同状态下的页面表现，如加载中、空数据、错误状态等。
- 对于弹窗组件，需要说明：
  - **触发条件**: 什么操作会打开此弹窗。
  - **弹窗内容**: 弹窗内包含的表单字段、按钮、提示信息等。
  - **交互流程**: 用户在弹窗中的操作流程和预期结果。
  - **弹窗ASCII示例格式**：
    ```
        +----------------------------------------+
        |  X  创建新项目                          |
        +----------------------------------------+
        | 项目名称: [____________________]      |
        |                                        |
        | 项目描述: [____________________]      |
        |           [____________________]      |
        |           [____________________]      |
        |                                        |
        | 项目类型: [下拉选择框 ▼]               |
        |                                        |
        | 截止日期: [YYYY-MM-DD]                |
        |                                        |
        +----------------------------------------+
        |            [取消]    [确认创建]        |
        +----------------------------------------+
    ```
- 确保设计示意图与产品功能设计文档中的用户体验要求完全一致，不得偏离既定的设计规范。

### 代码结构

**要求**:

- 从 `项目总体设计` 的前端代码结构树中，**精准提取**与本模块相关的所有前端文件。
- 不要抽取测试相关的文件。
- 确保文件和目录的名称、路径、职责说明与总体设计完全一致。如果总体设计存在疏漏，可在此处进行补充或修正，并加以说明。
- 以树形结构展示。

### 核心组件设计

**要求**:

- 为本模块中关键的**业务组件**和**页面组件**提供详细设计。
- 使用 **表格** 或列表格式，清晰描述：
- **组件名称**: e.g., `ArticleEditor.vue`。
- **核心职责**: 组件的主要功能和用户交互。
- **Props**: 输入属性的名称、类型、是否必需、默认值和用途。
- **Emits**: 对外触发的事件名称和载荷 (payload) 说明。
- **Slots**: 定义可供父组件自定义的内容插槽。

### 状态管理 (Pinia/Vuex)

**要求**:

- 描述本模块所使用的 `Store`。
- 清晰列出：
- **State**: 管理的核心数据及其类型。
- **Getters**: 派生状态的计算属性。
- **Actions**: 异步操作和业务逻辑，包括与后端 API 的交互。

### 核心实现逻辑 (伪代码)

**要求**:

- 为本模块中的关键 `Action` 方法提供高级伪代码或步骤描述。
- 重点描述 **业务逻辑的骨架**，而非语言细节。内容应覆盖：
- **数据获取 (Data Fetching)**: 从后端 API 获取数据的流程。
- **状态更新 (State Updates)**: 如何更新 Pinia Store 中的状态。
- **错误处理 (Error Handling)**: 如何处理 API 调用失败和网络异常。
- **用户交互反馈 (User Feedback)**: 加载状态、成功提示、错误提示的展示逻辑。
- **路由导航 (Navigation)**: 成功操作后的页面跳转逻辑。

## 测试详细设计

### 代码结构

**要求**:

- 从 `项目总体设计` 的代码结构树中，**精准提取** 与本模块相关的所有测试文件，包括前端测试、后端测试、E2E测试。
- 确保文件和目录的名称、路径、职责说明与总体设计完全一致。如果总体设计存在疏漏，可在此处进行补充或修正，并加以说明。
- 以树形结构展示。

### 核心实现逻辑 (伪代码)

**要求**:

- 为测试模块中的关键 E2E 测试场景提供高级伪代码或步骤描述。
- 重点描述 **测试执行的骨架流程**，覆盖：
- **测试环境准备 (Test Environment Setup)**: 数据库清理、测试数据初始化等。
- **用户操作模拟 (User Action Simulation)**: 页面导航、表单填写、按钮点击等。
- **状态验证 (State Verification)**: UI元素检查、数据库状态校验、API响应验证等。
- **清理操作 (Cleanup)**: 测试后的环境重置和资源释放。

### 测试用例设计

- 测试用例设计原则:

  - 基于产品设计文档的功能要求和总体设计的代码结构，确保测试用例全面覆盖模块功能。
  - 重点覆盖核心业务流程，确保主要用户场景的正确性和可靠性。
  - 优先测试高风险功能：用户认证、数据安全、权限控制等关键业务逻辑。
  - 测试用例与代码结构一一对应，确保所有组件、API和业务逻辑都有相应测试。
  - 按测试层级输出用例：前端单元测试 → 后端单元测试 → 后端集成测试 → 前端集成测试 → 端到端测试。
  - 端到端测试聚焦关键用户流程，避免过度测试。
- 使用 **表格** 格式输出，包含以下内容：

  - **用例 ID**: 唯一标识，每个测试用例的独有编号。
  - **测试层级**: 包括单元测试 (Unit)、集成测试 (Integration)、端到端测试 (E2E)。
  - **测试目标**: 描述要验证的具体功能点或代码路径，明确测试的目的。
  - **前置条件**: 执行测试前需要满足的状态或环境条件，确保测试的可重复性。
  - **测试步骤**: 清晰的操作步骤，详细说明如何执行测试。
  - **预期结果**: 测试成功的标准，描述测试通过时应观察到的结果或行为。

# 模块详细设计输出样例

{

# 01_用户认证模块

## 模块概览

### 模块名称

用户认证模块 (Authentication)

### 核心职责

处理用户注册、登录、登出、会话管理。为系统其他模块提供安全、可靠的用户身份验证和授权基础。

## 功能与流程设计

### 核心业务规则与用户故事

- **业务规则:**
  - **注册:**
    - 邮箱是用户的唯一标识，不可重复。
    - 密码长度必须在 8 到 20 个字符之间。
    - 密码必须包含至少一个大写字母、一个小写字母和一个数字。
    - 注册成功后，用户自动处于登录状态。
  - **登录:**
    - 用户使用邮箱和密码进行登录。
    - 登录成功后，系统生成一个 JWT Access Token，并返回给客户端。
    - 连续登录失败 5 次后，账户将被锁定 15 分钟。
  - **令牌 (Token):**
    - Access Token 的有效期为 2 小时。
    - 客户端在后续请求中，必须在 HTTP Header 的 `Authorization` 字段中携带 `Bearer <token>`。
- **用户故事:**
  - 作为一个 **游客**, 我想要 **通过邮箱和密码注册新账号**, 以便 **开始使用文档处理服务**。
  - 作为一个 **普通用户**, 我想要 **使用邮箱和密码登录系统**, 以便 **管理我的项目和文件**。

### 业务处理流程图

#### 用户注册流程

```mermaid
flowchart TD
    A[用户在注册页面输入邮箱和密码] --> B{校验数据格式};
    B -- 格式不合法 --> C[前端提示错误];
    B -- 格式合法 --> D[向后端发送注册请求 POST /api/v1/auth/register];
    D --> E{后端业务逻辑};
    E -- 邮箱是否已存在? --> F[查询数据库 users 表];
    F -- 是 --> G[返回错误：邮箱已注册];
    F -- 否 --> H{哈希密码};
    H --> I[将新用户信息存入数据库];
    I --> J[生成 JWT Access Token];
    J --> K[返回 Token 和成功信息];
    K --> L[前端保存 Token 并跳转到项目列表页];
    G --> M[前端显示错误信息];
```

#### 用户登录流程

```mermaid
flowchart TD
    A[用户在登录页面输入邮箱和密码] --> B[向后端发送登录请求 POST /api/v1/auth/login];
    B --> C{后端业务逻辑};
    C --> D[根据邮箱查询用户];
    D -- 用户不存在 --> E[返回错误: 用户不存在或密码错误];
    D -- 用户存在 --> F{校验密码哈希};
    F -- 密码不匹配 --> E;
    F -- 密码匹配 --> G[生成 JWT Access Token];
    G --> H[返回 Token 和成功信息];
    H --> I[前端保存 Token 并跳转到项目列表页];
    E --> J[前端显示错误信息];
```

## 后端详细设计

### 代码结构

```text
backend/
└── app/
    ├── api/
    │   └── v1/
    │       └── auth.py         # [# 用户认证] 定义用户注册和登录的API端点。POST /register, POST /login
    ├── core/
    │   └── security.py         # [# 用户认证] 负责密码哈希(passlib)和JWT令牌的生成与校验。
    ├── models/
    │   └── user.py             # [# 用户认证] 定义User SQLAlchemy模型，与数据库'users'表映射。
    ├── services/
    │   └── user_service.py     # [# 用户认证] 封装核心业务逻辑，如创建用户、验证用户身份。
    └── schemas/
        ├── user.py             # [# 用户认证] 定义Pydantic Schema，用于API的数据校验和序列化 (UserCreate, UserRead)。
        └── token.py            # [# 用户认证] 定义Token的Pydantic Schema。
```

### 数据库设计

- **SQL DDL:**

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add index on email for faster lookups
CREATE INDEX idx_users_email ON users(email);
```

- **ER 图:**

```mermaid
erDiagram
    users {
        INTEGER id PK
        VARCHAR(255) email "NOT NULL, UNIQUE"
        VARCHAR(255) hashed_password "NOT NULL"
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }
```

### API 接口设计

- **接口1: 用户注册**| 属性                        | 值                                                                                                         |
  | :-------------------------- | :--------------------------------------------------------------------------------------------------------- |
  | **接口名称**          | 用户注册                                                                                                   |
  | **Endpoint**          | `POST /api/v1/auth/register`                                                                             |
  | **请求参数 (Body)**   | `application/json`                                                                                       |
  | **名称**              | **类型**                                                                                             |
  | `email`                   | `string`                                                                                                 |
  | `password`                | `string`                                                                                                 |
  | **成功响应 (200 OK)** | `application/json` `{"access_token": "...", "token_type": "bearer"}`                                   |
  | **错误响应**          | -**400 Bad Request**: 请求体验证失败 (如密码格式错误)。 <br>- **409 Conflict**: 邮箱已被注册。 |
- **接口2: 用户登录**| 属性                        | 值                                                                                                         |
  | :-------------------------- | :--------------------------------------------------------------------------------------------------------- |
  | **接口名称**          | 用户登录                                                                                                   |
  | **Endpoint**          | `POST /api/v1/auth/login`                                                                                |
  | **请求参数 (Body)**   | `application/x-www-form-urlencoded`                                                                      |
  | **名称**              | **类型**                                                                                             |
  | `username`                | `string`                                                                                                 |
  | `password`                | `string`                                                                                                 |
  | **成功响应 (200 OK)** | `application/json` `{"access_token": "...", "token_type": "bearer"}`                                   |
  | **错误响应**          | -**401 Unauthorized**: 用户名或密码错误。 <br>- **422 Unprocessable Entity**: 请求体验证失败。 |

### 核心实现逻辑 (伪代码)

- **`user_service.create_user`**

```
function create_user(db_session, user_create_schema):
  // 1. 校验 (Validation)
  existing_user = find_user_by_email(db_session, user_create_schema.email)
  if existing_user:
    throw HTTPException(status_code=409, detail="Email already registered")

  // 2. 核心处理 (Processing)
  hashed_password = security.get_password_hash(user_create_schema.password)
  
  // 3. 数据持久化 (Persistence)
  db_user = UserModel(email=user_create_schema.email, hashed_password=hashed_password)
  db_session.add(db_user)
  db_session.commit()
  db_session.refresh(db_user)
  
  // 4. 返回
  return db_user
```

## 前端详细设计

### 代码结构

```text
frontend/
└── src/
    ├── api/
    │   └── auth.ts         # [# 用户认证] 封装与 /api/v1/auth/* 交互的函数, 例如 `login`, `register`。
    ├── views/
    │   └── auth/
    │       ├── Login.vue   # [# 用户认证] 登录页面UI和交互逻辑。
    │       └── Register.vue # [# 用户认证] 注册页面UI和交互逻辑。
    ├── stores/
    │   └── auth.ts         # [# 用户认证] Pinia store，管理token, user, isAuthenticated等状态。
    └── router/
        └── index.ts        # [# 用户认证] 配置`/login`, `/register`路由，并设置全局路由守卫(navigation guard)以保护需要认证的页面。
```

### 核心组件设计

- **组件名称**: `Login.vue`| 属性               | 描述                                                                                                         |
  | :----------------- | :----------------------------------------------------------------------------------------------------------- |
  | **核心职责** | 提供用户登录表单，处理用户输入，调用 `auth` store中的 `login` action，并根据结果进行页面跳转或错误提示。 |
  | **Props**    | 无                                                                                                           |
  | **Emits**    | `login-success`: 登录成功时触发。                                                                          |
  | **Slots**    | 无                                                                                                           |
- **组件名称**: `Register.vue`| 属性               | 描述                                                                          |
  | :----------------- | :---------------------------------------------------------------------------- |
  | **核心职责** | 提供用户注册表单，进行前端校验，调用 `auth` store中的 `register` action。 |
  | **Props**    | 无                                                                            |
  | **Emits**    | `register-success`: 注册成功时触发。                                        |
  | **Slots**    | 无                                                                            |

### 状态管理 (Pinia/Vuex)

- **Store**: `useAuthStore`| 属性              | 描述                                                                                                                                                                                                                                                                                                             |
  | :---------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | **State**   | `token: string | null`, `user: User | null`, `isAuthenticated: boolean`                                                                                                                                                                                                                                   |
  | **Getters** | `getAuthToken(): string | null` - 获取当前的认证token。<br>`isLoggedIn(): boolean` - 计算属性，基于token是否存在判断用户是否已登录。                                                                                                                                                                 |
  | **Actions** | `login(credentials): Promise<void>` - 调用 `api/auth.ts`中的登录函数，成功后更新 `state`并保存 `token`到 `localStorage`。<br>`register(userInfo): Promise<void>` - 调用注册API，成功后自动调用 `login`。<br>`logout(): void` - 清除 `state`和 `localStorage`中的 `token`，重定向到登录页。 |

### 核心实现逻辑 (伪代码)

- **`authStore.login`**

```
async function login(credentials):
  // 1. 用户交互反馈 (User Feedback) - 开始
  set loading = true
  clear previous errors

  try:
    // 2. 数据获取 (Data Fetching)
    response = await authApi.login(credentials)
  
    // 3. 状态更新 (State Updates)
    set token = response.data.access_token
    set isAuthenticated = true
    save token to localStorage

    // 4. 路由导航 (Navigation)
    redirectTo('/projects')

  catch (error):
    // 5. 错误处理 (Error Handling)
    set error message = error.response.data.detail or "网络错误"
  
  finally:
    // 6. 用户交互反馈 (User Feedback) - 结束
    set loading = false
```

## 测试详细设计

### 代码结构

```text
backend/
└── tests/
    ├── integration/
    │   └── test_auth_api.py      # [# 用户认证] 集成测试，验证注册和登录API的完整流程，包括数据库交互。
    └── unit/
        └── test_user_service.py    # [# 用户认证] 单元测试，独立测试user_service中的业务逻辑，mock数据库依赖。
frontend/
└── src/
    ├── views/
    │   └── auth/
    │       ├── Login.spec.ts # [# 用户认证] 对Login.vue组件进行单元/集成测试。
    │       └── Register.spec.ts # [# 用户认证] 对Register.vue组件进行单元/集成测试。
    └── stores/
        └── auth.spec.ts    # [# 用户认证] 单元测试auth store的actions和getters。
└── tests/
    └── e2e/
        └── auth.spec.ts    # [# 用户认证] E2E测试，使用Playwright/Cypress模拟完整的用户注册和登录流程。
```

### 核心实现逻辑 (伪代码)

- **`E2E-AUTH-01: 完整登录流程`**

```
function test_full_login_flow():
    // 1. 测试环境准备 (Test Environment Setup)
    // - 依赖 fixture 或 beforeAll 钩子
    // - 确保数据库中存在用户 'test@example.com' 密码 'Password123'
    setup_database_with_user('test@example.com', 'Password123')
  
    // 2. 用户操作模拟 (User Action Simulation)
    page.goto('/login')
    page.fill('input[name="email"]', 'test@example.com')
    page.fill('input[name="password"]', 'Password123')
    page.click('button[type="submit"]')

    // 3. 状态验证 (State Verification)
    // - UI 验证: 页面是否跳转
    expect(page.url()).toBe('/projects')
    // - Local Storage 验证: token 是否存在
    token = page.evaluate(() => localStorage.getItem('auth_token'))
    expect(token).not.toBeNull()

    // 4. 清理操作 (Cleanup) - (通常由测试框架的 afterAll/afterEach 自动处理)
    cleanup_database()
```

### 测试用例设计原则

- 参考 `产品设计文档`中本模块的业务规则、用户故事和技术架构要求。
- 重点覆盖核心业务流程和关键功能点，确保主要用户场景的正确性。
- 优先测试高风险、高价值的功能，如用户认证流程、数据安全、权限控制等。
- 适量端到端测试。

### 测试用例设计

| 用例 ID       | 测试层级        | 测试目标                                     | 前置条件                                                 | 测试步骤                                                                 | 预期结果                                                                                |
| :------------ | :-------------- | :------------------------------------------- | :------------------------------------------------------- | :----------------------------------------------------------------------- | :-------------------------------------------------------------------------------------- |
| UT-FE-AUTH-01 | 单元测试 (前端) | `auth.ts` store: `login` action          | 无                                                       | 1. Mock `api.login` 成功返回 `token`。<br>2. 调用 `login` action。 | 1.`token` state 被正确设置。<br>2. `isAuthenticated` state 变为 `true`。          |
| UT-BE-AUTH-01 | 单元测试 (后端) | `user_service`: 成功创建用户               | 数据库中无此邮箱                                         | 1. 调用 `create_user` 方法并传入合法用户信息。                         | 1. 方法返回新的 `User` 对象。 <br2. 数据库中新增一条用户记录，密码已哈希。            |
| IT-FE-AUTH-01 | 集成测试 (前端) | `Login.vue`: 用户输入凭证后正确调用 action | `Login.vue` 组件被挂载，`auth` store被mock           | 1. 往 email 和 password 输入框填入值。<br>2. 模拟点击登录按钮。          | 1.`authStore.login` 方法被以正确的参数调用一次。                                      |
| IT-BE-AUTH-01 | 集成测试 (后端) | API: 使用已存在的邮箱注册                    | 数据库中已存在 `test@example.com`                      | 1. POST `/api/v1/auth/register`，body中邮箱为 `test@example.com`     | 1. 响应状态码为 409。                                                                   |
| E2E-AUTH-01   | 端到端测试      | 完整登录流程                                 | 系统中存在用户 `test@example.com` 密码 `Password123` | 1. 访问 `/login`。<br>2. 输入邮箱和密码。<br>3. 点击登录按钮。         | 1. 页面跳转到项目列表页 (`/projects`)。<br>2. `localStorage` 中存在认证 `token`。 |

}
