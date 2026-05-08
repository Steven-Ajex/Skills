# clm-control-law-mbd-pipeline 输出模板

## 使用说明

- 目标:输出端到端 MBD 流程的阶段状态、门禁日志、跨库交接与下一步建议
- 主交付工件(Primary Artifact):`pipeline_status`
- 默认中文输出;专业术语首次出现附英文注释
- 本编排技能**只引用**原子 skill 工件,不重写专业结论

## 基本信息(Basic Context)

- `task_id`:
- `skill_name`:`clm-control-law-mbd-pipeline`
- `artifact_name`:`pipeline_status`
- 任务目标(用户原始描述):
- 任务范围(覆盖的阶段):
- 可用资产清单(模型 / 字典 / 生成代码 / 验证数据 / 上游 FMT 工件):

## 任务级工具矩阵(Tool Matrix)

| 阶段 | 工具 | 版本 | 许可证 | 备注 |
| --- | --- | --- | --- | --- |
| Stage 1 | Simulink |  |  |  |
| Stage 1 | Stateflow |  |  |  |
| Stage 3 | Embedded Coder |  |  |  |
| Stage 4 | SLDV / Polyspace |  |  |  |
| Stage 4 | HIL 平台 |  |  |  |

工具矩阵一致性结论:`无冲突` / `存在冲突(详见门禁日志)`

## 阶段状态表(Stage Status)

| 阶段 | 调用的原子 skill | 产出工件 | 状态 | 原因/备注 |
| --- | --- | --- | --- | --- |
| Stage 1: Model Reading | `clm-simulink-model-reader` | `simulink_model_map` | passed |  |
| Stage 1: Model Reading | `clm-stateflow-semantics-reader` | `stateflow_semantics` | passed / skipped |  |
| Stage 1: Model Reading | `clm-data-dictionary-reader` | `data_dictionary_map` | blocked(skill 待建) | 第二批待落地 |
| Stage 2: Model Authoring | `clm-control-law-pattern-author` | `control_law_pattern_skeleton` | skipped(任务未授权写) |  |
| Stage 3: Codegen Bridge | `clm-embedded-coder-config-reviewer` | `coder_config_review` | passed |  |
| Stage 3: Codegen Bridge | `clm-codegen-output-mapper` | `codegen_output_map` | passed / blocked(无生成代码) |  |
| Stage 4: Verification | `clm-test-harness-builder` | `test_harness_plan` | blocked(skill 待建) |  |
| Stage 5: Deploy Handoff | `clm-model-to-deploy-handoff` | — | blocked(skill 待建) |  |

状态枚举:`pending` / `running` / `passed` / `blocked` / `skipped`

## 门禁日志(Gate Log)

| Gate | 阶段 | 类型(入口/退出) | 结果(通过/阻断/警告) | 证据/原因 |
| --- | --- | --- | --- | --- |
| G1.in | Stage 1 | 入口 | 通过 | 任务描述含模型路径 |
| G1.out | Stage 1 | 退出 | 通过 |  |
| G3.in | Stage 3 | 入口 | 警告 | 模型与代码时间戳差 12h,降级标签随结论传递 |
| G3.out | Stage 3 | 退出 | 通过 |  |

## 未满足门禁(Unmet Gates)

| Gate | 原因 | 阻断的下游阶段 | 解锁动作 |
| --- | --- | --- | --- |
|  |  |  |  |

## 用户目标 ↔ 阶段映射

| 用户目标 | 关联阶段 | 关联工件 | 完成度(高/中/低/未达成) |
| --- | --- | --- | --- |
|  |  |  |  |

## 跨库交接(Cross-Library Handoff)

> 仅在任务涉及 FMT 时填写。

| 方向 | 本库工件 | FMT 端工件 | 命名一致性 | 备注 |
| --- | --- | --- | --- | --- |
| 输出至 FMT | `codegen_output_map.bridge_layer_contract` | `mbd_boundary_map` |  |  |
| 输出至 FMT | `pil_hil_replay_findings` | `control_performance_findings` |  |  |
| 接收自 FMT | — | `control_performance_findings` |  | 反哺 Stage 2 |

两侧上下文保留:

- 本库 `tool_context`:
- FMT 端 `firmware_context`:

## 残留风险(Risk Register)

| 风险 | 来源阶段 | 等级(高/中/低) | 影响 | 建议处置 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## 下一步建议(Next Actions)

- [ ] 解锁动作 A(对应 Gate ...):
- [ ] 第二批原子 skill 落地(阻断阶段对应 skill):
- [ ] 跨库交接确认(FMT 端):
- [ ] 用户决策点:

## 质量门禁自检(简表)

- [ ] 边界纯度:未重写原子 skill 的专业结论
- [ ] 阶段门禁纪律:每个 gate 通过/阻断/警告显式记录
- [ ] 工具上下文一致性:矩阵无冲突或冲突已阻断
- [ ] 跨库纪律:两侧上下文保留,命名一致性声明
- [ ] 用户目标可追溯:每个目标映射到阶段工件
- [ ] 失败/降级说明完整

## 共享规范引用

- `../../_meta/first-principles-skill-contract.md`(第 4 节"编排技能边界规则")
- `../../_meta/artifact-handoff-contract.md`(第 7 节"编排技能门禁检查")
- `../../_meta/quality-scorecard.md`
