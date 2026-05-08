# clm-requirement-trace-reader 输出模板

## 使用说明

- 目标:输出需求条目清单、三向追溯矩阵(需求 ↔ 模型对象 ↔ 用例)、orphan 与 broken link 清单
- 主交付工件(Primary Artifact):`requirement_trace_map`
- 默认中文输出;专业术语首次出现附英文注释
- 本 skill 不评审需求质量,只解析链接结构

## 基本信息(Basic Context)

- `task_id`:
- `skill_name`:`clm-requirement-trace-reader`
- `artifact_name`:`requirement_trace_map`
- `tool_context`:
  - 需求工具(Simulink Requirements / DOORS / ReqIF / Polarion / Jira / 自研):
  - 工具版本:
  - 需求源形态:
  - 链接存储形态:
  - 许可证可用性:
- `scope`(需求源路径 + 模型路径若提供):
- `version_or_branch`:

## 范围与假设(Scope & Assumptions)

- [ ] 是否提供 `simulink_model_map`
- [ ] 是否提供 `stateflow_semantics`
- [ ] 是否提供 `test_harness_plan`
- 事实(Fact)与推断(Inference)边界说明:

## 输入摘要(Input Summary)

- [ ] 需求源路径
- [ ] 上游工件清单
- 输入缺口(Gaps):

## 工件正文(Artifact Body)

### 1. 需求条目清单(Requirement Inventory)

- 总条目数:
- 按状态分布:`active=N` / `proposed=N` / `obsolete=N` / 其他
- 按优先级分布:`high=N` / `medium=N` / `low=N` / 未标注
- 按类型分布:`functional=N` / `safety=N` / `performance=N` / 其他

| 需求 ID | 标题 | 类型 | 优先级 | 状态 | 备注 |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

### 2. 三向矩阵(Three-Way Trace Matrix)

| 需求 ID | 模型对象目标(子系统/状态/转移) | 测试用例目标 | 链接质量(已审计/待评审/无理由) |
| --- | --- | --- | --- |
|  |  |  |  |

多目标链接(一对多):

| 需求 ID | 目标列表 | 备注 |
| --- | --- | --- |
|  |  |  |

多源链接(多对一):

| 目标对象 | 需求 ID 列表 | 备注 |
| --- | --- | --- |
|  |  |  |

### 3. 反向追溯结论(Reverse Traceability)

模型对象覆盖率(若有 `simulink_model_map`):

- 已被需求引用的子系统数:
- 未被需求引用的子系统数:
- 未引用对象清单(不判定为"不需要",仅列出):

| 子系统路径 | 备注 |
| --- | --- |
|  |  |

用例覆盖率(若有 `test_harness_plan`):

- 已映射到需求的用例数:
- 未映射到需求的用例数:
- 未映射用例清单:

| 用例 ID | 备注 |
| --- | --- |
|  |  |

状态/转移覆盖(若有 `stateflow_semantics`):

| 状态/转移路径 | 已被需求引用? | 备注 |
| --- | --- | --- |
|  |  |  |

### 4. 孤立条目(Orphan)清单

- 总数:
- 高优先级 + status=active 的高亮条目数:

| 需求 ID | 标题 | 优先级 | 状态 | 备注 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

零条目情况:`无 orphan`(显式声明)

### 5. 断链(Broken Link)清单

- 总数:
- 按断链类型分布:`目标对象不存在=N` / `路径变更=N` / `用例已删除=N` / `状态/转移不存在=N`

| 链接源(需求 ID) | 原目标 | 断链类型 | 推断原因 | 修复建议 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

零条目情况:`无 broken link`(显式声明)

### 6. 链接质量审查(Link Quality)

| 维度 | 通过 | 警告 | 失败 | 备注 |
| --- | --- | --- | --- | --- |
| 是否有理由说明 |  |  |  |  |
| 是否已审计 |  |  |  |  |
| 是否含"待评审"状态 |  |  |  |  |

## 关键事实(Facts)

- Fact-1:
- Fact-2:

## 关键推断(Inferences)

- Inference-1(置信度:高/中/低):
- Inference-2(置信度:高/中/低):

## 证据索引(Evidence Index)

- 需求证据:`requirements.slreqx > REQ-ATT-005` → 标题、状态、链接列表
- 模型对照:`simulink_model_map > Controller/AttitudeLoop` → 已被 REQ-ATT-005 引用
- 用例对照:`test_harness_plan > TC-EQ-01` → 已被 REQ-ATT-005 引用

## 缺口与风险(Gaps & Risks)

- 缺口(例:许可证缺失 / 上游工件缺失 / 需求源形态未识别):
- 风险:
- 降级策略:

## 下游输入建议(Next Skill Inputs)

- 推荐下游 skill:
  - `clm-test-harness-builder`(关注:无对应需求的用例 + orphan 高优先级条目作为补强用例)
  - `clm-coverage-gap-analyzer`(关注:需求 → 模型对象矩阵作为覆盖路由依据)
  - `clm-control-law-mbd-pipeline`(汇总到 `pipeline_status`)
- 建议关注的需求 ID / 模型对象 / 用例:
- 需要补充的输入或确认项:

## 质量门禁自检(简表)

- [ ] 边界纯度:未评审需求质量 / 未解读需求源文档 / 未修改文件 / 未设计用例
- [ ] 证据可追溯:每条链接给出需求 ID + 目标
- [ ] 工具上下文显式:需求工具/版本/链接形态/许可证已记录
- [ ] 矩阵完整性:三向矩阵 + orphan + broken 显式声明
- [ ] 反向追溯纪律:覆盖率已计算,未引用对象未判定为"不需要"
- [ ] 交接可用性:下游 skill 可直接消费
- [ ] 失败/降级说明完整

## 共享规范引用

- `../../_meta/first-principles-skill-contract.md`
- `../../_meta/artifact-handoff-contract.md`
- `../../_meta/quality-scorecard.md`
