# clm-simulink-model-reader 输出模板

## 使用说明

- 目标:输出 Simulink 模型层级、信号流、采样时间、原子单元的"模型地图",支持下游 Stateflow 语义、字典解读、代码生成映射等技能引用
- 主交付工件(Primary Artifact):`simulink_model_map`
- 默认中文输出;专业术语首次出现附英文注释(English Annotation)

## 基本信息(Basic Context)

- `task_id`:
- `skill_name`:`clm-simulink-model-reader`
- `artifact_name`:`simulink_model_map`
- `tool_context`:
  - Simulink / Stateflow 版本:
  - 模型形态(`.slx` / `.mdl`):
  - 是否绑定 `.sldd`:
  - 许可证可用性:
- `scope`(模型路径 / 关注子系统):
- `version_or_branch`:

## 范围与假设(Scope & Assumptions)

- [ ] 模型顶层入口
- [ ] 用户关注链路或子系统
- [ ] 引用模型(Model Reference)是否在范围内
- [ ] 库链接(Library Link)是否在范围内
- 事实(Fact)与推断(Inference)边界说明:

## 输入摘要(Input Summary)

- [ ] 模型路径
- [ ] 关联 `.sldd` 路径(若有)
- [ ] 用户关注子系统/信号
- 输入缺口(Gaps):

## 工件正文(Artifact Body)

### 1. 子系统层级树(Subsystem Hierarchy)

- 说明:列出子系统层级,标注类型(`Subsystem` / `Atomic Subsystem` / `Model Reference` / `Library Link` / `Stateflow Chart`)与 Mask 状态
- 内容:

```
ModelRoot/
├─ Inputs/                    [Subsystem, virtual]
├─ Controller/                [Atomic Subsystem]
│  ├─ AttitudeLoop/           [Atomic Subsystem]
│  │  └─ PID/                 [Masked Subsystem]
│  └─ RateLoop/               [Atomic Subsystem]
├─ ModeManager/               [Stateflow Chart, see clm-stateflow-semantics-reader]
└─ Outputs/                   [Subsystem, virtual]
```

### 2. 信号流路径(Signal Flow)

- 说明:列出至少一条端到端控制链路,使用 "源 → 经过 → 目的" 格式;Goto/From、Bus 操作显式标注
- 内容:

| 路径 ID | 起点 | 经过 | 终点 | 备注 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

### 3. 采样时间表(Sample Time Table)

- 说明:对每个 Atomic Subsystem 与关键 Block 抓取 SampleTime;标注 inherited / discrete / continuous;识别多速率边界
- 内容:

| 路径 | 类型 | SampleTime | 来源 | 多速率边界 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

### 4. 原子 vs 虚拟子系统对照(Atomic vs Virtual)

- 说明:Atomic Subsystem 是代码生成的函数边界,Virtual 只是视图;混淆会导致代码生成误判
- 内容:

| 子系统路径 | Atomic? | Function Packaging |
| --- | --- | --- |
|  |  |  |

### 5. Mask 子系统清单(Masked Subsystems)

- 说明:列出 Mask 子系统及其参数面板与初始化代码出处
- 内容:

| 路径 | 参数 | 初始化代码出处 |
| --- | --- | --- |
|  |  |  |

### 6. 引用模型与库链接(Model References & Library Links)

- 说明:列出指向与状态(已加载 / 未加载 / 缺失)
- 内容:

| 路径 | 类型 | 指向 | 状态 |
| --- | --- | --- | --- |
|  |  |  |  |

## 关键事实(Facts)

- Fact-1:
- Fact-2:

## 关键推断(Inferences)

- Inference-1(置信度:高/中/低):
- Inference-2(置信度:高/中/低):

## 证据索引(Evidence Index)

- 模型证据:`model.slx > Controller/AttitudeLoop/PID` → 结论
- 模型证据:`model.slx > ModeManager` → 结论(指向 Stateflow Chart,语义交由 `clm-stateflow-semantics-reader`)

## 缺口与风险(Gaps & Risks)

- 缺口(例:许可证缺失 / `.sldd` 未提供 / 子系统加密):
- 风险:
- 降级策略:

## 下游输入建议(Next Skill Inputs)

- 推荐下游 skill:
  - `clm-stateflow-semantics-reader`(关注:Stateflow Chart 路径清单)
  - `clm-data-dictionary-reader`(关注:`.sldd` 引用清单)
  - `clm-codegen-output-mapper`(关注:Atomic Subsystem 树 + 多速率边界)
  - `clm-embedded-coder-config-reviewer`(关注:多速率与原子单元信息)
- 建议关注的子系统/信号/路径:
- 需要补充的输入或确认项:

## 质量门禁自检(简表)

- [ ] 边界纯度(Boundary Purity):未越权给出 Stateflow 语义 / 代码生成结论
- [ ] 证据可追溯(Evidence Traceability):关键结论可回链到模型路径 + 子系统路径
- [ ] 工具上下文显式(Tool Context Explicitness):Simulink 版本与许可证状态已记录
- [ ] 交接可用性(Handoff Usability):下游 skill 可直接使用本输出
- [ ] 失败/降级说明完整:输入缺口、受影响结论、置信度变化已标注

## 共享规范引用

- `../../_meta/first-principles-skill-contract.md`
- `../../_meta/artifact-handoff-contract.md`
- `../../_meta/quality-scorecard.md`
