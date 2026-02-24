# 技能拆分方案输出模板（Output Template）

用于输出“单体 skill 拆分为技能库”的设计方案。

## 1. 拆分结论（Decision Summary）

- 是否建议拆分：是 / 否
- 拆分原因（3-5 条）
- 预期收益（触发准确性、专业性、效果、维护性）

## 2. 现有技能能力清单（Capability Inventory）

按能力项列出：

- 能力项名称
- 输入
- 输出
- 前置依赖
- 专业方法
- 常见误判/风险

## 3. 拆分策略（Splitting Strategy）

- 采用的拆分轴（阶段轴/输入形态轴/方法轴/触发语言轴/复用轴）
- 为什么选这些轴
- 为什么不选其他轴（可选）

## 4. 原子技能设计（Atomic Skills）

对每个原子技能给出：

1. 技能名（建议名）
2. 目标（负责什么）
3. 不负责项（边界）
4. 输入与前置依赖
5. 输出产物
6. 触发语句示例（2-3 条）
7. 与其他技能的关系（上游/下游/并列）

## 5. 编排技能设计（Workflow Skill, 如需要）

- 是否需要编排技能：是 / 否
- 编排技能名称
- 编排步骤顺序
- 前置条件校验
- 不可跳步规则
- 最终汇总输出结构

## 6. 仓库组织方案（Repository Taxonomy）

- 目录分层（例如 `code-reading/`, `log-analysis/`, `workflows/`）
- 命名规范（前缀、对象、动作）
- 何时新增 skill vs 扩展 skill
- 弃用策略（deprecation）

## 7. 迁移计划（Migration Plan）

- 原 skill 如何处理（保留/重构为编排技能/弃用）
- 迁移步骤
- 对历史用法的兼容策略

## 8. 风险与控制（Risks & Controls）

- 过度拆分风险
- 重叠边界风险
- 用户选择成本上升风险
- 对应控制措施（编排技能、README 指南、边界声明）

## 9. 下一步实施清单（Implementation Checklist）

- [ ] 初始化技能目录
- [ ] 编写每个 skill 的 `SKILL.md`
- [ ] 补齐 `agents/openai.yaml`
- [ ] 增加必要 `references/`
- [ ] 更新仓库目录文档
- [ ] 运行校验脚本
