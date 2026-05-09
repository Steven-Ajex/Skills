# 检查清单(Checklist)

用于在交付 `clm-polyspace-runtime-error-analyzer` 输出前做快速复核。

## clm-polyspace-runtime-error-analyzer 专项检查

- [ ] 至少覆盖报告中的 `Red`(已证有错)与 `Orange`(可能有错)级别条目
- [ ] 每条 finding 给出:错误类型 + 代码位置(文件:行号)+ 严重度 + 模型侧根因 + 闭环路由
- [ ] 模型侧根因经 `codegen_output_map` 中转,或显式标"无中转,根因为建议"
- [ ] 闭环路由四枚举:`refactor-model` / `adjust-config` / `accept-residual` / `out-of-mbd-scope`
- [ ] `out-of-mbd-scope` 路由含配置管理审批要求
- [ ] `accept-residual` 含具名评审签字
- [ ] 定点 Overflow 类 finding 关联 `fixed_point_refactor_plan`(若涉及)
- [ ] 存储类访问越界类 finding 关联 `storage_class_governance`(若涉及)
- [ ] 同关注点的 SLDV 属性对照(若有 `sldv_property_set`)

## 工具上下文(Tool Context)

- [ ] Polyspace 版本(Code Prover / Bug Finder / 联用)已确认或标注 `unknown`
- [ ] 报告形态(HTML / PSCV / API 导出 / 自定义)已记录
- [ ] 启用的规则集(Code Prover 抽象解释 / Bug Finder / MISRA C / CWE / CERT C)已记录
- [ ] 目标硬件(Word Length / Endianness)已记录;目标硬件未确认时 Overflow 类 finding 已标降级
- [ ] 是否启用并发分析已声明
- [ ] 许可证可用性已记录

## 输入与范围

- [ ] Polyspace 报告路径已记录;未提供时已阻断
- [ ] 生成代码目录已记录
- [ ] (强烈推荐)`codegen_output_map` 是否提供
- [ ] (推荐)`simulink_model_map` / `data_dictionary_map` / `fixed_point_refactor_plan` / `storage_class_governance` / `sldv_property_set` 是否提供
- [ ] 输入缺口(Gaps)已列出

## 严重度纪律(Severity Discipline)

- [ ] Red / Orange / Green / Gray 数量分布已统计
- [ ] Red 条目逐条已分析
- [ ] Orange 条目逐条已分析(允许针对项目特异性筛选,但筛选标准必须显式)
- [ ] Green / Gray 视情况覆盖

## 反推纪律(Root Cause Discipline)

- [ ] 每条 finding 根因反推路径清晰
- [ ] `codegen_output_map` 中转 (若有)
- [ ] 无中转时降级标签传递
- [ ] 没有"硬猜"模型侧根因

## 闭环路由纪律(Closure Routing Discipline)

- [ ] 每条 finding 落到四枚举之一
- [ ] `refactor-model` 优先(MBD 项目)
- [ ] `out-of-mbd-scope` 配置管理审批要求显式
- [ ] `accept-residual` 文档化 + 评审签字

## 设置审查纪律(Polyspace Settings Audit)

- [ ] 规则集严格度判断有依据(不主观)
- [ ] 误报 / 漏检 风险已声明
- [ ] 项目特异性建议已给出

## 边界与纪律

- [ ] 没有真实运行 Polyspace
- [ ] 没有修改代码或模型
- [ ] 没有替代手工 code review
- [ ] 没有解释 MISRA / CWE / CERT C 具体规则
- [ ] 没有给"已通过 Polyspace 门"结论

## 交接可用性(Artifact Handoff)

- [ ] 主交付工件名为 `polyspace_runtime_error_findings`
- [ ] 工件包含 `tool_context` / `scope` / `facts` / `inferences` / `evidence_index` / `gaps` / `next_skill_inputs` / `finding_table` / `severity_distribution` / `closure_routing`
- [ ] 下游 skill (`clm-codegen-compliance-refactor` / `clm-embedded-coder-config-reviewer` / `clm-fixed-point-refactor` / `clm-storage-class-governor`)可直接消费

## 失败与降级

- [ ] 输入不足时已采用降级输出
- [ ] 已标注受影响 finding 与置信度变化
- [ ] 已给出下一步最小补充动作

## 交付前确认

- [ ] 输出语言为中文,专业术语首次出现附英文注释
- [ ] 代码文件名 / 函数名 / 变量名 / 错误 ID 保持原文
- [ ] 结论不超出本技能职责边界
- [ ] 自评分(参考 `../../_meta/quality-scorecard.md`)≥10/12
