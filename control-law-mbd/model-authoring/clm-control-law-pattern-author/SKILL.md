---
name: clm-control-law-pattern-author
description: 按标准控制律结构(PID、LQR、增益调度、Anti-Windup、抗饱和、滤波、限幅、Lead-Lag、状态观测器等)输出 Simulink 建模骨架(subsystem 拓扑 + 参数对象声明 + 信号连接 + 采样时间与原子化策略 + 抗饱和实现 + 集成步骤)的写操作类技能。用于新建控制律子系统或为已有子系统提供"标准化重构骨架"时;不负责真实修改模型(只产出可被工程师采纳的骨架)、不负责审查 Embedded Coder 配置、不负责测试用例设计、不负责给具体参数数值(只给参数声明与默认值占位)。
---

# Control-Law-MBD: Control Law Pattern Author

## 目标

把"用户想做的控制律结构(PID / LQR / 增益调度 / Anti-Windup / 滤波 等)+ 已有的工具上下文与约束"映射成一份可被工程师直接照着搭建的 Simulink 建模骨架,产出 `control_law_pattern_skeleton` 工件。本 skill **不直接修改模型** — 它输出"骨架文档",由工程师手工或脚本化施工。

## 第一性原理任务定义(First-Principles Task Definition)

1. 最小任务单元(Minimum Task Unit)
   - 在单一控制律 pattern 选型 + 单一目标子系统路径范围内,完成 subsystem 拓扑、参数对象声明、信号连接、采样时间与原子化、抗饱和实现、集成步骤的设计,产出 `control_law_pattern_skeleton` 工件
2. 工具上下文(Tool Context)
   - Simulink 版本与目标库(Simulink 内置 vs 第三方 vs 公司库)
   - 目标采样时间 + 多速率边界(若涉及)
   - 数值形态(浮点 vs 定点;若定点,Word Length / Fraction Length)
   - 代码生成约束(Embedded Coder 默认 / 高完整性 / MISRA / AUTOSAR)
   - 公司级控制律建模规范(若提供)
3. 核心输入(Inputs)
   - Pattern 选型(必需:`pid` / `lqr` / `gain-scheduling` / `anti-windup` / `saturation` / `lead-lag` / `state-observer` / 其他自定义)
   - 目标子系统路径或"新建"标记(必需)
   - 采样时间(必需)
   - (可选)`clm-simulink-model-reader` 的 `simulink_model_map`(用于约束子系统层级与端口)
   - (可选)`clm-data-dictionary-reader` 的 `data_dictionary_map`(用于复用既有参数对象)
   - (可选)`clm-requirement-trace-reader` 的 `requirement_trace_map`(用于反向链接需求)
   - (可选)项目级控制律规范文档
4. 核心输出(Outputs)
   - 主交付工件:`control_law_pattern_skeleton`
   - Pattern 选型说明、subsystem 拓扑(Block 列表 + 信号连接)、参数对象声明清单(`Simulink.Parameter` 模板)、采样时间与原子化策略、抗饱和实现(若适用)、集成步骤(逐步)、风险登记(`risk_register`)
5. 完成判据(Definition of Done, DoD)
   - Pattern 选型已显式说明(为何选 PID 而非 LQR 等)
   - 至少一个完整 subsystem 拓扑被给出(Block 列表 + 端口 + 主要信号连接)
   - 所有可调参数已用 `Simulink.Parameter` 声明,含类型、默认值占位、Min/Max 占位、Storage Class 建议
   - 采样时间与原子化策略与目标代码生成约束一致
   - 抗饱和实现(若 pattern 含积分器)显式给出方案(Back-calculation / Conditional Integration / Clamping)
   - 集成步骤逐步可执行(从"新建子系统"到"配置参数"到"接入上层")
   - 工具上下文显式记录;数值形态(浮点/定点)显式声明
6. 输出语言约定(Language Convention)
   - 默认中文输出;专业术语首次出现附英文注释
   - 保留 Block 名 / 参数名 / 信号名(英文)原文

