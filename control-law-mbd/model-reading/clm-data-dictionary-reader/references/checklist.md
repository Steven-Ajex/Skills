# 检查清单(Checklist)

用于在交付 `clm-data-dictionary-reader` 输出前做快速复核。建议按顺序勾选;如未满足项导致结论降级,需在输出中显式写明。

## clm-data-dictionary-reader 专项检查

- [ ] SLDD 引用层级(Top + Reference Dictionaries)已明确
- [ ] 至少覆盖四类核心对象:`Simulink.Parameter` / `Simulink.Signal` / `Simulink.Bus` / `Simulink.AliasType`
- [ ] 每个对象记录了类型 / 作用域 / 初值 / 存储类(Storage Class)
- [ ] 类型链(Alias / Bus 指向)已梳理,循环引用已检测
- [ ] 至少识别一类风险(命名冲突 / 未引用对象 / 类型未指定 / 存储类不一致)
- [ ] Storage Class 为 `Auto` 的对象已显式标注"实际存储类由代码生成决定"

## 工具上下文(Tool Context)

- [ ] Simulink 版本已确认或标注 `unknown`
- [ ] SLDD 形态(单文件 / 含 Reference / 含 Configuration Sets)已记录
- [ ] 许可证可用性已记录;无许可证时降级到 SLDD 二进制 / XML 解析的路径已声明

## 输入与范围

- [ ] SLDD 路径已记录
- [ ] (可选)模型路径与 `simulink_model_map` 是否提供
- [ ] 加密 / 受保护字典已在 `gaps` 中登记
- [ ] 输入缺口(Gaps)及其影响已列出

## 引用一致性

- [ ] (若有模型)模型引用但字典缺失的对象已列入 `gaps`
- [ ] (若有模型)字典定义但模型未引用的对象已列入"未引用对象"
- [ ] 跨 Reference Dictionary 同名对象已结合作用域判断,未自动判为"冲突"

## 证据与结论

- [ ] 每条结论给出"SLDD 路径 + 对象名 + 段"
- [ ] 已区分事实(Fact)与推断(Inference)
- [ ] 没有越权给出"代码生成会怎样"的结论
- [ ] 没有给出"应该改成 X"的治理决策(已转交 `clm-storage-class-governor`)

## 交接可用性(Artifact Handoff)

- [ ] 主交付工件名为 `data_dictionary_map`
- [ ] 工件包含 `tool_context` / `scope` / `facts` / `inferences` / `evidence_index` / `gaps` / `next_skill_inputs` / `bus_object_table` / `parameter_object_table`
- [ ] 下游 skill (`clm-codegen-output-mapper` / `clm-storage-class-governor`) 可直接消费

## 失败与降级

- [ ] 输入不足时已采用降级输出
- [ ] 已标注受影响结论与置信度变化
- [ ] 已给出下一步最小补充动作(获取许可证 / 提供模型 / 解锁字典 等)

## 交付前确认

- [ ] 输出语言为中文,专业术语首次出现附英文注释
- [ ] 对象名 / 类型名 / 存储类名保持原文
- [ ] 结论不超出本技能职责边界
- [ ] 自评分(参考 `../../_meta/quality-scorecard.md`)≥10/12
