# 检查清单(Checklist)

用于在交付 `clm-codegen-output-mapper` 输出前做快速复核。建议按顺序勾选;如未满足项导致结论降级,需在输出中显式写明。

## clm-codegen-output-mapper 专项检查

- [ ] 至少一条完整路径"模型子系统 → 生成函数 → 输入/输出全局变量"被串起,带文件路径 + 行号
- [ ] 至少一条参数路径"`Simulink.Parameter` → 生成代码全局变量"被串起
- [ ] Step Function 入口形态(单 step / 多 rate / Reusable)已明确
- [ ] 文件角色地图(`*.c` / `*_data.c` / `*_private.h` / `*_types.h` 等)已给出
- [ ] 桥接层契合点已记录(若提供桥接代码),否则已在 `gaps` 中登记

## 工具上下文(Tool Context)

- [ ] Embedded Coder / Simulink Coder 版本已确认或标注 `unknown`
- [ ] 代码生成形态(单文件 / 模块化 / Reusable / Reentrant)已记录
- [ ] 类型定义来源(`rtwtypes.h` / 自定义 Type)已记录
- [ ] 代码生成时间戳与模型修改时间戳已比较;不一致时降级标签已传递

## 输入与范围

- [ ] 模型路径与生成代码目录已记录
- [ ] (可选)`simulink_model_map` 是否提供
- [ ] (可选)`coder_config_review` 是否提供
- [ ] (可选)桥接代码路径是否提供
- [ ] 输入缺口(Gaps)及其影响已列出

## 证据与结论

- [ ] 每条映射给出"模型对象路径 + 代码文件路径 + 行号"
- [ ] 已区分事实(Fact)与推断(Inference)
- [ ] 找不到对应函数的子系统已在 `gaps` 中列出,而不是硬猜
- [ ] 没有评价桥接代码质量(只标位置)
- [ ] 没有评价生成代码合规性(只建立映射)

## 一致性

- [ ] 已声明代码生成时间戳与模型时间戳是否一致
- [ ] 不一致时所有结论携带降级标签
- [ ] 已建议下一步动作(重新生成 / 重新审查)

## 交接可用性(Artifact Handoff)

- [ ] 主交付工件名为 `codegen_output_map`
- [ ] 工件包含 `tool_context` / `scope` / `facts` / `inferences` / `evidence_index` / `gaps` / `next_skill_inputs` / `model_to_code_map` / `bridge_layer_contract`
- [ ] 下游 skill (`clm-storage-class-governor` / `clm-codegen-compliance-refactor` / `clm-pil-hil-replay-analyzer`) 可直接消费
- [ ] 跨库衔接:`bridge_layer_contract` 字段齐全,可与 `fmt-mbd-interface-reader` 的 `mbd_boundary_map` 对接

## 失败与降级

- [ ] 输入不足时已采用降级输出
- [ ] 已标注受影响结论与置信度变化
- [ ] 已给出下一步最小补充动作

## 交付前确认

- [ ] 输出语言为中文,专业术语首次出现附英文注释
- [ ] 函数名 / 全局变量名 / 结构体名 / 字段名保持原文
- [ ] 结论不超出本技能职责边界
- [ ] 自评分(参考 `../../_meta/quality-scorecard.md`)≥10/12
