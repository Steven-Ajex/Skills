---
name: clm-gain-scheduling-author
description: 针对增益调度(Gain Scheduling)控制律 — 按工况(Operating Point)分段调参的结构 — 输出 Simulink 建模骨架的写操作类技能。覆盖调度变量(Scheduling Variable)选型、调度表(Lookup Table)结构(1-D / N-D)、插值方式、调度切换平滑(无 bumpless transfer 风险)、与既有 PID/LQR pattern 的接入、参数对象声明、风险登记。用于 VTOL 转换 / 高度速度变化 / 气动包线分段调参等场景;不重做 PID/LQR 选型(走 `clm-control-law-pattern-author`,本 skill 在已有 pattern 上做调度化扩展)、不修改模型(只产出骨架)、不给具体调度表数值。
---

# Control-Law-MBD: Gain Scheduling Author

## 目标

把"已有控制律 pattern + 调度变量 + 工况覆盖网格"扩展为可施工的增益调度(Gain Scheduling)建模骨架,产出 `gain_scheduling_skeleton` 工件。本 skill 是**专精 pattern 扩展** — 不替代 `clm-control-law-pattern-author`,而是在其基础上加调度结构。

## 第一性原理任务定义(First-Principles Task Definition)

1. 最小任务单元(Minimum Task Unit)
   - 在单一基础 pattern(PID / LQR / Lead-Lag / 状态反馈) + 单一调度变量集合 + 单一工况网格范围内,完成调度表结构、插值、平滑切换、参数对象声明、连接 diff,产出 `gain_scheduling_skeleton` 工件
2. 工具上下文(Tool Context)
   - Simulink 版本与 Lookup Table Block 类型(1-D / 2-D / n-D / Prelookup + Interpolation)
   - 数值形态(浮点 / 定点 — 定点时插值精度严格)
   - 采样时间 + 调度更新率(可与控制律不同)
   - 是否使用 `Simulink.LookupTable` 对象
3. 核心输入(Inputs)
   - **必需**:基础 pattern(已有 `control_law_pattern_skeleton` 或现成 Subsystem 路径)
   - **必需**:调度变量集合(信号名 + 类型 + 范围)— 例如 `velocity_mps`、`altitude_m`、`mass_kg`、`mode`
   - **必需**:工况网格(每个调度变量的离散点)
   - **推荐**:`clm-simulink-model-reader` 的 `simulink_model_map`(端口与原子化)
   - **推荐**:`clm-data-dictionary-reader` 的 `data_dictionary_map`(参数对象现状)
   - (可选)项目级调度规范(插值方式 / 平滑切换要求)
4. 核心输出(Outputs)
   - 主交付工件:`gain_scheduling_skeleton`
   - 调度变量声明(类型 / 范围 / 采样)
   - 调度表结构(1-D / N-D + 维度顺序 + 网格点)
   - 插值方式(线性 / 平直 / 三次样条 / 最近邻;边界外推策略)
   - 调度切换平滑(无突变 / Hold / Filter 等)
   - 参数对象声明(`Simulink.LookupTable` / `Simulink.Parameter` 模板,含数值占位)
   - 与基础 pattern 的接入 diff(每个 PID 增益从常量改为查表输出)
   - 多通道处置(各通道独立调度 vs 共享调度变量)
   - 风险登记(切换时的 bumpless transfer / 边界外推 / 数值精度)
5. 完成判据(Definition of Done, DoD)
   - 调度变量已声明(信号名 + 类型 + 范围)
   - 工况网格定义完整;每个维度的离散点已给出
   - 调度表结构(维度顺序 + 网格大小)显式
   - 插值方式 + 边界外推策略已说明
   - 调度切换平滑机制(防止 PID 增益突变引起的 bumpless 问题)已给出
   - 参数对象声明含 LookupTable 数据占位 + Storage Class 建议
   - 与基础 pattern 的 diff 可施工
   - 风险登记含 bumpless transfer / 边界外推 / 调度变量噪声 / 定点插值精度
   - 工具上下文显式记录;数值形态显式声明
