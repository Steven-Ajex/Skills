# clm-model-to-deploy-handoff 输出模板

## 使用说明

- 目标:聚合 Stage 1-4 工件 + `pipeline_status` 为可审计的"模型 → 部署"交接包
- 主交付工件(Primary Artifact):`deploy_handoff_package`
- 默认中文输出;专业术语首次出现附英文注释
- 本 skill 不重做专业判断 / 不下"已可投产"结论

## 基本信息(Basic Context)

- `task_id`:
- `skill_name`:`clm-model-to-deploy-handoff`
- `artifact_name`:`deploy_handoff_package`
- 任务里程碑(release ID / integration milestone):
- `pipeline_status` 引用:

## 工具矩阵一致性结论

| 维度 | 来源工件 | 值 | 一致? |
| --- | --- | --- | --- |
| Simulink 版本 |  |  |  |
| Embedded Coder 版本 |  |  |  |
| Simulink Test 版本 |  |  |  |
| 覆盖率工具 |  |  |  |
| 数值形态 |  |  |  |
| 目标硬件 |  |  |  |

总结:`一致(继续生成交接包)` / `冲突(阻断)`

## 工件正文(Artifact Body)

### 1. 版本与配置声明(Version Pin)

| 资产 | 版本/时间戳 | Checksum / Commit | 说明 |
| --- | --- | --- | --- |
| 模型 (`model.slx`) |  |  |  |
| 数据字典 (`design.sldd`) |  |  |  |
| 生成代码 (`./generated/`) |  |  | 时间戳 + 文件清单 |
| Simulink |  | — |  |
| Embedded Coder |  | — |  |
| Simulink Test |  | — |  |
| 覆盖率工具 |  | — |  |
| Fixed-Point Designer(若涉及) |  | — |  |

### 2. 合规摘要(Compliance Summary)

来源:Stage 3 三 skill 工件

#### 2.1 配置审查(`coder_config_review`)

| 类别 | 风险等级最高项 | 数量(高/中/低) | 备注 |
| --- | --- | --- | --- |
| Code Interface |  |  |  |
| Storage Class |  |  |  |
| Hardware Implementation |  |  |  |
| Solver |  |  |  |
| Optimization |  |  |  |
| Report & Diagnostics |  |  |  |

#### 2.2 代码生成形态(`codegen_output_map`)

- Step Function 入口签名:
- 文件打包形态(单文件 / 模块化 / Reusable):
- 桥接层契合(`bridge_layer_contract` 摘要):

#### 2.3 存储类治理结果(`storage_class_governance`)

| 决策类型 | 数量 | 备注 |
| --- | --- | --- |
| keep |  |  |
| adjust |  |  |
| rename |  |  |
| migrate |  |  |

命名一致性:`通过` / `存在违例(详见原工件)`

### 3. 验证摘要(Verification Summary)

来源:Stage 4 工件

#### 3.1 用例集合(`test_harness_plan`)

- 用例总数:
- 按分组分布:`等价类=N` / `边界=N` / `状态切换=N` / `故障注入=N` / `性能基线=N`
- 需求覆盖率(若有 `requirement_trace_map`):

#### 3.2 覆盖率(`coverage_gap_report`)

| 维度 | 覆盖率 % | 缺口分类汇总 |
| --- | --- | --- |
| Decision |  | unreachable=N / unexercised=N / unstable=N / needs-refactor=N |
| Condition |  |  |
| MCDC |  |  |
| Stateflow State |  |  |
| Stateflow Transition |  |  |

`accept-residual` 缺口数量 + 文档化引用:

#### 3.3 PIL/HIL 回放(`pil_hil_replay_findings`)

| 用例 ID | 评估 | 偏差量化 / NA 原因 |
| --- | --- | --- |
|  | PASS / FAIL / NA |  |

退化信号数量 + 关键退化信号清单:

#### 3.4 实飞对照(若有 `flight_log_replay_dataset`)

- 飞行段使用情况:
- 跨库 `firmware_context` 摘要:
- 单位一致性 / 变体一致性结论:

### 4. 跨库接口契约段(Bridge Layer Status)

#### 4.1 模型 → FMT 方向

| 接口期望项 | 本库值(`bridge_layer_contract`) | FMT 端期望 | 核对状态 | 处置 |
| --- | --- | --- | --- | --- |
| Step 入口签名 |  |  | 一致 / 差异 / 未核对 |  |
| 命名前缀 |  |  |  |  |
| extern / volatile |  |  |  |  |
| 类型定义文件 |  |  |  |  |

#### 4.2 FMT → 模型 方向(若涉及)

- `flight_log_replay_dataset` 状态:`已生成 / N/A`
- 跨库 `firmware_context` 与 `tool_context` 双侧保留:`是 / 否`
- 反向 handoff 状态:`已就绪 / 待补 / N/A`

