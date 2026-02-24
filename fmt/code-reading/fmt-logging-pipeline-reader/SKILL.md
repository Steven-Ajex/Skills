---
name: fmt-logging-pipeline-reader
description: 读取 FMT-Firmware 的嵌入式日志记录链路（`mlog`/`ulog`）并梳理日志任务、启停触发、缓冲与刷盘机制、命令入口和日志使用方式的专用技能。用于理解日志系统架构和日志可靠性风险，不负责飞行日志内容解码与控制性能分析。
---

# FMT Logging Pipeline Reader

## 目标

弄清 FMT 的日志系统是如何“被触发、被写入、被落盘、被使用”的，输出日志链路结构与风险点说明。

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

## 分析纪律

1. 对日志内容含义的判断留给后续解码/分析技能。
2. 优先区分“记录机制问题”与“控制问题”。
3. 对可靠性结论要基于代码路径和状态机，不凭经验泛化。
