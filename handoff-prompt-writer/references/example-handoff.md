# 示例：大型软件开发场景的交接提示词

> 示例中的项目、路径、commit 均为虚构，仅用于演示写法。

## 场景

`acme-shop` 是一个 pnpm monorepo：`apps/api`（Express）、`apps/web`（Next.js）、`packages/auth`（新建）。任务是把登录态从 express-session（服务端 Session + Redis）迁移到 JWT（15 分钟 access token + 7 天 refresh token 轮换）。会话已经进行了很久，上下文接近上限，需要换对话继续。

---

## 反例：流水账式交接

```text
我们今天主要在做认证迁移。一开始用 jsonwebtoken，后来不行换了 jose。然后做了登录接口和刷新接口，
刷新那块还差一点。中间件也写好了。之前说的那个 Cookie 问题已经解决了。
下一步继续完善刷新逻辑，然后把前端也改一下。注意别用 Strict。
```

问题逐条对照：

| 原文 | 问题 | 后果 |
|---|---|---|
| “后来不行换了 jose” | 失败原因缺失 | 新会话不知道只在 edge runtime 下不行，可能在 `apps/api` 里又换回来，或到处禁用 `jsonwebtoken` |
| “中间件也写好了” | 虚报完成：实际没有运行过测试 | 新会话把未验证代码当作可靠基础 |
| “之前说的那个 Cookie 问题” | 悬空指代 | 完全无法理解 |
| “继续完善刷新逻辑” | 下一步模糊 | 新会话要重新阅读代码、猜测还差什么 |
| “注意别用 Strict” | 约束没有理由 | 新会话不知道边界，遇到相近问题时无法判断 |
| （未提及） | 丢失用户要求：refresh token 必须放 HttpOnly Cookie；迁移期不能强制登出 | 新会话可能违反用户的明确要求 |
| （未提及） | 丢失接口契约与测试基线 | 新会话可能改动已冻结的类型，或去修与任务无关的失败用例 |

---

## 正例：完整版（`HANDOFF.md` + 引导提示词）

这个任务跨 3 个包、分 4 个阶段、预计还会多次交接，所以选择完整版。交接前已征得用户同意，把未完成的改动作为 WIP 提交并推送。

### `HANDOFF.md`

````markdown
# 任务交接：acme-shop 认证迁移（Session → JWT）

> 最后更新：2026-09-27（第 2 次交接）。你看不到之前的对话；本文与仓库实际状态冲突时，以仓库为准。

## 0. 接手协议

1. 阅读：`apps/api/src/routes/auth/refresh.ts`（下一步要改的文件）、`packages/auth/src/types.ts`（已冻结的接口契约）
2. 核对状态：运行 `pnpm --filter @acme/api test -- refresh`，预期 9 通过、2 失败（两个 `reuse detection` 用例，功能尚未实现，属预期内失败）
3. 若实际状态与本文不符：以仓库为准，先向用户报告差异，再继续
4. 核对无误后，直接从“下一步 #1”开始

## 1. 目标

- 最终目标：把登录态从 express-session 迁移到 JWT（access token 15 分钟，refresh token 7 天并轮换），最终移除 express-session 和 Redis
- 动机：新服务 `apps/mobile-bff` 需要独立验证登录态，不能依赖共享 Session 存储
- 完成标准：
  - `apps/api`、`apps/web` 全部改用 JWT，`pnpm test` 除测试基线中的已知失败外全部通过
  - 迁移期间旧 Session 用户不被强制登出（双模式运行，由 `AUTH_LEGACY_SESSION` 控制）
  - express-session 与 Redis 依赖在双模式结束后移除（P4）

## 2. 约束与偏好

