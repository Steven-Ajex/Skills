---
name: fmt-flight-control-param-optimizer
description: 面向 FMT-Firmware 的端到端飞控参数优化编排技能，用于在一个任务中协调代码理解、日志链路理解、`mlog` 解码、飞行阶段分段、控制性能分析与调参报告输出。适用于需要完整流程而非单点能力的场景；若只需子任务，优先使用 `fmt/` 目录下对应原子技能。
---

# FMT Flight Control Param Optimizer (Workflow)

## 角色定位

这是编排型技能（workflow skill），负责决定步骤顺序、检查前置条件、汇总结论。

它不应替代所有原子技能的专业判断；在执行中优先调用原子技能的思维边界。

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

## 何时引导用户改用原子技能

在以下情况应明确建议改用原子技能：

1. 用户只问 FMS 状态机
2. 用户只问 mlog 格式或日志解码
3. 用户只要报告整理，不需要重新分析

这样可以提升准确性并减少上下文冗余。
