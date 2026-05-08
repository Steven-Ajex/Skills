---
name: clm-embedded-coder-config-reviewer
description: 审查 Simulink 模型的 Embedded Coder 配置集(Configuration Set)与代码生成诊断的专用技能。用于需要确认"代码接口、存储类、目标硬件、求解器、优化、报告与诊断"等关键配置是否符合期望时;不负责模型层结构解读、不负责生成代码与桥接层的对接映射、不负责存储类的全局治理决策、不负责测试用例与覆盖率分析。
---

# Control-Law-MBD: Embedded Coder Config Reviewer

## 目标

在不修改模型与配置的前提下,把 Embedded Coder(嵌入式代码生成器)的配置集逐项审查清楚,产出一份"配置项 + 当前值 + 期望值 + 风险 + 修复路径"的审查工件,供工程师决策是否调整、供下游 `clm-codegen-output-mapper` 与 `clm-storage-class-governor` 接力。

## 第一性原理任务定义(First-Principles Task Definition)

1. 最小任务单元(Minimum Task Unit)
   - 在单一 Simulink 模型 + 单一配置集(Configuration Set)范围内,完成 Embedded Coder 关键配置项的审查与诊断,输出 `coder_config_review` 工件
2. 工具上下文(Tool Context)
   - Embedded Coder / Simulink Coder 版本(例:R2020b、R2023b)
   - 目标硬件(Target Hardware:Word Length、Endianness、Atomic Integer/Float Sizes)
   - 求解器(Solver:Type、Step Size、Tasking Mode)
   - 是否启用 SIL/PIL、是否使用代码替换库(Code Replacement Library)
   - 许可证可用性(无许可证时只能从模型源 `.slx` 解压的 `configSet` XML 解析存储值)
3. 核心输入(Inputs)
   - Simulink 模型路径(必需)
   - 目标配置集名称(可选,缺省审查 ActiveConfigSet)
   - 期望配置基线 / 公司级建模规范(可选,缺省采用通用高完整性建模建议)
   - (可选)生成代码目录 — 仅用于交叉验证配置是否生效,不替代 `clm-codegen-output-mapper`
4. 核心输出(Outputs)
   - 主交付工件:`coder_config_review`
   - 配置项审查表(Category × Item × Current × Expected × Risk × Fix)
   - 关键配置类别的小结(代码接口 / 存储类 / 目标硬件 / 求解器 / 优化 / 报告与诊断)
   - 与生成代码契合的关键标记(Step Function 形态、是否可重入、是否生成单一文件等)
5. 完成判据(Definition of Done, DoD)
   - 关键配置类别都已审查(至少:Code Interface、Storage Class、Hardware Implementation、Solver、Optimization、Report & Diagnostics)
   - 每条偏差有"期望值 + 风险 + 修复路径"
   - 工具上下文显式记录(Embedded Coder 版本、目标硬件、求解器、许可证状态)
   - 不擅自给出"生成代码不合规"结论 — 此类结论需引用 `codegen_output_map`(由 `clm-codegen-output-mapper` 产出)
6. 输出语言约定(Language Convention)
   - 默认中文输出;专业术语首次出现附英文注释
   - 保留配置项原文(如 `RTWGenerateMakefile`、`DefaultParameterBehavior`)

## 聚焦范围(只做这些)

1. 代码接口(Code Interface):Function Packaging、Step Function 形态、Reentrant、I/O Args 风格
2. 存储类(Storage Class):Default Storage Class、Custom Storage Class、Inlined Parameters、Default Parameter Behavior
3. 目标硬件(Hardware Implementation):Word Length、Endianness、Atomic Integer/Float Sizes
4. 求解器(Solver):Type、Step Size、Tasking Mode(SingleTasking / MultiTasking)
5. 优化(Optimization):Reusable Subsystems、Pass-by Pointer、Loop Unrolling、Conditional Input Branch Execution 等
6. 报告与诊断(Report & Diagnostics):Generation Report、Code Replacement Library、MISRA / AUTOSAR 规范勾选(如适用)

## 不负责

1. 模型层结构与信号流解读 → 走 `clm-simulink-model-reader`
2. 生成代码与手写桥接层的映射 → 走 `clm-codegen-output-mapper`
3. 存储类的全局治理与命名规则决策 → 走 `clm-storage-class-governor`(本 skill 仅标注问题点)
4. 模型重构 → 走 `model-authoring/`
5. 测试用例、覆盖率、SIL/PIL 数据回放 → 走 `verification/`

## 推荐审查顺序

1. 先确定"目标硬件 + 求解器" — 这两项决定下游所有结论是否有意义
2. 再看"代码接口" — 这决定生成代码与外部桥接层(如 FMT 接口层)的对接形式
3. 再看"存储类与默认参数行为" — 这决定参数标定能力与 RAM/ROM 占用
4. 再看"优化项" — 主要影响代码体积与可读性
5. 最后看"报告与诊断" — 含 MISRA/AUTOSAR 等合规勾选

## 执行步骤

