#!/usr/bin/env python3
"""
Generate a markdown skeleton for splitting a broad skill into atomic/workflow skills.

This script is intentionally lightweight and deterministic so it can be used as a
repeatable starting point when redesigning skills.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import pathlib
import re
from typing import List


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "skill"


def default_output_path(source_skill: str, out_dir: pathlib.Path | None) -> pathlib.Path:
    stem = f"split-plan-{slugify(source_skill)}.md"
    if out_dir is None:
        return pathlib.Path(stem)
    return out_dir / stem


def capability_rows(capabilities: List[str]) -> str:
    if not capabilities:
        return "| 能力项 | 输入 | 输出 | 前置依赖 | 专业方法 | 风险 |\n|---|---|---|---|---|---|\n| `<待补充>` |  |  |  |  |  |\n"

    rows = ["| 能力项 | 输入 | 输出 | 前置依赖 | 专业方法 | 风险 |", "|---|---|---|---|---|---|"]
    for cap in capabilities:
        rows.append(f"| `{cap}` |  |  |  |  |  |")
    return "\n".join(rows) + "\n"


def atomic_skill_blocks(prefix: str, count: int) -> str:
    blocks: List[str] = []
    for i in range(1, count + 1):
        blocks.append(
            f"""### 原子技能 {i}

- 技能名（建议）：`{prefix}-<object>-<action>`
- 主目标：
- 不负责项：
- 典型输入：
- 典型输出：
- 前置依赖：
- 触发语句示例：
  - “”
  - “”
- 质量判据（Definition of Done）：
"""
        )
    return "\n".join(blocks)


def render_markdown(
    source_skill: str,
    domain: str,
    capabilities: List[str],
    atomic_count: int,
    include_repo_design: bool,
) -> str:
    today = _dt.date.today().isoformat()
    prefix = slugify(domain) if domain else slugify(source_skill)

    repo_section = ""
    if include_repo_design:
        repo_section = f"""
## 7. 仓库组织方案（Repository Taxonomy）

推荐先按用途分层，再按对象命名：

```text
{prefix}/
├─ _meta/
├─ <stage-or-purpose-a>/
├─ <stage-or-purpose-b>/
└─ workflows/
```

- 目录分层建议：
- 命名规则建议：
- 新增 vs 扩展规则：
- 弃用策略（Deprecation）：

## 8. 迁移计划（Migration Plan）

- 原技能保留 / 重构为编排技能 / 弃用：
- 分阶段迁移步骤：
- 向后兼容策略：

## 9. 风险与控制（Risks & Controls）

- 过度拆分风险：
- 能力重叠风险：
- 用户选择成本风险：
- 控制措施：

## 10. 实施清单（Implementation Checklist）

- [ ] 初始化新技能目录
- [ ] 编写原子技能 `SKILL.md`
- [ ] 编写编排技能 `SKILL.md`（如需要）
- [ ] 补齐 `agents/openai.yaml`
- [ ] 补齐 `references/`
- [ ] 更新仓库目录文档
- [ ] 运行校验脚本
"""
    else:
        repo_section = """
## 7. 迁移计划（Migration Plan）

- 原技能保留 / 重构为编排技能 / 弃用：
- 分阶段迁移步骤：
- 向后兼容策略：

## 8. 风险与控制（Risks & Controls）

- 过度拆分风险：
- 能力重叠风险：
- 用户选择成本风险：
- 控制措施：
"""

    return f"""# 技能拆分方案骨架：`{source_skill}`

生成日期：`{today}`

> 本模板用于将单体技能拆分为原子技能（atomic skills）与编排技能（workflow skills）。
> 推荐先阅读 `skill-capability-splitter/references/splitting-heuristics.md` 与 `.../boundary-checklist.md`。

## 1. 第一性原理定义（First-Principles Framing）

先不要讨论目录或命名，先回答：

1. 这个技能的“不可再约简任务单元”是什么？（irreducible unit of work）
2. 输入是什么？输出是什么？完成判据是什么？（input / output / definition of done）
3. 哪些步骤是前置依赖，不能跳过？
4. 哪些步骤方法论不同，应该分开？

- 用户核心目标（Job-to-be-Done）：
- 成功判据（Success Criteria）：
- 失败模式（Failure Modes）：
- 高风险误用场景（Misuse Risks）：

## 2. 拆分结论（Decision Summary）

- 是否建议拆分：是 / 否
- 拆分原因（3-5 条）：
- 预期收益：
  - 触发准确性：
  - 专业性：
  - 可用性：
  - 可维护性：

## 3. 能力清单（Capability Inventory）

{capability_rows(capabilities)}

## 4. 拆分策略（Splitting Strategy）

- 采用拆分轴（阶段轴 / 输入形态轴 / 方法轴 / 触发轴 / 复用轴）：
- 主要拆分依据：
- 不拆分部分与原因：

## 5. 原子技能设计（Atomic Skills）

{atomic_skill_blocks(prefix, atomic_count)}

## 6. 编排技能设计（Workflow Skill, 如需要）

- 是否需要编排技能：是 / 否
- 编排技能名（建议）：`{prefix}-<workflow-action>`
- 适用场景（端到端任务）：
- 编排顺序：
  1.
  2.
  3.
- 不可跳步规则：
- 汇总输出结构：

{repo_section}
"""


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate a skill split plan markdown skeleton.")
    p.add_argument("--source-skill", required=True, help="Original skill name or title to split.")
    p.add_argument("--domain", default="", help="Domain prefix for generated naming suggestions.")
    p.add_argument(
        "--capability",
        action="append",
        default=[],
        help="Seed capability item name. Repeatable.",
    )
    p.add_argument(
        "--atomic-count",
        type=int,
        default=4,
        help="How many atomic skill placeholder blocks to generate (default: 4).",
    )
    p.add_argument(
        "--no-repo-design",
        action="store_true",
        help="Omit repository organization sections.",
    )
    p.add_argument("--out-dir", type=pathlib.Path, help="Output directory for generated markdown.")
    p.add_argument("--output", type=pathlib.Path, help="Explicit output file path.")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if args.atomic_count <= 0:
        raise SystemExit("--atomic-count must be > 0")

    output = args.output or default_output_path(args.source_skill, args.out_dir)
    output.parent.mkdir(parents=True, exist_ok=True)

    md = render_markdown(
        source_skill=args.source_skill,
        domain=args.domain,
        capabilities=args.capability,
        atomic_count=args.atomic_count,
        include_repo_design=not args.no_repo_design,
    )
    output.write_text(md, encoding="utf-8")
    print(f"[OK] Generated split plan skeleton: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
