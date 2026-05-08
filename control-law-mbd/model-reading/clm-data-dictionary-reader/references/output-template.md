# clm-data-dictionary-reader 输出模板

## 使用说明

- 目标:输出 SLDD 引用层级、对象清单、存储类、类型链与引用一致性,支持 `clm-codegen-output-mapper` 与 `clm-storage-class-governor` 等下游 skill
- 主交付工件(Primary Artifact):`data_dictionary_map`
- 默认中文输出;专业术语首次出现附英文注释

## 基本信息(Basic Context)

- `task_id`:
- `skill_name`:`clm-data-dictionary-reader`
- `artifact_name`:`data_dictionary_map`
- `tool_context`:
  - Simulink 版本:
  - SLDD 形态(单文件 / 含 Reference / 含 ConfigSets):
  - 许可证可用性:
- `scope`(SLDD 路径 + 模型路径若提供):
- `version_or_branch`:

## 范围与假设(Scope & Assumptions)

- [ ] 是否提供模型用于一致性检查
- [ ] 是否提供 `simulink_model_map`
- [ ] 用户关注的对象类别
- 事实(Fact)与推断(Inference)边界说明:

## 输入摘要(Input Summary)

- [ ] SLDD 路径
- [ ] 模型路径(若有)
- [ ] `simulink_model_map`(若有)
- 输入缺口(Gaps):

## 工件正文(Artifact Body)

### 1. SLDD 引用层级图(Reference Hierarchy)

```
TopDictionary.sldd
├─ ReferenceA.sldd
│  └─ ReferenceA1.sldd
└─ ReferenceB.sldd
```

循环引用检测:`无` / `存在(详见 gaps)`

### 2. 对象清单 — Parameter

| 对象名 | 类型 | 作用域 | 初值 | Min/Max | Storage Class | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

### 3. 对象清单 — Signal

| 对象名 | 类型 | 作用域 | 初值 | Storage Class | 备注 |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

### 4. 对象清单 — Bus Object

| 对象名 | 字段 | 字段类型 | 备注 |
| --- | --- | --- | --- |
|  |  |  |  |

### 5. 对象清单 — AliasType / Numeric Type

| 对象名 | 指向类型 | 备注 |
| --- | --- | --- |
|  |  |  |

### 6. 类型链(Type Chain)

| 起点对象 | 中间 Alias / Bus | 终点 Built-in / Fixed-Point | 循环引用? |
| --- | --- | --- | --- |
|  |  |  |  |

### 7. 引用一致性(若提供模型)

| 类别 | 对象列表 | 备注 |
| --- | --- | --- |
| 模型引用但字典缺失 |  |  |
| 字典定义但模型未引用 |  |  |
| 跨字典同名(经作用域判定) |  |  |

### 8. 风险清单(Risk Findings)

| 风险 | 涉及对象 | 等级(高/中/低) | 影响 | 建议下游 skill |
| --- | --- | --- | --- | --- |
| 类型未指定 |  |  |  | `clm-storage-class-governor` |
| Storage Class = Auto |  |  |  | `clm-codegen-output-mapper` |
| 命名冲突 |  |  |  | `clm-storage-class-governor` |
| Min/Max 为空 |  |  |  | `clm-storage-class-governor` |

## 关键事实(Facts)

- Fact-1:
- Fact-2:

## 关键推断(Inferences)

- Inference-1(置信度:高/中/低):
- Inference-2(置信度:高/中/低):

## 证据索引(Evidence Index)

- 字典证据:`Top.sldd > Design Data > Parameter > Kp_att` → 类型 = double, Storage Class = ExportedGlobal
- 字典证据:`Ref.sldd > Bus Object > AttitudeBus` → 字段清单

## 缺口与风险(Gaps & Risks)

- 缺口(例:许可证缺失 / Reference Dictionary 不可访问 / 模型未提供):
- 风险:
- 降级策略:

## 下游输入建议(Next Skill Inputs)

- 推荐下游 skill:
  - `clm-codegen-output-mapper`(关注:Storage Class + 类型链 — 用于匹配生成代码全局变量)
  - `clm-storage-class-governor`(关注:风险清单 — 作为治理输入)
  - `clm-codegen-compliance-refactor`(关注:类型未指定 / 命名冲突 — 作为重构 backlog)
- 建议关注的对象/字段:
- 需要补充的输入或确认项:

## 质量门禁自检(简表)

- [ ] 边界纯度:未审查模型层 / 未评价配置 / 未做治理决策
- [ ] 证据可追溯:每条结论给出 SLDD 路径 + 对象名 + 段
- [ ] 工具上下文显式:版本 + SLDD 形态 + 许可证已记录
- [ ] 引用一致性纪律:差异显式分类
- [ ] 交接可用性:下游 skill 可直接消费
- [ ] 失败/降级说明完整

## 共享规范引用

- `../../_meta/first-principles-skill-contract.md`
- `../../_meta/artifact-handoff-contract.md`
- `../../_meta/quality-scorecard.md`