## 聚焦范围(只做这些)

1. Pattern 选型说明(为何此选型适合,与替代方案的折中)
2. Subsystem 拓扑(Block 列表 + 端口 + 信号连接)
3. 参数对象声明(`Simulink.Parameter` 模板,含类型/默认值占位/Min/Max 占位/Storage Class 建议)
4. 采样时间与原子化策略
5. 抗饱和实现(若涉及积分器)
6. 滤波 / 限幅 / 死区等附属结构(若 pattern 要求)
7. 集成步骤(逐步可施工)
8. 风险登记(回归点 / 与既有结构冲突 / 数值稳定性)

## 不负责

1. 真实修改模型(本 skill 只产出骨架文档,工程师施工)
2. 给具体参数数值(只给类型 + 默认值占位 + Min/Max 占位)
3. 调参建议 → 走 `fmt-tuning-report-writer` 等
4. 审查 Embedded Coder 配置 → 走 `clm-embedded-coder-config-reviewer`
5. 设计测试用例 → 走 `clm-test-harness-builder`
6. 修改字典 → 由工程师按本骨架的参数声明手工实施

## 推荐设计顺序

1. 先确定"pattern 选型与折中" — 例如 PID + Anti-Windup vs PID + 限幅,差异是数值稳定性 vs 简洁性
2. 再确定"输入/输出端口" — 与上层模型对接的契约
3. 再确定"采样时间与原子化" — 多速率系统下原子化决定函数边界
4. 再设计"主拓扑" — 误差→比例/积分/微分→限幅→输出
5. 再补"抗饱和" — 必须配合积分器,不能事后加
6. 再补"滤波/死区" — 若 pattern 要求(例如 D 项需噪声抑制)
7. 最后写"集成步骤"与"风险登记"

## 执行步骤

1. **确认工具上下文**:Simulink 版本、目标采样时间、数值形态(浮点/定点)、代码生成约束
2. **Pattern 选型说明**:写出"为何选这个 pattern"+"与替代方案的折中"
3. **设计端口契约**:输入(参考、反馈、模式信号等)与输出(控制量、状态)
4. **设计主拓扑**:逐 Block 列出 + 信号连接 + 端口
5. **声明参数对象**:用 `Simulink.Parameter` 模板列出每个可调参数(`Kp` / `Ki` / `Kd` / `u_max` / `u_min` / `tau_filter` 等),含类型 / 默认值占位 / Min/Max 占位 / Storage Class 建议
6. **采样时间与原子化**:声明 SampleTime;若需要原子化(影响代码生成函数边界)显式说明
7. **抗饱和实现**(若 pattern 含积分器):列出 Back-calculation / Conditional Integration / Clamping 三种方案,选其一并给出连接细节
8. **附属结构**(若适用):滤波器(D 项)、死区、速率限制
9. **集成步骤**:从"新建子系统(或在 `<目标路径>` 下重构)"到"接入上层"的逐步指令
10. **风险登记**:回归点、数值稳定性、与既有结构冲突
11. **生成工件**:按 `references/output-template.md` 填充
12. **自检**:按 `references/checklist.md` 复核

## 输出要求

至少包含:

1. 工具上下文小结
2. Pattern 选型说明与折中
3. 端口契约(输入/输出端口表)
4. 主拓扑(Block 列表 + 信号连接 + 端口)
5. 参数对象声明清单(`Simulink.Parameter` 模板)
6. 采样时间与原子化策略
7. 抗饱和实现(若适用)
8. 附属结构(若适用)
9. 集成步骤(逐步)
10. 风险登记(`risk_register`)
11. 关键事实(Facts)、关键推断(Inferences)
12. 缺口与下游输入建议

## 上下游交接(Artifact Handoff)

1. 上游依赖
   - 用户提供的 pattern 选型 + 目标路径 + 采样时间 + 数值形态
   - (推荐)`simulink_model_map`(端口与原子化约束)
   - (推荐)`data_dictionary_map`(复用参数对象)
   - (推荐)`requirement_trace_map`(链接需求)
