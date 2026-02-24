# FMT MBD Interface Reader 输出模板

## 使用说明

- 目标：输出接口桥接层与 MBD 生成代码层的职责边界、参数绑定和 bus/topic 映射，避免混淆 glue code 与控制律本体。
- 主交付工件（Primary Artifact）：`mbd_boundary_map`
- 默认中文输出；专业术语首次出现附英文注释（English Annotation）。

## 基本信息（Basic Context）

- `task_id`：
- `skill_name`：
- `artifact_name`：`mbd_boundary_map`
- `variant`（`vtol` / `mc` / `fw` / `unknown`）：
- `scope`（代码路径 / 日志文件 / 时间段）：
- `version_or_branch`：

## 范围与假设（Scope & Assumptions）

- [ ] 目标模块目录（INS/FMS/Controller 变体）
- [ ] *_interface.c 与 lib/ 范围
- [ ] 变体/版本假设
- 事实（Fact）与推断（Inference）边界说明：

## 输入摘要（Input Summary）

- [ ] 目标模块路径
- [ ] 用户关注点（参数绑定/bus 映射/step 入口）
- [ ] 上游 control_loop_map（可选）
- 输入缺口（Gaps）：

## 工件正文（Artifact Body）

### 接口层 vs 生成代码层职责表

- 说明：明确哪些逻辑属于 glue code，哪些属于模型生成代码。
- 内容：

### 参数绑定路径

- 说明：列出 PARAM_GROUP_DEFINE / param_link_variable 的关键路径与证据。
- 内容：

### topic/bus 映射

- 说明：整理输入/输出 topic 与 MLOG_BUS_DEFINE 等映射关系。
- 内容：

### 模型调用入口

- 说明：指出 init/step 调用链与上下文。
- 内容：

### 隐藏复杂度清单

- 说明：标记必须进入生成代码才能确认的逻辑点。
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
