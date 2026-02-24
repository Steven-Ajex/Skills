---
name: fmt-logging-pipeline-reader
description: 读取 FMT-Firmware 的嵌入式日志记录链路（`mlog`/`ulog`）并梳理日志任务、启停触发、缓冲与刷盘机制、命令入口和日志使用方式的专用技能。用于理解日志系统架构和日志可靠性风险，不负责飞行日志内容解码与控制性能分析。
---

# FMT Logging Pipeline Reader

## 目标

弄清 FMT 的日志系统是如何“被触发、被写入、被落盘、被使用”的，输出日志链路结构与风险点说明。

## 第一性原理任务定义（First-Principles Task Definition）

1. 最小任务单元（Minimum Task Unit）
   - 在 FMT 嵌入式日志系统范围内，完成 `mlog/ulog` 触发、记录、缓冲、刷盘与使用路径的机制级梳理，不进入日志内容解码。
2. 核心输入（Inputs）
   - `task_logger`、`mlog`、`ulog`、状态任务与命令入口相关源码可读
   - 目标日志类型（`mlog` / `ulog` / 两者）与关注点（可靠性、启停、刷盘时机）
3. 核心输出（Outputs）
   - 主交付工件：`logging_pipeline_map`
   - 日志链路时序、自动/手动启停规则、缓冲与刷盘机制、可靠性风险点
   - 供 `fmt-mlog-decoder` 使用的格式与链路线索（来源文件/结构体/状态）
4. 完成判据（Definition of Done, DoD）
   - 已区分日志记录机制问题与日志内容语义问题
   - 至少串起一条 `mlog` 生命周期路径和一条触发路径（自动或手动）
   - 风险点结论对应具体代码路径或状态条件
5. 输出语言约定（Language Convention）
   - 默认中文输出；专业术语首次出现附英文注释（English Annotation）。
   - 保留参数名、信号名、结构体名、函数名原文，避免翻译造成歧义。

## 聚焦范围（只做这些）

1. `task_logger` 日志任务职责与异步输出机制
2. `mlog` 二进制日志模块结构（头、缓冲、消息写入、异步刷盘）
3. `ulog` 文本日志后端（控制台/文件）
4. arm/disarm 与日志启停关系
5. `cmd_mlog` 手动操作入口

## 不负责

1. `mlog` 二进制具体解码实现
2. 飞行阶段分段
3. 控制器性能分析和调参

## 推荐阅读顺序（FMT-Firmware）

1. `src/task/logger/task_logger.c`
2. `src/module/log/mlog.h`
3. `src/module/log/mlog.c`
4. `src/task/status/task_status.c`
5. `src/module/syscmd/cmd_mlog.c`

## 执行步骤

1. 先识别日志生产者（各模块 `mlog_push_msg(...)` / `ulog_*`）。
2. 再识别日志消费者/刷盘者（`task_logger_entry()` + `mlog_async_output()`）。
3. 梳理 `mlog` 生命周期：`init -> start -> logging -> stop -> flush/close`。
4. 梳理 `ulog` 生命周期与 backend 注册流程。
5. 标出自动启停和手动启停路径，以及配置参数影响。

## 输出要求

至少包含：

1. `mlog`/`ulog` 职责对比
2. 日志链路时序（生产 -> 缓冲 -> 事件 -> 刷盘）
3. 自动启停规则（arm/disarm、参数模式）
4. 手动控制入口（`cmd_mlog`）说明
5. 日志可靠性风险点（缓冲满、丢包、刷盘时机、关机风险等）

## 上下游交接（Artifact Handoff）

1. 上游依赖（Upstream Dependencies）
   - 代码工程可读性（日志相关模块）
2. 下游使用方（Downstream Consumers）
   - `fmt-mlog-decoder`
   - `fmt-tuning-report-writer`
   - `fmt-flight-control-param-optimizer`
3. 主交付工件（Primary Artifact）
   - `logging_pipeline_map`
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
   - 可靠性门禁：所有“丢日志/刷盘风险”判断必须给出触发条件与代码证据。
2. 自检建议（Self Check）
   - 可使用 `fmt/_meta/quality-scorecard.md` 对本次输出进行快速打分（至少检查 IO 契约、证据、降级策略）。

## 失败与降级策略（Failure / Fallback）

1. 输入不足处理
   - 若仅能读取部分日志模块：先输出已确认链路与缺失模块造成的盲区
   - 若 `ulog` 未启用：明确标注为编译配置/运行配置差异，不当作缺陷
2. 输出降级要求
   - 降级输出时必须显式标注受影响结论、受影响范围与置信度变化。
   - 降级不等于跳步；不得越过本技能职责直接给下游最终结论。

## references/ 使用建议

1. 快速输出时，先加载 `references/output-template.md` 作为骨架，避免遗漏交接字段。
2. 正式交付前，加载 `references/checklist.md` 做边界、证据、降级策略复核。
3. 专项提示：理解日志系统机制和可靠性风险时加载模板；输出前用清单确认没有越界到解码或性能分析结论。

## 分析纪律

1. 对日志内容含义的判断留给后续解码/分析技能。
2. 优先区分“记录机制问题”与“控制问题”。
3. 对可靠性结论要基于代码路径和状态机，不凭经验泛化。
