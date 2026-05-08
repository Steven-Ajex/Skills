# clm-stateflow-semantics-reader 输出模板

## 使用说明

- 目标:输出 Stateflow Chart 的状态/转移/事件/动作执行顺序语义,支持下游 `verification/`、`requirement-trace`、跨库 `fmt-fms-state-machine-reader` 引用
- 主交付工件(Primary Artifact):`stateflow_semantics`
- 默认中文输出;专业术语首次出现附英文注释

## 基本信息(Basic Context)

- `task_id`:
- `skill_name`:`clm-stateflow-semantics-reader`
- `artifact_name`:`stateflow_semantics`
- `tool_context`:
  - Stateflow / Simulink 版本:
  - Decomposition(Exclusive / Parallel):
  - Execute at Initialization:
  - Super Step / Early Return Logic:
  - Action Language(MATLAB / C):
  - 许可证可用性:
- `scope`(模型路径 + Chart 路径):
- `version_or_branch`:

## 范围与假设(Scope & Assumptions)

- [ ] 目标 Chart 已确定
- [ ] 是否提供 `simulink_model_map`
- [ ] 用户关注的状态/事件/转移
- 事实(Fact)与推断(Inference)边界说明:

## 输入摘要(Input Summary)

- [ ] 模型路径
- [ ] Chart 路径
- [ ] 关注状态/事件/转移
- 输入缺口(Gaps):

## 工件正文(Artifact Body)

### 1. Chart 属性小结

| 属性 | 值 |
| --- | --- |
| Decomposition |  |
| Execute at Initialization |  |
| Super Step |  |
| Early Return Logic |  |
| Action Language |  |
| Initialize Outputs Every Time Chart Wakes Up |  |

### 2. 状态层级树(State Hierarchy)

- 说明:列出状态层级,每个 sub-chart 标注 Decomposition;默认转移用 `[default]` 标注
- 内容:

```
ChartRoot/  [Exclusive]
├─ Init/             [entry: ...; during: ...]
├─ Active/           [Parallel]
│  ├─ AttitudeCtrl/  [Exclusive]
│  │  ├─ [default] Standby
│  │  ├─ Manual
│  │  └─ Auto
│  └─ ModeWatchdog/  [Exclusive]
└─ Fault/
```

### 3. 转移表(Transition Table)

| ID | 源状态 | 目标状态 | event | condition | condition_action | transition_action | 优先级 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 |  |  |  |  |  |  |  |

### 4. 事件清单(Event List)

| 事件名 | 类型(Local/Input/Output) | 触发位置(Broadcast / 上层) | 监听位置 |
| --- | --- | --- | --- |
|  |  |  |  |

### 5. 数据作用域表(Data Scope)

| 名称 | 作用域(Local/Input/Output/Parameter/Constant) | 类型 | 初值 | Min/Max |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

### 6. 完整状态切换路径示例(End-to-End State-Switch Walkthrough)

- 起始状态:
- 触发事件 / 触发条件:
- 路径(逐步):
  1. `Standby` `during`:监控条件 X
  2. `event mode_request[mode == AUTO]/clear_pending` 触发(`condition_action`)
  3. 转移完成,执行 `transition_action`
  4. 进入 `Auto` `entry`:初始化积分项
- 备注(早晚绑定 / Super Step 影响):

### 7. Junction 语义(若涉及)

| Junction 类型 | 位置 | 出入连接 | 备注 |
| --- | --- | --- | --- |
| Connective |  |  |  |
| History |  |  |  |

## 关键事实(Facts)

- Fact-1:
- Fact-2:

## 关键推断(Inferences)

- Inference-1(置信度:高/中/低):
- Inference-2(置信度:高/中/低):

## 证据索引(Evidence Index)

- Chart 证据:`model.slx > ModeManager > Active > AttitudeCtrl > Auto` → entry 动作
- 转移证据:`model.slx > ModeManager > T3` → 条件、动作

## 缺口与风险(Gaps & Risks)

- 缺口(例:许可证缺失 / Chart 加密 / Action Language 混用):
- 风险:
- 降级策略:

## 下游输入建议(Next Skill Inputs)

- 推荐下游 skill:
  - `clm-requirement-trace-reader`(关注:状态/事件 ↔ 需求条目)
  - `clm-test-harness-builder`(关注:状态切换路径作为测试用例骨架)
  - `clm-coverage-gap-analyzer`(关注:状态/转移作为覆盖率维度)
  - `fmt-fms-state-machine-reader`(跨库:状态/事件命名一致性)
- 建议关注的状态/事件/转移:
- 需要补充的输入或确认项:

## 质量门禁自检(简表)

- [ ] 边界纯度:未越权给 Simulink 顶层 / 代码生成结论
- [ ] 证据可追溯:每条结论给出 Chart 路径 + 状态/转移名
- [ ] 工具上下文显式:Stateflow 版本 / Chart 属性 / 许可证已记录
- [ ] 语义纪律:动作类型与转移动作显式区分
- [ ] 交接可用性:下游 skill 可直接使用
- [ ] 失败/降级说明完整

## 共享规范引用

- `../../_meta/first-principles-skill-contract.md`
- `../../_meta/artifact-handoff-contract.md`
- `../../_meta/quality-scorecard.md`
