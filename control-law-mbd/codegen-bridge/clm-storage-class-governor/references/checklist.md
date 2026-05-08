# 检查清单(Checklist)

用于在交付 `clm-storage-class-governor` 输出前做快速复核。建议按顺序勾选;如未满足项导致结论降级,需在输出中显式写明。

## clm-storage-class-governor 专项检查

- [ ] 至少覆盖三类对象:`Simulink.Parameter` / `Simulink.Signal` / `Simulink.Bus`
- [ ] 每个待治理对象给出:当前 Storage Class + 当前命名 + 治理决策 + 期望 + 影响 + 回归点
- [ ] 治理决策落到四类之一:`keep` / `adjust` / `rename` / `migrate`
- [ ] 命名前缀/后缀冲突已识别;跨字典命名冲突已结合作用域判定
- [ ] 标定可达性(Calibration Accessibility)审查表已给出
- [ ] 桥接层接口约定核对(若提供 FMT `mbd_boundary_map`)结论已声明

## 工具上下文(Tool Context)

- [ ] 上游工件 `tool_context` 已汇总成"治理对象的工具矩阵"
- [ ] 矩阵内无冲突;若有冲突已阻断治理结论
- [ ] 项目级规范来源(公司规范 / 通用建议)已显式声明

## 输入与范围

- [ ] `data_dictionary_map` 已提供(必需上游)
- [ ] `codegen_output_map` 已提供(必需上游)或已声明阻断
- [ ] (可选)`coder_config_review` / 项目规范 / FMT `mbd_boundary_map` 是否提供
- [ ] 输入缺口(Gaps)及其影响已列出

## 决策完整性

- [ ] 每条决策含 `keep/adjust/rename/migrate`
- [ ] 每条决策含期望 Storage Class + 期望命名
- [ ] 每条决策含影响范围
- [ ] 每条决策含回归点
- [ ] 没有"应该改成 X"式的孤立建议(无影响与回归点)

## 命名一致性

- [ ] 命名前缀/后缀分组扫描完成
- [ ] 跨字典同名结合作用域判定为"冲突 / 仅同名 / 故意复用"
- [ ] 命名规范的违例数量与样例已给出

## 标定可达性

- [ ] 每个对象给出可达性结论(外部读写 + 在线标定)
- [ ] `ImportedExtern` / `ExportedGlobal` / `Calibration` / `Tunable` 等存储类的影响已说明
- [ ] 不可达但被规范要求可达的对象已列入 backlog

## 桥接纪律(若涉及 FMT)

- [ ] 接口层期望(链接段 / extern / 命名前缀)已抓取
- [ ] 与本治理决策的差异显式列出
- [ ] 没有擅自调和差异

## 边界与纪律

- [ ] 没有审查配置 / 没有建立映射 / 没有解读字典 / 没有修改文件
- [ ] 没有给"已可执行改造"的结论(需 `clm-codegen-compliance-refactor` 接力)

## 改造 backlog

- [ ] 优先级(高/中/低)已标注
- [ ] 影响范围已声明
- [ ] 回归点已列出
- [ ] 高风险项目(影响多 ECU 接口或破坏标定流程)单独标记

## 交接可用性(Artifact Handoff)

- [ ] 主交付工件名为 `storage_class_governance`
- [ ] 工件包含 `tool_context` / `scope` / `facts` / `inferences` / `evidence_index` / `gaps` / `next_skill_inputs` / `naming_and_storage_class_table`
- [ ] 下游 skill (`clm-codegen-compliance-refactor`) 可直接消费

## 失败与降级

- [ ] 输入不足时已采用降级输出
- [ ] 已标注受影响决策与置信度变化
- [ ] 已给出下一步最小补充动作

## 交付前确认

- [ ] 输出语言为中文,专业术语首次出现附英文注释
- [ ] 对象名 / Storage Class 名 / 命名前缀-后缀保持原文
- [ ] 结论不超出本技能职责边界
- [ ] 自评分(参考 `../../_meta/quality-scorecard.md`)≥10/12
