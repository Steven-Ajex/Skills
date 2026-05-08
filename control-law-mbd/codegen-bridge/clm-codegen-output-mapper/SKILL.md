---
name: clm-codegen-output-mapper
description: 在 Embedded Coder 已经生成代码的前提下,建立"模型对象 ↔ 生成代码"的精确映射(文件/函数/全局变量/Bus 结构体/Step Function 入口),并识别与手写桥接层(如 FMT 接口层)的契合点的专用只读技能。用于需要确认生成代码的接口形态、参数与信号在代码中的存在形式、以及与外部代码的对接边界时;不负责审查 Embedded Coder 配置、不负责治理存储类、不负责修改模型或代码、不负责测试 harness。
---

# Control-Law-MBD: Codegen Output Mapper

## 目标

在不修改任何模型/代码的前提下,把"模型里的子系统/参数/信号"和"生成代码里的文件/函数/全局变量/结构体"对接起来,产出一份"模型 ↔ 代码"映射工件,供 `clm-storage-class-governor`、`fmt-mbd-interface-reader` 等下游 skill 直接消费。

## 第一性原理任务定义(First-Principles Task Definition)

1. 最小任务单元(Minimum Task Unit)
   - 在单一模型 + 单一次代码生成产物范围内,完成"模型对象 ↔ 生成代码"的映射梳理,产出 `codegen_output_map` 工件
2. 工具上下文(Tool Context)
   - Embedded Coder / Simulink Coder 版本
   - 代码生成形态(单文件 vs 模块化分文件;是否生成 `model_step` / `model_initialize` / `model_terminate`)
   - 是否使用 Reusable Subsystems、Reentrant
   - 目标硬件与类型定义来源(`rtwtypes.h` / 自定义 Type)
   - 代码生成时间戳(用于判断是否与当前模型一致)
3. 核心输入(Inputs)
   - Simulink 模型路径(必需)
   - 生成代码目录(必需)
   - (可选)`clm-simulink-model-reader` 的 `simulink_model_map` 工件
   - (可选)`clm-embedded-coder-config-reviewer` 的 `coder_config_review` 工件
   - (可选)手写桥接层代码路径(如 FMT 的 `*_interface.c`)
4. 核心输出(Outputs)
   - 主交付工件:`codegen_output_map`
   - 模型对象 ↔ 生成代码(文件 + 函数 + 全局变量 + 结构体)映射表
   - Step Function 入口与调用形态
   - 与手写桥接层的契合点(`bridge_layer_contract`)
5. 完成判据(Definition of Done, DoD)
   - 至少一条完整路径"模型子系统 → 生成函数 → 输入/输出全局变量"被串起,带文件路径 + 行号
   - 至少一条参数路径"`Simulink.Parameter` → 生成代码全局变量"被串起
   - 工具上下文显式记录,代码生成时间戳与模型修改时间戳已比较
   - 桥接层契合点有候选(若提供桥接代码),否则在 `gaps` 中登记
6. 输出语言约定(Language Convention)
   - 默认中文输出;专业术语首次出现附英文注释
   - 保留生成代码中的函数名、全局变量名、结构体名、字段名原文

## 聚焦范围(只做这些)

1. 生成代码文件结构(`*.c` / `*.h` / `*_data.c` / `*_private.h` / `*_types.h`)
2. Step Function 入口形态(`model_step` 单 step / 多 rate `model_step0/1` / Reusable 形态)
3. 模型子系统 ↔ 生成函数映射(原子子系统 → 函数边界)
4. 模型参数对象 ↔ 生成代码全局变量(含存储类前缀/后缀命名规则的实际落地)
5. Bus / 信号 ↔ 生成代码结构体与字段
6. 与手写桥接层(如 FMT 接口层)的契合点(调用入口、数据交换约定)

## 不负责

1. Embedded Coder 配置审查 → 走 `clm-embedded-coder-config-reviewer`
2. 存储类全局治理决策 → 走 `clm-storage-class-governor`
3. 模型层结构解读 → 走 `clm-simulink-model-reader`
4. Stateflow 内部语义 → 走 `clm-stateflow-semantics-reader`
5. 修改模型或代码 → 走 `model-authoring/`
6. 测试用例与覆盖率 → 走 `verification/`

## 推荐阅读顺序

1. 先看代码生成报告(若存在 `html/<model>_codegen_rpt.html` / `.txt`)— 直接给出主入口与 file 列表
2. 再看 `*_types.h`(类型定义)与 `*_private.h`(内部结构)
3. 再看 `*.c` 主文件(找 `model_step` / `model_initialize`)
4. 再看 `*_data.c`(参数与初值)
5. 最后(若提供)看手写桥接层(`*_interface.c`)的调用点

## 执行步骤

1. **确认工具上下文**:Embedded Coder 版本、生成时间戳、目标硬件、类型定义来源
2. **一致性预检**:对比代码生成时间戳与模型最新修改时间戳;不一致时标记"代码可能过时",不阻断,但所有结论携带降级标签
3. **抓取主入口**:从 `*.c` 找 `<model>_step` / `<model>_initialize` / `<model>_terminate` 与签名
4. **建立子系统 → 函数映射**:
   - 逐个 Atomic Subsystem 在生成代码中查找对应函数(命名常为子系统名 + 后缀,或在 `Reusable` 模式下集中在共享 utility)
   - 记录函数所在文件 + 行号
