---
name: clm-fault-injection-test-author
description: 针对控制律模型 + 嵌入式接口设计故障注入(Fault Injection)测试的写操作类技能 — 按 FMEA(Failure Mode and Effects Analysis)/ HARA(Hazard Analysis and Risk Assessment)/ FTA(Fault Tree Analysis)产物或项目级故障清单,逐故障设计"注入点 + 注入方式 + 触发场景 + 期望降级行为 + 通过判据 + 复位策略",输出可被 `clm-test-harness-builder` 与 `clm-coverage-gap-analyzer` 接力的故障测试规划。用于已识别故障模式需要落到测试用例时;不替代 FMEA / HARA / FTA 本身、不设计常规功能用例(走 test-harness-builder)、不修改模型、不真实运行测试。
---

# Control-Law-MBD: Fault Injection Test Author

## 目标

把"项目已识别的故障模式 + 控制律模型结构 + 接口契约"转化为可施工、可机器判定的故障注入测试规划,产出 `fault_injection_test_plan` 工件。本 skill **专注于故障专项**,不挤占常规功能测试 — 后者由 `clm-test-harness-builder` 负责。

## 第一性原理任务定义(First-Principles Task Definition)

1. 最小任务单元(Minimum Task Unit)
   - 在单一被测对象 + 单一故障模式清单(来自 FMEA / HARA / FTA 或项目级故障表)范围内,完成"注入点 + 注入方式 + 触发场景 + 期望降级行为 + 通过判据 + 复位策略"的设计,产出 `fault_injection_test_plan` 工件
2. 工具上下文(Tool Context)
   - Simulink Test 版本(故障注入实现机制;Test Sequence / 自定义 S-Function)
   - 是否启用 Simulink Fault Analyzer(若可用)
   - 是否启用代码侧故障注入(`Embedded Coder` + 代码补丁 / 自研框架)
   - 安全等级(ASIL / DAL / SIL / 项目自定义)
   - 许可证可用性
3. 核心输入(Inputs)
   - **必需**:故障模式清单(FMEA / HARA / FTA 产物或项目级故障表;含故障 ID / 描述 / 影响等级 / 检测要求)
   - **必需**:被测对象路径
   - **推荐**:`clm-simulink-model-reader` 的 `simulink_model_map`(注入点定位)
   - **推荐**:`clm-stateflow-semantics-reader` 的 `stateflow_semantics`(模式切换故障)
   - **推荐**:`clm-codegen-output-mapper` 的 `codegen_output_map`(代码侧注入)
   - **推荐**:`clm-requirement-trace-reader` 的 `requirement_trace_map`(故障 ↔ 需求映射)
   - (可选)`clm-test-harness-builder` 的 `test_harness_plan`(避免重复)
4. 核心输出(Outputs)
   - 主交付工件:`fault_injection_test_plan`
   - 故障矩阵(故障 ID × 注入点 × 注入方式 × 触发场景 × 期望降级 × 通过判据 × 复位策略)
   - 故障 ↔ 需求映射(若有需求工件)
   - 安全等级覆盖率(故障与 ASIL/DAL/SIL 等级映射)
   - 与常规用例的边界声明(不与 `test_harness_plan` 重复)
5. 完成判据(Definition of Done, DoD)
   - 至少覆盖故障清单中的高等级故障
   - 每条故障给出"注入点(信号 / 参数 / 模式)+ 注入方式(Stuck / Drift / Spike / Inversion / Loss)+ 触发场景 + 期望降级行为 + 通过判据(可机器判定)+ 复位策略"
   - 通过判据强制可机器判定(数值容差 / 状态序列 / 时间窗 / 输出范围)
   - 复位策略含"故障清除条件 + 系统状态恢复路径"
   - 安全等级覆盖率已统计;高等级故障 100% 覆盖
   - 与常规用例的边界显式声明
