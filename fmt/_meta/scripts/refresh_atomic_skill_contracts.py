from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


SKILLS = {
    "fmt/code-reading/fmt-control-loop-reader/SKILL.md": {
        "artifact": "control_loop_map",
        "unit": "在单一机型变体与单一任务入口范围内，完成 FMT 控制闭环调度与数据路径（sensor -> INS -> FMS -> Controller -> actuator）的证据化梳理。",
        "inputs": [
            "FMT-Firmware 代码路径（至少可读取 `src/task`、`src/module/sensor`、`src/model/*`）",
            "机型变体信息（`vtol` / `mc` / `fw`），未知时需显式标注 `unknown`",
            "任务入口或目标现象（如用户关注某条控制链路）",
        ],
        "outputs": [
            "主交付工件：`control_loop_map`",
            "控制循环顺序、模块边界、topic/MCN 数据路径、节拍关系与证据索引",
            "供下游使用的关注点（例如需要进一步查看的 FMS 状态字段或接口层 bus）",
        ],
        "dod": [
            "至少一条完整闭环路径被串起来（入口 -> 关键模块 -> 输出）",
            "周期/节拍判断有代码证据，不靠经验猜测",
            "明确当前变体与未确认宏开关/条件分支",
            "区分事实（Fact）与推断（Inference）",
        ],
        "upstream": ["代码工程可读性与变体信息"],
        "downstream": [
            "`fmt-mbd-interface-reader`",
            "`fmt-fms-state-machine-reader`",
            "`fmt-tuning-report-writer`",
            "`fmt-flight-control-param-optimizer`",
        ],
        "quality_extra": "时序门禁：凡是周期/节拍结论，必须指出触发条件或定时器/循环位置。",
        "fallback": [
            "变体未知时：允许输出“通用路径 + 变体差异待确认点”，但不下具体变体结论",
            "入口函数不明确时：先列候选入口并给出确认方法（任务注册/启动路径）",
        ],
    },
    "fmt/code-reading/fmt-mbd-interface-reader/SKILL.md": {
        "artifact": "mbd_boundary_map",
        "unit": "在单一控制律模块（INS/FMS/Controller 的某一变体目录）内，完成接口桥接层与 MBD 生成代码层的职责划分与数据映射梳理。",
        "inputs": [
            "目标模块目录（如 `src/model/fms/vtol_fms/`）",
            "`*_interface.c` 与 `lib/` 生成代码文件可读",
            "变体信息与任务关注点（参数绑定、bus 映射或模型入口）",
        ],
        "outputs": [
            "主交付工件：`mbd_boundary_map`",
            "接口层 vs 生成代码层职责对照、topic/bus 映射、参数绑定路径、模型 `init/step` 调用链",
            "需要进入生成代码进一步确认的隐藏复杂度清单",
        ],
        "dod": [
            "接口层与生成代码层边界已明确，未混淆 glue code 与控制律本体",
            "至少一条参数绑定路径和一条 bus/topic 映射路径可回链到代码",
            "对生成代码内部未验证部分显式标注为待确认项",
        ],
        "upstream": ["`fmt-control-loop-reader`（推荐）或用户指定的目标模块路径"],
        "downstream": [
            "`fmt-fms-state-machine-reader`",
            "`fmt-control-performance-analyzer`",
            "`fmt-tuning-report-writer`",
            "`fmt-flight-control-param-optimizer`",
        ],
        "quality_extra": "边界门禁：不把 `*_interface.c` 中的适配逻辑写成“控制律算法结论”。",
        "fallback": [
            "若生成代码文件过大：先输出文件角色地图（`*_types.h`/`*_data.c`/入口函数）再逐步下钻",
            "若模块变体未确认：并列列出候选目录差异，不混合字段语义",
        ],
    },
    "fmt/code-reading/fmt-fms-state-machine-reader/SKILL.md": {
        "artifact": "fms_state_semantics",
        "unit": "在单一 FMS 变体范围内，完成状态机（State Machine）状态集合、切换条件、输出语义与日志可观测字段的证据化说明。",
        "inputs": [
            "目标 FMS 变体目录（如 `vtol_fms`）",
            "`fms_interface.c` 与生成代码（`FMS.c`/`FMS_types.h` 等）可读",
            "用户关注的模式/状态问题（过渡段、自动模式、故障回退等，可选）",
        ],
        "outputs": [
            "主交付工件：`fms_state_semantics`",
            "状态/模式语义表、触发源清单、关键转换路径与输出影响",
            "供日志分段使用的字段建议与注意事项",
        ],
        "dod": [
            "至少覆盖一组关键状态转换链（触发条件 -> 状态变化 -> 输出变化）",
            "接口层字符串映射与生成代码真实切换逻辑已区分",
            "明确当前机型变体及 VTOL 特有字段适用性",
        ],
        "upstream": ["`fmt-mbd-interface-reader`（推荐）或已确认的 FMS 变体目录"],
        "downstream": [
            "`fmt-flight-log-segmenter`",
            "`fmt-control-performance-analyzer`",
            "`fmt-tuning-report-writer`",
            "`fmt-flight-control-param-optimizer`",
        ],
        "quality_extra": "语义门禁：状态字段含义必须以代码定义为准，不用日志现象反推替代代码证据。",
        "fallback": [
            "若生成代码状态逻辑难以快速确认：先交付接口层语义与疑难状态清单，标注低置信度区域",
            "若跨变体问题：拆成多个变体对照，不写统一规则",
        ],
    },
    "fmt/code-reading/fmt-logging-pipeline-reader/SKILL.md": {
        "artifact": "logging_pipeline_map",
        "unit": "在 FMT 嵌入式日志系统范围内，完成 `mlog/ulog` 触发、记录、缓冲、刷盘与使用路径的机制级梳理，不进入日志内容解码。",
        "inputs": [
            "`task_logger`、`mlog`、`ulog`、状态任务与命令入口相关源码可读",
            "目标日志类型（`mlog` / `ulog` / 两者）与关注点（可靠性、启停、刷盘时机）",
        ],
        "outputs": [
            "主交付工件：`logging_pipeline_map`",
            "日志链路时序、自动/手动启停规则、缓冲与刷盘机制、可靠性风险点",
            "供 `fmt-mlog-decoder` 使用的格式与链路线索（来源文件/结构体/状态）",
        ],
        "dod": [
            "已区分日志记录机制问题与日志内容语义问题",
            "至少串起一条 `mlog` 生命周期路径和一条触发路径（自动或手动）",
            "风险点结论对应具体代码路径或状态条件",
        ],
        "upstream": ["代码工程可读性（日志相关模块）"],
        "downstream": [
            "`fmt-mlog-decoder`",
            "`fmt-tuning-report-writer`",
            "`fmt-flight-control-param-optimizer`",
        ],
        "quality_extra": "可靠性门禁：所有“丢日志/刷盘风险”判断必须给出触发条件与代码证据。",
        "fallback": [
            "若仅能读取部分日志模块：先输出已确认链路与缺失模块造成的盲区",
            "若 `ulog` 未启用：明确标注为编译配置/运行配置差异，不当作缺陷",
        ],
    },
    "fmt/log-analysis/fmt-mlog-decoder/SKILL.md": {
        "artifact": "mlog_decode_summary",
        "unit": "在单个或一组 `mlog` 二进制文件范围内，完成 header/schema/record 的结构化解码与完整性评估，不输出控制性能结论。",
        "inputs": [
            "`mlog*.bin` 文件（或二进制流）",
            "对应版本的 FMT `mlog` 格式线索（代码或已知版本信息）",
            "目标导出格式需求（表格/CSV/Parquet-ready，可选）",
        ],
        "outputs": [
            "主交付工件：`mlog_decode_summary`（含解码摘要、schema、完整性）",
            "结构化数据引用（或字段清单/导出路径说明）",
            "下游分段与性能分析需要的关键信号可用性清单",
        ],
        "dod": [
            "先完成 schema 解析再进入 records 解码",
            "明确解码成功率、损坏/截断范围与恢复范围",
            "字段名、类型、时间戳来源可说明且可复现",
        ],
        "upstream": ["`fmt-logging-pipeline-reader`（推荐，用于格式线索）或等效源码线索"],
        "downstream": [
            "`fmt-flight-log-segmenter`",
            "`fmt-control-performance-analyzer`",
            "`fmt-tuning-report-writer`",
            "`fmt-flight-control-param-optimizer`",
        ],
        "quality_extra": "格式门禁：未知 schema 时禁止靠固定 payload 长度硬编码解码。",
        "fallback": [
            "日志损坏时：输出可恢复时间段与不可恢复段，不跨到性能结论",
            "版本不匹配时：先做版本差异记录，必要时停止并请求对应源码/版本信息",
        ],
    },
    "fmt/log-analysis/fmt-flight-log-segmenter/SKILL.md": {
        "artifact": "flight_phase_segments",
        "unit": "在已解码的单次飞行日志时间轴上，完成飞行阶段分段与关键事件索引，并给出可复现的分段规则。",
        "inputs": [
            "已解码结构化日志数据（至少包含时间轴与核心状态/控制信号）",
            "机型变体信息（`vtol` / `mc` / `fw`）",
            "可选 `ulog` 事件文本或任务背景说明",
        ],
        "outputs": [
            "主交付工件：`flight_phase_segments`",
            "阶段时间轴、关键事件索引、分段依据与质量问题列表",
            "供性能分析使用的推荐观察窗口与注意事项",
        ],
        "dod": [
            "分段规则可复现（字段、阈值、条件清楚）",
            "VTOL 过渡段与非 VTOL 规则不混写",
            "边界模糊和缺数据段被显式标注",
        ],
        "upstream": [
            "`fmt-mlog-decoder` 或等效结构化日志输入",
            "`fmt-fms-state-machine-reader`（推荐，用于状态语义）",
        ],
        "downstream": [
            "`fmt-control-performance-analyzer`",
            "`fmt-tuning-report-writer`",
            "`fmt-flight-control-param-optimizer`",
        ],
        "quality_extra": "分段门禁：每个关键阶段边界必须对应证据信号或状态字段变化。",
        "fallback": [
            "缺失 `FMS_Out` 时：可用 `INS_Out` + 执行器信号做近似分段，但必须降级置信度",
            "时间轴不连续时：分段结果按连续片段分别输出，不给全局连续结论",
        ],
    },
    "fmt/log-analysis/fmt-control-performance-analyzer/SKILL.md": {
        "artifact": "control_performance_findings",
        "unit": "在已完成解码与分段的单次飞行日志范围内，对控制表现进行分层（INS/FMS/Controller/Actuator）分析，形成证据化现象与候选根因。",
        "inputs": [
            "已解码结构化日志数据",
            "飞行阶段分段与关键事件索引",
            "机型变体与参数快照（缺失时需显式降级）",
        ],
        "outputs": [
            "主交付工件：`control_performance_findings`",
            "现象清单、证据链、候选根因分层、候选参数方向（directional only）",
            "下游报告撰写所需的优先级、置信度与待验证项",
        ],
        "dod": [
            "至少形成一条“现象 -> 证据 -> 候选根因”链条",
            "区分状态机切换瞬态与控制器性能问题",
            "在缺失参数快照时不输出具体参数值修改量",
        ],
        "upstream": [
            "`fmt-mlog-decoder`",
            "`fmt-flight-log-segmenter`",
            "`fmt-fms-state-machine-reader`（推荐）",
        ],
        "downstream": [
            "`fmt-tuning-report-writer`",
            "`fmt-flight-control-param-optimizer`",
        ],
        "quality_extra": "归因门禁：没有分段或模式上下文时，不给全局控制器增益归因结论。",
        "fallback": [
            "缺失参数快照：只给方向级候选参数组与验证建议",
            "关键信号缺失：先给数据缺口导致的分析盲区，再输出可确认的局部现象",
        ],
    },
    "fmt/log-analysis/fmt-tuning-report-writer/SKILL.md": {
        "artifact": "tuning_recommendation_report",
        "unit": "在已有代码理解与日志分析证据基础上，输出可执行、可验证、可追踪的参数优化报告与试飞验证计划，不新增分析证据。",
        "inputs": [
            "代码理解工件（至少控制结构与日志链路）",
            "日志分析工件（现象、证据、候选根因）",
            "参数快照/当前参数列表与任务目标",
        ],
        "outputs": [
            "主交付工件：`tuning_recommendation_report`",
            "结构化报告、参数建议条目、风险与副作用、Test Card",
            "未闭环问题与待补数据清单",
        ],
        "dod": [
            "每条建议都有证据回链、风险与验证指标",
            "候选根因与确定性结论被明确区分",
            "缺失证据时输出缺口与补试建议，而非凑结论",
        ],
        "upstream": [
            "代码阅读类工件（至少一项）",
            "`control_performance_findings`（推荐）",
        ],
        "downstream": ["`fmt-flight-control-param-optimizer` 或最终交付给飞控工程师"],
        "quality_extra": "可执行性门禁：每条调参建议必须包含验证指标与通过条件。",
        "fallback": [
            "证据不足时：输出“调参前置条件未满足”报告，而不是给具体参数改值",
            "参数快照缺失时：明确建议补采/导出参数快照并限制建议粒度",
        ],
    },
}