5. **建立参数 → 全局变量映射**:
   - 从 `*_data.c` / `*_private.h` 抓取参数对象
   - 对照模型 `Simulink.Parameter` 名(若提供 `simulink_model_map` 直接索引)
   - 记录存储类与命名前缀/后缀
6. **建立 Bus → 结构体映射**:
   - 从 `*_types.h` 抓取结构体定义与字段
   - 对照模型 Bus Object 名
7. **桥接层契合点识别**:
   - 若提供手写桥接层路径,扫描调用 `<model>_step` 的位置、读写生成代码全局变量的位置
   - 不评价桥接代码质量,只标位置
8. **生成工件**:按 `references/output-template.md` 填充 `codegen_output_map`
9. **自检**:按 `references/checklist.md` 复核

## 输出要求

至少包含:

1. 工具上下文小结(版本、生成形态、时间戳一致性)
2. 文件结构地图(`*.c` / `*.h` / `*_data.c` / `*_private.h` / `*_types.h` 的角色)
3. Step Function 入口表(函数签名、所在文件、调用约定)
4. 子系统 ↔ 函数映射表
5. 参数 ↔ 全局变量映射表
6. Bus ↔ 结构体映射表
7. 桥接层契合点表(如提供)
8. 关键事实(Facts)、关键推断(Inferences,带置信度)
9. 证据索引(代码文件路径 + 行号 + 模型对象路径)
10. 缺口清单与下游输入建议

## 上下游交接(Artifact Handoff)

1. 上游依赖(Upstream Dependencies)
   - 用户提供的模型 + 生成代码 + (可选)桥接代码
   - (推荐)`clm-simulink-model-reader` 的 `simulink_model_map`
   - (推荐)`clm-embedded-coder-config-reviewer` 的 `coder_config_review`
2. 下游使用方(Downstream Consumers)
   - `clm-storage-class-governor`(消费参数 ↔ 全局变量映射作为治理输入)
   - `clm-codegen-compliance-refactor`(消费"非预期映射"作为重构 backlog)
   - `clm-pil-hil-replay-analyzer`(消费 Step Function 入口与全局变量名以做 PIL/HIL 数据回放)
   - `clm-control-law-mbd-pipeline`(编排技能)
   - `fmt-mbd-interface-reader`(跨库:本工件 `bridge_layer_contract` ↔ FMT 工件 `mbd_boundary_map`)
3. 主交付工件(Primary Artifact)
   - `codegen_output_map`
   - 字段:`tool_context`、`scope`、`facts`、`inferences`、`evidence_index`、`gaps`、`next_skill_inputs`、`model_to_code_map`、`bridge_layer_contract`(详见 `../../_meta/artifact-handoff-contract.md`)
4. 共享规范(Shared Contracts)
   - `../../_meta/first-principles-skill-contract.md`
   - `../../_meta/artifact-handoff-contract.md`
   - `../../_meta/quality-scorecard.md`

## 质量门禁(Quality Gates)

1. 必过门禁(Mandatory Gates)
   - 边界门禁(Boundary Purity):不审查配置、不治理存储类、不评价桥接代码质量
   - 证据门禁(Evidence Traceability):每条映射都给出"模型对象路径 + 代码文件路径 + 行号"
   - 工具上下文门禁:版本 + 生成时间戳 + 模型时间戳已比较;不一致时降级标签必须随结论传递
   - 一致性门禁(Consistency Discipline):若映射不完整(如某子系统找不到对应函数),必须在 `gaps` 列出而不是硬猜
   - 交接门禁:下游可直接消费,不只描述
2. 自检建议(Self Check)
   - 使用 `../../_meta/quality-scorecard.md` 打分(目标 ≥10/12)

## 失败与降级策略(Failure / Fallback)

1. 输入不足处理
   - **未提供生成代码**:本 skill 无法运行;请用户先生成代码或转交 `clm-embedded-coder-config-reviewer` 审查配置
   - **代码与模型版本不匹配**(时间戳差异 / 校验和差异):降级标签随所有结论传递,优先要求重新生成代码
   - **未提供 `simulink_model_map`**:可继续工作,但模型对象名只能从代码反推(置信度降级)
   - **未提供桥接层代码**:跳过桥接层契合点章节,在 `gaps` 中登记
   - **生成代码过大**:先输出文件角色地图,再按用户指定的子系统/参数下钻
2. 输出降级要求
   - 降级输出必须显式标注受影响结论与置信度变化
   - 降级不等于跳步;不得越过本技能职责评价桥接代码或生成代码合规性

## references/ 使用建议

1. 输出前先加载 `references/output-template.md` 作为骨架
2. 交付前用 `references/checklist.md` 复核映射完整性、证据、降级
3. 跨库交接场景(对接 `fmt-mbd-interface-reader`)前重点检查 `bridge_layer_contract` 字段齐全

## 分析纪律

1. 不把"代码生成时间戳一致"误作"代码与模型一致" — 还要看 checksum / 配置 / 关键签名
2. 不把"找不到子系统对应函数"误作"没生成" — 可能是 Reusable / Inlined,需要追内联点
3. 不在本 skill 内对桥接代码下"接错了"的结论 — 这要 `clm-storage-class-governor` 或人工 review
4. 跨库交接保留两侧 `tool_context` / `firmware_context`,不混用