6. 输出语言约定(Language Convention)
   - 默认中文输出;专业术语首次出现附英文注释
   - 保留故障 ID / 信号名 / 模式名 / 用例 ID 原文

## 聚焦范围(只做这些)

1. 故障矩阵设计(故障 × 注入 × 触发 × 期望 × 判据 × 复位)
2. 注入点选择(信号级 / 参数级 / 模式级 / 接口级)
3. 注入方式分类(Stuck-At / Drift / Spike / Inversion / Signal Loss / Bit-Flip / 模式跳变)
4. 触发场景设计(故障引入时的工况:稳态 / 瞬态 / 模式切换 / 边界)
5. 期望降级行为(进入哪个安全模式 / 输出限幅 / 备份逻辑触发 等)
6. 通过判据(机器可判)
7. 复位策略(故障清除 + 系统恢复)
8. 安全等级覆盖率(ASIL/DAL/SIL)
9. 与 `test_harness_plan` 的边界

## 不负责

1. 替代 FMEA / HARA / FTA 本身(本 skill 消费其产物)
2. 设计常规功能用例 → 走 `clm-test-harness-builder`
3. 修改模型 / 添加故障注入 Block(只产出方案)
4. 真实运行测试 / 配置覆盖率工具
5. 调参建议
6. 安全分析的因果链推导(由安全工程师在 FMEA / FTA 中完成)

## 推荐设计顺序

1. 先把"故障清单 + 安全等级"对齐 — 高等级优先,覆盖率门槛由安全等级决定
2. 再选"注入点" — 信号 / 参数 / 模式 / 接口,粒度对应注入工具能力
3. 再选"注入方式" — 与故障性质匹配(Stuck-At ≠ Drift)
4. 再设计"触发场景" — 故障引入的工况关键
5. 再写"期望降级行为" — 必须可观测
6. 再写"通过判据" — 必须可机器判定
7. 再写"复位策略" — 单次故障 vs 持续故障 复位差别大
8. 最后做"故障 ↔ 需求映射"与"安全等级覆盖率"

## 执行步骤

1. **确认工具上下文**:Simulink Test 版本、故障注入框架、代码侧注入能力、安全等级、许可证
2. **故障清单对齐**:校验 FMEA / HARA / FTA 产物的格式与字段;按安全等级排序
3. **注入点选择**:每条故障决定注入层级(信号 / 参数 / 模式 / 接口);依据 `simulink_model_map` + `codegen_output_map` 定位
4. **注入方式选择**:Stuck-At / Drift / Spike / Inversion / Signal Loss / Bit-Flip / 模式跳变
5. **触发场景设计**:稳态 / 瞬态 / 模式切换 / 边界;与 `stateflow_semantics` 对齐(若涉及模式)
6. **期望降级行为**:与 FMEA / HARA 中的"故障检测 + 缓解响应"对齐
7. **通过判据**:数值容差 / 状态序列 / 时间窗 / 输出范围
8. **复位策略**:故障清除条件 + 系统状态恢复路径
9. **故障 ↔ 需求映射**(若有 `requirement_trace_map`)
10. **安全等级覆盖率统计**:每个 ASIL/DAL 等级的故障覆盖比例
11. **与 `test_harness_plan` 边界声明**:避免重复
12. **生成工件**:按 `references/output-template.md` 填充
13. **自检**:按 `references/checklist.md` 复核

## 输出要求

至少包含:

1. 工具上下文小结
2. 故障清单对齐结论
3. 故障矩阵(主表)
4. 故障 ↔ 需求映射(若适用)
5. 安全等级覆盖率
6. 与 `test_harness_plan` 边界声明
7. 关键事实(Facts)、关键推断(Inferences)
8. 缺口与下游输入建议

## 上下游交接(Artifact Handoff)

1. 上游依赖
   - **必需**:故障模式清单
   - **必需**:被测对象路径
   - (推荐)`simulink_model_map` / `stateflow_semantics` / `codegen_output_map` / `requirement_trace_map`
   - (可选)`test_harness_plan`(边界对齐)
