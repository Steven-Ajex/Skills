from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


SKILLS = {
    "fmt/code-reading/fmt-control-loop-reader": {
        "display": "FMT Control Loop Reader",
        "artifact": "control_loop_map",
        "domain": "code-reading",
        "template_goal": "输出 FMT 控制闭环调度与数据路径地图，支持后续接口层阅读、状态机阅读和调参报告引用。",
        "scope_examples": ["机型变体（vtol/mc/fw）", "入口任务（如 task_vehicle）", "宏开关/运行模式假设"],
        "input_examples": ["代码路径", "任务入口函数", "用户关注链路（姿态/高度/速度/执行器）"],
        "section_prompts": [
            ("控制循环顺序图", "按一轮循环顺序写出：触发条件 -> 函数/模块 -> 输入 -> 输出 -> 下一步。"),
            ("模块职责边界", "列出 sensor / INS / FMS / Controller / actuator 的职责与边界，标注不确定项。"),
            ("MCN/Topic 数据流", "按 发布者 -> 订阅者 方式整理关键 topic 或 bus。"),
            ("周期与节拍关系", "给出周期/节拍判断及证据，注明条件分支。"),
        ],
        "specific_checks": [
            "至少串起一条完整闭环路径（入口到执行器输出）。",
            "周期/节拍结论必须指向具体代码位置或触发条件。",
            "变体未确认时明确降级，不混用 vtol/mc/fw 结论。",
        ],
        "reference_usage": "需要快速输出控制闭环地图时先读模板；提交给下游技能前再用清单复核时序与证据完整性。",
    },
    "fmt/code-reading/fmt-mbd-interface-reader": {
        "display": "FMT MBD Interface Reader",
        "artifact": "mbd_boundary_map",
        "domain": "code-reading",
        "template_goal": "输出接口桥接层与 MBD 生成代码层的职责边界、参数绑定和 bus/topic 映射，避免混淆 glue code 与控制律本体。",
        "scope_examples": ["目标模块目录（INS/FMS/Controller 变体）", "*_interface.c 与 lib/ 范围", "变体/版本假设"],
        "input_examples": ["目标模块路径", "用户关注点（参数绑定/bus 映射/step 入口）", "上游 control_loop_map（可选）"],
        "section_prompts": [
            ("接口层 vs 生成代码层职责表", "明确哪些逻辑属于 glue code，哪些属于模型生成代码。"),
            ("参数绑定路径", "列出 PARAM_GROUP_DEFINE / param_link_variable 的关键路径与证据。"),
            ("topic/bus 映射", "整理输入/输出 topic 与 MLOG_BUS_DEFINE 等映射关系。"),
            ("模型调用入口", "指出 init/step 调用链与上下文。"),
            ("隐藏复杂度清单", "标记必须进入生成代码才能确认的逻辑点。"),
        ],
        "specific_checks": [
            "不要把 interface 层适配逻辑写成控制律算法结论。",
            "至少给出一条参数绑定路径和一条 topic/bus 映射路径证据。",
            "生成代码内部未验证部分必须标注待确认。",
        ],
        "reference_usage": "在需要区分 interface glue code 与控制律本体时加载模板；输出前用清单检查边界纯度。",
    },
    "fmt/code-reading/fmt-fms-state-machine-reader": {
        "display": "FMT FMS State Machine Reader",
        "artifact": "fms_state_semantics",
        "domain": "code-reading",
        "template_goal": "输出 FMS 状态机状态/模式语义、切换触发和关键转换路径，供日志分段与行为解释使用。",
        "scope_examples": ["FMS 变体目录（vtol_fms/mc_fms/fw_fms）", "关注阶段（过渡/返航/自动模式）", "代码版本"],
        "input_examples": ["fms_interface.c", "FMS.c/FMS_types.h 等生成代码", "用户关注的异常模式切换现象（可选）"],
        "section_prompts": [
            ("状态/模式字段语义表", "用中文说明并在首次出现附英文术语。"),
            ("触发源清单", "列出 Pilot/GCS/Auto/Mission/INS 等输入源及影响字段。"),
            ("关键转换路径", "整理 触发条件 -> 状态变化 -> 输出语义变化。"),
            ("日志分段建议字段", "给下游 segmenter 推荐字段与注意事项。"),
        ],
        "specific_checks": [
            "接口层字符串映射与生成代码真实切换逻辑必须区分。",
            "状态字段语义以代码定义为准，不用日志现象反推替代。",
            "VTOL 特有字段（如 ext_state）适用范围必须写清。",
        ],
        "reference_usage": "分析模式切换或为日志分段建立状态语义时加载模板；用清单防止把日志现象反推成代码逻辑。",
    },
    "fmt/code-reading/fmt-logging-pipeline-reader": {
        "display": "FMT Logging Pipeline Reader",
        "artifact": "logging_pipeline_map",
        "domain": "code-reading",
        "template_goal": "输出 FMT 嵌入式日志系统（mlog/ulog）的触发、记录、缓冲与刷盘机制，以及可靠性风险点。",
        "scope_examples": ["mlog / ulog / 两者", "自动启停与手动命令入口", "日志任务与刷盘路径"],
        "input_examples": ["task_logger.c", "mlog.h/mlog.c", "task_status.c", "cmd_mlog.c"],
        "section_prompts": [
            ("日志链路时序", "按 生产 -> 缓冲 -> 事件 -> 刷盘 -> 关闭 写出机制路径。"),
            ("自动/手动启停规则", "说明 arm/disarm 和 cmd_mlog 的触发条件。"),
            ("mlog vs ulog 职责对比", "说明两类日志的定位与使用方式。"),
            ("可靠性风险点", "写出缓冲满、掉电、刷盘时机等风险及代码证据。"),
            ("给 decoder 的格式线索", "列出 mlog 结构体/版本号/状态机线索。"),
        ],
        "specific_checks": [
            "区分日志记录机制问题与日志内容语义问题。",
            "风险点必须写触发条件与代码路径，不能仅凭经验泛化。",
            "至少串起一条 mlog 生命周期路径。",
        ],
        "reference_usage": "理解日志系统机制和可靠性风险时加载模板；输出前用清单确认没有越界到解码或性能分析结论。",
    },
    "fmt/log-analysis/fmt-mlog-decoder": {
        "display": "FMT Mlog Decoder",
        "artifact": "mlog_decode_summary",
        "domain": "log-analysis",
        "template_goal": "输出 mlog 解码摘要、schema 和完整性评估，并给下游分段/性能分析提供可用信号目录。",
        "scope_examples": ["日志文件名与批次", "FMT mlog 版本/代码分支", "导出格式（CSV/Parquet-ready）"],
        "input_examples": ["mlog*.bin", "mlog 格式源码线索", "目标字段或导出需求"],
        "section_prompts": [
            ("解码摘要", "记录版本、bus 数量、参数组数量、时间范围。"),
            ("schema 清单", "列出重点 bus、字段类型、时间戳字段来源。"),
            ("records 解码完整性", "说明成功率、损坏/截断范围、恢复范围。"),
            ("结构化导出说明", "给出字段名、类型、导出路径/格式。"),
            ("下游可用性清单", "说明 segmenter/analyzer 所需信号是否齐全。"),
        ],
        "specific_checks": [
            "先 schema 后 records，禁止未知 schema 下硬编码 payload 长度。",
            "日志损坏时优先报告恢复范围，不输出性能结论。",
            "版本不匹配时写明差异并决定是否停止。",
        ],
        "reference_usage": "执行 mlog 解码时先用模板组织输出；交付给 segmenter/analyzer 前用清单确认 schema、时间轴、完整性信息齐全。",
    },
    "fmt/log-analysis/fmt-flight-log-segmenter": {
        "display": "FMT Flight Log Segmenter",
        "artifact": "flight_phase_segments",
        "domain": "log-analysis",
        "template_goal": "输出可复现的飞行阶段分段与关键事件索引，为性能分析提供可靠的时间上下文。",
        "scope_examples": ["单架次日志", "机型变体（vtol/mc/fw）", "时间轴连续片段范围"],
        "input_examples": ["已解码结构化日志", "FMS 状态语义（可选）", "ulog 事件文本（可选）"],
        "section_prompts": [
            ("分段规则定义", "明确使用字段、阈值、条件和优先级。"),
            ("飞行阶段时间轴", "列出阶段名、起止时间、证据信号。"),
            ("关键事件索引", "记录模式切换、过渡、异常、降落等事件。"),
            ("分段质量问题", "说明缺数据、状态跳变、边界模糊及影响。"),
            ("下游观察窗口建议", "给 analyzer 标出重点时间段和注意事项。"),
        ],
        "specific_checks": [
            "分段规则必须可复现，不可只给经验性描述。",
            "VTOL 与非 VTOL 规则必须分开说明。",
            "关键边界必须有证据信号或状态字段变化支撑。",
        ],
        "reference_usage": "进行阶段划分时先按模板固化规则；交付前用清单复核可复现性和边界证据。",
    },
    "fmt/log-analysis/fmt-control-performance-analyzer": {
        "display": "FMT Control Performance Analyzer",
        "artifact": "control_performance_findings",
        "domain": "log-analysis",
        "template_goal": "输出分层控制性能分析结论（INS/FMS/Controller/Actuator），形成现象到证据再到候选根因的链条。",
        "scope_examples": ["单架次或单阶段窗口", "机型变体", "参数快照可用性状态"],
        "input_examples": ["已解码结构化日志", "分段结果与事件索引", "参数快照（可选但推荐）"],
        "section_prompts": [
            ("分析范围与前置检查", "确认分段、时间轴、关键信号、参数快照状态。"),
            ("现象清单（按严重度）", "记录振荡、超调、延迟、饱和等现象。"),
            ("证据链", "按 现象 -> 时间段 -> 信号 -> 阶段/模式 上下文 写明证据。"),
            ("候选根因分层", "按估计器/FMS/控制器/执行器/传感器分层归因。"),
            ("候选参数方向与验证建议", "仅给方向级建议，注明置信度和待验证项。"),
        ],
        "specific_checks": [
            "没有分段或模式上下文时，不给全局控制器增益归因。",
            "状态机切换瞬态与控制器性能问题必须分开判断。",
            "缺失参数快照时不输出具体参数值修改量。",
        ],
        "reference_usage": "进行性能分析时先按模板组织证据链；交付给报告技能前用清单检查归因边界和置信度标注。",
    },
    "fmt/log-analysis/fmt-tuning-report-writer": {
        "display": "FMT Tuning Report Writer",
        "artifact": "tuning_recommendation_report",
        "domain": "log-analysis",
        "template_goal": "输出可执行、可验证、可追踪的参数优化报告和试飞验证计划（Test Card），不新增证据。",
        "scope_examples": ["任务背景与目标", "机型/版本/日志批次", "本轮报告覆盖范围"],
        "input_examples": ["代码理解工件", "control_performance_findings", "参数快照/当前参数列表"],
        "section_prompts": [
            ("任务背景与范围", "说明机型、版本、日志来源、目标现象和本次分析边界。"),
            ("证据摘要", "汇总代码侧与日志侧关键证据，明确缺口。"),
            ("参数优化建议（分优先级）", "每条建议包含目标现象、参数、方向、预期效果、风险。"),
            ("风险与副作用", "说明可能引入的耦合影响和安全风险。"),
            ("试飞验证计划（Test Card）", "给出工况、观察项、通过条件、回退条件。"),
            ("待补数据与下一轮动作", "列出仍需采集或验证的最小动作。"),
        ],
        "specific_checks": [
            "每条建议必须有证据回链、验证指标和通过条件。",
            "候选根因与确定性结论必须区分，避免过度确定。",
            "证据不足时输出前置条件未满足，不凑具体参数值。",
        ],
        "reference_usage": "生成正式调参报告和 Test Card 时先套模板；交付前用清单复核证据回链、风险和验证条件。",
    },
}


