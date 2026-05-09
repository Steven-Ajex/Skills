# 检查清单(Checklist)

用于在交付 `clm-fault-injection-test-author` 输出前做快速复核。

## clm-fault-injection-test-author 专项检查

- [ ] 至少覆盖故障清单中的高等级故障(ASIL/DAL 高等 100% 覆盖)
- [ ] 每条故障六字段齐全:注入点 + 注入方式 + 触发场景 + 期望降级 + 通过判据 + 复位策略
- [ ] 通过判据(Pass Criterion)可机器判定 — 数值容差 / 状态序列 / 时间窗 / 输出范围
- [ ] 复位策略含"故障清除条件 + 系统状态恢复路径"
- [ ] 注入方式与故障性质匹配(Stuck-At / Drift / Spike / Inversion / Signal Loss / Bit-Flip / 模式跳变)
- [ ] 触发场景显式声明(稳态 / 瞬态 / 模式切换 / 边界)

## 故障清单对齐(Fault List Alignment)

- [ ] 故障清单格式校验完成(故障 ID / 描述 / 影响 / 安全等级齐全)
- [ ] 缺字段的故障已标注降级,要求安全工程师补
- [ ] 安全等级与项目标准一致(ASIL A-D / DAL A-E / SIL 1-4 / 项目自定义)

## 工具上下文(Tool Context)

- [ ] Simulink Test 版本已确认或标注 `unknown`
- [ ] 故障注入框架(Simulink Test Sequence / Simulink Fault Analyzer / 自定义 / 代码补丁)已记录
- [ ] 是否启用代码侧故障注入已声明
- [ ] 安全等级标准已记录
- [ ] 许可证可用性已记录

## 输入与范围

- [ ] 故障模式清单已提供(必需);未提供时已阻断
- [ ] 被测对象路径已记录
- [ ] (可选)`simulink_model_map` / `stateflow_semantics` / `codegen_output_map` / `requirement_trace_map` / `test_harness_plan` 是否提供
- [ ] 输入缺口(Gaps)已列出

## 故障矩阵完整性(Fault Matrix Completeness)

- [ ] 每条故障六字段齐全
- [ ] 任一字段缺失列入 `gaps`
- [ ] 高等级故障(ASIL D / DAL A 等)单独标记

## 安全等级覆盖(Safety Coverage)

- [ ] 每个安全等级的故障覆盖比例已统计
- [ ] 高等级故障 100% 覆盖
- [ ] 中等级覆盖率符合项目要求

## 与 `test_harness_plan` 的边界

- [ ] 与常规用例边界显式声明
- [ ] 重复部分(若有)显式列出并说明
- [ ] 故障专项与常规用例不互相挤占

## 边界与纪律

- [ ] 没有替代 FMEA / HARA / FTA(本 skill 消费产物)
- [ ] 没有设计常规功能用例
- [ ] 没有修改模型 / 没有真实运行测试
- [ ] 没有做安全因果链推导
- [ ] 没有给"故障覆盖足够"的最终结论

## 交接可用性(Artifact Handoff)

- [ ] 主交付工件名为 `fault_injection_test_plan`
- [ ] 工件包含 `tool_context` / `scope` / `facts` / `inferences` / `evidence_index` / `gaps` / `next_skill_inputs` / `fault_matrix` / `requirement_to_fault_matrix` / `safety_level_coverage`
- [ ] 下游 skill (`clm-test-harness-builder` 合并 harness / `clm-coverage-gap-analyzer` 安全维度 / `clm-pil-hil-replay-analyzer` 故障判据)可直接消费

## 失败与降级

- [ ] 输入不足时已采用降级输出
- [ ] 已标注受影响段与置信度变化
- [ ] 已给出下一步最小补充动作

## 交付前确认

- [ ] 输出语言为中文,专业术语首次出现附英文注释
- [ ] 故障 ID / 信号名 / 模式名 / 用例 ID 保持原文
- [ ] 结论不超出本技能职责边界
- [ ] 自评分(参考 `../../_meta/quality-scorecard.md`)≥10/12