2. 下游使用方
   - `clm-test-harness-builder`(消费故障矩阵作为额外用例分组,合并 harness)
   - `clm-coverage-gap-analyzer`(消费安全等级覆盖率作为额外覆盖维度)
   - `clm-pil-hil-replay-analyzer`(消费故障注入下的通过判据 + 复位策略)
   - `clm-control-law-mbd-pipeline`(编排技能)
3. 主交付工件
   - `fault_injection_test_plan`
   - 字段:`tool_context`、`scope`、`facts`、`inferences`、`evidence_index`、`gaps`、`next_skill_inputs`、`fault_matrix`、`requirement_to_fault_matrix`、`safety_level_coverage`(详见 `../../_meta/artifact-handoff-contract.md`)
4. 共享规范
   - `../../_meta/first-principles-skill-contract.md`
   - `../../_meta/artifact-handoff-contract.md`
   - `../../_meta/quality-scorecard.md`

## 质量门禁(Quality Gates)

1. 必过门禁(Mandatory Gates)
   - 边界门禁:不替代 FMEA/HARA/FTA / 不设计常规用例 / 不修改模型 / 不真实运行测试
   - 故障矩阵完整性(Fault Matrix Completeness):每条故障六字段齐全(注入点 + 注入方式 + 触发场景 + 期望降级 + 通过判据 + 复位策略);任一缺失列入 `gaps`
   - 通过判据纪律(Pass Criterion Discipline):必须可机器判定
   - 复位纪律(Reset Discipline):故障清除条件 + 系统恢复路径必须显式
   - 安全等级覆盖纪律(Safety Coverage Discipline):高等级故障必须 100% 覆盖
   - 边界纪律(Scope Boundary):与 `test_harness_plan` 不重复;若有重复显式列出并说明
   - 工具上下文门禁:Simulink Test 版本、注入框架、安全等级、许可证显式记录
2. 自检建议:使用 `../../_meta/quality-scorecard.md` 打分(目标 ≥10/12)

## 失败与降级策略(Failure / Fallback)

1. 输入不足处理
   - **未提供故障模式清单**:阻断;故障注入测试的硬前提是已识别故障
   - **故障清单格式不规范**(如缺安全等级 / 缺影响描述):标注降级,要求安全工程师补
   - **未提供 `simulink_model_map`**:注入点定位降级为"建议位置",置信度低
   - **未提供 `codegen_output_map`**:代码侧注入章节降级或跳过
   - **`stateflow_semantics` 未提供但故障涉及模式跳变**:列入 `gaps`,提示先做 Stage 1
   - **故障注入工具不可用**:测试矩阵仍可设计,但实施层降级为"理论方案",标注需手工实现
2. 输出降级要求
   - 降级输出必须显式标注受影响段
   - 降级不等于跳步;不得给"故障覆盖足够"的最终结论 — 由 `clm-coverage-gap-analyzer` 与编排技能聚合判定

## references/ 使用建议

1. 输出前先加载 `references/output-template.md`,故障矩阵直接套用
2. 交付前用 `references/checklist.md` 复核完整性、判据纪律、复位纪律、安全覆盖
3. 大型故障清单(高等级 > 30 条)分批输出

## 设计纪律

1. 故障注入测试不能"想到就写" — 必须基于 FMEA/HARA/FTA 产物
2. 通过判据不允许模糊 — "进入安全模式"要写"`mode_status == SAFE` 在 `t < 200 ms`"
3. 复位策略必须区分单次/持续故障 — 否则会有不可恢复测试残留
4. 高等级故障不允许"软覆盖" — 必须有具名用例
5. 注入方式与故障性质匹配 — Stuck-At、Drift、Spike、Inversion、Signal Loss、Bit-Flip 各有适用场景,不允许混用
6. 不在本 skill 内做安全因果链推导 — 那是 FMEA / FTA 的职责