### 5. 残留风险登记(Risk Register)

| 风险 ID | 来源工件 | 等级 | 影响 | 类型(refactor / accept-residual / defer) | 文档化位置 | 评审签字环节 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  | 高 |  |  |  |  | 高风险标记 |
|  |  | 中 |  |  |  |  |  |

风险等级分布:

| 等级 | 数量 | 关键条目 ID |
| --- | --- | --- |
| 高 |  |  |
| 中 |  |  |
| 低 |  |  |

`accept-residual` 独立清单:

| 风险 ID | 文档位置 | 评审签字环节 | 复核条件 |
| --- | --- | --- | --- |
|  |  |  |  |

### 6. 回归点清单(Regression Points)

下次改动时需要重跑的 skill / 测试:

| 触发条件 | 需重跑 skill | 需重跑测试 / 验证 | 备注 |
| --- | --- | --- | --- |
| 模型改动 |  |  |  |
| 字典改动 |  |  |  |
| 配置改动 |  |  |  |
| 代码生成重做 |  |  |  |
| 工具版本升级 |  |  | 高敏感:Embedded Coder / Fixed-Point Designer |
| 目标硬件变更 |  |  |  |
| FMT 接口契约变更 |  |  | 跨库回归 |

### 7. 工件索引表(Artifact Index)

| 工件名 | 产出 skill | `pipeline_status` 索引 | 路径(若可访问) | 备注 |
| --- | --- | --- | --- | --- |
| `simulink_model_map` | clm-simulink-model-reader | stages.Stage1.artifacts |  |  |
| `data_dictionary_map` | clm-data-dictionary-reader | stages.Stage1.artifacts |  |  |
| `coder_config_review` | clm-embedded-coder-config-reviewer | stages.Stage3.artifacts |  |  |
| `codegen_output_map` | clm-codegen-output-mapper | stages.Stage3.artifacts |  |  |
| `storage_class_governance` | clm-storage-class-governor | stages.Stage3.artifacts |  |  |
| `test_harness_plan` | clm-test-harness-builder | stages.Stage4.artifacts |  |  |
| `coverage_gap_report` | clm-coverage-gap-analyzer | stages.Stage4.artifacts |  |  |
| `pil_hil_replay_findings` | clm-pil-hil-replay-analyzer | stages.Stage4.artifacts |  |  |
|  |  |  |  |  |

### 8. 下一步动作(Next Actions,分角色)

#### Release Manager

- [ ] 决策:基于本交接包是否签发本里程碑(决策点参考"残留风险" + "覆盖率" + "PIL/HIL 通过率")
- [ ] 决策:`accept-residual` 高/中等级条目是否进入 release notes
- [ ] 截止条件:

#### 集成工程师 / 嵌入式侧

- [ ] 接收 `codegen_output_map.bridge_layer_contract` + 命名/前缀差异条目
- [ ] 评估嵌入式 wrapper 适配工作量
- [ ] 与 FMT 维护方对齐 wrapper 边界
- [ ] 截止条件:

#### FMT 维护方

- [ ] 核对 `bridge_layer_contract` 与 `mbd-interface-reader` 期望
- [ ] 接收 `pil_hil_replay_findings` 与 `flight_log_replay_dataset` 用作下一轮 `control-performance-analyzer` 输入
- [ ] 截止条件:

#### 项目评审 / 审计

- [ ] 复核 `accept-residual` 文档化清单
- [ ] 复核工具版本对 release 决策的影响
- [ ] 截止条件:

## 关键事实(Facts)

- Fact-1:
- Fact-2:

## 关键推断(Inferences)

- Inference-1(置信度:高/中/低):
- Inference-2(置信度:高/中/低):

## 缺口与风险(Gaps & Risks)

- 缺口(例:某 Stage = blocked / 工具矩阵冲突 / 跨库未核对):
- 风险:
- 降级策略:

## 质量门禁自检(简表)

- [ ] 边界纯度:未重做专业判断 / 未修改文件 / 未替代 release / 未下"已可投产"结论
- [ ] 工具矩阵一致性
- [ ] 完整性:七项齐全
- [ ] 风险纪律:`accept-residual` 含理由 + 文档 + 签字
- [ ] 跨库纪律:接口契约状态显式
- [ ] 工件索引纪律:可回链 `pipeline_status`
- [ ] 下一步动作:角色 + 截止条件齐全
- [ ] 失败/降级说明完整

## 共享规范引用

- `../../_meta/first-principles-skill-contract.md`(第 4 节"编排技能边界规则")
- `../../_meta/artifact-handoff-contract.md`
- `../../_meta/quality-scorecard.md`