2. 下游使用方
   - 工程师 / 评审(直接读骨架施工)
   - `clm-codegen-compliance-refactor`(消费"风险登记 + 与既有结构冲突"作为重构 backlog)
   - `clm-test-harness-builder`(消费端口与状态机以建立测试 harness)
   - `clm-control-law-mbd-pipeline`(编排技能)
3. 主交付工件
   - `control_law_pattern_skeleton`
   - 字段:`tool_context`、`scope`、`facts`、`inferences`、`evidence_index`、`gaps`、`next_skill_inputs`、`pattern_choice`、`structural_constraints`、`risk_register`(详见 `../../_meta/artifact-handoff-contract.md`)
4. 共享规范
   - `../../_meta/first-principles-skill-contract.md`(第 4 节"原子技能边界规则")
   - `../../_meta/artifact-handoff-contract.md`
   - `../../_meta/quality-scorecard.md`

## 质量门禁(Quality Gates)

1. 必过门禁(Mandatory Gates)
   - 边界门禁:不直接修改模型 / 不给具体参数数值 / 不审查 Coder 配置 / 不设计测试用例
   - 完整性门禁(Completeness Gate):至少 pattern 选型 + 端口契约 + 主拓扑 + 参数对象 + 采样时间 + 集成步骤 + 风险登记 七项齐全
   - 抗饱和纪律(Anti-Windup Discipline):若 pattern 含积分器,抗饱和必须显式给出方案,不能事后再补
   - 工具上下文门禁:Simulink 版本、采样时间、数值形态、代码生成约束显式记录
   - 参数对象纪律:只给类型 + 默认值占位 + Min/Max 占位 + Storage Class 建议,不给具体调参数值
   - 集成步骤可施工:每一步可被工程师直接执行,不写"开始建模"等模糊语
   - 交接门禁:工件可被下游 skill 与工程师直接消费
2. 自检建议:使用 `../../_meta/quality-scorecard.md` 打分(目标 ≥10/12)

## 失败与降级策略(Failure / Fallback)

1. 输入不足处理
   - **未指定 pattern**:列出常见 pattern 与适用场景请用户选择,不擅自选型
   - **未指定采样时间**:阻断;采样时间是采样周期/原子化/抗饱和的前提
   - **未提供 `simulink_model_map`**:可继续工作,但端口契约改为"建议端口"(置信度降级),施工时需工程师确认
   - **未提供 `data_dictionary_map`**:参数对象命名只能给候选,不复用既有对象;在 `gaps` 中登记
   - **数值形态(浮点/定点)未指定**:阻断;两者的 Block 选型与 Anti-Windup 实现明显不同
2. 输出降级要求
   - 降级输出必须显式标注受影响骨架部分与置信度变化
   - 降级不等于跳步;不得越过本技能职责给"已可投产"的结论 — 由工程师与编排技能决定

## references/ 使用建议

1. 输出前先加载 `references/output-template.md`,主拓扑表与参数声明清单直接套用
2. 交付前用 `references/checklist.md` 复核完整性、抗饱和纪律、降级
3. 大型 pattern(如增益调度 + Anti-Windup + 滤波):分章节给出,先核心 PID,再扩展为 GS-PID

## 设计纪律

1. Anti-Windup 必须随 pattern 一起设计,不允许事后补 — 后补常引入数值不一致
2. 不在没有数值形态(浮点/定点)的情况下给定点 pattern 骨架(影响 Q 格式选择)
3. 采样时间纪律:若上层是多速率,本子系统的 SampleTime 必须显式而非继承
4. 参数对象命名遵循"项目规范优先,无规范时使用通用建议(如 `Kp_<axis>`)"
5. 不给具体调参数值,但要给"合理的默认值占位区间"以避免施工后立即发散
6. 风险登记不可遗漏 — 至少含"数值稳定性 / 与既有结构冲突 / 多速率边界 / 抗饱和死区"四类
