---
name: fmt-fms-state-machine-reader
description: 读取 FMT-Firmware FMS 模块的状态机与模式切换逻辑（status/state/ext_state/ctrl_mode/mode），梳理状态集合、触发条件、切换路径和输出语义的专用技能。用于需要专门分析 FMS 行为、模式切换、过渡段逻辑而不是整个控制律或日志解码时。
---

# FMT FMS State Machine Reader

## 目标

对 FMS 状态机（State Machine）与模式管理逻辑建立准确认识，并输出可用于后续飞行日志分段与行为解释的“状态语义说明”。

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

## 分析纪律

1. 区分接口层“状态名映射”与生成代码“真实切换逻辑”。
2. 不用日志现象反推状态机，先看代码证据。
3. 说明当前分析变体（`vtol_fms` / `mc_fms` / `fw_fms`）。
