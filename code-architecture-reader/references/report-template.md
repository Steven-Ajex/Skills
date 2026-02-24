# 深度版架构解读报告模板

按此模板输出；根据项目规模裁剪小节，但保留“证据”和“不确定项”。

## 1. 结论摘要（Executive Summary）

- 项目类型与目标（推断时标注）
- 架构风格判断（如分层架构 Layered Architecture、六边形架构 Hexagonal Architecture、模块化单体 Modular Monolith、微服务 Microservices）
- 主要优点（2-4 条）
- 主要风险（2-4 条）
- 建议优先级总览

## 2. 分析范围与方法（Scope & Method）

- 分析范围：哪些目录/模块被覆盖，哪些未覆盖
- 输出档位：快读版 / 标准版 / 深度版
- 入口与关键证据来源
- 方法：目录扫描、调用链追踪、配置与依赖装配分析、测试代码对照
- 抽样策略与时间盒（如适用）
- 事实 (Fact) 与推断 (Inference) 标记说明

## 3. 架构总览（Architecture Overview）

### 3.1 分层/模块划分

- 模块 A：职责、边界、对外接口
- 模块 B：职责、边界、对外接口
- 模块 C：职责、边界、对外接口

### 3.2 依赖方向（Dependency Direction）

- 期望依赖方向
- 实际依赖方向（列出偏离点）
- 循环依赖 (Cyclic Dependency) 或潜在循环依赖（如有）

### 3.3 横切关注点（Cross-Cutting Concerns）

- 日志 (Logging)
- 错误处理 (Error Handling)
- 鉴权/鉴权决策 (Authentication / Authorization)
- 配置管理 (Configuration Management)
- 监控与追踪 (Observability / Tracing)

## 4. 关键路径分析（Critical Path Analysis）

至少 1 条，建议 2 条。

### 4.1 路径名称：`<业务动作>`

- 触发入口（API/CLI/Job/Event）
- 主调用链（按顺序）
- 状态变更点（State Mutation Points）
- 外部依赖交互点（DB/API/MQ/Cache）
- 错误路径与回退路径（Fallback / Retry / Compensation）
- 证据引用（文件 + 行号）

### 4.2 路径名称：`<第二条业务动作>`（可选）

- 同上

## 5. 设计优点（Strengths）

每条优点使用同一结构：

### 优点 N：`<标题>`

- 现象（代码事实）
- 为什么这是优点（工程价值）
- 适用范围/边界
- 置信度（高/中/低）
- 证据引用

常见候选维度：

- 职责分离 (Separation of Concerns)
- 抽象稳定 (Stable Abstractions)
- 扩展点明确 (Clear Extension Points)
- 失败隔离 (Failure Isolation)
- 可测试性良好 (Testability)
- 配置与运行分离 (Config/Runtime Separation)

## 6. 设计缺点与风险（Weaknesses / Risks）

每条风险使用同一结构：

### 风险 N：`<标题>`

- 优先级（P1 / P2 / P3）
- 现象（代码事实）
- 影响（影响模块/场景）
- 触发条件
- 后果（维护成本、缺陷概率、性能问题、扩展阻力等）
- 建议方向（先给方向，不必直接重写代码）
- 置信度（高/中/低）
- 证据引用

常见候选维度：

- 隐式耦合 (Implicit Coupling)
- 边界泄漏 (Boundary Leakage)
- 共享可变状态 (Shared Mutable State)
- 错误处理分散/不一致 (Inconsistent Error Handling)
- 事务边界不清 (Unclear Transaction Boundary)
- 抽象过度/不足 (Over/Under Abstraction)

## 7. 改进建议（Prioritized Recommendations）

### 7.1 立即可做（Quick Wins）

- 建议 1：目标 / 范围 / 收益 / 风险 / 验证方式
- 建议 2：目标 / 范围 / 收益 / 风险 / 验证方式

### 7.2 中期改造（Mid-term Refactors）

- 建议 1：目标 / 涉及模块 / 收益 / 风险 / 验证方式

### 7.3 长期演进（Long-term Evolution）

- 建议 1：演进方向、前置条件、迁移策略 (Migration Strategy)

## 8. 残余风险与测试盲区（Residual Risks / Testing Gaps）

- 需要运行时验证但当前无法确认的点
- 未覆盖模块可能带来的结论偏差
- 建议补充的测试或运行证据

## 9. 不确定项与需确认问题（Unknowns / Questions）

- 无法从代码静态阅读确认的运行时行为
- 依赖业务上下文才能判断的设计取舍
- 需要用户提供的资料（部署拓扑、流量规模、故障案例、性能指标、领域规则）

## 10. 附录：证据索引（Evidence Index）

- `path/to/fileA.ext:123`
- `path/to/fileB.ext:45`
- `path/to/fileC.ext:78`
