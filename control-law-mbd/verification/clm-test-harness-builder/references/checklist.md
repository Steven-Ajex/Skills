# 检查清单(Checklist)

用于在交付 `clm-test-harness-builder` 输出前做快速复核。建议按顺序勾选;如未满足项导致结论降级,需在输出中显式写明。

## clm-test-harness-builder 专项检查

- [ ] 至少一条用例满足"用例 ID + 目标 + 激励 + 期望 + 通过判据 + 覆盖维度"五项齐全
- [ ] 每条通过判据(Pass Criterion)可机器判定(数值容差 / 状态序列 / 时间窗),没有"行为合理"等模糊语
- [ ] 用例分组覆盖至少:等价类 / 边界 / 状态切换(若涉及 Stateflow)
- [ ] 状态切换用例覆盖至少一条非平凡转移
- [ ] 用例 ID 可追溯到"分组 + 需求 ID 或状态路径"
- [ ] SIL 模式下生成代码版本、目标硬件、接口对接三项已确认;缺一即降级到 MIL

## 工具上下文(Tool Context)

- [ ] Simulink Test 版本已确认或标注 `unknown`
- [ ] 求解器与采样时间(继承自被测模型)已记录
- [ ] 是否启用 SIL 已声明
- [ ] 激励/观察机制(Signal Builder / Test Sequence / MATLAB-based / From Workspace)已选型
- [ ] 许可证可用性已记录;无 Simulink Test 许可证时降级到"Subsystem 包装 + From Workspace"的最小方案已声明

## 输入与范围

- [ ] 被测对象路径已记录
- [ ] 测试目标已声明(需求 / 状态路径 / 性能基线 / 边界扫描)
- [ ] (可选)`simulink_model_map` / `stateflow_semantics` / `requirement_trace_map` / `codegen_output_map` 是否提供
- [ ] 输入缺口(Gaps)及其影响已列出

## 用例完整性

- [ ] 等价类用例已列出
- [ ] 边界用例已列出(参数边界 / 输入信号边界)
- [ ] 状态切换用例已列出(若适用)
- [ ] 异常 / 故障注入用例已列出(若需求层有要求)
- [ ] 性能基线用例已列出(若有飞行/PIL 数据)

## 需求 → 用例矩阵

- [ ] (若有需求工件)矩阵已构建
- [ ] 未覆盖的需求已列入 `gaps`
- [ ] 一条需求映射多条用例的关系已显式

## 边界与纪律

- [ ] 没有真实运行测试 / 没有配置覆盖率工具 / 没有修改模型
- [ ] 没有给"测试通过/不通过"结论(本 skill 只设计计划)
- [ ] 没有用经验代替通过判据

## 交接可用性(Artifact Handoff)

- [ ] 主交付工件名为 `test_harness_plan`
- [ ] 工件包含 `tool_context` / `scope` / `facts` / `inferences` / `evidence_index` / `gaps` / `next_skill_inputs` / `requirement_to_test_matrix`
- [ ] 下游 skill (`clm-coverage-gap-analyzer` / `clm-pil-hil-replay-analyzer`) 可直接消费

## 失败与降级

- [ ] 输入不足时已采用降级输出
- [ ] 已标注受影响用例与置信度变化
- [ ] 已给出下一步最小补充动作

## 交付前确认

- [ ] 输出语言为中文,专业术语首次出现附英文注释
- [ ] 信号名 / 子系统名 / 状态名保持原文
- [ ] 结论不超出本技能职责边界
- [ ] 自评分(参考 `../../_meta/quality-scorecard.md`)≥10/12
