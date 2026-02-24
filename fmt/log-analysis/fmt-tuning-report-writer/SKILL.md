---
name: fmt-tuning-report-writer
description: 将 FMT 飞行日志分析结果整理为结构化控制参数优化报告与下一轮试飞验证计划（Test Card）的专用技能。用于在已有代码理解和日志分析证据的基础上输出高质量报告；不负责生成证据或解码日志。
---

# FMT Tuning Report Writer

## 目标

把已有分析证据整理成一份可执行、可复飞验证、可追踪的参数优化报告。

默认用中文输出；专业术语首次出现时附英文注释。

## 第一性原理任务定义（First-Principles Task Definition）

1. 最小任务单元（Minimum Task Unit）
   - 在已有代码理解与日志分析证据基础上，输出可执行、可验证、可追踪的参数优化报告与试飞验证计划，不新增分析证据。
2. 核心输入（Inputs）
   - 代码理解工件（至少控制结构与日志链路）
   - 日志分析工件（现象、证据、候选根因）
   - 参数快照/当前参数列表与任务目标
3. 核心输出（Outputs）
   - 主交付工件：`tuning_recommendation_report`
   - 结构化报告、参数建议条目、风险与副作用、Test Card
   - 未闭环问题与待补数据清单
4. 完成判据（Definition of Done, DoD）
   - 每条建议都有证据回链、风险与验证指标
   - 候选根因与确定性结论被明确区分
   - 缺失证据时输出缺口与补试建议，而非凑结论
5. 输出语言约定（Language Convention）
   - 默认中文输出；专业术语首次出现附英文注释（English Annotation）。
   - 保留参数名、信号名、结构体名、函数名原文，避免翻译造成歧义。

## 前置输入（必需）

1. 代码理解结论（至少包含控制结构与日志链路）
2. 日志分析结论（现象、证据、候选根因）
3. 参数快照或当前参数列表（建议）
4. 机型与任务背景

## 聚焦范围（只做这些）

1. 报告结构化输出
2. 调参建议条目化
3. 风险与副作用说明
4. 下一轮试飞验证计划（Test Card）

## 不负责

1. 新的代码阅读结论
2. 新的日志解码
3. 新的控制性能计算

## 报告骨架（默认）

1. 任务背景（机型、目标、日志来源、版本）
2. 代码侧理解摘要（调度/INS/FMS/Controller/日志链路）
3. 日志数据完整性与分析范围
4. 飞行阶段与关键事件摘要
5. 关键现象与证据（按严重度）
6. 候选根因（分层：INS/FMS/Controller/执行器）
7. 参数优化建议（分优先级）
8. 风险与副作用
9. 下一轮试飞验证计划（Test Card）
10. 不确定项与待补数据

## 每条调参建议的必填字段

1. 目标现象
2. 证据时间段与信号
3. 候选参数（如 `CONTROL.xxx` / `FMS.xxx` / `INS.xxx`）
4. 调整方向（增大/减小）
5. 预期效果
6. 风险/副作用
7. 验证指标与通过条件

## 上下游交接（Artifact Handoff）

1. 上游依赖（Upstream Dependencies）
   - 代码阅读类工件（至少一项）
   - `control_performance_findings`（推荐）
2. 下游使用方（Downstream Consumers）
   - `fmt-flight-control-param-optimizer` 或最终交付给飞控工程师
3. 主交付工件（Primary Artifact）
   - `tuning_recommendation_report`
   - 工件至少包含：分析范围（scope）、关键事实（facts）、关键推断（inferences）、证据索引（evidence index）、缺口清单（gaps）、下游输入建议（next skill inputs）。
4. 共享规范（Shared Contracts）
   - 参考 `fmt/_meta/first-principles-skill-contract.md`
   - 参考 `fmt/_meta/artifact-handoff-contract.md`

## 质量门禁（Quality Gates）

1. 必过门禁（Mandatory Gates）
   - 边界门禁（Boundary Purity）：不输出超出本技能职责的确定性结论。
   - 证据门禁（Evidence Traceability）：关键结论必须能回链到代码路径行号或日志时间段。
   - 变体门禁（Variant Scope）：明确 `vtol/mc/fw` 适用范围，未知时标注 `unknown`。
   - 交接门禁（Handoff Usability）：输出可被下游技能直接消费，不只给散文式描述。
   - 可执行性门禁：每条调参建议必须包含验证指标与通过条件。
2. 自检建议（Self Check）
   - 可使用 `fmt/_meta/quality-scorecard.md` 对本次输出进行快速打分（至少检查 IO 契约、证据、降级策略）。

## 失败与降级策略（Failure / Fallback）

1. 输入不足处理
   - 证据不足时：输出“调参前置条件未满足”报告，而不是给具体参数改值
   - 参数快照缺失时：明确建议补采/导出参数快照并限制建议粒度
2. 输出降级要求
   - 降级输出时必须显式标注受影响结论、受影响范围与置信度变化。
   - 降级不等于跳步；不得越过本技能职责直接给下游最终结论。

## references/ 使用建议

1. 快速输出时，先加载 `references/output-template.md` 作为骨架，避免遗漏交接字段。
2. 正式交付前，加载 `references/checklist.md` 做边界、证据、降级策略复核。
3. 专项提示：生成正式调参报告和 Test Card 时先套模板；交付前用清单复核证据回链、风险和验证条件。

## 纪律约束

1. 不要编造未提供的证据。
2. 不要把候选根因写成确定结论（除非证据充分）。
3. 对缺失数据明确标注，不用空泛话术填充。
