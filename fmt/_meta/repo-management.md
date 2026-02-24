# FMT Skills 仓库组织与管理逻辑

用于后续持续新增 FMT 相关 skills 时保持结构稳定、命名一致、职责清晰。

## 1. 组织逻辑（Repository Taxonomy）

### 一级：按用途分层，而不是按机型分层

当前使用三层：

1. `code-reading/`：代码结构/逻辑理解
2. `log-analysis/`：日志解码、分段、分析、报告
3. `workflows/`：编排型技能（组合多个原子技能）

原因：

- 机型（VTOL/MC/FW）会横跨多种任务
- 用途分层更利于复用与检索
- 能避免“同一能力按机型复制多份 skill”

### 二级：技能按最小能力单元命名

命名格式：

- 前缀统一 `fmt-`
- 中间写能力对象
- 末尾写动作（`reader` / `decoder` / `segmenter` / `analyzer` / `writer` / `optimizer`）

示例：

- `fmt-fms-state-machine-reader`
- `fmt-mlog-decoder`
- `fmt-control-performance-analyzer`

## 2. 新增 Skill 的设计流程（建议）

1. 先判断是“原子技能”还是“编排技能”
2. 检查是否与已有技能职责重叠
3. 按第一性原理写清最小任务单元、完成判据（DoD）、失败/降级策略
4. 写清输入/输出边界（尤其是前置数据依赖）与交接工件（Artifact）
5. 对齐共享规范（`fmt/_meta/first-principles-skill-contract.md`、`fmt/_meta/artifact-handoff-contract.md`）
6. 只在该 skill 内放必要知识；详细模板放 `references/`
7. 校验结构（`quick_validate.py`）
8. 在 `fmt/README.md` 更新目录与使用时机

## 3. 何时新增新 Skill，何时扩展旧 Skill

### 新增新 Skill（优先）

满足任一条件时应新增：

1. 新能力可以独立完成一个子任务
2. 新能力需要不同输入/输出边界
3. 新能力会显著增加现有 skill 的触发范围（导致误触发）
4. 新能力需要明显不同的专业方法（如频域分析、故障注入分析）

### 扩展旧 Skill

满足以下条件时可直接扩展：

1. 只是增加同一任务的规则/检查项
2. 不改变触发范围本质
3. 不会让 skill 跨越多个专业步骤

## 4. 变体与机型管理（VTOL / MC / FW）

原则：

1. 能共用方法论就共用 skill（例如 mlog 解码）
2. 机型差异大且会影响分析步骤时，再拆分变体 skill

推荐做法：

- 先在通用 FMT skill 中写“变体选择步骤”
- 当变体特有逻辑变得复杂时，再新增：
  - `fmt-vtol-transition-analyzer`
  - `fmt-fw-tecs-tuning-analyzer`
  - `fmt-mc-rate-loop-tuning-analyzer`

## 5. 仓库管理规则（Git / 版本）

### 5.1 提交粒度

建议按以下粒度提交：

1. `feat(fmt-skills): add <skill-name>`
2. `refactor(fmt-skills): split <old-skill> into ...`
3. `docs(fmt-skills): update catalog or management rules`
4. `fix(fmt-skills): tighten trigger description for <skill-name>`

### 5.2 变更同步规则

当新增或修改 FMT skill 时，至少同步更新：

1. `fmt/README.md`（技能目录与使用时机）
2. 对应 skill 的 `SKILL.md`
3. （如适用）对应 skill 的 `references/`
4. （如修改了通用规则）`fmt/_meta/*.md`

### 5.4 批量一致性维护（推荐）

当你批量优化原子技能（例如统一增加门禁、交接字段、语言约定）时，优先使用脚本化维护，减少手工漂移：

1. 使用 `fmt/_meta/scripts/refresh_atomic_skill_contracts.py` 统一刷新原子技能契约块
2. 运行后逐个抽样检查（至少代码阅读类/日志分析类各 1 个）
3. 再执行 `quick_validate.py` 全量校验

### 5.3 弃用（Deprecation）规则

不要直接删除正在使用的 skill。先做两步：

1. 在旧 skill 的 `SKILL.md` 中注明替代 skill（如果有）
2. 在 `fmt/README.md` 标注 deprecated 状态与迁移路径

## 6. 推荐的后续扩展清单（Backlog Seeds）

代码阅读类：

- `fmt-ins-estimator-reader`（更专注 INS/EKF）
- `fmt-actuator-mixer-reader`
- `fmt-parameter-scope-mapper`（参数到代码路径的映射）

日志分析类：

- `fmt-vtol-transition-analyzer`
- `fmt-failure-event-analyzer`
- `fmt-frequency-response-analyzer`（如果后续需要频域）
- `fmt-log-quality-checker`

工作流类：

- `fmt-flight-test-review-workflow`
- `fmt-regression-comparison-workflow`（多架次对比）

## 7. 质量门槛（每个 Skill 最低要求）

1. 描述能准确触发（写清何时使用）
2. 边界清晰（写清不负责什么）
3. 输入/输出与交接工件明确（下游可复用）
4. 明确失败与降级策略（输入不足时不跳步）
5. 至少一个专业检查点（不是泛泛流程）
6. 校验通过（`quick_validate.py`）
