---
name: clm-pil-hil-replay-analyzer
description: 把 PIL(Processor-in-the-Loop)/HIL(Hardware-in-the-Loop)采集到的运行数据与基线(模型仿真输出 / 上一版本 PIL/HIL / 已批准基线)做对齐与对比,识别退化信号(`regression_signals`)、按 `test_harness_plan` 的通过判据逐条评估,并形成与 `fmt-control-performance-analyzer` 跨库对接的回放分析工件的专用只读分析技能。用于已经有 PIL/HIL 数据需要做基线对比时;不负责采集数据、不负责设计测试用例、不负责修改模型或代码。
---

# Control-Law-MBD: PIL/HIL Replay Analyzer

## 目标

把"已采集的 PIL/HIL 数据 + 基线参考"对齐、对比、量化偏差,产出一份可被工程师 review、可与 FMT 实飞分析对照的"回放分析"工件。本 skill 不替工程师"采数",只把"数已采到 → 偏差结论"这一段做严谨。

## 第一性原理任务定义(First-Principles Task Definition)

1. 最小任务单元(Minimum Task Unit)
   - 在单一被测对象 + 单一基线(参考)+ 单批 PIL/HIL 数据范围内,完成时间对齐、信号对比、通过判据评估、退化信号识别,产出 `pil_hil_replay_findings` 工件
2. 工具上下文(Tool Context)
   - PIL/HIL 平台(Simulink Real-Time / Speedgoat / dSPACE / 自研)与版本
   - 目标硬件(Target Hardware)与时钟源
   - 数据形态(`.mat` / `.mdf` / `.csv` / 自定义)
   - 采样率(Sampling Rate)与时间戳精度
   - 是否启用 Code-in-the-Loop 验证(SIL → PIL 一致性)
   - 许可证可用性
3. 核心输入(Inputs)
   - PIL/HIL 数据文件(必需)
   - 基线数据(必需:模型仿真 / 上一版本 PIL/HIL / 已批准基线 — 三选一)
   - (强烈推荐)`clm-test-harness-builder` 的 `test_harness_plan`(用于通过判据评估)
   - (推荐若做 SIL→PIL 对照)`clm-codegen-output-mapper` 的 `codegen_output_map`(信号名 ↔ 全局变量映射)
   - (可选)`clm-coverage-gap-analyzer` 的 `coverage_gap_report`(已显式接受的残留覆盖,不应在回放中新增规约)
   - (跨库可选)FMT 的 `control_performance_findings`(用于把仿真侧偏差对照实飞侧)
4. 核心输出(Outputs)
   - 主交付工件:`pil_hil_replay_findings`
   - 时间对齐说明、信号对比表、通过判据评估表、退化信号清单(`regression_signals`)、跨库交接段
5. 完成判据(Definition of Done, DoD)
   - 至少一条信号给出"PIL/HIL 时间窗 + 基线时间窗 + 量化偏差(峰值 / RMS / 相位)"
   - 时间对齐方法(交叉相关 / 触发事件 / 共同时基)与对齐残差已声明
   - `test_harness_plan` 中通过判据(若提供)逐条评估为 `PASS` / `FAIL` / `NA(不适用)`,`NA` 必须说明原因
   - 退化信号(`regression_signals`)清单含偏差指标与超限阈值
   - 工具上下文显式记录;采样率不一致时重采样方法已声明
   - 跨库交接字段(若涉及 FMT)齐全
6. 输出语言约定(Language Convention)
   - 默认中文输出;专业术语首次出现附英文注释
   - 保留信号名、模式名、用例 ID 原文

## 聚焦范围(只做这些)

1. 时间对齐(Time Alignment:交叉相关 / 触发事件 / 共同时基)
2. 采样率不一致的重采样方法(零阶保持 / 线性插值 / 抗混叠滤波)
3. 信号对比(峰值 / RMS / 相位 / 包络)
4. 通过判据评估(逐条 PASS / FAIL / NA + 证据)
5. 退化信号识别(超出基线容差或基线区间)
6. 跨库交接段(对接 `fmt-control-performance-analyzer`)

## 不负责

1. 采集 PIL/HIL 数据(用户工程实施)
2. 设计测试用例与通过判据 → 走 `clm-test-harness-builder`
3. 解读飞行日志 → 走 `fmt/log-analysis/*`
4. 控制律调参建议 → 走 `fmt-tuning-report-writer`(本 skill 只输出偏差,不给调参建议)
5. 修改模型或代码 → 走 `model-authoring/`
6. 覆盖率分析 → 走 `clm-coverage-gap-analyzer`

## 推荐分析顺序

1. 先做"时间对齐" — 这是所有后续结论的前提;对齐残差大于一定阈值时,后续偏差结论必须降级
2. 再做"采样率核对" — 不一致时声明重采样方法
3. 再做"通过判据逐条评估" — 优先于"我看到的偏差"分析,避免主观先入
4. 再做"全信号扫描" — 列出退化信号
5. 最后(若涉及 FMT)做跨库对照 — 仿真侧偏差 vs 实飞侧偏差是否互相印证

## 执行步骤

1. **确认工具上下文**:平台、版本、目标硬件、数据形态、采样率、许可证
2. **加载并对齐数据**:选用对齐方法(交叉相关 / 触发事件 / 共同时基),记录对齐残差
3. **采样率核对**:若不一致,声明重采样方法与混叠风险
4. **逐条评估通过判据**(若提供 `test_harness_plan`):
   - PASS:满足判据,给出证据时间窗
   - FAIL:不满足,给出偏差量化与责任窗
   - NA:不适用(数据未覆盖该用例),给出原因
