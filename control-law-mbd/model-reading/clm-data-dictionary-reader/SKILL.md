---
name: clm-data-dictionary-reader
description: 读取 Simulink Data Dictionary(`.sldd`)及其引用层级、`Simulink.Parameter` / `Simulink.Signal` / `Simulink.Bus` / `Simulink.AliasType` 等参数对象的作用域、类型、初值、存储类的专用只读技能。用于需要把"参数/信号到底是什么类型、定义在哪、谁可见、生成代码会落到哪类全局变量"梳理清楚时;不负责模型层结构解读、不负责 Stateflow 语义、不负责 Embedded Coder 配置审查、不负责修改字典。
---

# Control-Law-MBD: Data Dictionary Reader

## 目标

在不修改任何字典或模型的前提下,把指定 Simulink Data Dictionary(SLDD,`.sldd`)的对象层级、引用关系、作用域、类型、初值、存储类梳理清楚,产出一份可被 `clm-codegen-output-mapper` 与 `clm-storage-class-governor` 直接消费的字典地图工件。

## 第一性原理任务定义(First-Principles Task Definition)

1. 最小任务单元(Minimum Task Unit)
   - 在单一 SLDD(及其 Reference Dictionary 引用链)范围内,完成对象清单、作用域、类型、初值、存储类的证据化梳理,产出 `data_dictionary_map` 工件
2. 工具上下文(Tool Context)
   - Simulink 版本(影响 SLDD 内部 schema)
   - SLDD 形态(单文件 / 含 Reference Dictionaries / Configuration Sets 是否存于字典)
   - 是否启用 Source Control 集成(SLDD 与外部源控的合并语义)
   - 许可证可用性(无许可证时只能从 `.sldd` 二进制 / XML 解析对象,部分 API 不可用)
3. 核心输入(Inputs)
   - SLDD 路径(必需)
   - (可选)绑定 SLDD 的模型路径(用于交叉验证哪些对象被实际使用)
   - (可选)`clm-simulink-model-reader` 的 `simulink_model_map`(从中提取模型实际引用的字典对象集合)
4. 核心输出(Outputs)
   - 主交付工件:`data_dictionary_map`
   - 引用层级图、对象清单(类型 / 作用域 / 初值 / 存储类)、未引用对象列表、跨字典命名冲突检测
5. 完成判据(Definition of Done, DoD)
   - SLDD 引用层级(Top dictionary → Reference dictionaries)已明确
   - 至少覆盖 `Simulink.Parameter` / `Simulink.Signal` / `Simulink.Bus` / `Simulink.AliasType` 四类对象
   - 每个对象的存储类(Storage Class)与生成代码影响已记录(SimulinkGlobal / ExportedGlobal / ImportedExtern / Custom 等)
   - 至少识别一类常见风险(命名冲突 / 未引用对象 / 存储类不一致 / 类型未指定)
   - 工具上下文显式记录,许可证缺失时降级路径明确
6. 输出语言约定(Language Convention)
   - 默认中文输出;专业术语首次出现附英文注释
   - 保留对象名、类型名、存储类名原文

## 聚焦范围(只做这些)

1. SLDD 引用层级(Top / Reference Dictionary 树)
2. 对象清单与分类(Parameter / Signal / Bus / AliasType / Numeric Type 等)
3. 类型(Built-in / Alias / Bus / Enum / Fixed-Point)
4. 作用域(Design Data / Configuration Sets / Other Data)
5. 初值与 Min/Max
6. 存储类(Storage Class:`SimulinkGlobal` / `ExportedGlobal` / `ImportedExtern` / `Custom` / `Auto`)
7. 引用一致性(模型实际引用 vs 字典定义)与命名冲突

## 不负责

1. 模型层结构 → 走 `clm-simulink-model-reader`
2. Stateflow 内部语义 → 走 `clm-stateflow-semantics-reader`
3. Embedded Coder 配置审查 → 走 `clm-embedded-coder-config-reviewer`
4. 生成代码 ↔ 字典对象的具体映射 → 走 `clm-codegen-output-mapper`(本 skill 只标存储类策略)
5. 存储类全局治理决策 → 走 `clm-storage-class-governor`(本 skill 只发现问题点)
6. 修改字典 → 走 `model-authoring/`

## 推荐阅读顺序

1. 先看 Top SLDD 的属性与 Reference Dictionaries 引用清单
2. 再看 Design Data 段(Parameter / Signal / Bus 主战场)
3. 再看 Configuration Sets 段(若字典内置配置)
4. 再看 Other Data 段
5. 最后做"模型 vs 字典"引用一致性比对(若提供 `simulink_model_map`)

## 执行步骤