- 用户要求（原话）：“refresh token 必须放在 HttpOnly Cookie 里，不能放 localStorage。”（原因：防止 XSS 窃取）
- 用户要求（原话）：“迁移期间老用户不能被强制登出。”
- 用户要求（原话）：“不想引入新的认证框架，团队要能看懂每一行。”（因此不用 next-auth 等框架）
- 禁止：升级 Next.js 版本（原因：`apps/web` 依赖的内部 UI 库只兼容当前版本）
- 协作约定：遵循仓库根目录 `AGENTS.md`（提交格式、代码风格）

## 3. 环境与命令

- 安装依赖：`pnpm install`
- 启动数据库：`docker compose up -d db`
- 执行迁移：`pnpm db:migrate`
- 开发运行：`pnpm dev`
- 测试：全量 `pnpm test`；api 单包 `pnpm --filter @acme/api test`；单个文件 `pnpm --filter @acme/api test -- refresh`
- 开发用密钥：`pnpm --filter @acme/auth gen-keys`（生成到 `.keys/`，已被 gitignore）
- 所需环境变量（只写名称）：`DATABASE_URL`、`JWT_PRIVATE_KEY_PATH`、`JWT_PUBLIC_KEY_PATH`、`AUTH_LEGACY_SESSION`

## 4. 当前状态快照

- 分支：`feat/jwt-auth`；HEAD：`9f8e7d6 wip(auth): refresh reuse detection`；已推送到 `origin/feat/jwt-auth`
- 未提交改动：无
- PR：尚未创建（用户要求 P2 完成后再开 PR）
- 测试基线：`apps/web/e2e/checkout.spec.ts` 在 main 上就失败（第三方支付沙箱超时），与本任务无关，不要修
- 非 git 状态：迁移 `0042_refresh_tokens.sql` 只在本地数据库执行过，staging 未执行

## 5. 任务看板

| 阶段/模块 | 任务 | 状态 | 证据/位置 |
|---|---|---|---|
| P1 / packages/auth | 签发与验签（jose，RS256） | [已验证] | `a1b2c3d`；`pnpm --filter @acme/auth test` 18 通过 |
| P1 / packages/db | `refresh_tokens` 表迁移 | [已验证] | `packages/db/migrations/0042_refresh_tokens.sql`，本地已执行 |
| P2 / apps/api | `/auth/login` 签发双 token | [已验证] | `d4e5f6a` |
| P2 / apps/api | `/auth/refresh` 轮换 | [进行中] | 轮换已完成；重用检测未完成，停在 `apps/api/src/routes/auth/refresh.ts:57` |
| P2 / apps/api | 双模式鉴权中间件 | [未验证] | `apps/api/src/middleware/authenticate.ts` 已写完，未写测试、未运行 |
| P3 / apps/web | `middleware.ts` 改用 jose 验签 | [已验证] | `b7c8d9e`；`pnpm --filter @acme/web test` 通过 |
| P3 / apps/web | 登录页改用新接口 | [未开始] | `apps/web/app/login/actions.ts` |
| P4 / 全局 | 移除 express-session 与 Redis | [未开始] | 双模式结束后进行 |

## 6. 接口契约

- `AuthClaims` 类型（`packages/auth/src/types.ts:5`）：`{ sub, sid, roles, iat, exp }`。[已冻结]：`apps/mobile-bff` 团队已按它开发
- `POST /auth/refresh` 响应体 `{ accessToken, expiresIn }`：[可调整]，目前只有 `apps/web` 使用

## 7. 关键决策

- D1：签名算法采用 RS256，而不是 HS256。理由：`apps/mobile-bff` 需要独立验签，RS256 只需分发公钥。推翻条件：确认只有单一服务验签
- D2：迁移期双模式——中间件先验 JWT，失败再回退到 Session，回退路径由 `AUTH_LEGACY_SESSION` 控制。理由：满足“老用户不能被强制登出”。推翻条件：用户确认可以接受强制登出
- D3：refresh token 只存哈希，存于 Postgres `refresh_tokens` 表；每次轮换使旧 token 立即失效；检测到已轮换的 token 被再次使用时，撤销同一 `family_id` 下的全部 token。理由：去掉 Redis 依赖，同时能发现 token 被盗用

