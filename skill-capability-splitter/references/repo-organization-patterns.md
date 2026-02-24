# Skills 仓库组织模式（Repository Organization Patterns）

用于在技能拆分后为技能库建立稳定的目录和治理模式。

## 模式 A：按用途分层（推荐）

示例：

```text
domain/
├─ code-reading/
├─ data-processing/
├─ analysis/
├─ reporting/
└─ workflows/
```

适用：

- 一个领域内有多个阶段能力
- 后续会持续扩展

优点：

- 可组合性好
- 检索和维护清晰

## 模式 B：按对象分层

示例：

```text
domain/
├─ estimator/
├─ controller/
├─ logger/
└─ workflows/
```

适用：

- 领域对象边界稳定且专业团队按对象分工

风险：

- 同一阶段能力会分散在多个对象目录

## 模式 C：混合模式（对象 + 用途）

示例：

```text
domain/
├─ code-reading/
│  ├─ estimator-reader
│  └─ controller-reader
├─ analysis/
│  ├─ estimator-analyzer
│  └─ controller-analyzer
└─ workflows/
```

适用：

- 既要保持流程分层，也要保留对象语义

## 命名建议（通用）

推荐模式：

- `domain-object-action`
- `domain-stage-action`

动作后缀建议统一：

- `reader`
- `decoder`
- `segmenter`
- `analyzer`
- `writer`
- `optimizer`
- `workflow`（或保留具体动作）

## 管理建议（最小集合）

拆分后至少维护：

1. 领域入口文档（目录总览）
2. 拆分分析记录（为什么这么拆）
3. 仓库管理规则（新增/扩展/弃用）
4. 原子技能与编排技能的关系说明
