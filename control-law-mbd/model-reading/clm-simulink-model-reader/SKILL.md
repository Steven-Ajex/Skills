---
name: clm-simulink-model-reader
description: 读取 Simulink 模型(`.slx` / `.mdl`)的层级结构、子系统、信号流、采样时间(Sample Time)与原子单元(Atomic Subsystem)边界的专用只读技能。用于需要建立"模型在做什么、信号怎么走、节拍如何分布"的认识时;不负责修改模型、不负责 Stateflow 状态机内部语义、不负责数据字典深入解读、不负责代码生成配置审查。
---

# Control-Law-MBD: Simulink Model Reader

## 目标

在不修改任何模型的前提下,把 Simulink 模型的**层级、信号流、采样时间、原子单元**梳理清楚,产出一份可被下游 skill 与人工 reviewer 直接引用的"模型地图"。

## 第一性原理任务定义(First-Principles Task Definition)

1. 最小任务单元(Minimum Task Unit)
   - 在单一 Simulink 模型(及其引用模型 Model Reference 与绑定的数据字典)范围内,完成层级、子系统、信号流、采样时间一致性、原子单元识别的证据化梳理。
2. 工具上下文(Tool Context)
   - Simulink / Stateflow 版本(例:R2020b、R2023b)
   - 模型形态(`.slx` 或 `.mdl`)、是否含引用模型(Model Reference)、是否绑定 `.sldd`
   - 许可证可用性(无许可证时只能从模型源解析,Model Advisor 等运行时查询不可用)
3. 核心输入(Inputs)
   - Simulink 模型路径(必需)
   - 关联的 `.sldd` 数据字典路径(可选,推荐)
   - 用户关注的子系统或信号(可选,缺省时从顶层开始)
4. 核心输出(Outputs)
   - 主交付工件:`simulink_model_map`
   - 子系统层级树、信号流路径、采样时间表、原子/虚拟子系统标记、Mask 子系统清单、证据索引、缺口清单
5. 完成判据(Definition of Done, DoD)
   - 至少一条完整"输入信号 → 子系统链 → 输出信号"路径被串起
   - 采样时间结论有模型证据(块级 SampleTime 或继承关系),不依赖默认假设
   - 原子子系统(Atomic Subsystem)与虚拟子系统(Virtual Subsystem)被显式区分
   - 工具上下文显式记录,许可证缺失时降级路径明确
6. 输出语言约定(Language Convention)
   - 默认中文输出;专业术语首次出现附英文注释(English Annotation)
   - 保留子系统名、信号名、参数名、Bus 名原文,避免翻译造成歧义

## 聚焦范围(只做这些)

1. 子系统层级与命名(含 Subsystem / Atomic Subsystem / Model Reference / Library Link)
2. 信号流(In/Out 端口、Goto/From、Bus Creator/Selector、Mux/Demux)
3. 采样时间(Sample Time)与离散/连续标记
4. 原子单元(Atomic Subsystem)与虚拟子系统的边界
5. Mask 子系统的参数面板与初始化代码出处

## 不负责

1. Stateflow 内部状态/转移/事件语义 → 走 `clm-stateflow-semantics-reader`
2. `.sldd` 数据字典与 `Simulink.Parameter` / `Simulink.Bus` 深入解读 → 走 `clm-data-dictionary-reader`
3. 需求与模型的双向追溯链 → 走 `clm-requirement-trace-reader`
4. 模型修改、控制律建模、合规重构 → 走 `model-authoring/`
5. Embedded Coder 配置审查 → 走 `clm-embedded-coder-config-reviewer`
6. 生成代码诊断 → 走 `clm-codegen-output-mapper`

## 推荐阅读顺序

1. 模型顶层(根节点的端口、求解器配置概览)
2. 一级子系统层级与命名约定
3. 关键控制链路(顺向追:输入端口 → 中间子系统 → 输出端口)
4. Stateflow 块的位置(只标位置与端口,不深入语义)
5. Mask 子系统的参数面板与回调
6. 引用模型(Model Reference)与库链接(Library Link)的指向

## 执行步骤

1. **确认工具上下文**:Simulink 版本、模型形态、是否绑定 `.sldd`、许可证是否可用。无许可证时声明降级到模型源解析(`.slx` 解压后的 XML 或 `.mdl` 文本)。
2. **抓顶层结构**:列出根级 Block / Subsystem,标注端口数与命名。
3. **逐层下钻**:按用户关注链路或顶层默认顺序,记录每层子系统的输入、输出、内部主要 Block。
4. **采样时间核对**:对每个 Subsystem 与关键 Block 抓取 SampleTime,标记 inherited / discrete / continuous,识别多速率(Multirate)边界。
5. **原子单元识别**:扫描 `Atomic Subsystem` 标记,标注与虚拟子系统的差异(影响代码生成边界)。
6. **Mask 与引用**:列出 Mask 子系统的参数面板与初始化代码出处;列出 Model Reference 与 Library Link 的目标。
7. **生成工件**:按 `references/output-template.md` 填充 `simulink_model_map`。
8. **自检**:按 `references/checklist.md` 复核边界、证据、降级。

