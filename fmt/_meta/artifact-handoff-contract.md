# FMT Skills 工件交接契约（Artifact Handoff Contract）

用于统一 FMT 原子技能之间、以及原子技能到编排技能之间的交接格式，降低技能组合时的歧义和信息丢失。

## 1. 交接目标

1. 让上游输出能被下游直接消费（而不是重新解释）
2. 让“证据、范围、置信度、缺口”随工件一起传递
3. 让工作流技能能做门禁检查（Gate Check）

## 2. 工件最低字段（所有技能通用）

每个交接工件至少包含以下字段（可用表格或分节表达）：

1. `artifact_name`：工件名称（例如 `control_loop_map`）
2. `skill_name`：产出该工件的 skill 名称
3. `variant`：`vtol` / `mc` / `fw` / `unknown`
4. `scope`：分析范围（代码路径 / 日志文件 / 时间段）
5. `facts`：关键事实结论（带证据）
6. `inferences`：关键推断结论（带置信度）
7. `evidence_index`：证据索引（代码路径行号或日志时间段）
8. `gaps`：缺口与不确定项（输入缺失、版本不匹配、日志损坏等）
9. `next_skill_inputs`：下游技能建议使用的输入字段或观察点

## 3. 代码阅读类工件（Code Reading Artifacts）

典型工件：

1. `control_loop_map`
2. `mbd_boundary_map`
3. `fms_state_semantics`
4. `logging_pipeline_map`

额外建议字段：

1. `module_boundary_table`：模块职责和边界
2. `call_chain`：关键调用链（入口 -> 关键函数）
3. `topic_or_bus_map`：MCN/topic/bus 映射
4. `variant_assumptions`：变体假设与宏开关假设

## 4. 日志分析类工件（Log Analysis Artifacts）

典型工件：

1. `mlog_decode_summary`
2. `flight_phase_segments`
3. `control_performance_findings`
4. `tuning_recommendation_report`

额外建议字段：

1. `timebase`：时间基准与对齐说明
2. `signal_catalog`：关键信号清单（字段名、单位、频率）
3. `phase_index`：分段结果与关键事件索引
4. `confidence`：整体置信度（高/中/低）

## 5. 编排技能门禁检查（Workflow Gate Checks）

工作流技能在进入下一阶段前，至少检查：

1. 工件存在（Artifact Exists）
2. 范围匹配（Variant / 文件 / 时间段一致）
3. 关键字段齐全（Facts / Evidence / Gaps）
4. 缺口是否阻断（Blocking Gap vs Non-Blocking Gap）

## 6. 常见失败模式（Common Failure Modes）

1. 只给结论，不给证据索引
2. 变体未确认却混用 `vtol/mc/fw` 规则
3. 分段工件未说明分段依据，导致性能分析误判
4. 报告工件没有回链到现象与证据，导致建议不可验证