COMMON_LANG = [
    "默认中文输出；专业术语首次出现附英文注释（English Annotation）。",
    "保留参数名、信号名、结构体名、函数名原文，避免翻译造成歧义。",
]

COMMON_GATES = [
    "边界门禁（Boundary Purity）：不输出超出本技能职责的确定性结论。",
    "证据门禁（Evidence Traceability）：关键结论必须能回链到代码路径行号或日志时间段。",
    "变体门禁（Variant Scope）：明确 `vtol/mc/fw` 适用范围，未知时标注 `unknown`。",
    "交接门禁（Handoff Usability）：输出可被下游技能直接消费，不只给散文式描述。",
]


def build_first_block(meta: dict) -> list[str]:
    lines: list[str] = []
    lines += ["## 第一性原理任务定义（First-Principles Task Definition）", ""]
    lines += ["1. 最小任务单元（Minimum Task Unit）", f"   - {meta['unit']}"]
    lines += ["2. 核心输入（Inputs）"] + [f"   - {x}" for x in meta["inputs"]]
    lines += ["3. 核心输出（Outputs）"] + [f"   - {x}" for x in meta["outputs"]]
    lines += ["4. 完成判据（Definition of Done, DoD）"] + [f"   - {x}" for x in meta["dod"]]
    lines += ["5. 输出语言约定（Language Convention）"] + [f"   - {x}" for x in COMMON_LANG]
    return lines


