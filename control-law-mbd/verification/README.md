# Verification（MIL / SIL / PIL / HIL 验证）

控制律 MBD **在环验证类**原子技能（atomic skill）的容器目录。

## 1. 职责（What）

负责把控制律从"建模/代码生成完成"推进到"经过验证可交付"的所有专业判断:

- MIL / SIL / PIL / HIL 测试用例与 harness 落地
- Decision / Condition / MCDC 覆盖率评估与缺口补齐
- PIL / HIL 数据回放与控制律性能基线对比

## 2. 规划 skill 列表

| Skill 名 | 最小任务单元 | 主要工件 | 状态 |
| --- | --- | --- | --- |
| `clm-test-harness-builder` | 从需求到 MIL/SIL 测试 harness 的落地方案 | `test_harness_plan` | 已落地 |
| `clm-coverage-gap-analyzer` | Decision / Condition / MCDC 覆盖率缺口分析与补齐建议 | `coverage_gap_report` | 已落地 |
| `clm-pil-hil-replay-analyzer` | PIL / HIL 回放数据对比与基线偏差识别 | `pil_hil_replay_findings` | 已落地 |

| `clm-flight-log-replay-bridge` | 反向跨库桥:FMT 飞行日志 → MIL/SIL/PIL/HIL 回放激励数据集 | `flight_log_replay_dataset` | 已落地 |

后续候选(Backlog):

- `clm-sldv-property-author`
- `clm-polyspace-runtime-error-analyzer`
- `clm-fault-injection-test-author`

## 3. 不负责（Out of Scope）

- 模型解读 → 走 `../model-reading/`
- 模型重构与控制律建模 → 走 `../model-authoring/`
- Embedded Coder 配置与生成代码诊断 → 走 `../codegen-bridge/`
- 实飞日志解码与飞行段控制性能分析 → 走 `fmt/log-analysis/*`
- 跨阶段端到端编排 → 走 `../workflows/`

## 4. 触发边界（When NOT to use）

- 没有可用的需求/用例/基线数据(应先在工件 `gaps` 中登记)
- 验证工具（SLDV / Polyspace / 第三方 HIL 平台）不可用且无降级路径
- 仅有飞行日志而无台架/PIL/HIL 数据(应交回 `fmt/log-analysis/*`)

## 5. 与 `fmt/` 库的衔接

- `pil_hil_replay_findings`（本目录）↔ `control_performance_findings`（`fmt-control-performance-analyzer`）
  描述同一性能问题在仿真侧 vs 实飞侧的证据,`regression_signals` 信号名应保持一致
- 跨库交接时保留各自 `tool_context` / `firmware_context`,不互相覆盖

## 6. 共同输出契约

工件必须满足 `../_meta/artifact-handoff-contract.md`,并额外包含：

- `requirement_to_test_matrix`：需求 ↔ 用例覆盖矩阵
- `coverage_breakdown`：Decision / Condition / MCDC 各维度覆盖率
- `replay_baseline`：基线模型/版本 + 比较指标 + 通过判据
- `regression_signals`：与基线相比出现退化的信号清单
