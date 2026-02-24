---
name: fmt-mlog-decoder
description: 面向 FMT-Firmware 的 `mlog` 二进制日志解码专用技能，负责识别日志头、提取 bus schema、解析消息流并形成结构化信号表。用于已拿到 `mlog*.bin` 文件、需要先完成日志格式与数据解码时；不负责飞行阶段分段或控制性能结论。
---

# FMT Mlog Decoder

## 目标

把 `mlog` 文件从二进制记录流还原成可分析的数据结构（schema + records + 时间轴）。

## 聚焦范围（只做这些）

1. 日志头（header）解析
2. bus schema / 字段类型识别
3. 消息流解码（按 `msg_id` 和 payload schema）
4. 时间戳字段抽取与基础对齐准备
5. 参数快照提取（如果日志头包含）

## 不负责

1. 飞行阶段分段
2. 控制性能分析与调参建议
3. FMS 状态机语义解释（只保留字段）

## 执行步骤（FMT 语境）

1. 先从源码确认格式线索（`src/module/log/mlog.h`, `src/module/log/mlog.c`）：
   - 版本号
   - 消息开始/结束标记
   - header 内容组成
2. 解析 header，提取：
   - `model_info`
   - bus 列表（name / elem list）
   - 参数组与参数值快照
3. 建立 `msg_id -> bus schema` 映射。
4. 扫描记录流并解码 payload。
5. 输出结构化结果（至少是表格/字典/CSV/Parquet-ready 结构）。

## 输出要求

至少包含：

1. 解码摘要（版本、bus 数量、参数组数量）
2. bus schema 清单（重点 bus 标记）
3. 解码成功率/完整性说明（是否截断、是否损坏）
4. 结构化数据导出说明（字段名、类型、时间戳）
5. 不确定项（字节序/版本差异/异常帧）

## 纪律约束

1. 先解析 schema，再解析 records，避免硬编码字段长度。
2. 不在本技能里给控制结论。
3. 如果日志损坏，优先报告恢复范围，不继续推断性能问题。
