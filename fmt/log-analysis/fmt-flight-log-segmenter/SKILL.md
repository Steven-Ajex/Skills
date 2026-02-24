---
name: fmt-flight-log-segmenter
description: 基于已解码的 FMT 飞行日志数据，对飞行阶段（起飞/巡航/过渡/返航/降落等）进行分段并建立关键事件索引的专用技能。用于为后续控制性能分析和调参报告提供时间段上下文；不负责底层二进制解码或最终调参建议。
---

# FMT Flight Log Segmenter

## 目标

把“长日志”切成可解释的飞行阶段与关键事件段，形成后续分析的时间索引。

## 第一性原理任务定义（First-Principles Task Definition）

1. 最小任务单元（Minimum Task Unit）
   - 在已解码的单次飞行日志时间轴上，完成飞行阶段分段与关键事件索引，并给出可复现的分段规则。
2. 核心输入（Inputs）
   - 已解码结构化日志数据（至少包含时间轴与核心状态/控制信号）
   - 机型变体信息（`vtol` / `mc` / `fw`）
   - 可选 `ulog` 事件文本或任务背景说明
3. 核心输出（Outputs）
   - 主交付工件：`flight_phase_segments`
   - 阶段时间轴、关键事件索引、分段依据与质量问题列表
   - 供性能分析使用的推荐观察窗口与注意事项
4. 完成判据（Definition of Done, DoD）
   - 分段规则可复现（字段、阈值、条件清楚）
   - VTOL 过渡段与非 VTOL 规则不混写
   - 边界模糊和缺数据段被显式标注
5. 输出语言约定（Language Convention）
   - 默认中文输出；专业术语首次出现附英文注释（English Annotation）。
   - 保留参数名、信号名、结构体名、函数名原文，避免翻译造成歧义。

## 前置输入（理想）

1. 已解码 `mlog` 数据（至少包含 `FMS_Out`, `INS_Out`, `Control_Out`）
2. 可选 `ulog.txt`（用于辅助事件解释）
3. 当前机型变体信息（`vtol` / `mc` / `fw`）

## 聚焦范围（只做这些）

1. 飞行阶段划分（Flight Phase Segmentation）
2. 关键事件索引（解锁、模式切换、过渡、异常、降落等）
3. 分段质量评估（数据缺失/状态不连续）

## 不负责

1. `mlog` 二进制解码
2. 控制参数调优建议
3. 深入控制器根因分析

## 分段优先信号（FMT 推荐）

1. `FMS_Out.status`
2. `FMS_Out.state`
3. `FMS_Out.ext_state`（VTOL 重点）
4. `FMS_Out.mode` / `FMS_Out.ctrl_mode`
5. `Control_Out.actuator_cmd`
6. `INS_Out` 高度/速度/姿态变化

## 执行步骤

1. 检查关键信号是否存在、时间轴是否可用。
2. 用 `FMS_Out` 字段建立主分段（模式/状态驱动）。
3. 用 `INS_Out` 与执行器输出修正边界（例如起飞/着陆窗口）。
4. 对 VTOL 日志单独标出过渡段（`ext_state` 变化）。
5. 建立事件索引表（timestamp、事件类型、证据信号）。

## 输出要求

至少包含：

1. 飞行阶段时间轴（阶段名、起止时间）
2. 关键事件索引（含证据信号）
3. 分段依据说明（字段与阈值/规则）
4. 分段质量问题（缺数据、状态跳变、边界模糊）
5. 对后续性能分析的建议观察窗口

## 上下游交接（Artifact Handoff）

1. 上游依赖（Upstream Dependencies）
   - `fmt-mlog-decoder` 或等效结构化日志输入
   - `fmt-fms-state-machine-reader`（推荐，用于状态语义）
2. 下游使用方（Downstream Consumers）
   - `fmt-control-performance-analyzer`
   - `fmt-tuning-report-writer`
   - `fmt-flight-control-param-optimizer`
3. 主交付工件（Primary Artifact）
   - `flight_phase_segments`
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
   - 分段门禁：每个关键阶段边界必须对应证据信号或状态字段变化。
2. 自检建议（Self Check）
   - 可使用 `fmt/_meta/quality-scorecard.md` 对本次输出进行快速打分（至少检查 IO 契约、证据、降级策略）。

## 失败与降级策略（Failure / Fallback）

1. 输入不足处理
   - 缺失 `FMS_Out` 时：可用 `INS_Out` + 执行器信号做近似分段，但必须降级置信度
   - 时间轴不连续时：分段结果按连续片段分别输出，不给全局连续结论
2. 输出降级要求
   - 降级输出时必须显式标注受影响结论、受影响范围与置信度变化。
   - 降级不等于跳步；不得越过本技能职责直接给下游最终结论。

## references/ 使用建议

1. 快速输出时，先加载 `references/output-template.md` 作为骨架，避免遗漏交接字段。
2. 正式交付前，加载 `references/checklist.md` 做边界、证据、降级策略复核。
3. 专项提示：进行阶段划分时先按模板固化规则；交付前用清单复核可复现性和边界证据。

## 纪律约束

1. 分段规则要可复现（写清用哪些字段和阈值/条件）。
2. 不把性能现象当成分段依据的唯一来源。
3. VTOL 与非 VTOL 的规则分开说明。
