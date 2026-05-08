# Control Law MBD Skills 工件交接契约（Artifact Handoff Contract）

用于统一 `control-law-mbd/` 原子技能之间、原子技能到编排技能之间,以及与 `fmt/` 库之间的交接格式,降低技能组合时的歧义和信息丢失。

## 1. 交接目标

1. 让上游输出能被下游直接消费（而不是重新解释）
2. 让“证据、范围、置信度、缺口、工具上下文”随工件一起传递
3. 让工作流技能能做门禁检查（Gate Check）
4. 让本库与 `fmt/` 库的工件能够互相引用（模型层 ↔ 嵌入式层）

## 2. 工件最低字段（所有技能通用）

每个交接工件至少包含以下字段（可用表格或分节表达）：

1. `artifact_name`：工件名称（例如 `simulink_model_map`、`coder_config_review`）
2. `skill_name`：产出该工件的 skill 名称
3. `tool_context`：工具上下文（Simulink/Stateflow/Embedded Coder 版本、模型形态、操作系统、许可证可用性）
4. `scope`：分析范围（模型路径 / `.sldd` 路径 / 生成代码目录 / 测试 harness / 时间段）
5. `facts`：关键事实结论（带证据）
6. `inferences`：关键推断结论（带置信度）
7. `evidence_index`：证据索引（模型路径 + 子系统路径 / 字典对象名 / 代码路径行号 / 用例 ID）
8. `gaps`：缺口与不确定项（许可证缺失、模型版本不匹配、覆盖率报告缺失等）
9. `next_skill_inputs`：下游技能建议使用的输入字段或观察点

> `tool_context` 是相对 `fmt/` 工件契约的额外字段,因为 MBD 跨工具/跨版本风险显著高于嵌入式纯代码侧。

## 3. 模型理解类工件（Model Reading Artifacts）

典型工件：

1. `simulink_model_map`
2. `stateflow_semantics`
3. `data_dictionary_map`
4. `requirement_trace_map`

额外建议字段：

1. `subsystem_tree`：子系统层级与原子单元（Atomic Subsystem）标记
2. `sample_time_table`：采样时间一致性检查
3. `bus_object_table`：Bus / Bus Object 与字段
4. `parameter_object_table`：`Simulink.Parameter` / `Simulink.Signal` 与作用域
5. `traceability_index`：需求 ↔ 子系统 ↔ 用例 三向追溯索引

## 4. 建模与重构类工件（Model Authoring Artifacts）

典型工件：

1. `control_law_pattern_skeleton`
2. `compliance_refactor_diff`

额外建议字段：

1. `pattern_choice`：所选控制律结构（PID / LQR / 增益调度 / Anti-Windup 等）
2. `structural_constraints`：原子化、采样时间、内联条件等约束清单
3. `refactor_steps`：从原模型到合规模型的步骤说明
4. `risk_register`：重构对功能/性能可能造成的影响

## 5. 代码生成与桥接类工件（Codegen Bridge Artifacts）

典型工件：

1. `coder_config_review`
2. `codegen_output_map`
3. `storage_class_governance`

额外建议字段：

1. `config_findings`：Embedded Coder 配置项 + 当前值 + 期望值 + 风险
2. `model_to_code_map`：模型对象 ↔ 生成代码（文件 + 函数 + 全局变量）映射
3. `bridge_layer_contract`：与手写桥接层的对接点（例如 FMT 接口层）
4. `naming_and_storage_class_table`：命名约定与存储类一致性

## 6. 验证类工件（Verification Artifacts）

典型工件：

1. `test_harness_plan`
2. `coverage_gap_report`
3. `pil_hil_replay_findings`

额外建议字段：

1. `requirement_to_test_matrix`：需求 ↔ 用例覆盖矩阵
2. `coverage_breakdown`：Decision / Condition / MCDC 各维度覆盖率
3. `replay_baseline`：基线模型/版本 + 比较指标 + 通过判据
4. `regression_signals`：与基线相比出现退化的信号清单

## 7. 编排技能门禁检查（Workflow Gate Checks）

工作流技能在进入下一阶段前,至少检查：

1. 工件存在（Artifact Exists）
2. 工具上下文匹配（版本 / 形态 / 许可证一致）
3. 范围匹配（模型路径 / `.sldd` / 生成代码 / 用例集合一致）
4. 关键字段齐全（Facts / Evidence / Gaps）
5. 缺口是否阻断（Blocking Gap vs Non-Blocking Gap）

## 8. 与 `fmt/` 库的跨库工件衔接

为了让“模型侧 → 嵌入式 → 飞行验证”形成闭环,建议遵循以下衔接：

1. `codegen_output_map`（本库）↔ `mbd_boundary_map`（`fmt-mbd-interface-reader`）
   两者描述同一接口的两侧；建议在 `evidence_index` 中互相引用
2. `pil_hil_replay_findings`（本库）↔ `control_performance_findings`（`fmt-control-performance-analyzer`）
   同一性能问题在仿真侧 vs 实飞侧的证据,建议在 `regression_signals` 中保持信号名一致
3. 跨库工件交接时,必须各自保留 `tool_context` 与 `firmware_context`,避免相互污染

## 9. 常见失败模式（Common Failure Modes）

1. 只给结论,不给证据索引（特别是模型路径/子系统路径缺失）
2. 工具上下文未确认却混用不同 Simulink 版本规则
3. 生成代码工件没有回链到模型对象,导致改动来源不明
4. 覆盖率报告未说明工具与配置（SLDV / Polyspace / 第三方）
5. 跨库交接时丢失变体（vtol / mc / fw）信息,导致飞行侧验证错位
