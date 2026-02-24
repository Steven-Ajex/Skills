# FMT Logging Pipeline Reader 输出模板

## 使用说明

- 目标：输出 FMT 嵌入式日志系统（mlog/ulog）的触发、记录、缓冲与刷盘机制，以及可靠性风险点。
- 主交付工件（Primary Artifact）：`logging_pipeline_map`
- 默认中文输出；专业术语首次出现附英文注释（English Annotation）。

## 基本信息（Basic Context）

- `task_id`：
- `skill_name`：
- `artifact_name`：`logging_pipeline_map`
- `variant`（`vtol` / `mc` / `fw` / `unknown`）：
- `scope`（代码路径 / 日志文件 / 时间段）：
- `version_or_branch`：

## 范围与假设（Scope & Assumptions）

- [ ] mlog / ulog / 两者
- [ ] 自动启停与手动命令入口
- [ ] 日志任务与刷盘路径
- 事实（Fact）与推断（Inference）边界说明：

## 输入摘要（Input Summary）

- [ ] task_logger.c
- [ ] mlog.h/mlog.c
- [ ] task_status.c
- [ ] cmd_mlog.c
- 输入缺口（Gaps）：

## 工件正文（Artifact Body）

### 日志链路时序

- 说明：按 生产 -> 缓冲 -> 事件 -> 刷盘 -> 关闭 写出机制路径。
- 内容：

### 自动/手动启停规则

- 说明：说明 arm/disarm 和 cmd_mlog 的触发条件。
- 内容：

### mlog vs ulog 职责对比

- 说明：说明两类日志的定位与使用方式。
- 内容：

### 可靠性风险点

- 说明：写出缓冲满、掉电、刷盘时机等风险及代码证据。
- 内容：

### 给 decoder 的格式线索

- 说明：列出 mlog 结构体/版本号/状态机线索。
- 内容：

## 关键事实（Facts）

- Fact-1：
- Fact-2：

## 关键推断（Inferences）

- Inference-1（置信度：高/中/低）：
- Inference-2（置信度：高/中/低）：

## 证据索引（Evidence Index）

- 代码证据：`path/to/file.c:line` -> 结论
- 代码证据：`path/to/file.h:line` -> 结论

## 缺口与风险（Gaps & Risks）

- 缺口：
- 风险：
- 降级策略：

## 下游输入建议（Next Skill Inputs）

- 推荐下游技能：
- 建议关注字段/信号/路径：
- 需要补充的数据或确认项：

## 质量门禁自检（简表）

- [ ] 边界纯度（Boundary Purity）：没有越权给下游/上游结论
- [ ] 证据可追溯（Evidence Traceability）：关键结论可回链到代码/日志证据
- [ ] 交接可用性（Handoff Usability）：下游技能可直接使用本输出
- [ ] 失败/降级说明完整：输入缺口、受影响结论、置信度变化已标注

## 共享规范引用

- `fmt/_meta/first-principles-skill-contract.md`
- `fmt/_meta/artifact-handoff-contract.md`
- `fmt/_meta/quality-scorecard.md`