5. **退化信号识别**:对所有共有信号扫描,峰值/RMS/相位偏差超基线容差时列入 `regression_signals`
6. **SIL→PIL 一致性**(若涉及):对照 `codegen_output_map` 的全局变量名,检查 SIL 与 PIL 数据一致性
7. **跨库段**(若涉及 FMT):生成 `cross_library_findings`,声明信号名映射与变体一致性
8. **生成工件**:按 `references/output-template.md` 填充 `pil_hil_replay_findings`
9. **自检**:按 `references/checklist.md` 复核

## 输出要求

至少包含:

1. 工具上下文小结
2. 时间对齐方法与残差
3. 采样率核对与重采样说明
4. 通过判据评估表(逐条 PASS / FAIL / NA + 证据)
5. 退化信号清单(`regression_signals`)
6. 跨库交接段(若涉及 FMT)
7. 关键事实(Facts)、关键推断(Inferences)
8. 证据索引(数据文件路径 + 时间窗 + 信号名)
9. 缺口清单与下游输入建议

## 上下游交接(Artifact Handoff)

1. 上游依赖
   - 用户提供的 PIL/HIL 数据 + 基线
   - (强烈推荐)`clm-test-harness-builder` 的 `test_harness_plan`
   - (推荐)`clm-codegen-output-mapper` 的 `codegen_output_map`
   - (可选)`clm-coverage-gap-analyzer` 的 `coverage_gap_report`
   - (跨库)FMT 的 `control_performance_findings`(若做对照)
2. 下游使用方
   - `clm-control-law-mbd-pipeline`(编排技能)
   - `fmt-control-performance-analyzer`(跨库:仿真侧偏差 vs 实飞侧偏差对照)
   - `fmt-tuning-report-writer`(跨库:作为调参证据之一)
3. 主交付工件
   - `pil_hil_replay_findings`
   - 字段:`tool_context`、`scope`、`facts`、`inferences`、`evidence_index`、`gaps`、`next_skill_inputs`、`replay_baseline`、`regression_signals`、`cross_library_findings`(详见 `../../_meta/artifact-handoff-contract.md`)
4. 共享规范
   - `../../_meta/first-principles-skill-contract.md`
   - `../../_meta/artifact-handoff-contract.md`
   - `../../_meta/quality-scorecard.md`

## 质量门禁(Quality Gates)

1. 必过门禁(Mandatory Gates)
   - 边界门禁:不采数 / 不设计用例 / 不给调参建议 / 不修改模型或代码
   - 证据门禁:每条偏差结论给出"数据文件路径 + 时间窗 + 信号名 + 量化指标"
   - 工具上下文门禁:平台、版本、目标硬件、采样率、对齐残差显式记录
   - 时间对齐纪律(Time Alignment Discipline):对齐方法 + 残差声明;残差超阈值时所有偏差结论降级
   - 通过判据纪律(Pass Criterion Discipline):逐条 PASS / FAIL / NA;NA 必须有原因
   - 跨库纪律(Cross-Library Discipline):与 FMT 衔接时信号名/变体/单位一致性显式声明
   - 交接门禁:工件可被下游 skill 与跨库 skill 直接消费
2. 自检建议:使用 `../../_meta/quality-scorecard.md` 打分(目标 ≥10/12)

## 失败与降级策略(Failure / Fallback)

1. 输入不足处理
   - **未提供基线**:本 skill 无法做对比,提示用户提供模型仿真 / 上一版本 PIL/HIL / 已批准基线之一
   - **时间对齐残差过大**:所有偏差结论降级为"粗对比",显式标注无法量化精确偏差
   - **采样率不一致且无法重采样**(单边数据缺失):降级为粗包络对比,标注混叠/虚假偏差风险
   - **未提供 `test_harness_plan`**:跳过通过判据评估章节,只做退化信号扫描
   - **未提供 `codegen_output_map`**:SIL→PIL 一致性章节降级,信号名只能从数据本身推断
   - **数据格式未识别**:列出已知支持形态,请用户提供格式说明或转换
2. 输出降级要求
   - 降级输出必须显式标注受影响结论与置信度变化
   - 降级不等于跳步;不得给出"PIL/HIL 通过 / 不通过"的最终结论 — 该结论由编排技能或工程师在汇总后给出

## references/ 使用建议

1. 输出前先加载 `references/output-template.md`,通过判据表与退化信号表直接套用
2. 交付前用 `references/checklist.md` 复核对齐纪律、判据纪律、跨库一致性
3. 涉及 FMT 跨库交接时重点检查信号名/变体/单位字段

## 分析纪律

1. 时间对齐残差不可省略 — 残差量化是后续偏差结论的可信度基础
2. 不在采样率不一致时直接逐点对比 — 必须先重采样并声明方法
3. 不在 PIL 数据上下"PIL 不通过"的最终结论 — 通过判据评估是 PASS/FAIL/NA 的逐条记录,聚合判定由编排技能或工程师做
4. 跨库对照时,本库 `regression_signals` 的信号名必须与 FMT 端 `control_performance_findings` 的信号名一致(经 `codegen_output_map` 中转)
5. 不给调参建议 — 这是 `fmt-tuning-report-writer` 的职责
