# 检查清单(Checklist)

用于在交付 `clm-control-law-mbd-pipeline` 输出前做快速复核。建议按顺序勾选;如未满足项导致结论降级,需在输出中显式写明。

## 边界与编排纪律

- [ ] 没有重写任何原子 skill 的专业结论(只引用工件)
- [ ] 没有擅自合并阶段或跳过阶段(裁剪阶段必有显式原因)
- [ ] 没有假装阶段已通过(Blocking Gap 阻断已传递到 `pipeline_status`)
- [ ] 没有替代用户的设计决策(只汇总并提示)

## 阶段门禁(Stage Gates)

- [ ] 每阶段入口门禁已检查(上游工件存在 / `tool_context` 齐全 / 范围一致)
- [ ] 每阶段退出门禁已检查并记录通过 / 阻断 / 警告
- [ ] 阶段间工具上下文冲突时已阻断后续阶段
- [ ] Blocking Gap 与 Non-Blocking Gap 已显式分类
- [ ] 第二批未落地原子 skill 对应阶段已标记 `blocked` 或 `skipped` 并写明原因

## 工具上下文一致性

- [ ] 各阶段 `tool_context` 已汇总成"任务级工具矩阵"
- [ ] 矩阵内无冲突;若有冲突已阻断
- [ ] Embedded Coder / Simulink / Stateflow 版本一致性已声明
- [ ] 模型与代码时间戳一致性结论(若涉及 Stage 3)已传递

## 跨库交接(Cross-Library Handoff)

- [ ] 若涉及 FMT,`cross_library_handoff` 段已生成
- [ ] 工件映射(本库 → FMT、FMT → 本库)已列出
- [ ] 命名一致性(状态名/信号名/变体)已显式声明
- [ ] 两侧 `tool_context` / `firmware_context` 各自保留,未互相覆盖

## 用户目标可追溯

- [ ] 用户每个目标都映射到具体阶段工件
- [ ] 未达成的目标已列入 `next_actions` 与解锁动作

## 输入与范围

- [ ] 任务描述、目标、范围已记录
- [ ] 可用资产清单(模型/字典/生成代码/验证数据/上游 FMT 工件)已记录
- [ ] 缺失资产已在 `gaps` 中登记

## 交接可用性(Artifact Handoff)

- [ ] 主交付工件名为 `pipeline_status`
- [ ] 工件包含 `tool_matrix` / `stages` / `gate_log` / `unmet_gates` / `cross_library_handoff` / `risk_register` / `next_actions`
- [ ] 各阶段原子工件已附带或清晰索引
- [ ] 下游(工程师 / 评审 / FMT 工作流)可直接消费

## 失败与降级

- [ ] 输入不足时已请求用户澄清,而不是擅自裁剪
- [ ] 已显式列出未完成阶段及解锁动作
- [ ] 没有给出"端到端通过"的结论(若有 Blocking)

## 交付前确认

- [ ] 输出语言为中文,专业术语首次出现附英文注释
- [ ] 子工件字段保留原文,未重新解释
- [ ] 结论不超出本编排技能职责边界
- [ ] 自评分(参考 `../../_meta/quality-scorecard.md`)≥10/12
