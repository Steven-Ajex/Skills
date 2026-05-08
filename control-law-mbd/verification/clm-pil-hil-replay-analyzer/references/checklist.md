# 检查清单(Checklist)

用于在交付 `clm-pil-hil-replay-analyzer` 输出前做快速复核。建议按顺序勾选;如未满足项导致结论降级,需在输出中显式写明。

## clm-pil-hil-replay-analyzer 专项检查

- [ ] 时间对齐方法(交叉相关 / 触发事件 / 共同时基)已声明
- [ ] 时间对齐残差(单位:s 或 sample)已量化;残差超阈值时所有偏差结论降级
- [ ] 采样率核对完成;不一致时重采样方法已声明,混叠风险已评估
- [ ] 至少一条信号给出"PIL/HIL 时间窗 + 基线时间窗 + 量化偏差(峰值/RMS/相位)"
- [ ] 通过判据(若有 `test_harness_plan`)逐条评估为 PASS / FAIL / NA;NA 必须有原因
- [ ] 退化信号清单(`regression_signals`)含偏差指标与超限阈值
- [ ] SIL→PIL 一致性(若涉及)对照 `codegen_output_map` 全局变量名

## 工具上下文(Tool Context)

- [ ] PIL/HIL 平台与版本已确认或标注 `unknown`
- [ ] 目标硬件与时钟源已记录
- [ ] 数据形态(`.mat` / `.mdf` / `.csv` / 自定义)已记录
- [ ] 采样率与时间戳精度已记录
- [ ] 是否启用 Code-in-the-Loop 一致性验证已声明
- [ ] 许可证可用性已记录

## 输入与范围

- [ ] PIL/HIL 数据路径已记录
- [ ] 基线类型(模型仿真 / 上一版本 PIL/HIL / 已批准基线)已声明
- [ ] (可选)`test_harness_plan` / `codegen_output_map` / `coverage_gap_report` / FMT `control_performance_findings` 是否提供
- [ ] 输入缺口(Gaps)及其影响已列出

## 时间对齐纪律(Time Alignment Discipline)

- [ ] 对齐方法显式声明
- [ ] 对齐残差量化
- [ ] 残差超阈值时降级标签随结论传递
- [ ] 没有用"看上去对齐了"的描述代替量化残差

## 通过判据纪律(Pass Criterion Discipline)

- [ ] 每条用例/判据有 PASS / FAIL / NA 标签
- [ ] 每条 FAIL 给出偏差量化与责任窗
- [ ] 每条 NA 有原因(数据未覆盖 / 信号缺失 / 配置不匹配)
- [ ] 没有"看上去通过了"的描述代替证据

## 退化信号识别

- [ ] 全信号扫描已完成
- [ ] 偏差超基线容差的信号列入 `regression_signals`
- [ ] 每条退化信号给出偏差指标(峰值 / RMS / 相位)
- [ ] 已显式接受的残留(参考 `coverage_gap_report`)未在本 skill 内新增规约

## 跨库纪律(Cross-Library Discipline)

- [ ] (若涉及 FMT)信号名映射已声明(经 `codegen_output_map` 中转)
- [ ] 变体(vtol / mc / fw)信息保留
- [ ] 单位一致性显式声明
- [ ] 两侧 `tool_context` / `firmware_context` 各自保留,未互相覆盖

## 边界与纪律

- [ ] 没有采集数据 / 没有设计用例 / 没有给调参建议 / 没有修改模型或代码
- [ ] 没有给"PIL/HIL 通过/不通过"的最终结论(由编排技能或工程师聚合)
- [ ] 没有用经验代替证据

## 交接可用性(Artifact Handoff)

- [ ] 主交付工件名为 `pil_hil_replay_findings`
- [ ] 工件包含 `tool_context` / `scope` / `facts` / `inferences` / `evidence_index` / `gaps` / `next_skill_inputs` / `replay_baseline` / `regression_signals` / `cross_library_findings`
- [ ] 下游 skill (`fmt-control-performance-analyzer` / `fmt-tuning-report-writer` / `clm-control-law-mbd-pipeline`) 可直接消费

## 失败与降级

- [ ] 输入不足时已采用降级输出
- [ ] 已标注受影响结论与置信度变化
- [ ] 已给出下一步最小补充动作

## 交付前确认

- [ ] 输出语言为中文,专业术语首次出现附英文注释
- [ ] 信号名 / 模式名 / 用例 ID 保持原文
- [ ] 结论不超出本技能职责边界
- [ ] 自评分(参考 `../../_meta/quality-scorecard.md`)≥10/12
