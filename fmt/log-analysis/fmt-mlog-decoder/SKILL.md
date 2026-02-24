---
name: fmt-mlog-decoder
description: 面向 FMT-Firmware 的 `mlog` 二进制日志解码专用技能，负责识别日志头、提取 bus schema、解析消息流并形成结构化信号表。用于已拿到 `mlog*.bin` 文件、需要先完成日志格式与数据解码时；不负责飞行阶段分段或控制性能结论。
---

# FMT Mlog Decoder

## 目标

把 `mlog` 文件从二进制记录流还原成可分析的数据结构（schema + records + 时间轴）。

## 第一性原理任务定义（First-Principles Task Definition）

1. 最小任务单元（Minimum Task Unit）
   - 在单个或一组 `mlog` 二进制文件范围内，完成 header/schema/record 的结构化解码与完整性评估，不输出控制性能结论。
2. 核心输入（Inputs）
   - `mlog*.bin` 文件（或二进制流）
   - 对应版本的 FMT `mlog` 格式线索（代码或已知版本信息）
   - 目标导出格式需求（表格/CSV/Parquet-ready，可选）
3. 核心输出（Outputs）
   - 主交付工件：`mlog_decode_summary`（含解码摘要、schema、完整性）
   - 结构化数据引用（或字段清单/导出路径说明）
   - 下游分段与性能分析需要的关键信号可用性清单
4. 完成判据（Definition of Done, DoD）
   - 先完成 schema 解析再进入 records 解码
   - 明确解码成功率、损坏/截断范围与恢复范围
   - 字段名、类型、时间戳来源可说明且可复现
5. 输出语言约定（Language Convention）
   - 默认中文输出；专业术语首次出现附英文注释（English Annotation）。
   - 保留参数名、信号名、结构体名、函数名原文，避免翻译造成歧义。

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

## 上下游交接（Artifact Handoff）

1. 上游依赖（Upstream Dependencies）
   - `fmt-logging-pipeline-reader`（推荐，用于格式线索）或等效源码线索
2. 下游使用方（Downstream Consumers）
   - `fmt-flight-log-segmenter`
   - `fmt-control-performance-analyzer`
   - `fmt-tuning-report-writer`
   - `fmt-flight-control-param-optimizer`
3. 主交付工件（Primary Artifact）
   - `mlog_decode_summary`
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
   - 格式门禁：未知 schema 时禁止靠固定 payload 长度硬编码解码。
2. 自检建议（Self Check）
   - 可使用 `fmt/_meta/quality-scorecard.md` 对本次输出进行快速打分（至少检查 IO 契约、证据、降级策略）。

## 失败与降级策略（Failure / Fallback）

1. 输入不足处理
   - 日志损坏时：输出可恢复时间段与不可恢复段，不跨到性能结论
   - 版本不匹配时：先做版本差异记录，必要时停止并请求对应源码/版本信息
2. 输出降级要求
   - 降级输出时必须显式标注受影响结论、受影响范围与置信度变化。
   - 降级不等于跳步；不得越过本技能职责直接给下游最终结论。

## references/ 使用建议

1. 快速输出时，先加载 `references/output-template.md` 作为骨架，避免遗漏交接字段。
2. 正式交付前，加载 `references/checklist.md` 做边界、证据、降级策略复核。
3. 专项提示：执行 mlog 解码时先用模板组织输出；交付给 segmenter/analyzer 前用清单确认 schema、时间轴、完整性信息齐全。

## 纪律约束

1. 先解析 schema，再解析 records，避免硬编码字段长度。
2. 不在本技能里给控制结论。
3. 如果日志损坏，优先报告恢复范围，不继续推断性能问题。
