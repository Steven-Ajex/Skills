# clm-codegen-compliance-refactor 输出模板

## 使用说明

- 目标:聚合上游 finding,输出模型层重构方案与排序 backlog
- 主交付工件(Primary Artifact):`compliance_refactor_diff`
- 默认中文输出;专业术语首次出现附英文注释
- 本 skill 只产出方案,不直接修改模型

## 基本信息(Basic Context)

- `task_id`:
- `skill_name`:`clm-codegen-compliance-refactor`
- `artifact_name`:`compliance_refactor_diff`
- `tool_context`(汇总自上游):
  - Simulink 版本与 Model Advisor 规则集:
  - 数值形态(浮点 / 定点 + Q 格式):
  - 目标合规规范基线:
- `scope`(模型路径 / 关注子系统):
- `version_or_branch`:

## 上游工件回引(Upstream Artifacts)

- `coder_config_review`(若有):
- `coverage_gap_report`(若有):
- `storage_class_governance`(若有):
- `control_law_pattern_skeleton`(若有):
- `simulink_model_map`(若有):

## 工具矩阵一致性结论

| 维度 | 来源工件 | 值 | 一致性结论 |
| --- | --- | --- | --- |
| Simulink 版本 |  |  |  |
| 数值形态 |  |  |  |
| 模型时间戳 |  |  |  |

总结:`一致(继续重构方案)` / `冲突(阻断,要求上游对齐)`

## 目标合规规范声明

- 基线:`High Integrity Modeling Guidelines` / `MAAB` / `MISRA Modeling` / `AUTOSAR` / 公司规范 / 通用高完整性
- 来源文档:
- 关键条款:

## 工件正文(Artifact Body)

### 1. finding 聚合表(Aggregated Findings)

按"模型对象路径"主键去重,保留各上游来源标签。

| Finding ID | 模型对象 | 来源(可多) | 描述 | 决策 | 决策理由 |
| --- | --- | --- | --- | --- | --- |
| F-001 | `model.slx > Controller/AttitudeLoop` | coder_config_review:Storage Class, storage_class_governance:RF-002 | 默认存储类与公司规范不一致 | refactor |  |
| F-002 | `model.slx > FaultMonitor/Limiter` | coverage_gap_report:GP-002(needs-model-refactor) | 条件分支结构不利于 MCDC | accept-residual | 条件互斥已文档化 |
| F-003 | Embedded Coder Setting `RTWGenerateMakefile` | coder_config_review | 当前值与目标不一致 | cannot-fix-in-model | 由配置层处理 |

决策枚举:`refactor` / `accept-residual` / `defer` / `cannot-fix-in-model`

### 2. 重构步骤表(Refactor Steps)

仅列出决策为 `refactor` 的条目。

| Finding ID | 最小重构步骤(逐 Block / 逐参数) | 期望结果 | 工具操作 |
| --- | --- | --- | --- |
| F-001 | 1. 在数据字典中把 `Kp_att` 的 Storage Class 改为 `Calibration`<br>2. 重命名为 `att_Kp` 以符合命名规则<br>3. 在 Block 参数中刷新引用 | 存储类与命名一致 | Model Advisor 复核 |

### 3. 风险与影响表(Risk & Impact)

| Finding ID | 风险等级 | 影响范围 | 回归点 | 高风险标记 |
| --- | --- | --- | --- | --- |
| F-001 | 中 | 本子系统 + 标定接口 | MIL 用例 + SIL 一致性 + Calibration 流程 |  |

### 4. 与既有结构冲突清单(Structural Conflicts)

| Finding ID | 冲突对象 | 冲突类型 | 处置建议 |
| --- | --- | --- | --- |
|  |  |  |  |

### 5. 接受残留(Accept Residual)文档

| Finding ID | 决策 | 文档化理由 | 评审签字环节 | 复核条件 |
| --- | --- | --- | --- | --- |
| F-002 | accept-residual | 条件互斥代码,Coverage 缺口为 `unreachable` | DV 评审 | 模型重构后再评估 |

### 6. 推迟(Defer)文档

| Finding ID | 决策 | 延迟原因 | 触发再评审条件 |
| --- | --- | --- | --- |
|  | defer |  |  |

### 7. 转交(Cannot Fix In Model)

| Finding ID | 转交对象 skill / 角色 | 备注 |
| --- | --- | --- |
| F-003 | `clm-embedded-coder-config-reviewer` 后续动作 / 配置工程师 |  |

### 8. 排序 backlog

| 排序 | Finding ID | 优先级 | 易修复度(高/中/低) | 高风险标记 |
| --- | --- | --- | --- | --- |
| 1 | F-001 | 中 | 高 |  |
| 2 |  |  |  |  |

排序依据:`高风险 + 高影响 + 易修复优先`

## 关键事实(Facts)

- Fact-1:
- Fact-2:

## 关键推断(Inferences)

- Inference-1(置信度:高/中/低):
- Inference-2(置信度:高/中/低):

## 证据索引(Evidence Index)

- 配置证据:`coder_config_review > Storage Class > Default Storage Class` → 当前值
- 覆盖率证据:`coverage_gap_report > GP-002` → unreachable 推断
- 治理证据:`storage_class_governance > RF-002` → 期望命名
- 模型证据:`simulink_model_map > Controller/AttitudeLoop` → 影响范围

## 缺口与风险(Gaps & Risks)

- 缺口(例:上游 finding 不足 / `simulink_model_map` 未提供 / 数值形态未确认):
- 风险:
- 降级策略:

## 反馈环路(Feedback Loop)

重构后必须由对应上游 skill 再次验证;本 skill 不下"重构成功"结论。

| 重构条目 | 再次验证 skill | 关注点 |
| --- | --- | --- |
| F-001 | `clm-storage-class-governor` + `clm-codegen-output-mapper` | 存储类已生效 + 生成代码命名已变更 |

## 下游输入建议(Next Skill Inputs)

- 推荐下游 skill:
  - 工程师 / 评审(直接施工)
  - `clm-control-law-mbd-pipeline`(汇总到 `pipeline_status`)
  - 反馈环路:重构后再次运行上游 skill 验证
- 建议关注的 finding ID / backlog 项:
- 需要补充的输入或确认项:

## 质量门禁自检(简表)

- [ ] 边界纯度:未直接改模型 / 未审查配置 / 未做覆盖率分析 / 未做治理决策
- [ ] 决策完整性:每条 finding 落到四类之一,带步骤或理由
- [ ] 风险纪律:`refactor` 含等级 + 影响 + 回归点
- [ ] 接受残留纪律:`accept-residual` 有文档化理由 + 评审签字
- [ ] 工具矩阵一致性
- [ ] 反馈环路已说明
- [ ] 交接可用性:工程师可直接施工
- [ ] 失败/降级说明完整

## 共享规范引用

- `../../_meta/first-principles-skill-contract.md`
- `../../_meta/artifact-handoff-contract.md`
- `../../_meta/quality-scorecard.md`