## 输出要求

至少包含:

1. 子系统层级树(含 Atomic / Virtual / Model Reference 标记)
2. 信号流路径(至少一条端到端控制链路)
3. 采样时间表(块级 SampleTime + 多速率边界)
4. Mask 子系统清单与参数面板出处
5. 引用模型 / 库链接清单
6. 关键事实(Facts)、关键推断(Inferences,带置信度)
7. 证据索引(模型路径 + 子系统路径,如 `model.slx > Controller/AttitudeLoop/PID`)
8. 缺口清单(许可证缺失、字典未解析、子系统加密等)与下游输入建议

## 上下游交接(Artifact Handoff)

1. 上游依赖(Upstream Dependencies)
   - 用户提供的模型路径与工具上下文
   - (可选)`clm-requirement-trace-reader` 的需求 → 子系统映射
2. 下游使用方(Downstream Consumers)
   - `clm-stateflow-semantics-reader`(消费 Stateflow 块位置)
   - `clm-data-dictionary-reader`(消费字典引用清单)
   - `clm-codegen-output-mapper`(消费子系统树以建立模型 ↔ 代码映射)
   - `clm-embedded-coder-config-reviewer`(消费多速率与原子单元信息以评估配置合规)
   - `clm-control-law-mbd-pipeline`(编排技能)
3. 主交付工件(Primary Artifact)
   - `simulink_model_map`
   - 工件至少包含:`tool_context`、`scope`、`facts`、`inferences`、`evidence_index`、`gaps`、`next_skill_inputs`(详见 `../../_meta/artifact-handoff-contract.md`)
4. 共享规范(Shared Contracts)
   - `../../_meta/first-principles-skill-contract.md`
   - `../../_meta/artifact-handoff-contract.md`
   - `../../_meta/quality-scorecard.md`

## 质量门禁(Quality Gates)

1. 必过门禁(Mandatory Gates)
   - 边界门禁(Boundary Purity):不输出 Stateflow 状态语义、不输出代码生成结论、不修改模型
   - 证据门禁(Evidence Traceability):关键结论必须能回链到模型路径 + 子系统路径
   - 工具上下文门禁(Tool Context Explicitness):Simulink 版本与许可证状态必须显式记录
   - 交接门禁(Handoff Usability):工件可被下游 skill 直接消费,不只给散文式描述
   - 速率门禁(Sample Time Discipline):多速率结论必须指明具体 Block / Subsystem 与 SampleTime 值
2. 自检建议(Self Check)
   - 使用 `../../_meta/quality-scorecard.md` 对本次输出快速打分(目标 ≥10/12)

## 失败与降级策略(Failure / Fallback)

1. 输入不足处理
   - **无 Simulink 许可证**:降级到从 `.slx` 解压的 XML 或 `.mdl` 文本读取结构,显式标注"无法运行 Model Advisor / 无法查询 CompiledSampleTime"
   - **模型过大**:先输出顶层结构地图,再按用户指定子系统下钻;不一次性下钻全部
   - **`.sldd` 缺失**:声明无法解读字典对象,引用 `clm-data-dictionary-reader` 作为后续依赖
   - **子系统加密 / 受保护**:列出无法访问的子系统并在 `gaps` 中登记
2. 输出降级要求
   - 降级输出必须显式标注受影响结论、受影响范围、置信度变化
   - 降级不等于跳步;不得越过本技能职责给出 Stateflow 语义或代码生成结论

## references/ 使用建议

1. 输出前先加载 `references/output-template.md` 作为骨架,避免遗漏交接字段
2. 交付前用 `references/checklist.md` 复核边界、证据、采样时间纪律、降级策略
3. 顶层结构地图阶段可以不加载模板;下钻阶段建议加载

## 分析纪律

1. 不把 Subsystem 名(中文/英文/缩写)误作语义结论,要回到内部 Block 与端口
2. 不把虚拟子系统(Virtual Subsystem)与原子子系统(Atomic Subsystem)混用 — 后者是代码生成的函数边界,前者只是视图
3. 多速率系统中不假设单一基准节拍,要标注每条链路的采样时间来源
4. 不在本技能内给出"代码会怎么生成"的结论 — 这是 `codegen-bridge/` 的职责
