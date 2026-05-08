---
name: clm-control-law-mbd-pipeline
description: 端到端控制律 MBD 模型开发编排技能,协调"模型理解 → 建模/重构 → 代码生成与桥接 → 在环验证 → 部署交接"五个阶段,基于 control-law-mbd 库内的原子 skill 工件做阶段门禁与跨阶段汇总。用于完整流程任务(从模型解读一路走到验证报告)时;不替代任何原子 skill 的专业判断,只做顺序、门禁、汇总,以及与 FMT 库工作流的工件衔接。
---

# Control-Law-MBD: Pipeline (Workflow Skill)

## 目标

协调 `control-law-mbd/` 内的原子 skill,完成"端到端"控制律 MBD 任务,产出每阶段的状态与跨阶段的汇总结论;**所有专业结论必须来自原子 skill 工件**,本技能只做编排与门禁。

## 第一性原理任务定义(First-Principles Task Definition)

1. 最小任务单元(Minimum Task Unit)
   - 在用户给定任务范围内,按顺序调用并集成下属原子 skill 的工件,完成阶段门禁(Gate Check)与跨阶段汇总,产出 `pipeline_status` 工件
2. 工具上下文(Tool Context)
   - 由各阶段原子 skill 各自的 `tool_context` 累加形成"任务级工具矩阵";本技能负责检查矩阵一致性,而不是产生工具上下文
3. 核心输入(Inputs)
   - 任务描述(必需:用户目标、范围、是否含已生成代码、是否含验证数据)
   - (可选)期望基线 / 公司规范文档
   - (可选)上游 FMT 工件(如 `control_performance_findings`,用于反哺模型层)
4. 核心输出(Outputs)
   - 主交付工件:`pipeline_status` + 各阶段原子工件汇总
   - 阶段状态表(`pending` / `running` / `passed` / `blocked` / `skipped`)
   - 未满足门禁清单(`unmet_gates`)
   - 跨库交接记录(`cross_library_handoff`)
5. 完成判据(Definition of Done, DoD)
   - 每个被纳入本次执行的阶段都有原子 skill 工件或显式跳过原因
   - 阶段间门禁已逐条检查,Blocking Gap 阻断后续阶段并显式说明
   - 用户目标已被关联到产出的具体阶段工件
   - 与 FMT 工作流的衔接(若用户任务涉及)显式声明
6. 输出语言约定(Language Convention)
   - 默认中文输出;专业术语首次出现附英文注释
   - 子工件字段保留原文,不重新解释

## 编排范围(只做这些)

1. 阶段顺序决策(默认顺序见下文)
2. 阶段门禁(Gate Check)
3. 跨阶段结论汇总(只引用原子工件,不重写专业结论)
4. 用户目标 ↔ 阶段映射
5. 与 `fmt/workflows/fmt-flight-control-param-optimizer` 的工件衔接

## 不负责

1. 任何**单阶段**的专业判断(全部委派到原子 skill)
2. 替代用户的设计决策(只汇总并提示,不擅自决定 trade-off)
3. 修改模型 / 代码 / 配置(写操作仍委派到 `model-authoring/` 或工程师)
4. 嵌入式集成与飞行验证(转交 FMT 工作流)
5. 跳过原子 skill 直接给最终结论

## 默认阶段顺序与门禁

> 若用户任务范围只覆盖部分阶段,被排除阶段标记为 `skipped` 并写明原因。

### Stage 1:Model Reading(模型理解)

候选原子 skill:

- `clm-simulink-model-reader` → `simulink_model_map`
- `clm-stateflow-semantics-reader` → `stateflow_semantics`(若模型含 Stateflow)
- `clm-data-dictionary-reader` → `data_dictionary_map`(若绑定 `.sldd`)
- `clm-requirement-trace-reader` → `requirement_trace_map`(若含需求追溯)

入口门禁:任务描述明确目标模型路径与工具上下文。

