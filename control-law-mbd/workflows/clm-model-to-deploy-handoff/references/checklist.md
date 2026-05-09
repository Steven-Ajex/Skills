# 检查清单(Checklist)

用于在交付 `clm-model-to-deploy-handoff` 输出前做快速复核。

## clm-model-to-deploy-handoff 专项检查

- [ ] `pipeline_status` 已读取并解析
- [ ] 工具矩阵一致性结论已声明;不一致时已阻断
- [ ] 版本与配置声明完整(模型 + 字典 + 代码 + 至少 4 类工具版本)
- [ ] 合规摘要含 Stage 3 三 skill 关键结论
- [ ] 验证摘要含覆盖率三维度 + PIL/HIL 通过判据评估
- [ ] 跨库接口契约段含 `bridge_layer_contract` 与 FMT 端核对状态(`一致 / 差异 / 未核对`)
- [ ] 残留风险按等级排序
- [ ] `accept-residual` 条目独立列出,含理由 + 文档位置 + 评审签字环节
- [ ] 回归点清单(下次改动模型 / 配置 / 工具 各对应需重跑的 skill 与测试)
- [ ] 工件索引完整,每条可回链到 `pipeline_status`
- [ ] 下一步动作分角色(release / 集成 / FMT 维护方),含截止条件

## 边界与纪律

- [ ] 没有重做 Stage 1-4 的专业判断
- [ ] 没有修改任何模型 / 字典 / 代码 / 配置
- [ ] 没有替代 release 流程本身
- [ ] 没有给"已可投产 / 已可交付"的最终结论

## 工具上下文(Tool Context)

- [ ] Stage 1-4 工具上下文已汇总成"任务级工具矩阵"
- [ ] 矩阵内无冲突;若有冲突已阻断
- [ ] 工具版本作为 release 决策依据已显式列出

## Stage 状态处置

- [ ] `blocked` Stage 已显式标注 + 阻断原因 + 下一步动作
- [ ] `passed_with_warnings` Stage 的 warning 已聚合进残留风险
- [ ] `skipped` Stage 已声明跳过原因

## 跨库纪律(Cross-Library Discipline)

- [ ] `bridge_layer_contract` 与 FMT 端核对状态显式
- [ ] 差异条目转交建议明确(给谁 / 何时 / 决策点)
- [ ] `firmware_context` 与 `tool_context` 各自保留,未互相覆盖
- [ ] 反向跨库桥(`flight_log_replay_dataset`)状态(若涉及)已记录

## 风险登记纪律(Risk Register Discipline)

- [ ] 每条 `accept-residual` 含具名评审签字
- [ ] 高风险条目(高等级 + 影响面广)单独标记
- [ ] 不允许"软批准"的 `accept-residual`
- [ ] 风险等级分布(高/中/低 数量)已统计

## 工件索引纪律(Artifact Index Discipline)

- [ ] 每条索引可回链到 `pipeline_status`
- [ ] 没有"断链"(索引指向但 `pipeline_status` 无对应 artifact)
- [ ] 索引含工件 ID + 路径(若可访问)+ 产出 skill

## 下一步动作纪律(Next Actions Discipline)

- [ ] 每条动作有"接收角色"
- [ ] 每条动作有"截止条件 / 触发再评审条件"
- [ ] 没有"应该做 X"式的孤立动作

## 输入与范围

- [ ] `pipeline_status` 已提供(必需)
- [ ] Stage 1-4 主要工件已提供
- [ ] (可选)项目 release 模板 / 集成对接清单 是否提供
- [ ] 输入缺口(Gaps)已列出

## 失败与降级

- [ ] 输入不足时已采用降级输出
- [ ] 已标注哪些段落基于不完整输入与置信度变化
- [ ] 已给出下一步最小补充动作

## 交付前确认

- [ ] 输出语言为中文,专业术语首次出现附英文注释
- [ ] 模型路径 / 字典对象名 / 配置项 / 用例 ID / FMT 端字段名保持原文
- [ ] 结论不超出本技能职责边界
- [ ] 自评分(参考 `../../_meta/quality-scorecard.md`)≥10/12
