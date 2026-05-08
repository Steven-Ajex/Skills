# clm-coverage-gap-analyzer 输出模板

## 使用说明

- 目标:输出覆盖率三维度细分、缺口分类与闭环路由,支持 `clm-test-harness-builder`(用例增补)与 `clm-codegen-compliance-refactor`(模型重构)接力
- 主交付工件(Primary Artifact):`coverage_gap_report`
- 默认中文输出;专业术语首次出现附英文注释

## 基本信息(Basic Context)

- `task_id`:
- `skill_name`:`clm-coverage-gap-analyzer`
- `artifact_name`:`coverage_gap_report`
- `tool_context`:
  - 覆盖率工具与版本:
  - 报告形态(HTML / XML / cvt / 自定义):
  - 维度配置(Decision / Condition / MCDC / Stateflow):
  - Filter 状态:
  - 许可证可用性:
- `scope`(被测对象路径 + 覆盖率报告路径):
- `version_or_branch`:

## 范围与假设(Scope & Assumptions)

- [ ] 是否提供 `test_harness_plan`
- [ ] 是否提供 `simulink_model_map` / `stateflow_semantics`
- [ ] 用户关注的覆盖维度
- 事实(Fact)与推断(Inference)边界说明:

## 输入摘要(Input Summary)

- [ ] 覆盖率报告路径
- [ ] 被测对象路径
- [ ] 上游工件清单
- 输入缺口(Gaps):

## 工件正文(Artifact Body)

### 1. 覆盖率细分(Coverage Breakdown)

| 维度 | 总点数 | 覆盖点数 | 覆盖率 % | Filter 抑制点数 | 备注 |
| --- | --- | --- | --- | --- | --- |
| Decision |  |  |  |  |  |
| Condition |  |  |  |  |  |
| MCDC |  |  |  |  |  |
| Stateflow State(若适用) |  |  |  |  |  |
| Stateflow Transition(若适用) |  |  |  |  |  |

### 2. 缺口清单(Gap List)

| 缺口 ID | 模型对象 | 维度 | 分类 | 分类依据 | 闭环路径 | 关联用例分组 / 重构 backlog |
| --- | --- | --- | --- | --- | --- | --- |
| GP-001 | `model.slx > Controller/AttitudeLoop` | Decision | unexercised | 输入未触发 false 分支 | 用例增补 | `clm-test-harness-builder` 边界分组 |
| GP-002 | `model.slx > FaultMonitor/Limiter` | MCDC | unreachable | 条件互斥(见证据) | 显式接受 | 文档化 |
| GP-003 | `model.slx > ModeManager > Active.AttitudeCtrl: Standby → Auto` | Transition | unexercised | 状态切换路径未触发 | 用例增补 | `clm-test-harness-builder` 状态切换分组 |

分类枚举:`unreachable` / `unexercised` / `unstable` / `needs-model-refactor`

### 3. Coverage Filter 审查(Filter Audit)

| Filter ID | 过滤对象 | 理由 | 文档位置 | 是否可审查(是/否) | 审查结论 |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

不可审查 Filter 已升级为正式缺口的清单:

### 4. 状态/转移覆盖(若涉及 Stateflow)

| 状态/转移路径 | 类型 | 是否覆盖 | 缺口 ID(若未覆盖) | 备注 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

依据:`stateflow_semantics` 转移表的非平凡转移清单

### 5. 闭环路由汇总(Closure Routing Summary)

| 路由类型 | 缺口数量 | 关键缺口 ID | 接收 skill / 文档 |
| --- | --- | --- | --- |
| 用例增补 |  |  | `clm-test-harness-builder`(分组级建议) |
| 模型重构 |  |  | `clm-codegen-compliance-refactor` backlog |
| 显式接受 |  |  | 项目级残留风险文档 |

## 关键事实(Facts)

- Fact-1:
- Fact-2:

## 关键推断(Inferences)

- Inference-1(置信度:高/中/低):
- Inference-2(置信度:高/中/低):

## 证据索引(Evidence Index)

- 报告证据:`coverage_report.html#decision-12` → 未覆盖,关联 `model.slx > Controller/AttitudeLoop`
- 模型证据:`model.slx > FaultMonitor/Limiter` → 条件互斥代码 → `unreachable` 推断依据

## 缺口与风险(Gaps & Risks)

- 缺口(例:报告形态未识别 / `test_harness_plan` 未提供 / Filter 大量启用):
- 风险:
- 降级策略:

## 下游输入建议(Next Skill Inputs)

- 推荐下游 skill:
  - `clm-test-harness-builder`(关注:用例增补路由 — 哪类分组需要补强)
  - `clm-codegen-compliance-refactor`(关注:模型重构 backlog)
  - `clm-pil-hil-replay-analyzer`(关注:已显式接受的残留 — 不应有新规约)
- 建议关注的缺口 ID / 模型对象:
- 需要补充的输入或确认项:

## 质量门禁自检(简表)

- [ ] 边界纯度:未运行覆盖率工具 / 未重写用例 / 未修改模型
- [ ] 证据可追溯:每条结论给出报告 + 模型对象路径
- [ ] 工具上下文显式:工具/版本/维度/Filter 已记录
- [ ] 缺口分类纪律:每条缺口落到四类之一
- [ ] Filter 审查纪律:不可审查 Filter 已升级
- [ ] 闭环路由纪律:`unexercised` 指向具体用例分组
- [ ] 交接可用性:下游 skill 可直接使用
- [ ] 失败/降级说明完整

## 共享规范引用

- `../../_meta/first-principles-skill-contract.md`
- `../../_meta/artifact-handoff-contract.md`
- `../../_meta/quality-scorecard.md`