def build_handoff_block(meta: dict) -> list[str]:
    lines: list[str] = []
    lines += ["## 上下游交接（Artifact Handoff）", ""]
    lines += ["1. 上游依赖（Upstream Dependencies）"] + [f"   - {x}" for x in meta["upstream"]]
    lines += ["2. 下游使用方（Downstream Consumers）"] + [f"   - {x}" for x in meta["downstream"]]
    lines += ["3. 主交付工件（Primary Artifact）", f"   - `{meta['artifact']}`"]
    lines += [
        "   - 工件至少包含：分析范围（scope）、关键事实（facts）、关键推断（inferences）、证据索引（evidence index）、缺口清单（gaps）、下游输入建议（next skill inputs）。"
    ]
    lines += [
        "4. 共享规范（Shared Contracts）",
        "   - 参考 `fmt/_meta/first-principles-skill-contract.md`",
        "   - 参考 `fmt/_meta/artifact-handoff-contract.md`",
        "",
    ]
    lines += ["## 质量门禁（Quality Gates）", ""]
    lines += ["1. 必过门禁（Mandatory Gates）"] + [f"   - {x}" for x in (COMMON_GATES + [meta["quality_extra"]])]
    lines += [
        "2. 自检建议（Self Check）",
        "   - 可使用 `fmt/_meta/quality-scorecard.md` 对本次输出进行快速打分（至少检查 IO 契约、证据、降级策略）。",
        "",
    ]
    lines += ["## 失败与降级策略（Failure / Fallback）", ""]
    lines += ["1. 输入不足处理"] + [f"   - {x}" for x in meta["fallback"]]
    lines += [
        "2. 输出降级要求",
        "   - 降级输出时必须显式标注受影响结论、受影响范围与置信度变化。",
        "   - 降级不等于跳步；不得越过本技能职责直接给下游最终结论。",
    ]
    return lines


