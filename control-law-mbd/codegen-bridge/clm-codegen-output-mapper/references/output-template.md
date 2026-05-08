# clm-codegen-output-mapper 输出模板

## 使用说明

- 目标:输出"模型 ↔ 生成代码"映射地图,支持下游 `codegen-bridge/` 内其他 skill、`verification/` 与跨库 `fmt-mbd-interface-reader` 引用
- 主交付工件(Primary Artifact):`codegen_output_map`
- 默认中文输出;专业术语首次出现附英文注释

## 基本信息(Basic Context)

- `task_id`:
- `skill_name`:`clm-codegen-output-mapper`
- `artifact_name`:`codegen_output_map`
- `tool_context`:
  - Embedded Coder 版本:
  - 代码生成形态(单文件 / 模块化 / Reusable / Reentrant):
  - 类型定义来源(`rtwtypes.h` / 自定义):
  - 模型修改时间戳:
  - 代码生成时间戳:
  - 时间戳一致性:
- `scope`(模型路径 / 生成代码目录 / 桥接代码路径):
- `version_or_branch`:

## 范围与假设(Scope & Assumptions)

- [ ] 是否提供 `simulink_model_map` 上游工件
- [ ] 是否提供 `coder_config_review` 上游工件
- [ ] 是否提供桥接代码
- 事实(Fact)与推断(Inference)边界说明:

## 输入摘要(Input Summary)

- [ ] 模型路径
- [ ] 生成代码目录
- [ ] 桥接代码路径(若有)
- 输入缺口(Gaps):

## 工件正文(Artifact Body)

### 1. 文件角色地图(File Role Map)

| 文件 | 角色 | 关键内容 |
| --- | --- | --- |
| `<model>.c` | 主入口 + Step | `model_step` / `model_initialize` / `model_terminate` |
| `<model>.h` | 公共声明 |  |
| `<model>_data.c` | 参数初值 |  |
| `<model>_private.h` | 内部结构 |  |
| `<model>_types.h` | 类型定义 |  |

### 2. Step Function 入口表(Step Function Entries)

| 函数名 | 签名 | 所在文件:行号 | 调用约定 | 备注 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

### 3. 子系统 ↔ 函数映射(Subsystem to Function)

| 子系统路径 | Atomic? | 生成函数 | 文件:行号 | 内联/Reusable 备注 |
| --- | --- | --- | --- | --- |
| `model.slx > Controller/AttitudeLoop` |  |  |  |  |

### 4. 参数 ↔ 全局变量映射(Parameter to Global Variable)

| 模型参数 | 存储类 | 生成变量名 | 文件:行号 | 命名前缀/后缀 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

### 5. Bus ↔ 结构体映射(Bus to Struct)

| Bus Object | 字段 | 生成结构体名 | 字段名 | 文件:行号 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

### 6. 桥接层契合点(Bridge Layer Contract)

> 仅在提供桥接代码时填写;否则在 `gaps` 中登记。本 skill 只标位置,不评价桥接代码质量。

| 类型 | 桥接代码位置 | 调用/读写对象 | 备注 |
| --- | --- | --- | --- |
| Step 调用 |  |  |  |
| 参数读写 |  |  |  |
| 信号读写 |  |  |  |

跨库交接关键字段(供 `fmt-mbd-interface-reader` 直接消费):

- `model_step` 入口签名:
- `model_initialize` 入口签名:
- 接口层期望的全局变量分组:
- 类型定义文件:

## 关键事实(Facts)

- Fact-1:
- Fact-2:

## 关键推断(Inferences)

- Inference-1(置信度:高/中/低):
- Inference-2(置信度:高/中/低):

## 证据索引(Evidence Index)

- 模型 ↔ 代码:`model.slx > Controller/AttitudeLoop` ↔ `controller.c:128 controller_step()`
- 参数 ↔ 变量:`Simulink.Parameter Kp_att` ↔ `controller_data.c:42 Kp_att`

## 缺口与风险(Gaps & Risks)

- 缺口(例:代码与模型时间戳不一致 / 桥接代码未提供 / 找不到对应函数):
- 风险:
- 降级策略:

## 下游输入建议(Next Skill Inputs)

- 推荐下游 skill:
  - `clm-storage-class-governor`(关注:参数 ↔ 全局变量映射 + 命名前缀/后缀)
  - `clm-codegen-compliance-refactor`(关注:非预期映射、内联点)
  - `clm-pil-hil-replay-analyzer`(关注:Step Function 入口、可读写全局变量名)
  - `fmt-mbd-interface-reader`(跨库:`bridge_layer_contract` 字段)
- 建议关注的子系统/参数/信号:
- 需要补充的输入或确认项:

## 质量门禁自检(简表)

- [ ] 边界纯度:未审查配置 / 未治理存储类 / 未评价桥接代码质量
- [ ] 证据可追溯:每条映射给出"模型对象 + 代码文件 + 行号"
- [ ] 工具上下文显式:版本 + 时间戳一致性已记录
- [ ] 一致性纪律:不一致时降级标签已传递
- [ ] 交接可用性:`bridge_layer_contract` 可被 FMT 端直接消费
- [ ] 失败/降级说明完整

## 共享规范引用

- `../../_meta/first-principles-skill-contract.md`
- `../../_meta/artifact-handoff-contract.md`
- `../../_meta/quality-scorecard.md`