退出门禁(进入下一阶段前必须通过):

- 工件 `tool_context` 字段齐全
- 至少 `simulink_model_map` 已产出
- Atomic Subsystem 与多速率边界结论与下游需求一致

### Stage 2:Model Authoring(建模与重构,可选)

候选原子 skill:

- `clm-control-law-pattern-author` → `control_law_pattern_skeleton`
- `clm-codegen-compliance-refactor` → `compliance_refactor_diff`

入口门禁:Stage 1 已通过,且任务范围明确含写操作授权。

退出门禁:

- 重构结论包含 `risk_register` 与回归点
- 与 `simulink_model_map` 的修改差异显式列出

### Stage 3:Codegen Bridge(代码生成与桥接)

候选原子 skill:

- `clm-embedded-coder-config-reviewer` → `coder_config_review`
- `clm-codegen-output-mapper` → `codegen_output_map`(需先有生成代码)
- `clm-storage-class-governor` → `storage_class_governance`

入口门禁:

- Stage 1 通过(若任务跳过 Stage 2,需说明)
- 若需要 `codegen_output_map`,确认生成代码与模型时间戳一致

退出门禁:

- `coder_config_review` 高/中风险偏差有修复路径或显式接受
- 若产出 `codegen_output_map`,`bridge_layer_contract` 字段齐全(供 FMT 接力)
- 时间戳不一致警告必须随结论传递,不阻断,但下游必须感知

### Stage 4:Verification(在环验证)

候选原子 skill:

- `clm-test-harness-builder` → `test_harness_plan`
- `clm-coverage-gap-analyzer` → `coverage_gap_report`
- `clm-pil-hil-replay-analyzer` → `pil_hil_replay_findings`

入口门禁:

- Stage 1 通过
- 若做 PIL/HIL 回放,Stage 3 的 `codegen_output_map` 已产出且时间戳一致

退出门禁:

- 覆盖率维度齐全(Decision/Condition/MCDC),缺口已分类(Blocking / Non-Blocking)
- 退化信号(`regression_signals`)与基线对比通过判据已声明

### Stage 5:Deploy Handoff(部署交接)

候选原子 skill(规划中,本仓库当前未落地):

- `clm-model-to-deploy-handoff`(待建)

入口门禁:Stage 4 通过(或显式接受残留风险)。

退出门禁:与 FMT 库或集成项目的交接清单已生成。

## 跨库交接(与 FMT 工作流)

| 方向 | 本库工件 | FMT 端工件 | 用途 |
| --- | --- | --- | --- |
| 输出至 FMT | `codegen_output_map.bridge_layer_contract` | `mbd_boundary_map` | 嵌入式接口对接 |
| 输出至 FMT | `pil_hil_replay_findings` | `control_performance_findings`(对照) | 仿真 vs 实飞性能基线 |
| 接收 FMT | `control_performance_findings` | — | 反哺模型层调参 / 重构 |
| 接收 FMT | `tuning_recommendation_report` | — | 作为下一轮 Model Authoring 输入 |

跨库交接必须保留两侧 `tool_context` / `firmware_context`,不互相覆盖;命名(状态名 / 信号名 / 变体)一致性显式声明。

## 执行步骤

1. **解析任务**:从用户任务中提取目标、范围、可用资产(模型 / 字典 / 生成代码 / 验证数据 / 上游 FMT 工件)
2. **裁剪阶段**:决定哪些阶段进入本次执行,哪些标记 `skipped` 并写明原因
3. **入口门禁检查**:每阶段开始前检查上游工件 / 工具上下文 / 范围一致性
4. **逐阶段调用原子 skill**:按候选清单调用;若同一阶段有多个候选,按用户目标决定优先级
5. **汇总阶段结论**:只引用原子工件,不重写专业结论
6. **退出门禁检查**:Blocking Gap 阻断,Non-Blocking Gap 标注后继续
7. **跨库交接**:若任务涉及 FMT,生成 `cross_library_handoff` 段,声明工件映射与命名一致性
8. **生成 `pipeline_status`**:按 `references/output-template.md` 填充
9. **自检**:按 `references/checklist.md` 复核

