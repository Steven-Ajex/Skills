# FMT Skills 第一性原理技能契约（First-Principles Skill Contract）

用于统一 `fmt/` 下原子技能（atomic skill）与编排技能（workflow skill）的设计质量，避免后续新增/优化时边界漂移。

## 1. 设计目标（Why）

1. 让每个 skill 只解决一个最小可复用问题（Minimum Reusable Capability）
2. 让输入/输出可验证、可交接、可复用
3. 让结论回链到代码证据或日志证据，避免“经验化跳步”
4. 让工作流技能只做编排，不替代原子技能的专业判断

## 2. 每个 Skill 必须回答的 5 个问题（What）

1. 最小任务单元（Minimum Task Unit）是什么
2. 核心输入（Inputs）是什么，哪些是必需、哪些是可选
3. 核心输出（Outputs）是什么，下游谁消费
4. 完成判据（Definition of Done, DoD）是什么
5. 失败与降级策略（Failure / Fallback）是什么

## 3. 原子技能（Atomic Skill）边界规则（Boundary Rules）

1. 不跨多个专业步骤给结论（例如未分段先做全局调参结论）
2. 不吞并上下游职责（例如 `decoder` 不直接写 tuning report）
3. 可以指出候选方向，但必须标注“不负责最终结论”的边界
4. 输入不足时优先输出“缺口清单（Gap List）”，而不是补全假设

## 4. 编排技能（Workflow Skill）边界规则

1. 负责顺序、门禁（Gate）、汇总，不替代原子技能的专业分析细节
2. 任何跨阶段结论都必须引用上游工件（Artifact）
3. 可根据场景裁剪步骤，但必须说明跳过原因与风险
4. 必须在输出中显式列出尚未完成的阶段与未满足门禁

## 5. 证据纪律（Evidence Discipline）

1. 代码结论：给出文件路径 + 行号，并区分事实（Fact）与推断（Inference）
2. 日志结论：给出时间段（timestamp/window）+ 信号 + 阶段/模式上下文
3. 无法确认时写“不确定项（Unknowns）”，不要写成确定性结论

## 6. 输出语言约定（Language Convention）

1. 默认中文输出
2. 专业术语首次出现附英文注释（例如：状态机（State Machine））
3. 保留信号名、参数名、结构体名、函数名原文

## 7. 质量门禁（Quality Gates）最低要求

1. 触发准确性（Trigger Accuracy）：明确何时使用、何时不使用
2. 边界纯度（Boundary Purity）：不越权给下游结论
3. 证据可追溯性（Evidence Traceability）：关键结论可回链
4. 交接可用性（Handoff Usability）：下游可直接消费输出
5. 失败可控性（Failure Containment）：输入不足时能安全降级

## 8. 推荐的优化顺序（Optimization Order）

1. 先收紧边界（做什么 / 不做什么）
2. 再定义交接工件（Artifact Contract）
3. 再补质量门禁（Quality Gates）
4. 最后优化模板与示例（避免一开始堆细节）
