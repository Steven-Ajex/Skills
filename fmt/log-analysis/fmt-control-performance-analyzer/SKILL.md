---
name: fmt-control-performance-analyzer
description: 基于已解码并完成分段的 FMT 飞行日志，对估计器/FMS/Controller 分层进行控制性能分析，提取振荡、超调、延迟、饱和等调参证据并形成候选根因的专用技能。用于调参前的证据分析，不负责最终报告排版或 mlog 解码。
---

# FMT Control Performance Analyzer

## 目标

在不跳过前置步骤的前提下，给出“现象 -> 证据 -> 候选根因”的分层控制分析结论。

## 第一性原理任务定义（First-Principles Task Definition）

1. 最小任务单元（Minimum Task Unit）
   - 在已完成解码与分段的单次飞行日志范围内，对控制表现进行分层（INS/FMS/Controller/Actuator）分析，形成证据化现象与候选根因。
2. 核心输入（Inputs）
   - 已解码结构化日志数据
   - 飞行阶段分段与关键事件索引
   - 机型变体与参数快照（缺失时需显式降级）
3. 核心输出（Outputs）
   - 主交付工件：`control_performance_findings`
   - 现象清单、证据链、候选根因分层、候选参数方向（directional only）
   - 下游报告撰写所需的优先级、置信度与待验证项
4. 完成判据（Definition of Done, DoD）
   - 至少形成一条“现象 -> 证据 -> 候选根因”链条
   - 区分状态机切换瞬态与控制器性能问题
   - 在缺失参数快照时不输出具体参数值修改量
5. 输出语言约定（Language Convention）
   - 默认中文输出；专业术语首次出现附英文注释（English Annotation）。
   - 保留参数名、信号名、结构体名、函数名原文，避免翻译造成歧义。

## 前置输入（建议）

1. 已解码日志数据（结构化）
2. 已完成飞行阶段分段与关键事件索引
3. 机型变体信息（`vtol` / `mc` / `fw`）
4. 当前参数快照（来自 `mlog` header 或独立导出）

## 聚焦范围（只做这些）

1. 估计器侧与控制器侧问题分离（Estimator vs Controller）
2. 状态机切换瞬态与控制性能问题区分
3. 跟踪误差、超调、振荡、稳态误差、饱和等现象分析
4. 候选调参方向的证据提取（不是最终建议）

## 不负责

1. mlog 二进制解码
2. 飞行阶段分段
3. 最终报告与试飞计划编写

## 分析框架（建议顺序）

1. 先看数据质量与估计器健康（INS 有效性、跳变、延迟）
2. 再看 FMS 模式切换是否引入命令突变
3. 最后看 Controller 输出与执行器表现（含饱和、限幅）

## 典型输出结构

1. 现象清单（按严重度）
2. 每个现象的证据：
   - 时间段
   - 相关信号
   - 与阶段/模式的关系
3. 候选根因分层：
   - 估计器 / 状态机 / 控制器 / 执行器 / 传感器
4. 候选参数组（仅指出范围，不直接下最终改值）

## 输出要求

至少包含：

1. 分层分析结论（INS/FMS/Controller）
2. 关键现象与证据表
3. 候选根因列表（含置信度）
4. 候选参数范围（`CONTROL` / `FMS` / `INS`）
5. 需要补充的数据/试验（如无法定性）

## 上下游交接（Artifact Handoff）

1. 上游依赖（Upstream Dependencies）
   - `fmt-mlog-decoder`
   - `fmt-flight-log-segmenter`
   - `fmt-fms-state-machine-reader`（推荐）
2. 下游使用方（Downstream Consumers）
   - `fmt-tuning-report-writer`
   - `fmt-flight-control-param-optimizer`
3. 主交付工件（Primary Artifact）
   - `control_performance_findings`
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
   - 归因门禁：没有分段或模式上下文时，不给全局控制器增益归因结论。
2. 自检建议（Self Check）
   - 可使用 `fmt/_meta/quality-scorecard.md` 对本次输出进行快速打分（至少检查 IO 契约、证据、降级策略）。

## 失败与降级策略（Failure / Fallback）

1. 输入不足处理
   - 缺失参数快照：只给方向级候选参数组与验证建议
   - 关键信号缺失：先给数据缺口导致的分析盲区，再输出可确认的局部现象
2. 输出降级要求
   - 降级输出时必须显式标注受影响结论、受影响范围与置信度变化。
   - 降级不等于跳步；不得越过本技能职责直接给下游最终结论。

## references/ 使用建议

1. 快速输出时，先加载 `references/output-template.md` 作为骨架，避免遗漏交接字段。
2. 正式交付前，加载 `references/checklist.md` 做边界、证据、降级策略复核。
3. 专项提示：进行性能分析时先按模板组织证据链；交付给报告技能前用清单检查归因边界和置信度标注。

## 纪律约束

1. 没有前置分段就不要直接给全局结论。
2. 避免将状态机切换瞬态误判为控制器增益问题。
3. 避免在缺失参数快照时给具体参数值建议。
