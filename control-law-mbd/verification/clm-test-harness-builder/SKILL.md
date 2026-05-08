---
name: clm-test-harness-builder
description: 从需求或目标 Subsystem/Chart 出发,设计 Simulink Test 测试 harness 与测试用例骨架(MIL/SIL 优先,PIL 占位),输出可被 `clm-coverage-gap-analyzer` 与 `clm-pil-hil-replay-analyzer` 接力的测试规划工件的专用技能。用于需要把"控制律某子系统 / 模式切换 Chart"落到测试 harness 与用例上时;不负责真实运行测试、不负责覆盖率工具配置、不负责 PIL/HIL 数据回放、不修改被测模型。
---

# Control-Law-MBD: Test Harness Builder

## 目标

把"被测对象(Subsystem / Chart / 整模型)+ 测试目标(需求条目 / 模式切换路径 / 性能基线)"映射成一份可以直接落地为 Simulink Test 工程的测试 harness 与用例骨架,产出 `test_harness_plan` 工件。本 skill 不替工程师"写"运行环境,而是把工程师做这件事所需的设计决策与边界条件全部固化。

## 第一性原理任务定义(First-Principles Task Definition)

1. 最小任务单元(Minimum Task Unit)
   - 在单一被测对象 + 单一测试目标层(MIL 或 SIL)范围内,完成"测试 harness 结构 + 用例骨架 + 输入激励 + 期望输出 + 通过判据"的设计,产出 `test_harness_plan` 工件
2. 工具上下文(Tool Context)
   - Simulink Test 版本
   - 求解器(Solver)与采样时间(继承自被测模型)
   - 是否启用 SIL(若启用,生成代码与目标硬件已确认)
   - Signal Builder / Test Sequence / MATLAB-based Test 选型
   - 许可证可用性
3. 核心输入(Inputs)
   - 被测对象路径(Subsystem / Chart / Model;必需)
   - 测试目标(需求条目 / 状态切换路径 / 性能基线 / 边界扫描;必需)
   - (可选)`clm-simulink-model-reader` 的 `simulink_model_map`(用于端口与采样时间)
   - (可选)`clm-stateflow-semantics-reader` 的 `stateflow_semantics`(用于状态切换用例)
   - (可选)`clm-requirement-trace-reader` 的 `requirement_trace_map`(用于需求 → 用例映射)
   - (可选)`clm-codegen-output-mapper`(用于 SIL 模式下的接口)
4. 核心输出(Outputs)
   - 主交付工件:`test_harness_plan`
   - Harness 结构(被测对象包装、激励源、观察点)、用例表(用例 ID、目标、激励、期望、通过判据、覆盖维度)、需求 → 用例矩阵、SIL/PIL 准备清单(如适用)
5. 完成判据(Definition of Done, DoD)
   - 至少一条用例满足"用例 ID + 测试目标 + 激励信号 + 期望输出 + 通过判据 + 覆盖维度"五项齐全
   - 需求 → 用例映射矩阵已构建(若提供 `requirement_trace_map`),否则在 `gaps` 中登记
   - 状态切换用例覆盖至少一条非平凡转移(若涉及 Stateflow)
   - 边界扫描用例显式标注扫描维度(参数 / 输入信号 / 模式切换)
   - 工具上下文显式记录,SIL 模式下生成代码与模型时间戳一致性已声明
6. 输出语言约定(Language Convention)
   - 默认中文输出;专业术语首次出现附英文注释
   - 保留信号名、子系统名、状态名原文

## 聚焦范围(只做这些)

1. 测试 harness 结构(Test Harness Block / Subsystem 包装)
2. 输入激励选型(Signal Builder / Test Sequence / MATLAB-based / From Workspace)
3. 用例表(用例 ID / 测试目标 / 激励 / 期望输出 / 通过判据 / 覆盖维度)
4. 期望输出与通过判据(等价类 / 边界 / 容差 / 时间窗)
5. 需求 → 用例映射矩阵
6. 状态切换用例(基于 `stateflow_semantics`)
7. SIL/PIL 准备清单(如目标硬件已就绪)

## 不负责

1. 真实运行测试(用户工程实施)
2. 覆盖率工具(SLDV / Polyspace)的配置 → 走 `clm-coverage-gap-analyzer`
3. PIL/HIL 数据回放与基线对比 → 走 `clm-pil-hil-replay-analyzer`
4. 修改被测模型 → 走 `model-authoring/`
5. 需求源文档解读 → 走 `clm-requirement-trace-reader`(本 skill 只消费其工件)

## 推荐设计顺序

1. 先界定"被测对象边界" — 端口、采样时间、是否原子化(影响 harness 包装方式)
2. 再选"激励来源" — Signal Builder vs Test Sequence(取决于事件驱动 vs 时间驱动)
3. 再写"等价类 + 边界 + 异常"用例骨架
4. 再补"状态切换"与"模式连锁"用例(若涉及 Stateflow)
5. 最后写"通过判据"与"需求 → 用例矩阵"

## 执行步骤

1. **确认工具上下文**:Simulink Test 版本、求解器、是否启用 SIL、激励/观察机制、许可证
2. **抓被测对象边界**:从 `simulink_model_map`(如有)抓端口、采样时间、原子单元;否则从模型本身抓
3. **设计 harness 结构**:Test Harness Block 包装、激励源、观察点(Test Assessment / Verify)
4. **设计用例分组**:
   - 等价类(Equivalence Partition)
   - 边界(Boundary)
   - 状态切换(基于 `stateflow_semantics`)
   - 异常 / 故障注入(若需求层有要求)
   - 性能基线(对照已有飞行/PIL 数据)