def remove_inserted_contract_blocks(lines: list[str]) -> list[str]:
    keywords = (
        "First-Principles Task Definition",
        "Artifact Handoff",
        "Quality Gates",
        "Failure / Fallback",
    )
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## ") and any(k in line for k in keywords):
            i += 1
            while i < len(lines) and not lines[i].startswith("## "):
                i += 1
            continue
        out.append(line)
        i += 1
    return out


def insert_before_nth_heading(lines: list[str], heading_ordinal: int, block: list[str]) -> list[str]:
    heading_indices = [i for i, line in enumerate(lines) if line.startswith("## ")]
    if len(heading_indices) <= heading_ordinal:
        raise RuntimeError(f"Not enough headings to insert at ordinal {heading_ordinal}")
    insert_at = heading_indices[heading_ordinal]
    return lines[:insert_at] + block + [""] + lines[insert_at:]


def insert_before_last_heading(lines: list[str], block: list[str]) -> list[str]:
    heading_indices = [i for i, line in enumerate(lines) if line.startswith("## ")]
    if not heading_indices:
        raise RuntimeError("No headings found")
    insert_at = heading_indices[-1]
    return lines[:insert_at] + block + [""] + lines[insert_at:]


def main() -> None:
    changed = []
    for rel, meta in SKILLS.items():
        path = ROOT / rel
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="gbk")
        text = text.replace("\r\n", "\n")
        lines = text.split("\n")

        # Remove previously inserted contract blocks (including mojibake variants).
        cleaned = remove_inserted_contract_blocks(lines)

        # Insert fresh UTF-8 blocks.
        cleaned = insert_before_nth_heading(cleaned, 1, build_first_block(meta))
        cleaned = insert_before_last_heading(cleaned, build_handoff_block(meta))

        new_text = "\n".join(cleaned).rstrip("\n") + "\n"
        if new_text != text:
            # Keep SKILL.md compatible with the local validator, which uses locale default encoding on Windows.
            path.write_text(new_text, encoding="gbk", newline="\n")
            changed.append(rel)

    print(f"Refreshed {len(changed)} atomic FMT skills.")
    for rel in changed:
        print(rel)


if __name__ == "__main__":
    main()
