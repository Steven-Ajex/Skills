# Control Law MBD Skills 仓库组织与管理逻辑

用于后续持续新增控制律 MBD 相关 skills 时保持结构稳定、命名一致、职责清晰。

## 1. 组织逻辑（Repository Taxonomy）

### 一级：按 MBD 流程阶段分层，而不是按工具厂商分层

当前规划五层：

1. `model-reading/`：模型/字典/需求理解
2. `model-authoring/`：建模与重构
3. `codegen-bridge/`：代码生成与桥接
4. `verification/`：MIL / SIL / PIL / HIL 验证
5. `workflows/`：编排型技能

原因：

- 工具会随版本/许可证变化（Simulink、Embedded Coder、SLDV、Polyspace、HIL 平台）
- MBD 流程阶段相对稳定，按阶段分层利于复用
- 避免“同一能力按工具复制多份 skill”

### 二级：技能按最小能力单元命名

命名格式：

- 前缀统一 `clm-`（control-law-mbd 简写，避免与 `fmt-` 等领域库冲突）
- 中间写能力对象（model / dictionary / coder-config / coverage 等）
- 末尾写动作（`reader` / `author` / `refactor` / `reviewer` / `mapper` / `governor` / `builder` / `analyzer` / `pipeline`）

示例：

- `clm-simulink-model-reader`
- `clm-embedded-coder-config-reviewer`
- `clm-coverage-gap-analyzer`

## 2. 新增 Skill 的设计流程（建议）

1. 先判断是“原子技能”还是“编排技能”
2. 检查是否与已有技能职责重叠（特别是 `model-reading/` 与 `codegen-bridge/` 的边界）
3. 按第一性原理写清最小任务单元、完成判据（DoD）、失败/降级策略
4. 写清输入/输出边界与工具上下文（Simulink 版本、模型形态：`.slx`/`.sldd`/生成代码/覆盖率报告）
5. 对齐共享规范（`_meta/first-principles-skill-contract.md`、`_meta/artifact-handoff-contract.md`）
6. 只在该 skill 内放必要知识；详细模板放 `references/`
7. 在 `control-law-mbd/README.md` 更新目录与使用时机

## 3. 何时新增新 Skill,何时扩展旧 Skill

### 新增新 Skill（优先）

满足任一条件时应新增：

1. 新能力可以独立完成一个子任务（单工具、单阶段）
2. 新能力需要不同输入/输出边界（如从“模型”切换到“生成代码”）
3. 新能力会显著扩大现有 skill 的触发范围（导致误触发）
4. 新能力需要明显不同的专业方法（如频域设计、故障注入、形式化验证）

### 扩展旧 Skill

满足以下条件时可直接扩展：

1. 只是增加同一阶段的规则/检查项（如 Embedded Coder 新增一类配置检查）
2. 不改变触发范围本质
3. 不会让 skill 跨越多个 MBD 阶段

## 4. 工具与版本变体管理

原则：

1. 能共用方法论就共用 skill（例如“数据字典阅读”跨 Simulink 版本基本通用）
2. 工具版本差异大且会影响分析步骤时，再拆分变体或在 skill 内部加“版本分叉”

推荐做法：

- 先在通用 skill 中写“版本/工具上下文确认步骤”
- 当版本差异变得复杂时，再新增：
  - `clm-r2024b-coder-config-reviewer`（举例，仅在确有差异时）
  - `clm-polyspace-mcdc-analyzer`（与 SLDV 流程明显不同时）

## 5. 仓库管理规则（Git / 版本）

### 5.1 提交粒度

建议按以下粒度提交：

1. `feat(clm-skills): add <skill-name>`
2. `refactor(clm-skills): split <old-skill> into ...`
3. `docs(clm-skills): update catalog or management rules`
4. `fix(clm-skills): tighten trigger description for <skill-name>`

亦可沿用仓库现有 `[FEAT](control-law-mbd): ...` 风格,与 `fmt-skills` 提交风格保持一致。

### 5.2 变更同步规则

新增或修改 skill 时,至少同步更新：

1. `control-law-mbd/README.md`（技能目录与使用时机）
2. 对应 skill 的 `SKILL.md`
3. （如适用）对应 skill 的 `references/`
4. （如修改了通用规则）`control-law-mbd/_meta/*.md`

### 5.3 弃用（Deprecation）规则

不要直接删除正在使用的 skill。先做两步：

1. 在旧 skill 的 `SKILL.md` 中注明替代 skill（如有）
2. 在 `control-law-mbd/README.md` 标注 deprecated 状态与迁移路径

## 6. 推荐的后续扩展清单（Backlog Seeds）

模型理解类：

- `clm-bus-object-mapper`（专注 Bus / Bus Object 与生成代码结构体的映射）
- `clm-sample-time-consistency-checker`
- `clm-virtual-vs-atomic-subsystem-analyzer`

建模与重构类：

- `clm-anti-windup-author`
- `clm-gain-scheduling-author`
- `clm-fixed-point-refactor`

代码生成与桥接类：

- `clm-tlc-customization-reviewer`
- `clm-step-function-entrypoint-mapper`
- `clm-shared-utility-deduper`

验证类：

- `clm-sldv-property-author`
- `clm-polyspace-runtime-error-analyzer`
- `clm-fault-injection-test-author`
- `clm-flight-log-replay-bridge`（与 `fmt/log-analysis/*` 的衔接桥）

工作流类：

- `clm-model-to-deploy-handoff`
- `clm-mbd-regression-comparison`（多版本模型对比）

## 7. 质量门槛（每个 Skill 最低要求）

1. 描述能准确触发（写清何时使用、何时不使用、面向哪种工具上下文）
2. 边界清晰（写清不负责什么、不会跨越的 MBD 阶段）
3. 输入/输出与交接工件明确（下游可复用）
4. 明确失败与降级策略（输入不足时不跳步）
5. 至少一个专业检查点（不是泛泛流程）
6. 与 `fmt/` 库的衔接点明确（如有）