## 输出要求

至少包含:

1. 任务级工具矩阵(各阶段 `tool_context` 汇总 + 一致性结论)
2. 阶段状态表(每阶段调用的原子 skill、产出工件、状态、原因)
3. 阶段门禁记录(每个 gate 的通过 / 阻断 / 警告)
4. 用户目标 ↔ 阶段映射表
5. 跨库交接段(若涉及 FMT)
6. 残留风险与建议下一步

## 上下游交接(Artifact Handoff)

1. 上游依赖
   - 用户任务描述(必需)
   - (可选)上游 FMT 工件
2. 下游使用方
   - 工程师 / 评审 / 项目经理(直接读 `pipeline_status`)
   - `fmt-flight-control-param-optimizer`(消费 `cross_library_handoff` 与 `bridge_layer_contract`)
3. 主交付工件
   - `pipeline_status`(本工件)+ 各阶段原子工件(由阶段 skill 各自产出)
   - 字段:`tool_matrix`、`stages`、`gate_log`、`unmet_gates`、`cross_library_handoff`、`risk_register`、`next_actions`
4. 共享规范
   - `../../_meta/first-principles-skill-contract.md`(第 4 节"编排技能边界规则")
   - `../../_meta/artifact-handoff-contract.md`(第 7 节"编排技能门禁检查")
   - `../../_meta/quality-scorecard.md`

## 质量门禁(Quality Gates)

1. 必过门禁(Mandatory Gates)
   - 边界门禁(Boundary Purity):不替代任何原子 skill 的专业结论;所有跨阶段结论必须引用原子工件
   - 阶段门禁纪律(Stage Gate Discipline):每个 gate 通过 / 阻断 / 警告必须显式记录
   - 工具上下文一致性(Tool Context Consistency):各阶段 `tool_context` 矩阵无冲突,冲突时阻断
   - 跨库纪律(Cross-Library Discipline):与 FMT 衔接时不混用命名 / 不互相覆盖上下文
   - 用户目标可追溯:用户每个目标都能映射到具体阶段工件
2. 自检建议(Self Check)
   - 使用 `../../_meta/quality-scorecard.md` 打分(目标 ≥10/12)

## 失败与降级策略(Failure / Fallback)

1. 输入不足处理
   - **任务描述不清**:列出关键决策点请用户澄清,不擅自裁剪阶段
   - **某阶段必需上游工件缺失**:阻断该阶段并标记 `blocked`,显式说明阻断原因与解锁动作
   - **阶段间工具上下文冲突**(如 Simulink 版本不一致):阻断后续阶段,要求统一上下文
   - **第二批原子 skill 尚未落地**(如 `clm-data-dictionary-reader` / `clm-test-harness-builder` 等):该子任务降级为"待补",不假装产出
2. 输出降级要求
   - 降级输出必须显式列出哪些阶段未完成、什么原因、解锁动作
   - 不得跳步给"端到端通过"的结论 — 任何 Blocking Gap 阻断时必须标记任务未完成

## references/ 使用建议

1. 输出前先加载 `references/output-template.md` 作为骨架,阶段表与门禁日志直接套用
2. 交付前用 `references/checklist.md` 复核边界、门禁纪律、跨库交接

## 编排纪律

1. 不重写原子 skill 的专业结论 — 引用即可
2. 不擅自合并阶段 — 即使两个阶段产物相似,也按门禁顺序逐一通过
3. 不假装阶段已通过 — Blocking Gap 阻断必须传递到 `pipeline_status`
4. 跨库交接保留两侧上下文,命名一致性显式声明
5. 第二批原子 skill 未落地的阶段一律标记 `blocked` 或 `skipped`,不在本 skill 内"代行"它们的职责
