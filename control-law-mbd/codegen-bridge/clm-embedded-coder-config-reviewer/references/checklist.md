# 检查清单(Checklist)

用于在交付 `clm-embedded-coder-config-reviewer` 输出前做快速复核。建议按顺序勾选;如未满足项导致结论降级,需在输出中显式写明。

## clm-embedded-coder-config-reviewer 专项检查

- [ ] 已审查六大类别:Code Interface / Storage Class / Hardware Implementation / Solver / Optimization / Report & Diagnostics
- [ ] 每条偏差有"期望值 + 风险等级 + 影响维度 + 修复路径"
- [ ] 关键标记小结(Step Function 形态、Reentrant、文件打包形态)已给出
- [ ] 没有越权下"生成代码不合规"的结论(此类结论需引用 `codegen_output_map`)
- [ ] 没有替代 `clm-storage-class-governor` 做全局治理决策

## 工具上下文(Tool Context)

- [ ] Embedded Coder / Simulink Coder 版本已确认或标注 `unknown`
- [ ] 目标硬件(Word Length、Endianness)已记录或标注"待确认"
- [ ] 求解器(Type、Step Size、Tasking Mode)已记录
- [ ] 许可证可用性已记录;无许可证时降级到 `configSet` XML 解析的路径已声明
- [ ] 多 ConfigSet 时已指定审查目标(或请求用户指定)

## 输入与范围

- [ ] 模型路径与 ConfigSet 名称已记录
- [ ] 期望基线(公司规范 / 高完整性建议 / 自定义)已声明
- [ ] (可选)生成代码目录是否参与交叉验证已说明
- [ ] 输入缺口(Gaps)及其影响已列出

## 证据与结论

- [ ] 关键结论给出配置项原名(如 `RTWGenerateMakefile`、`DefaultParameterBehavior`)
- [ ] 证据来源(`get_param` 调用 / `configSet` XML 路径)已记录
- [ ] 已区分事实(Fact)与推断(Inference)
- [ ] 模型层问题(如未原子化的子系统)已转交 `clm-codegen-compliance-refactor`,未混入配置审查结论
- [ ] 没有把"当前值 ≠ 默认值"等同为"有问题"

## 风险与影响

- [ ] 每条偏差有风险等级(高 / 中 / 低)
- [ ] 影响维度(代码体积 / 标定能力 / 性能 / 合规 / 可维护)已标注
- [ ] 修复路径(配置层 / 模型层 / 需求层)清晰

## 交接可用性(Artifact Handoff)

- [ ] 主交付工件名为 `coder_config_review`
- [ ] 工件包含 `tool_context` / `scope` / `facts` / `inferences` / `evidence_index` / `gaps` / `next_skill_inputs`
- [ ] 下游 skill (`clm-codegen-output-mapper` / `clm-storage-class-governor` / `clm-codegen-compliance-refactor`) 可直接消费
- [ ] 跨库衔接:与 `fmt-mbd-interface-reader` 的对接点(Step Function 形态 + 文件打包形态)字段齐全

## 失败与降级

- [ ] 输入不足时已采用降级输出,而不是跳步给终局结论
- [ ] 已标注受影响结论与置信度变化
- [ ] 已给出下一步最小补充动作(获取许可证 / 提供基线 / 确认目标硬件 / 指定 ConfigSet 等)

## 交付前确认

- [ ] 输出语言为中文,专业术语首次出现附英文注释
- [ ] 配置项原名(如 `RTWGenerateMakefile`)保持原文
- [ ] 结论不超出本技能职责边界
- [ ] 自评分(参考 `../../_meta/quality-scorecard.md`)≥10/12