1. **确认工具上下文**:Embedded Coder 版本、目标硬件、求解器、许可证可用性
2. **抓取配置集**:确定 ActiveConfigSet 名称;若有多 ConfigSet 需明确审查的目标
3. **分类审查**:对六大类别逐项抓取当前值,对照期望基线
4. **风险标注**:每条偏差填写风险等级(高 / 中 / 低)与影响(代码体积 / 可调标定能力 / 性能 / 合规 / 可维护)
5. **修复建议**:给出最小修复路径(配置项调整、模型层调整、需求层澄清)
6. **交叉验证(可选)**:若提供了生成代码目录,抓取若干关键 marker(如 Step Function 形态、全局变量存储类的命名前缀)与配置预期对比;不一致时只标注差异,不下"生成代码不合规"的结论
7. **生成工件**:按 `references/output-template.md` 填充 `coder_config_review`
8. **自检**:按 `references/checklist.md` 复核

## 输出要求

至少包含:

1. 工具上下文小结(版本、目标硬件、求解器、许可证)
2. 六大类别的审查表(Category × Item × Current × Expected × Risk × Fix)
3. 关键标记小结(Step Function 形态、Reentrant、文件打包形态)
4. 关键事实(Facts)、关键推断(Inferences,带置信度)
5. 证据索引(配置项原名 + 在 `.slx` 解压后的 XML 路径或 `get_param` 调用语法)
6. 缺口清单(许可证缺失、配置基线未提供、目标硬件未确认等)
7. 下游输入建议(`codegen-bridge/` 内其他 skill 的关注字段)

## 上下游交接(Artifact Handoff)

1. 上游依赖(Upstream Dependencies)
   - 用户提供的模型路径与目标配置集
   - (可选)`clm-simulink-model-reader` 的 `simulink_model_map`(用于评估多速率与原子单元配置是否匹配)
2. 下游使用方(Downstream Consumers)
   - `clm-codegen-output-mapper`(消费 Step Function 形态、文件打包形态、存储类策略)
   - `clm-storage-class-governor`(消费 Default Storage Class、Inlined Parameters 设置作为治理输入)
   - `clm-codegen-compliance-refactor`(消费风险项作为重构 backlog)
   - `clm-control-law-mbd-pipeline`(编排技能)
   - `fmt-mbd-interface-reader`(跨库:本 skill 的 Step Function 形态 + 文件打包形态结论与 FMT 接口层期望对接形式互相验证)
3. 主交付工件(Primary Artifact)
   - `coder_config_review`
   - 工件至少包含:`tool_context`、`scope`、`facts`、`inferences`、`evidence_index`、`gaps`、`next_skill_inputs`(详见 `../../_meta/artifact-handoff-contract.md`)
4. 共享规范(Shared Contracts)
   - `../../_meta/first-principles-skill-contract.md`
   - `../../_meta/artifact-handoff-contract.md`
   - `../../_meta/quality-scorecard.md`

## 质量门禁(Quality Gates)

1. 必过门禁(Mandatory Gates)
   - 边界门禁(Boundary Purity):不输出"生成代码不合规"的确定性结论(需 `codegen_output_map` 支撑);不修改任何配置;不替代 `clm-storage-class-governor` 的全局治理决策
   - 证据门禁(Evidence Traceability):每条结论给出配置项原名 + 来源(`get_param` / `configSet` XML 路径)
   - 工具上下文门禁(Tool Context Explicitness):Embedded Coder 版本、目标硬件、求解器、许可证状态必须显式记录
   - 风险门禁(Risk Discipline):每条偏差必须有风险等级 + 影响维度,不能只写"建议改成 X"
   - 交接门禁(Handoff Usability):下游 skill 可直接消费,不只是描述文字
2. 自检建议(Self Check)
   - 使用 `../../_meta/quality-scorecard.md` 对本次输出快速打分(目标 ≥10/12)

## 失败与降级策略(Failure / Fallback)

1. 输入不足处理
   - **无 Embedded Coder 许可证**:降级到从 `.slx` 解压的 `configSet` XML 解析存储值,声明"无法运行 Model Advisor / 无法做 Configuration Set Reference 解析"
   - **未提供配置基线**:采用通用高完整性建模建议(显式声明所用基线名称),并提示用户提供公司基线以提升结论强度
   - **目标硬件未确认**:只给"目标无关"的结论(如代码接口、存储类),目标硬件相关项标注"待目标硬件确认"
   - **多 ConfigSet 未指定**:列出所有候选 ConfigSet 并请求用户指定;不擅自选择
2. 输出降级要求
   - 降级输出必须显式标注受影响结论与置信度变化
   - 降级不等于跳步;不得越过本技能职责给出生成代码合规性的最终结论

## references/ 使用建议

1. 输出前先加载 `references/output-template.md` 作为骨架,六大类别表格直接套用
2. 交付前用 `references/checklist.md` 复核边界、证据、风险标注、降级策略
3. 项目级标定治理大改造场景:本 skill 输出后转交 `clm-storage-class-governor`,不要在本 skill 内推动治理决策

## 分析纪律

1. 不把"配置项当前值与默认值不同"当成"有问题"的结论 — 是否问题取决于期望基线
2. 不把"代码生成报告 warning"当成必修项 — 部分 warning 是项目级别可接受的
3. 不把模型层问题(如未原子化的子系统)归为 Embedded Coder 配置问题 — 这类问题转交 `clm-codegen-compliance-refactor`
4. 跨库交接:与 `fmt-mbd-interface-reader` 的对接结论必须保留两侧 `tool_context` / `firmware_context`,不混用版本规则
