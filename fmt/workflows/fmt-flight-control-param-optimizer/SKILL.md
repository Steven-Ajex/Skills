---
name: fmt-flight-control-param-optimizer
description: 面向 FMT-Firmware 的端到端飞控参数优化编排技能，用于在一个任务中协调代码理解、日志链路理解、`mlog` 解码、飞行阶段分段、控制性能分析与调参报告输出。适用于需要完整流程而非单点能力的场景；若只需子任务，优先使用 `fmt/` 目录下对应原子技能。
---

# FMT Flight Control Param Optimizer (Workflow)

## 角色定位

这是编排型技能（workflow skill），负责决定步骤顺序、检查前置条件、汇总结论。

它不应替代所有原子技能的专业判断；在执行中优先调用原子技能的思维边界。

默认用中文输出；专业术语首次出现附英文注释。

## 第一性原理工作流定义（First-Principles Workflow Definition）

1. 最小任务单元（Minimum Task Unit）
   - 在给定一次任务输入（代码、日志或二者）下，完成一轮“可证据回链”的 FMT 调参分析闭环或阶段性闭环（代码侧闭环 / 日志侧闭环）。
2. 核心输入（Inputs）
   - 机型变体（`vtol` / `mc` / `fw`）与分析对象版本/分支
   - 代码工程路径（至少 `FMT-Firmware` 可读）
   - 实飞日志或已解码结构化数据（如有）
   - 任务目标与现象描述（例如姿态振荡、过渡段超调、降落抖动）
3. 核心输出（Outputs）
   - 阶段工件清单（上游原子技能产物）
   - 编排汇总结论（代码理解摘要、日志分析摘要、调参建议、验证计划）
   - 缺口清单（Gap List）与下一步需要的数据/试验
4. 完成判据（Definition of Done, DoD）
   - 已明确执行到哪个阶段、哪些阶段被跳过以及原因
   - 所有最终建议均回链到代码证据或日志证据（通过上游工件）
   - 明确区分事实（Fact）、推断（Inference）与待验证项（To Validate）
   - 如果输入不足以支持调参建议，停止在证据分析阶段并输出阻断缺口

## 工件清单与交接约束（Artifact Handoff）

编排技能不直接“重做”原子分析，优先消费以下工件（可部分存在）：

1. `control_loop_map`
2. `mbd_boundary_map`
3. `fms_state_semantics`
4. `logging_pipeline_map`
5. `mlog_decode_summary`（以及结构化数据引用）
6. `flight_phase_segments`
7. `control_performance_findings`
8. `tuning_recommendation_report`（最终阶段）

交接最低字段和门禁检查参考：

1. `fmt/_meta/artifact-handoff-contract.md`
2. `fmt/_meta/first-principles-skill-contract.md`

## 原子技能编排顺序（默认）

代码理解层：

1. `fmt-control-loop-reader`
2. `fmt-mbd-interface-reader`
3. `fmt-fms-state-machine-reader`（如任务涉及模式切换/VTOL 过渡）
4. `fmt-logging-pipeline-reader`

日志分析层：

5. `fmt-mlog-decoder`
6. `fmt-flight-log-segmenter`
7. `fmt-control-performance-analyzer`
8. `fmt-tuning-report-writer`

## 输入场景决策

### 场景 A：只有代码，没有实飞日志

执行到第 4 步停止，输出：

1. 控制结构理解结论
2. 日志链路理解结论
3. 后续需要采集/提供的日志清单

### 场景 B：有日志，但代码理解不完整

至少先完成：

1. `fmt-control-loop-reader`
2. `fmt-mbd-interface-reader`
3. `fmt-logging-pipeline-reader`

再开始日志分析，避免误判。

### 场景 C：已有解码结果和分段结果

直接从：

1. `fmt-control-performance-analyzer`
2. `fmt-tuning-report-writer`

开始，但先验证输入完整性。

## 编排规则（质量控制）

1. 不允许跳过 `mlog` 解码直接做性能分析（除非用户已提供结构化数据）。
2. 不允许跳过飞行阶段分段直接给全局调参建议。
3. 不允许在未确认机型变体时混用 `vtol/mc/fw` 结论。
4. 所有最终建议必须回链到证据（代码位置或日志时间段）。

## 阶段门禁（Stage Gates）

1. `G0` 场景识别门禁：确认是“代码理解任务 / 日志分析任务 / 端到端任务”，并确认机型变体或明确为 `unknown`。
2. `G1` 代码结构门禁：若任务涉及调参解释，至少完成 `fmt-control-loop-reader` + `fmt-mbd-interface-reader` + `fmt-logging-pipeline-reader` 之一组合中的必要项。
3. `G2` 日志可用性门禁：进入日志分析前，确认日志文件完整性或结构化数据可用性；损坏日志应先输出恢复范围。
4. `G3` 分段门禁：进入控制性能分析前，必须有 `flight_phase_segments` 或等效分段结果（含分段依据）。
5. `G4` 证据门禁：进入调参建议前，必须有“现象 -> 证据 -> 候选根因”的链条，且说明置信度。
6. `G5` 验证计划门禁：输出最终建议时必须包含风险、副作用、验证指标与通过条件（Test Card）。

## 失败与中止策略（Failure / Stop Rules）

1. 机型变体不明且显著影响结论时：停止给具体调参建议，先输出变体确认清单。
2. 日志损坏或字段缺失导致无法分段时：停止在 `mlog` 解码/分段阶段，输出恢复范围与补采建议。
3. 缺失参数快照时：可以给方向级（directional）建议，但不输出具体参数值修改量。
4. 代码版本与日志版本明显不匹配时：先标记高风险，避免把代码结论直接映射到日志现象。

## 最终输出要求（编排技能）

汇总输出应包含：

1. 任务背景与目标
2. 代码侧理解摘要（调度、控制结构、状态机、日志链路）
3. 日志解码与完整性摘要
4. 飞行阶段分段与关键事件摘要
5. 控制性能分析与候选根因
6. 参数优化建议（优先级）
7. 下一轮验证计划（Test Card）
8. 不确定项与待补数据

## 编排输出质量要求（Quality Expectations）

1. 汇总内容必须显式标明各阶段工件来源（哪些已完成、哪些缺失）。
2. 对每条调参建议给出优先级（P1/P2/P3）与置信度（高/中/低）。
3. 对无法闭环的问题给出“下一步最小验证动作”（例如补采某段日志、增加某信号记录、复飞某工况）。

## 何时引导用户改用原子技能

在以下情况应明确建议改用原子技能：

1. 用户只问 FMS 状态机
2. 用户只问 mlog 格式或日志解码
3. 用户只要报告整理，不需要重新分析

这样可以提升准确性并减少上下文冗余。
