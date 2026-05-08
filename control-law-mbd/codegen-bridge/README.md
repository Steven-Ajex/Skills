# Codegen Bridge（代码生成与桥接）

Embedded Coder 自动代码生成与**模型 ↔ 手写桥接层**对接类原子技能（atomic skill）的容器目录。

## 1. 职责（What）

负责处理"模型生成代码"侧的所有专业判断:

- Embedded Coder 配置审查与生成代码诊断
- 生成代码与手写桥接层（如 `fmt-mbd-interface-reader` 描述的 FMT 接口层）的契合点分析
- 参数 / 信号 / Bus 的存储类（Storage Class）、命名、标定治理

## 2. 规划 skill 列表

| Skill 名 | 最小任务单元 | 主要工件 | 状态 |
| --- | --- | --- | --- |
| `clm-embedded-coder-config-reviewer` | 审查 Embedded Coder 配置与代码生成诊断 | `coder_config_review` | 已落地 |
| `clm-codegen-output-mapper` | 建立模型对象 ↔ 生成代码的映射,识别桥接层契合点 | `codegen_output_map` | 待建 |
| `clm-storage-class-governor` | 治理参数/信号/Bus 的存储类、命名、标定一致性 | `storage_class_governance` | 待建 |

后续候选（Backlog）：

- `clm-tlc-customization-reviewer`
- `clm-step-function-entrypoint-mapper`
- `clm-shared-utility-deduper`

> 当前为 placeholder。具体 skill 落地前请先对照 `../_meta/first-principles-skill-contract.md`。

## 3. 不负责（Out of Scope）

- 模型层结构与信号流解读 → 走 `../model-reading/`
- 模型重构 → 走 `../model-authoring/`
- 测试用例与覆盖率 → 走 `../verification/`
- 嵌入式集成（手写桥接层的实际改造）→ 走 `fmt/code-reading/fmt-mbd-interface-reader` 与 FMT 库后续 skill

## 4. 触发边界（When NOT to use）

- 输入只有模型而无生成代码（应先生成或降级到 `model-reading/`）
- 输入只有生成代码而无模型源（无法回链到模型对象,应显式登记缺口）
- Embedded Coder 许可证不可用（应在工件 `tool_context.licensing` 中显式标注）

## 5. 与 `fmt/` 库的衔接

本目录是与 `fmt/` 库**对接最频繁**的能力域,衔接关系：

- `codegen_output_map`（本目录）↔ `mbd_boundary_map`（`fmt-mbd-interface-reader`）
  两者描述同一接口的两侧,工件 `evidence_index` 必须互相引用
- 跨库交接时各自保留 `tool_context`（本库)和 `firmware_context`（FMT 库）,不混用版本规则

## 6. 共同输出契约

工件必须满足 `../_meta/artifact-handoff-contract.md`,并额外包含：

- `model_to_code_map`：模型对象 ↔ 生成代码（文件 + 函数 + 全局变量）
- `bridge_layer_contract`：与手写桥接层的对接点（如有）
- `naming_and_storage_class_table`：命名约定与存储类一致性
