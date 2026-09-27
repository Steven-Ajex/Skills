#!/usr/bin/env python3
"""
Collect an objective repository state snapshot for writing a handoff prompt.

The output is Markdown (Chinese headings) intended for the "当前状态快照"
section of a handoff prompt. The script is read-only: it never modifies the
repository, the index, or any ref.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import pathlib
import re
import subprocess
import sys
from typing import List, Optional, Tuple

# Files whose presence hints at how to build/test the project.
PROJECT_MARKERS = [
    "package.json",
    "pnpm-workspace.yaml",
    "pyproject.toml",
    "requirements.txt",
    "setup.py",
    "go.mod",
    "Cargo.toml",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "CMakeLists.txt",
    "Makefile",
    "Dockerfile",
    "docker-compose.yml",
    "compose.yaml",
]

# Project-level rule files: a handoff prompt should reference them, not repeat them.
RULE_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    ".cursorrules",
    ".github/copilot-instructions.md",
    "CONTRIBUTING.md",
]

# Existing handoff files from earlier sessions (handoff chain).
HANDOFF_FILES = ["HANDOFF.md", "docs/handoff/HANDOFF.md"]

TODO_PATTERN = re.compile(r"\b(TODO|FIXME|XXX|HACK)\b")
HUNK_PATTERN = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")
CONFLICT_CODES = {"DD", "AU", "UD", "UA", "DU", "AA", "UU"}


def run_git(repo: pathlib.Path, *args: str) -> Tuple[int, str]:
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError:
        return 127, ""
    return proc.returncode, proc.stdout.rstrip("\n")


def git_out(repo: pathlib.Path, *args: str) -> Optional[str]:
    code, out = run_git(repo, *args)
    return out if code == 0 else None


def code_block(text: str) -> str:
    return f"```text\n{text}\n```"


def truncate(lines: List[str], limit: int) -> List[str]:
    if len(lines) <= limit:
        return lines
    return lines[:limit] + [f"... 另有 {len(lines) - limit} 项未列出（用 --max-files 调整）"]


def parse_status(porcelain: str) -> dict:
    result = {"staged": [], "unstaged": [], "untracked": [], "conflicted": []}
    for line in porcelain.splitlines():
        if len(line) < 4:
            continue
        xy, path = line[:2], line[3:]
        if xy == "??":
            result["untracked"].append(path)
        elif xy in CONFLICT_CODES:
            result["conflicted"].append(path)
        else:
            if xy[0] not in " ?":
                result["staged"].append(f"{xy[0]} {path}")
            if xy[1] not in " ?":
                result["unstaged"].append(f"{xy[1]} {path}")
    return result


def added_todos(diff_text: str) -> List[str]:
    """Return `path:line: text` for TODO-like markers on added lines of a -U0 diff."""
    found: List[str] = []
    current_file: Optional[str] = None
    new_line = 0
    for line in diff_text.splitlines():
        if line.startswith("+++ "):
            target = line[4:]
            current_file = None if target == "/dev/null" else re.sub(r"^b/", "", target)
            continue
        if line.startswith("--- "):
            continue
        hunk = HUNK_PATTERN.match(line)
        if hunk:
            new_line = int(hunk.group(1))
            continue
        if line.startswith("+"):
            if current_file and TODO_PATTERN.search(line):
                found.append(f"{current_file}:{new_line}: {line[1:].strip()}")
            new_line += 1
    return found


def section_basics(repo: pathlib.Path) -> Tuple[str, List[str]]:
    warnings: List[str] = []
    branch = git_out(repo, "branch", "--show-current") or "(detached HEAD)"
    head = git_out(repo, "log", "-1", "--date=short", "--format=%h %ad %s")
    lines = [
        "## 基本信息",
        "",
        f"- 仓库根目录：`{repo}`",
        f"- 当前分支：`{branch}`",
        f"- HEAD：`{head}`" if head else "- HEAD：（尚无提交）",
    ]

    upstream = git_out(repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    if upstream:
        counts = git_out(repo, "rev-list", "--left-right", "--count", f"{upstream}...HEAD")
        if counts and len(counts.split()) == 2:
            behind, ahead = counts.split()
            lines.append(f"- 上游分支：`{upstream}`（本地领先 {ahead} 个提交，落后 {behind} 个提交）")
            if ahead != "0":
                warnings.append(f"有 {ahead} 个提交尚未推送到 `{upstream}`：在其他机器/环境接手时将看不到这些提交。")
        else:
            lines.append(f"- 上游分支：`{upstream}`")
    elif branch != "(detached HEAD)":
        lines.append("- 上游分支：未设置")
        warnings.append("当前分支没有上游分支（可能从未推送）：在其他机器/环境接手时无法获取。")

    return "\n".join(lines), warnings


def section_worktree(repo: pathlib.Path, max_files: int) -> Tuple[str, List[str]]:
    warnings: List[str] = []
    porcelain = git_out(repo, "status", "--porcelain=v1") or ""
    status = parse_status(porcelain)
    lines = ["## 工作区状态", ""]

    if not any(status.values()):
        lines.append("- 工作区干净（无未提交改动、无未跟踪文件）")
        return "\n".join(lines), warnings

    labels = [
        ("conflicted", "合并冲突"),
        ("staged", "已暂存"),
        ("unstaged", "未暂存"),
        ("untracked", "未跟踪"),
    ]
    for key, label in labels:
        items = status[key]
        if not items:
            continue
        lines.append(f"- {label}（{len(items)}）：")
        lines.extend(f"  - `{item}`" for item in truncate(items, max_files))

    diff_stat = git_out(repo, "diff", "--stat", "HEAD")
    if diff_stat:
        lines += ["", "未提交改动统计（相对 HEAD，含已暂存与未暂存）：", "", code_block(diff_stat)]

    if status["conflicted"]:
        warnings.append("存在未解决的合并冲突：交接前应解决，或在交接提示词中写明冲突文件与处理思路。")
    warnings.append(
        "存在未提交改动：若新会话在另一台机器或临时/云端环境中进行，这些改动会丢失。"
        "建议征得用户同意后提交 WIP 并推送，或在交接提示词中逐个列出这些文件及其完成度。"
    )
    return "\n".join(lines), warnings


def section_base(repo: pathlib.Path, base: str, log_count: int) -> str:
    lines = [f"## 相对基线 `{base}` 的改动", ""]
    merge_base = git_out(repo, "merge-base", base, "HEAD")
    if not merge_base:
        lines.append(f"- 无法计算与 `{base}` 的共同祖先（分支名是否正确？是否已 fetch？）")
        return "\n".join(lines)

    commits = git_out(repo, "log", "--oneline", f"-n{log_count * 3}", f"{base}..HEAD") or ""
    commit_lines = commits.splitlines()
    lines.append(f"- 共同祖先：`{merge_base[:10]}`")
    lines.append(f"- 本分支新增提交：{len(commit_lines)}")
    if commit_lines:
        lines += ["", code_block(commits)]
    stat = git_out(repo, "diff", "--stat", f"{base}...HEAD")
    if stat:
        lines += ["", "已提交改动统计：", "", code_block(stat)]
    return "\n".join(lines)


def section_recent(repo: pathlib.Path, log_count: int) -> str:
    log = git_out(repo, "log", f"-n{log_count}", "--date=short", "--format=%h %ad %s")
    lines = ["## 最近提交", ""]
    lines.append(code_block(log) if log else "- （尚无提交）")
    return "\n".join(lines)


def section_stash(repo: pathlib.Path) -> Tuple[Optional[str], List[str]]:
    stash = git_out(repo, "stash", "list")
    if not stash:
        return None, []
    count = len(stash.splitlines())
    body = "\n".join(["## Stash", "", code_block(stash)])
    return body, [f"有 {count} 条 stash：确认其中是否有与当前任务相关、需要在交接中说明的改动。"]


def section_todos(repo: pathlib.Path, base: Optional[str], max_files: int) -> Optional[str]:
    diffs = [git_out(repo, "diff", "-U0", "HEAD") or ""]
    if base and git_out(repo, "merge-base", base, "HEAD"):
        diffs.append(git_out(repo, "diff", "-U0", f"{base}...HEAD") or "")
    todos: List[str] = []
    for diff_text in diffs:
        for item in added_todos(diff_text):
            if item not in todos:
                todos.append(item)
    if not todos:
        return None
    scope = f"未提交改动与相对 `{base}` 的改动" if base else "未提交改动"
    lines = [f"## 新增的 TODO / FIXME（{scope}中新增的行）", ""]
    lines.extend(f"- `{item}`" for item in truncate(todos, max_files))
    return "\n".join(lines)


def section_project_files(repo: pathlib.Path) -> Optional[str]:
    markers = [name for name in PROJECT_MARKERS if (repo / name).exists()]
    rules = [name for name in RULE_FILES if (repo / name).exists()]
    handoffs = [name for name in HANDOFF_FILES if (repo / name).exists()]
    if not (markers or rules or handoffs):
        return None
    lines = ["## 项目文件线索", ""]
    if markers:
        lines.append("- 构建/依赖标识文件（据此写出构建与测试命令）：" + "、".join(f"`{m}`" for m in markers))
    if rules:
        lines.append("- 项目规则文件（交接提示词引用即可，不要重复其内容）：" + "、".join(f"`{r}`" for r in rules))
    if handoffs:
        lines.append(
            "- 已存在的交接文件（交接链）：" + "、".join(f"`{h}`" for h in handoffs)
            + "；更新它而不是新建，并重新核实其中的状态声明"
        )
    return "\n".join(lines)


def build_report(repo: pathlib.Path, base: Optional[str], log_count: int, max_files: int, todos: bool) -> str:
    now = _dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    sections: List[str] = [f"# 交接状态快照（采集于 {now}）"]
    warnings: List[str] = []

    basics, warn = section_basics(repo)
    sections.append(basics)
    warnings += warn

    worktree, warn = section_worktree(repo, max_files)
    sections.append(worktree)
    warnings += warn

    if base:
        sections.append(section_base(repo, base, log_count))

    sections.append(section_recent(repo, log_count))

    stash, warn = section_stash(repo)
    if stash:
        sections.append(stash)
    warnings += warn

    if todos:
        todo_section = section_todos(repo, base, max_files)
        if todo_section:
            sections.append(todo_section)

    project = section_project_files(repo)
    if project:
        sections.append(project)

    reminder = ["## 交接前提醒", ""]
    reminder.extend(f"- ⚠ {w}" for w in warnings)
    reminder.append("- 本快照只覆盖 git 可见状态；构建/测试结果、数据库迁移、运行中的服务、环境变量（只写名称）需另行补充。")
    sections.append("\n".join(reminder))

    return "\n\n".join(sections) + "\n"


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect a read-only git state snapshot (Markdown) for writing a handoff prompt."
    )
    parser.add_argument("--repo", default=".", help="Path inside the target git repository (default: .)")
    parser.add_argument("--base", help="Base branch to compare against, e.g. main or origin/main")
    parser.add_argument("--log-count", type=int, default=10, help="Number of recent commits to show (default: 10)")
    parser.add_argument("--max-files", type=int, default=40, help="Max entries per file list (default: 40)")
    parser.add_argument("--no-todos", action="store_true", help="Skip scanning added lines for TODO/FIXME markers")
    parser.add_argument("--output", help="Write the snapshot to this file instead of stdout")
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    start = pathlib.Path(args.repo).resolve()
    code, top = run_git(start, "rev-parse", "--show-toplevel")
    if code == 127:
        print("error: git is not installed or not on PATH", file=sys.stderr)
        return 2
    if code != 0 or not top:
        print(f"error: {start} is not inside a git repository", file=sys.stderr)
        return 2

    report = build_report(pathlib.Path(top), args.base, args.log_count, args.max_files, not args.no_todos)

    if args.output:
        out = pathlib.Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
        print(f"wrote {out}")
    else:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