## 8. 已排除路径（不要重试）

- 尝试：在 `apps/web/middleware.ts` 中用 `jsonwebtoken` 验签 → 现象：`Error: The edge runtime does not support Node.js 'crypto' module.` → 原因：Next.js middleware 运行在 edge runtime → 结论：web 端用 `jose`；`apps/api`（Node runtime）可以继续用任一库，但为统一起见已全部改用 `jose`
- 尝试：refresh Cookie 设为 `SameSite=Strict` → 现象：从第三方支付页回跳到 `/checkout/return` 时 Cookie 不发送，用户显示为未登录 → 原因：跨站顶级导航不携带 Strict Cookie → 结论：使用 `SameSite=Lax`，并对 `POST /auth/refresh` 校验 CSRF token

## 9. 代码地图

- `packages/auth/src/sign.ts:23`：签发 access/refresh token
- `packages/auth/src/verify.ts:10`：验签，返回 `AuthClaims`
- `apps/api/src/routes/auth/refresh.ts`：refresh 接口，轮换逻辑在 30–55 行，57 行为待实现的重用检测
- `apps/api/src/middleware/authenticate.ts`：双模式鉴权中间件（未验证）
- `packages/db/migrations/0042_refresh_tokens.sql`：`refresh_tokens` 表，含 `family_id`、`revoked_at`

## 10. 下一步

1. 在 `refresh.ts:57` 实现重用检测：收到已轮换过的 token 时，撤销同一 `family_id` 下全部 token 并返回 401。验证：`pnpm --filter @acme/api test -- refresh` 全部 11 个用例通过
2. 为 `authenticate.ts` 补测试，覆盖三种情况：JWT 有效；JWT 过期时回退到 Session；`AUTH_LEGACY_SESSION=false` 时拒绝 Session。验证：新测试通过
3. P2 完成后，按 `AGENTS.md` 的格式创建 PR（用户要求在此时开 PR）
4. 开始 P3：`apps/web/app/login/actions.ts` 改用 `/auth/login`

## 11. 未决问题与风险

- Q1：双模式持续多久？用户说“至少一周”，具体关闭日期未定。当前假设：`AUTH_LEGACY_SESSION` 默认为 true，由用户决定何时关闭
- Q2：staging 何时执行迁移 0042？需要用户安排
- 风险：access token 在 15 分钟有效期内无法撤销（登出后最长仍可用 15 分钟）。用户已知晓并接受

## 12. 交接历史

- 2026-09-27 第 2 次：完成 `/auth/login`、refresh 轮换、双模式中间件（未验证）；停在重用检测
- 2026-09-25 第 1 次：完成 P1 与 web 端 `middleware.ts`
````

### 引导提示词（粘贴到新对话）

```text
请接手 acme-shop 的认证迁移（Session → JWT）工作。你看不到之前的对话。
1. 先完整阅读仓库根目录的 HANDOFF.md，按其中“0. 接手协议”核对仓库状态；
2. 如果文档与仓库实际状态不一致，以仓库为准，先告诉我差异；
3. 然后从“下一步 #1”开始。
```

---

## 正例为什么有效

1. **接手协议给出了可对照的预期结果**（9 通过、2 失败），新会话一运行就知道状态是否与文档一致。
2. **每个已排除路径都写了原因**，新会话知道 `jsonwebtoken` 只是在 edge runtime 下不能用，而不是整体不可用。
3. **“未验证”如实标注**，新会话会先给中间件补测试，而不是在它之上继续堆代码。
4. **用户原话被保留**，HttpOnly、不能强制登出、不引入框架这三条硬约束不会在交接中被稀释。
5. **接口契约和测试基线**防止了两类典型的越界：改动已冻结的类型，以及去修与任务无关的失败用例。
6. **代码和日志都只给了指针**，整份文档约 4500 个字符，远小于原对话，却覆盖了新会话需要的全部 A 类和 B 类信息。