6. 输出语言约定(Language Convention)
   - 默认中文输出;专业术语首次出现附英文注释
   - 保留调度变量名 / 参数名 / Block 名(英文)原文

## 聚焦范围(只做这些)

1. 调度变量选型与声明
2. 工况网格定义(每个维度离散点)
3. 调度表结构(维度顺序 / 网格大小 / `Simulink.LookupTable` 选型)
4. 插值方式 + 边界外推策略
5. 调度切换平滑(bumpless transfer)
6. 多通道调度处置(独立 / 共享)
7. 与基础 pattern 的接入 diff(增益从常量 → 查表)
8. 参数对象声明(LookupTable + 数值占位)
9. 风险登记

## 不负责

1. 重做基础 pattern 选型 → 走 `clm-control-law-pattern-author`
2. 修改模型(只产出骨架)
3. 给具体调度表数值 — 只给数值占位 + 选型范围
4. 真实做调度网格的"工况点采集" — 由系统辨识 / 飞行测试 完成,本 skill 消费产物
5. 审查 Coder 配置 / 设计测试用例
6. 定点重构 → 走 `clm-fixed-point-refactor`(本 skill 在浮点假设下推导,定点形态时声明降级)

## 推荐设计顺序

1. 先确认"基础 pattern 边界" — 增益数量、增益类型(标量 / 向量 / 矩阵)
2. 再选"调度变量" — 飞行包线 / 工况覆盖一致;数量越少越好(查表维度暴增)
3. 再设计"工况网格" — 关键工况点 + 边界 + 插值密度
4. 再选"调度表结构" — 1-D 优先;N-D 慎用(数据量爆炸)
5. 再选"插值方式 + 边界外推" — 线性最常用,定点形态需要平直查表
6. 再设计"调度切换平滑" — bumpless transfer 必须考虑
7. 再做"多通道处置" — 共享调度变量 vs 独立查表
8. 最后写"接入 diff" + "风险登记"

## 执行步骤

1. **确认工具上下文**:Simulink 版本、Lookup Table Block 类型、数值形态、采样时间、调度更新率
2. **基础 pattern 边界**:从上游 `control_law_pattern_skeleton` 抓增益清单(`Kp` / `Ki` / `Kd` / 状态反馈矩阵 K 等)
3. **调度变量选型**:
   - 信号名 + 类型 + 范围
   - 选型理由(飞行包线相关性 + 噪声敏感性 + 可观测性)
4. **工况网格**:
   - 每个调度变量的离散点(关键工况点 + 边界点)
   - 网格密度选择理由
5. **调度表结构**:
   - 1-D / 2-D / N-D
   - 维度顺序(影响内存布局)
   - 是否使用 `Simulink.LookupTable` 对象
6. **插值方式**:
   - 线性 / 平直(Flat) / 三次样条 / 最近邻
   - 定点形态用平直查表(Lookup Table Direct)更合适
   - 边界外推策略(Clip / Linear Extrap / Hold)
7. **调度切换平滑**:
   - bumpless transfer 实现(增益突变时的过渡)
   - 用一阶低通滤波 / 渐变(Slew Rate Limit)
   - 与积分项的相互作用(若涉及)
8. **多通道处置**:独立查表 / 共享调度变量 / MIMO 调度矩阵
9. **接入 diff**:逐增益从"Constant Block / Parameter"改为"Lookup Table 输出"
10. **参数对象声明**:`Simulink.LookupTable` 含数据占位 + Storage Class 建议
11. **风险登记**:
    - bumpless transfer
    - 边界外推风险
    - 调度变量噪声引起的增益抖动
    - 定点插值精度损失
    - 网格点之间增益变化率过大导致系统不稳
12. **生成工件**:按 `references/output-template.md` 填充
13. **自检**:按 `references/checklist.md` 复核

## 输出要求

至少包含:

