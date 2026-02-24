---
name: fmt-fms-state-machine-reader
description: 读取 FMT-Firmware FMS 模块的状态机与模式切换逻辑（status/state/ext_state/ctrl_mode/mode），梳理状态集合、触发条件、切换路径和输出语义的专用技能。用于需要专门分析 FMS 行为、模式切换、过渡段逻辑而不是整个控制律或日志解码时。
---

# FMT FMS State Machine Reader

## 目标

对 FMS 状态机（State Machine）与模式管理逻辑建立准确认识，并输出可用于后续飞行日志分段与行为解释的“状态语义说明”。

## 第一性原理任务定义（First-Principles Task Definition）

1. 最小任务单元（Minimum Task Unit）
   - 在单一 FMS 变体范围内，完成状态机（State Machine）状态集合、切换条件、输出语义与日志可观测字段的证据化说明。
2. 核心输入（Inputs）
   - 目标 FMS 变体目录（如 `vtol_fms`）
   - `fms_interface.c` 与生成代码（`FMS.c`/`FMS_types.h` 等）可读
   - 用户关注的模式/状态问题（过渡段、自动模式、故障回退等，可选）
3. 核心输出（Outputs）
   - 主交付工件：`fms_state_semantics`
   - 状态/模式语义表、触发源清单、关键转换路径与输出影响
   - 供日志分段使用的字段建议与注意事项
4. 完成判据（Definition of Done, DoD）
   - 至少覆盖一组关键状态转换链（触发条件 -> 状态变化 -> 输出变化）
   - 接口层字符串映射与生成代码真实切换逻辑已区分
   - 明确当前机型变体及 VTOL 特有字段适用性
5. 输出语言约定（Language Convention）
   - 默认中文输出；专业术语首次出现附英文注释（English Annotation）。
   - 保留参数名、信号名、结构体名、函数名原文，避免翻译造成歧义。

## 聚焦范围（只做这些）

1. `FMS_Out` 关键字段语义（`status/state/ext_state/ctrl_mode/mode/reset/...`）
2. 状态集合与模式集合
3. 切换触发输入（Pilot/GCS/Auto/Mission/INS/Control 等）
4. 状态切换路径与关键条件
5. 状态切换对输出命令的影响（高层语义层面）

## 不负责

1. 控制器增益与执行器输出调参
2. `mlog` 文件解码
3. 日志阶段划分（可为后续技能提供语义基础）

## 推荐阅读顺序（以 VTOL 为例）

1. `src/model/fms/vtol_fms/fms_interface.c`
2. `src/model/fms/vtol_fms/lib/FMS.h`
3. `src/model/fms/vtol_fms/lib/FMS_types.h`
4. `src/model/fms/vtol_fms/lib/FMS.c`
5. 相关状态消费方（如 `task/status/task_status.c`、Controller 接口）

## 执行步骤

1. 先从 `fms_interface.c` 提取状态/模式字符串映射和 `FMS_Out` bus 字段。
2. 列出 FMS 输入源（Pilot/GCS/Auto/Mission/INS/Control）。
3. 在 `FMS.c` 中定位状态机状态变量和切换分支（必要时按关键词/枚举追踪）。
4. 将“切换条件 -> 状态变化 -> 关键输出字段变化”整理成表。
5. 标出 VTOL 特有字段（如 `ext_state`）和普通机型差异点。

## 输出要求

至少包含：

1. 状态/模式字段语义表（中文 + 英文术语）
2. 状态切换触发源清单
3. 关键转换路径（含证据）
4. 对飞行日志分段有用的字段建议（例如用哪些字段分起飞/过渡/降落）
5. 不确定项（生成代码内难以快速确认的条件）

## 上下游交接（Artifact Handoff）

1. 上游依赖（Upstream Dependencies）
   - `fmt-mbd-interface-reader`（推荐）或已确认的 FMS 变体目录
2. 下游使用方（Downstream Consumers）
   - `fmt-flight-log-segmenter`
   - `fmt-control-performance-analyzer`
   - `fmt-tuning-report-writer`
   - `fmt-flight-control-param-optimizer`
3. 主交付工件（Primary Artifact）
   - `fms_state_semantics`
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
   - 语义门禁：状态字段含义必须以代码定义为准，不用日志现象反推替代代码证据。
2. 自检建议（Self Check）
   - 可使用 `fmt/_meta/quality-scorecard.md` 对本次输出进行快速打分（至少检查 IO 契约、证据、降级策略）。

## 失败与降级策略（Failure / Fallback）

1. 输入不足处理
   - 若生成代码状态逻辑难以快速确认：先交付接口层语义与疑难状态清单，标注低置信度区域
   - 若跨变体问题：拆成多个变体对照，不写统一规则
2. 输出降级要求
   - 降级输出时必须显式标注受影响结论、受影响范围与置信度变化。
   - 降级不等于跳步；不得越过本技能职责直接给下游最终结论。

## references/ 使用建议

1. 快速输出时，先加载 `references/output-template.md` 作为骨架，避免遗漏交接字段。
2. 正式交付前，加载 `references/checklist.md` 做边界、证据、降级策略复核。
3. 专项提示：分析模式切换或为日志分段建立状态语义时加载模板；用清单防止把日志现象反推成代码逻辑。

## 分析纪律

1. 区分接口层“状态名映射”与生成代码“真实切换逻辑”。
2. 不用日志现象反推状态机，先看代码证据。
3. 说明当前分析变体（`vtol_fms` / `mc_fms` / `fw_fms`）。