5. **填写用例表**:每条用例至少含 ID / 目标 / 激励 / 期望 / 通过判据 / 覆盖维度
6. **构建需求 → 用例矩阵**(若有 `requirement_trace_map`):未覆盖的需求列入 `gaps`
7. **SIL/PIL 准备清单**(若涉及):生成代码版本、目标硬件、接口对接(对照 `codegen_output_map`)
8. **生成工件**:按 `references/output-template.md` 填充 `test_harness_plan`
9. **自检**:按 `references/checklist.md` 复核

## 输出要求

至少包含:

1. 工具上下文小结
2. Harness 结构图(包装方式 + 激励源 + 观察点)
3. 用例表(至少含等价类 + 边界 + 状态切换 + 通过判据)
4. 需求 → 用例矩阵(若有需求工件)
5. SIL/PIL 准备清单(若适用)
6. 关键事实(Facts)、关键推断(Inferences)
7. 证据索引(被测对象路径 + 需求 ID + Stateflow 路径)
8. 缺口清单与下游输入建议

## 上下游交接(Artifact Handoff)

1. 上游依赖
   - 用户提供的被测对象 + 测试目标
   - (推荐)`clm-simulink-model-reader` 的 `simulink_model_map`
   - (推荐若涉及状态机)`clm-stateflow-semantics-reader` 的 `stateflow_semantics`
   - (可选)`clm-requirement-trace-reader` 的 `requirement_trace_map`
   - (可选若涉及 SIL)`clm-codegen-output-mapper` 的 `codegen_output_map`
2. 下游使用方
   - `clm-coverage-gap-analyzer`(消费用例集合作为覆盖率分析的起点)
   - `clm-pil-hil-replay-analyzer`(消费 SIL/PIL 准备清单与通过判据作为基线对比依据)
   - `clm-control-law-mbd-pipeline`(编排技能)
3. 主交付工件
   - `test_harness_plan`
   - 字段:`tool_context`、`scope`、`facts`、`inferences`、`evidence_index`、`gaps`、`next_skill_inputs`、`requirement_to_test_matrix`(详见 `../../_meta/artifact-handoff-contract.md`)
4. 共享规范
   - `../../_meta/first-principles-skill-contract.md`
   - `../../_meta/artifact-handoff-contract.md`
   - `../../_meta/quality-scorecard.md`

## 质量门禁(Quality Gates)

1. 必过门禁(Mandatory Gates)
   - 边界门禁:不真实运行测试 / 不配置覆盖率工具 / 不修改被测模型
   - 证据门禁:每条用例可回链到"被测对象路径 + 测试目标(需求 ID / 状态路径 / 信号窗口)"
   - 工具上下文门禁:Simulink Test 版本、求解器、SIL 状态显式记录
   - 用例完整性纪律:用例表五项(目标 / 激励 / 期望 / 通过判据 / 覆盖维度)齐全;不齐全则列入 `gaps`
   - 通过判据纪律:不写"应正常工作"等模糊语,必须含数值容差 / 状态序列 / 时间窗
   - 交接门禁:工件可被 `clm-coverage-gap-analyzer` 与 `clm-pil-hil-replay-analyzer` 直接消费
2. 自检建议:使用 `../../_meta/quality-scorecard.md` 打分(目标 ≥10/12)

## 失败与降级策略(Failure / Fallback)

1. 输入不足处理
   - **被测对象边界未明确**:列出关键决策点请用户澄清,不擅自包装
   - **未提供需求工件**:跳过需求 → 用例矩阵章节,在 `gaps` 中登记
   - **未提供 `stateflow_semantics`**:跳过状态切换用例,标注"模式切换覆盖不足"
   - **SIL 启用但无生成代码**:SIL 模式降级为 MIL 计划,显式标注
   - **Simulink Test 许可证缺失**:用例表仍可设计,但 Harness 形态降级为"Subsystem 包装 + From Workspace 激励"的最小可行方案,标注其与 Simulink Test 的差异
2. 输出降级要求
   - 降级输出必须显式标注受影响结论与置信度变化
   - 降级不等于跳步;不得越过本技能职责给出"测试通过 / 不通过"的结论(本 skill 只设计计划)

## references/ 使用建议

1. 输出前先加载 `references/output-template.md`,用例表与需求矩阵直接套用
2. 交付前用 `references/checklist.md` 复核用例完整性、通过判据纪律、降级策略
3. 状态切换用例较多时,建议按"每条非平凡转移至少一个用例"的密度规划

## 设计纪律

1. 通过判据(Pass Criterion)必须可机器判定 — 不写"行为合理",写"|err| < 0.1 deg 持续 t∈[1.0, 2.0] s"
2. 不假设"等价类 + 边界 + 异常"覆盖完整 — 状态机/连锁切换属于专项分组
3. 用例 ID 命名必须可追溯到"分组 + 需求 ID 或状态路径"(便于覆盖率与回归对照)
4. SIL 模式必须确认"生成代码版本 + 目标硬件 + 接口对接"三项,缺一项即降级到 MIL
5. 不在本 skill 内对"是否通过覆盖率"下结论 — 转交 `clm-coverage-gap-analyzer`
