# clm-pil-hil-replay-analyzer 输出模板

## 使用说明

- 目标:输出 PIL/HIL 数据的对齐结果、通过判据评估、退化信号清单与跨库交接段
- 主交付工件(Primary Artifact):`pil_hil_replay_findings`
- 默认中文输出;专业术语首次出现附英文注释
- 本 skill 不采数 / 不设计用例 / 不给调参建议

## 基本信息(Basic Context)

- `task_id`:
- `skill_name`:`clm-pil-hil-replay-analyzer`
- `artifact_name`:`pil_hil_replay_findings`
- `tool_context`:
  - PIL/HIL 平台与版本:
  - 目标硬件 + 时钟源:
  - 数据形态:
  - 采样率(Hz)+ 时间戳精度:
  - 是否启用 Code-in-the-Loop 一致性:
  - 许可证可用性:
- `scope`(被测对象 + PIL/HIL 数据 + 基线):
- `version_or_branch`:
- `replay_baseline`:
  - 类型(模型仿真 / 上一版本 PIL/HIL / 已批准基线):
  - 来源(文件 / 版本号):
  - 通过判据来源(`test_harness_plan` 或自定义):

## 范围与假设(Scope & Assumptions)

- [ ] 是否提供 `test_harness_plan` / `codegen_output_map` / `coverage_gap_report` / FMT `control_performance_findings`
- 事实(Fact)与推断(Inference)边界说明:

## 输入摘要(Input Summary)

- [ ] PIL/HIL 数据路径
- [ ] 基线数据路径
- [ ] 上游工件清单
- 输入缺口(Gaps):

## 工件正文(Artifact Body)

### 1. 时间对齐(Time Alignment)

- 对齐方法:`交叉相关` / `触发事件` / `共同时基` / 其他
- 对齐残差:`<= X ms` / `<= N samples`
- 残差是否超阈值:`否(继续精确对比)` / `是(所有偏差结论降级为粗对比)`
- 触发事件位置(若使用):

### 2. 采样率核对(Sampling Rate)

| 数据流 | 采样率(Hz) | 重采样方法(若必要) | 混叠风险 |
| --- | --- | --- | --- |
| PIL/HIL |  |  |  |
| 基线 |  |  |  |

### 3. 通过判据评估(Pass Criterion Evaluation)

> 仅在提供 `test_harness_plan` 时填写。

| 用例 ID | 通过判据 | 评估结果(PASS/FAIL/NA) | 偏差量化 / NA 原因 | 责任窗(t_start, t_end) | 证据 |
| --- | --- | --- | --- | --- | --- |
| TC-EQ-01 |  |  |  |  |  |
| TC-BD-01 |  |  |  |  |  |
| TC-SF-01 |  |  |  |  |  |

### 4. 退化信号清单(`regression_signals`)

| 信号名 | 单位 | 偏差指标 | 偏差值 | 基线容差 | 责任窗 | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
|  | rad |  峰值 |  |  |  |  |
|  | rad |  RMS  |  |  |  |  |
|  | — | 相位差 |  |  |  |  |

### 5. SIL→PIL 一致性(若涉及)

| 信号 / 全局变量 | 模型路径 | 生成代码变量名 | SIL 数据 | PIL 数据 | 一致性结论 |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

依据:`codegen_output_map` 中的 model_to_code_map

### 6. 跨库交接段(Cross-Library Findings,对接 FMT)

> 仅在用户任务涉及 FMT 时填写。

- 信号名映射(本库 ↔ FMT 端):
- 变体(`vtol` / `mc` / `fw` / `unknown`):
- 单位一致性:
- 仿真侧偏差 vs 实飞侧偏差对照:

| 现象 | 本库证据(PIL/HIL) | FMT 端证据(实飞) | 互相印证 / 矛盾 / 无对照 |
| --- | --- | --- | --- |
|  |  |  |  |

跨库 `tool_context` / `firmware_context` 双侧保留:

- 本库 `tool_context`:
- FMT 端 `firmware_context`:

## 关键事实(Facts)

- Fact-1:
- Fact-2:

## 关键推断(Inferences)

- Inference-1(置信度:高/中/低):
- Inference-2(置信度:高/中/低):

## 证据索引(Evidence Index)

- 数据证据:`pil_run_001.mat[t=2.0s..3.5s]` → `attitude_err` 峰值 = 1.2 deg
- 基线证据:`baseline_v3.mat[t=2.0s..3.5s]` → `attitude_err` 峰值 = 0.4 deg
- 偏差结论:Δ = 0.8 deg,基线容差 0.5 deg,列入 `regression_signals`

## 缺口与风险(Gaps & Risks)

- 缺口(例:基线缺失 / 采样率不一致且无法重采样 / 数据格式未识别):
- 风险:
- 降级策略:

## 下游输入建议(Next Skill Inputs)

- 推荐下游 skill:
  - `clm-control-law-mbd-pipeline`(汇总到 `pipeline_status`)
  - `fmt-control-performance-analyzer`(跨库:仿真侧偏差对照实飞侧)
  - `fmt-tuning-report-writer`(跨库:作为调参证据,本 skill 不下调参建议)
- 建议关注的信号 / 用例 ID / 时间窗:
- 需要补充的输入或确认项:

## 质量门禁自检(简表)

- [ ] 边界纯度:未采数 / 未设计用例 / 未给调参建议 / 未修改模型或代码
- [ ] 证据可追溯:每条偏差给出数据文件 + 时间窗 + 信号名 + 量化指标
- [ ] 工具上下文显式:平台/版本/采样率/对齐残差已记录
- [ ] 时间对齐纪律:对齐方法 + 残差声明
- [ ] 通过判据纪律:逐条 PASS/FAIL/NA + 证据
- [ ] 跨库纪律:信号名/变体/单位一致性显式
- [ ] 交接可用性:下游与跨库 skill 可直接使用
- [ ] 失败/降级说明完整

## 共享规范引用

- `../../_meta/first-principles-skill-contract.md`
- `../../_meta/artifact-handoff-contract.md`
- `../../_meta/quality-scorecard.md`