1. 工具上下文小结
2. 基础 pattern 引用
3. 调度变量声明
4. 工况网格
5. 调度表结构
6. 插值方式 + 边界外推策略
7. 调度切换平滑机制
8. 多通道处置(若适用)
9. 接入 diff
10. 参数对象声明
11. 风险登记
12. 关键事实(Facts)、关键推断(Inferences)
13. 缺口与下游输入建议

## 上下游交接(Artifact Handoff)

1. 上游依赖
   - **必需**:基础 pattern 引用
   - **必需**:调度变量集合 + 工况网格
   - (推荐)`simulink_model_map` / `data_dictionary_map`
   - (可选)`control_law_pattern_skeleton` / 项目级调度规范
2. 下游使用方
   - 工程师 / 评审(直接施工)
   - `clm-codegen-compliance-refactor`(消费风险登记)
   - `clm-test-harness-builder`(消费工况网格作为测试场景)
   - `clm-fixed-point-refactor`(若涉及定点)
   - `clm-control-law-mbd-pipeline`(编排技能)
3. 主交付工件
   - `gain_scheduling_skeleton`
   - 字段:`tool_context`、`scope`、`facts`、`inferences`、`evidence_index`、`gaps`、`next_skill_inputs`、`pattern_choice`(此处 = "gain-scheduling")、`scheduling_variables`、`grid_definition`、`lookup_structure`、`risk_register`(详见 `../../_meta/artifact-handoff-contract.md`)
4. 共享规范
   - `../../_meta/first-principles-skill-contract.md`
   - `../../_meta/artifact-handoff-contract.md`
   - `../../_meta/quality-scorecard.md`

## 质量门禁(Quality Gates)

1. 必过门禁(Mandatory Gates)
   - 边界门禁:不重做基础 pattern / 不修改模型 / 不给具体数值 / 不采集工况点
   - 调度变量纪律(Scheduling Variable Discipline):每个变量含信号名 + 类型 + 范围 + 选型理由
   - 工况网格纪律(Grid Discipline):网格密度选择有理由;边界点必含
   - 平滑切换纪律(Bumpless Discipline):必须显式给出 bumpless 机制,不能默认
   - 多通道纪律:独立 / 共享 / MIMO 必须显式判定
   - 工具上下文门禁:Simulink 版本 / Lookup Table 类型 / 数值形态 / 采样 显式记录
   - 完整性门禁:13 项输出齐全(若适用项缺失须显式标注)
2. 自检建议:使用 `../../_meta/quality-scorecard.md` 打分(目标 ≥10/12)

## 失败与降级策略(Failure / Fallback)

1. 输入不足处理
   - **未提供基础 pattern**:阻断;调度化必须基于已有 pattern
   - **未提供调度变量**:阻断 — 调度的核心
   - **未提供工况网格**:阻断或降级为"建议网格密度",标注需补充
   - **数值形态(浮点/定点)未确定**:浮点假设下推导,标注定点形态需评估插值精度
   - **未提供 `simulink_model_map`**:接入 diff 降级为"建议位置",置信度低
   - **多通道但耦合关系未提供**:默认"独立调度",显式声明假设
2. 输出降级要求
   - 降级输出必须显式标注受影响段
   - 降级不等于跳步;不得给"调度已可投产"结论 — 由测试与回放验证

## references/ 使用建议

1. 输出前先加载 `references/output-template.md`
2. 交付前用 `references/checklist.md` 复核调度变量纪律、bumpless 纪律、降级
3. N-D 调度场景重点检查"维度顺序"和"网格点存储布局"

## 设计纪律

1. 调度变量数 ≤ 3 优先 — N-D 表数据量爆炸
2. 调度切换 bumpless transfer 不能省 — 否则瞬态会很大
3. 边界外推策略不能默认 — 飞行包线之外的行为必须显式
4. 定点形态下 Lookup Table 插值精度敏感 — 转 `clm-fixed-point-refactor` 评估
5. 调度变量噪声会引起增益抖动 — 必须考虑前置滤波或低通
6. 不在本 skill 内做"调度增益数值"决策 — 那是系统辨识 / 调参的产物