COMMON_TEMPLATE_FOOTER = [
    "## 质量门禁自检（简表）",
    "",
    "- [ ] 边界纯度（Boundary Purity）：没有越权给下游/上游结论",
    "- [ ] 证据可追溯（Evidence Traceability）：关键结论可回链到代码/日志证据",
    "- [ ] 交接可用性（Handoff Usability）：下游技能可直接使用本输出",
    "- [ ] 失败/降级说明完整：输入缺口、受影响结论、置信度变化已标注",
    "",
    "## 共享规范引用",
    "",
    "- `fmt/_meta/first-principles-skill-contract.md`",
    "- `fmt/_meta/artifact-handoff-contract.md`",
    "- `fmt/_meta/quality-scorecard.md`",
]


COMMON_CHECKLIST_HEAD = [
    "# 检查清单（Checklist）",
    "",
    "用于在交付本技能输出前做快速复核。建议按顺序勾选；如未满足项导致结论降级，需在输出中显式写明。",
    "",
]


def write_reference_files(skill_dir: Path, meta: dict) -> None:
    ref_dir = skill_dir / "references"
    ref_dir.mkdir(parents=True, exist_ok=True)

    output_template = []
    output_template += [f"# {meta['display']} 输出模板", ""]
    output_template += ["## 使用说明", ""]
    output_template += [f"- 目标：{meta['template_goal']}"]
    output_template += [f"- 主交付工件（Primary Artifact）：`{meta['artifact']}`"]
    output_template += ["- 默认中文输出；专业术语首次出现附英文注释（English Annotation）。", ""]

    output_template += ["## 基本信息（Basic Context）", ""]
    output_template += ["- `task_id`：", "- `skill_name`：", f"- `artifact_name`：`{meta['artifact']}`"]
    output_template += ["- `variant`（`vtol` / `mc` / `fw` / `unknown`）：", "- `scope`（代码路径 / 日志文件 / 时间段）：", "- `version_or_branch`：", ""]

    output_template += ["## 范围与假设（Scope & Assumptions）", ""]
    for item in meta["scope_examples"]:
        output_template += [f"- [ ] {item}"]
    output_template += ["- 事实（Fact）与推断（Inference）边界说明：", ""]

    output_template += ["## 输入摘要（Input Summary）", ""]
    for item in meta["input_examples"]:
        output_template += [f"- [ ] {item}"]
    output_template += ["- 输入缺口（Gaps）：", ""]

    output_template += ["## 工件正文（Artifact Body）", ""]
    for title, prompt in meta["section_prompts"]:
        output_template += [f"### {title}", "", f"- 说明：{prompt}", "- 内容：", ""]

    output_template += ["## 关键事实（Facts）", "", "- Fact-1：", "- Fact-2：", ""]
    output_template += ["## 关键推断（Inferences）", "", "- Inference-1（置信度：高/中/低）：", "- Inference-2（置信度：高/中/低）：", ""]
    output_template += ["## 证据索引（Evidence Index）", ""]
    if meta["domain"] == "code-reading":
        output_template += ["- 代码证据：`path/to/file.c:line` -> 结论", "- 代码证据：`path/to/file.h:line` -> 结论", ""]
    else:
        output_template += ["- 日志证据：`t=[start,end]` + 信号名 -> 结论", "- 日志证据：事件索引/阶段 -> 结论", ""]

    output_template += ["## 缺口与风险（Gaps & Risks）", "", "- 缺口：", "- 风险：", "- 降级策略：", ""]
    output_template += ["## 下游输入建议（Next Skill Inputs）", "", "- 推荐下游技能：", "- 建议关注字段/信号/路径：", "- 需要补充的数据或确认项：", ""]
    output_template += COMMON_TEMPLATE_FOOTER
    (ref_dir / "output-template.md").write_text("\n".join(output_template).rstrip("\n") + "\n", encoding="utf-8")

    checklist = []
    checklist += COMMON_CHECKLIST_HEAD
    checklist += [f"## {meta['display']} 专项检查", ""]
    for item in meta["specific_checks"]:
        checklist += [f"- [ ] {item}"]
    checklist += [""]
    checklist += ["## 输入与范围", ""]
    checklist += [
        "- [ ] 已明确分析范围（代码路径 / 日志文件 / 时间段）",
        "- [ ] 已明确机型变体（或标注 `unknown`）",
        "- [ ] 已列出输入缺口（Gaps）与其影响",
        "",
    ]
    checklist += ["## 证据与结论", ""]
    if meta["domain"] == "code-reading":
        checklist += [
            "- [ ] 关键代码结论均有文件路径 + 行号证据",
            "- [ ] 已区分 Fact 与 Inference",
            "- [ ] 未把接口/外围机制误写为核心算法结论（如适用）",
            "",
        ]
    else:
        checklist += [
            "- [ ] 关键日志结论均有时间段/信号/阶段上下文",
            "- [ ] 已区分现象、证据、候选根因",
            "- [ ] 已标注置信度与待验证项",
            "",
        ]
    checklist += ["## 交接可用性（Artifact Handoff）", ""]
    checklist += [
        f"- [ ] 已明确主交付工件名：`{meta['artifact']}`",
        "- [ ] 工件包含 scope / facts / inferences / evidence index / gaps / next skill inputs",
        "- [ ] 下游技能无需重做本技能即可继续",
        "",
    ]
    checklist += ["## 失败与降级", ""]
    checklist += [
        "- [ ] 输入不足时已采用降级输出，而不是跳步给终局结论",
        "- [ ] 已标注受影响结论和置信度变化",
        "- [ ] 已给出下一步最小补充动作（代码确认 / 补录日志 / 补参数快照 等）",
        "",
    ]
    checklist += ["## 交付前确认", ""]
    checklist += [
        "- [ ] 输出语言为中文，专业术语首次出现附英文注释",
        "- [ ] 参数名/信号名/结构体名/函数名保持原文",
        "- [ ] 结论不超出本技能职责边界",
    ]
    (ref_dir / "checklist.md").write_text("\n".join(checklist).rstrip("\n") + "\n", encoding="utf-8")