1. **确认工具上下文**:Simulink 版本、SLDD 形态、是否含 Reference Dictionaries、许可证可用性
2. **抓引用层级**:从 Top SLDD 递归列出 Reference Dictionaries,标注循环引用风险
3. **抓对象清单**:对四类核心对象逐一列出名称、类型、作用域
4. **抓存储类**:每个 Parameter / Signal 的 Storage Class 与代码生成影响
5. **抓类型链**:Alias Type 与 Bus Object 的指向链(避免类型循环)
6. **一致性检查**(若提供 `simulink_model_map`):
   - 模型引用但字典缺失的对象 → 列入 `gaps`
   - 字典定义但模型未引用的对象 → 列入"未引用对象"
   - 跨 Reference Dictionary 同名对象 → 列入"命名冲突"
7. **风险识别**:类型未指定、存储类设置为 `Auto` 但用户期望显式控制、Min/Max 为空等
8. **生成工件**:按 `references/output-template.md` 填充 `data_dictionary_map`
9. **自检**:按 `references/checklist.md` 复核

## 输出要求

至少包含:

1. 工具上下文小结
2. SLDD 引用层级图
3. 对象清单(分类列表,含类型 / 作用域 / 初值 / 存储类)
4. 类型链(Alias / Bus 指向)
5. 引用一致性结论(若有 `simulink_model_map`)
6. 风险清单(命名冲突 / 未引用 / 类型未指定 / 存储类不一致)
7. 关键事实(Facts)、关键推断(Inferences,带置信度)
8. 证据索引(SLDD 路径 + 对象名 + 段)
9. 缺口清单与下游输入建议

## 上下游交接(Artifact Handoff)

1. 上游依赖
   - 用户提供的 SLDD 路径与(可选)模型路径
   - (推荐)`clm-simulink-model-reader` 的 `simulink_model_map`
2. 下游使用方
   - `clm-codegen-output-mapper`(消费存储类策略 + 类型链以匹配生成代码全局变量)
   - `clm-storage-class-governor`(消费对象清单 + 风险作为治理输入)
   - `clm-codegen-compliance-refactor`(消费风险作为重构 backlog)
   - `clm-control-law-mbd-pipeline`(编排技能)
3. 主交付工件
   - `data_dictionary_map`
   - 字段:`tool_context`、`scope`、`facts`、`inferences`、`evidence_index`、`gaps`、`next_skill_inputs`、`bus_object_table`、`parameter_object_table`(详见 `../../_meta/artifact-handoff-contract.md`)
4. 共享规范
   - `../../_meta/first-principles-skill-contract.md`
   - `../../_meta/artifact-handoff-contract.md`
   - `../../_meta/quality-scorecard.md`

## 质量门禁(Quality Gates)

1. 必过门禁(Mandatory Gates)
   - 边界门禁:不审查模型层结构 / 不评价 Embedded Coder 配置 / 不替代 `clm-storage-class-governor` 的全局治理决策
   - 证据门禁:每条结论给出"SLDD 路径 + 对象名 + 段"
   - 工具上下文门禁:Simulink 版本、SLDD 形态、许可证状态显式记录
   - 引用一致性纪律:模型 vs 字典差异显式分类(模型引用但字典缺失 / 字典定义但模型未引用 / 命名冲突)
   - 交接门禁:工件可被下游 skill 直接消费
2. 自检建议:使用 `../../_meta/quality-scorecard.md` 打分(目标 ≥10/12)

## 失败与降级策略(Failure / Fallback)

1. 输入不足处理
   - **无 Simulink 许可证**:降级到从 `.sldd` 二进制 / XML 解析对象,声明"无法运行字典 API / 无法做 Configuration Set Reference 解析";部分高级查询(如脚本化对象)不可用
   - **未提供模型**:可继续工作,但跳过引用一致性检查并在 `gaps` 中登记
   - **Reference Dictionary 缺失**:列入 `gaps`,不假设其内容
   - **字典加密 / 受保护**:不硬猜内容
   - **SLDD 与模型版本不匹配**:降级标签随结论传递
2. 输出降级要求
   - 降级输出必须显式标注受影响结论与置信度变化
   - 降级不等于跳步;不得越过本技能职责给出"代码生成会怎样"的结论

## references/ 使用建议

1. 输出前先加载 `references/output-template.md` 作为骨架
2. 交付前用 `references/checklist.md` 复核引用一致性、风险分类、降级
3. 大型字典:先输出 Top + Reference 层级图,再按用户关注对象分类下钻

## 分析纪律

1. 不把"对象类型为 Built-in double"等同为"无风险" — 还要看 Storage Class 与 Min/Max
2. 不把"未引用对象"立刻视为应删除 — 可能是测试 harness 或外部脚本使用
3. 不把跨字典同名对象自动当作"冲突" — 需结合作用域判断
4. Storage Class 为 `Auto` 时显式标注"实际存储类由代码生成决定",不假设结果
5. 不在本 skill 内做"应该改成 X"的治理决策 — 转交 `clm-storage-class-governor`
