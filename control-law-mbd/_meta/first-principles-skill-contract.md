# Control Law MBD Skills 第一性原理技能契约（First-Principles Skill Contract）

用于统一 `control-law-mbd/` 下原子技能（atomic skill）与编排技能（workflow skill）的设计质量，避免后续新增/优化时边界漂移。

## 1. 设计目标（Why）

1. 让每个 skill 只解决一个最小可复用问题（Minimum Reusable Capability）
2. 让输入/输出可验证、可交接、可复用,工具上下文（Tool Context）显式可查
3. 让结论回链到模型证据、生成代码证据或验证证据,避免“经验化跳步”
4. 让工作流技能只做编排,不替代原子技能的专业判断

## 2. 每个 Skill 必须回答的 6 个问题（What）

1. 最小任务单元（Minimum Task Unit）是什么
2. 工具上下文（Tool Context）是什么（Simulink 版本、模型形态、是否含生成代码、是否含覆盖率/回放数据）
3. 核心输入（Inputs）是什么,哪些必需、哪些可选
4. 核心输出（Outputs）是什么,下游谁消费
5. 完成判据（Definition of Done, DoD）是什么
6. 失败与降级策略（Failure / Fallback）是什么

> 第 2 项是控制律 MBD 域相对 FMT 域的额外要求,因为 MBD 流程跨工具、跨版本,工具上下文错位是最常见的误判来源。

## 3. 原子技能（Atomic Skill）边界规则（Boundary Rules）

1. 不跨多个 MBD 阶段给结论（例如未审查代码生成配置就给“生成代码不合规”的结论）
2. 不吞并上下游职责（例如 `coverage-gap-analyzer` 不直接重构模型）
3. 可以指出候选方向,但必须标注“不负责最终结论”的边界
4. 输入不足时优先输出“缺口清单（Gap List）”,而不是补全假设
5. 工具上下文不一致时（例如生成代码版本与模型版本不匹配）必须显式标注并降级

## 4. 编排技能（Workflow Skill）边界规则

1. 负责顺序、门禁（Gate）、汇总,不替代原子技能的专业分析细节
2. 任何跨阶段结论都必须引用上游工件（Artifact）
3. 可根据场景裁剪步骤,但必须说明跳过原因与风险
4. 必须在输出中显式列出尚未完成的阶段与未满足门禁
5. 与 `fmt/` 工作流（如 `fmt-flight-control-param-optimizer`）衔接时,必须显式声明工件转换关系（模型侧工件 ↔ 飞行验证工件）

## 5. 证据纪律（Evidence Discipline）

1. 模型结论：给出模型路径 + 子系统路径(如 `model.slx > Controller/PID`) + 信号/参数名,并区分事实（Fact）与推断（Inference）
2. 数据字典结论：给出 `.sldd` 路径 + 对象名 + 作用域
3. 生成代码结论：给出代码文件路径 + 行号 + 与模型对象的回链关系
4. 验证结论：给出测试用例 ID + 覆盖率报告位置 + 信号/时间窗
5. 无法确认时写“不确定项（Unknowns）”,不要写成确定性结论

## 6. 输出语言约定（Language Convention）

1. 默认中文输出
2. 专业术语首次出现附英文注释（例如：状态机（State Machine）、原子子系统（Atomic Subsystem）、存储类（Storage Class））
3. 保留信号名、参数名、子系统名、Bus 名、生成函数名原文

## 7. 质量门禁（Quality Gates）最低要求

1. 触发准确性（Trigger Accuracy）：明确何时使用、何时不使用、面向哪种工具上下文
2. 边界纯度（Boundary Purity）：不越权给下游结论
3. 证据可追溯性（Evidence Traceability）：关键结论可回链到模型/字典/代码/验证证据
4. 交接可用性（Handoff Usability）：下游可直接消费输出（含 `fmt/` 库下游）
5. 失败可控性（Failure Containment）：输入不足时能安全降级
6. 工具上下文显式性（Tool Context Explicitness）：版本/形态/缺失部分均显式记录

## 8. 推荐的优化顺序（Optimization Order）

1. 先收紧边界（做什么 / 不做什么 / 工具上下文）
2. 再定义交接工件（Artifact Contract）
3. 再补质量门禁（Quality Gates）
4. 最后优化模板与示例（避免一开始堆细节）