def load_skill_md(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    try:
        return raw.decode("gbk").replace("\r\n", "\n"), "gbk"
    except UnicodeDecodeError:
        return raw.decode("utf-8").replace("\r\n", "\n"), "utf-8"


def dump_skill_md(path: Path, text: str, encoding: str) -> None:
    path.write_text(text.rstrip("\n") + "\n", encoding=encoding, newline="\n")


def refresh_reference_usage_section(skill_dir: Path, meta: dict) -> None:
    skill_md = skill_dir / "SKILL.md"
    text, enc = load_skill_md(skill_md)
    lines = text.split("\n")

    # Remove previous "references/ 使用建议" block if present
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## ") and "references/" in line and "使用建议" in line:
            i += 1
            while i < len(lines) and not lines[i].startswith("## "):
                i += 1
            continue
        out.append(line)
        i += 1

    block = [
        "## references/ 使用建议",
        "",
        "1. 快速输出时，先加载 `references/output-template.md` 作为骨架，避免遗漏交接字段。",
        "2. 正式交付前，加载 `references/checklist.md` 做边界、证据、降级策略复核。",
        f"3. 专项提示：{meta['reference_usage']}",
    ]

    headings = [idx for idx, line in enumerate(out) if line.startswith("## ")]
    if not headings:
        return
    insert_at = headings[-1]  # insert before the final discipline section
    out = out[:insert_at] + block + [""] + out[insert_at:]
    dump_skill_md(skill_md, "\n".join(out), enc)


def main() -> None:
    changed = []
    for rel, meta in SKILLS.items():
        skill_dir = ROOT / rel
        write_reference_files(skill_dir, meta)
        refresh_reference_usage_section(skill_dir, meta)
        changed.append(rel)

    print(f"Generated references for {len(changed)} atomic FMT skills.")
    for rel in changed:
        print(rel)


if __name__ == "__main__":
    main()
