#!/usr/bin/env python3
"""One-time harvest of style usage data from existing _style_fix worktrees.

Parses EVALUATION.md files to extract style file references and Fix Summary
statuses, then writes JSONL entries to log.jsonl.
"""

from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime
from datetime import timezone
from pathlib import Path
from typing import TypedDict


class _FindingEntryRequired(TypedDict):
    finding: int
    status: str


class FindingEntry(_FindingEntryRequired, total=False):
    reason: str


class LogEntry(TypedDict):
    timestamp: str
    style_id: str
    style_file: str
    local: bool
    project: str
    base_branch: str
    findings: list[FindingEntry]


RUST_DIR = Path.home() / "rust"
NATE_STYLE_DIR = RUST_DIR / "nate_style"
LOG_FILE = NATE_STYLE_DIR / "usage" / "log.jsonl"

# Patterns for parsing EVALUATION.md
STYLE_FILE_RE = re.compile(r"\*\*Style file\*\*:\s*`?([^`\n]+)`?")
FINDING_HEADER_RE = re.compile(r"^### (\d+)\.\s+(.+)$")
FIX_FINDING_RE = re.compile(r"^### Finding (\d+):")
FIX_STATUS_RE = re.compile(r"^\*\*Status:\*\*\s*(.+)$")
FIX_ISSUES_RE = re.compile(r"^\*\*Issues:\*\*\s*(.+)$")


def get_current_branch(project_dir: Path) -> str:
    """Get the current branch of a project directory."""
    result = subprocess.run(
        ["git", "-C", str(project_dir), "branch", "--show-current"],
        capture_output=True,
        text=True,
    )
    branch = result.stdout.strip()
    return branch if branch else "main"


def normalize_style_path(raw_path: str) -> tuple[str, str, bool]:
    """Normalize a style file path to (style_id, style_file, local).

    Returns (style_id, display_name, is_local).
    """
    raw_path = raw_path.strip().rstrip("/")
    # Expand ~ to home
    if raw_path.startswith("~"):
        raw_path = str(Path(raw_path).expanduser())

    nate_style_str = str(NATE_STYLE_DIR)
    basename = Path(raw_path).name

    if nate_style_str in raw_path:
        # Shared style — extract path relative to nate_style dir
        idx = raw_path.index(nate_style_str) + len(nate_style_str) + 1
        relative = raw_path[idx:]
        return f"shared:{relative}", basename, False

    if "docs/style/" in raw_path:
        return f"local:unknown:{basename}", basename, True

    # Fallback: treat as shared with just the basename
    return f"shared:rust/{basename}", basename, False


def parse_evaluation(content: str) -> tuple[dict[int, str], dict[int, tuple[str, str]]]:
    """Parse EVALUATION.md content.

    Returns:
        findings_styles: {finding_number: style_file_path}
        fix_statuses: {finding_number: (status, reason)}
    """
    findings_styles: dict[int, str] = {}
    fix_statuses: dict[int, tuple[str, str]] = {}

    lines = content.splitlines()
    current_finding: int | None = None
    in_fix_summary = False
    current_fix_finding: int | None = None

    for line in lines:
        # Track finding numbers in the Improvements section
        finding_match = FINDING_HEADER_RE.match(line)
        if finding_match and not in_fix_summary:
            current_finding = int(finding_match.group(1))
            continue

        # Track style file references
        style_match = STYLE_FILE_RE.search(line)
        if style_match and current_finding is not None and not in_fix_summary:
            findings_styles[current_finding] = style_match.group(1)
            continue

        # Detect Fix Summary section
        if line.strip() == "## Fix Summary":
            in_fix_summary = True
            continue

        if in_fix_summary:
            fix_match = FIX_FINDING_RE.match(line)
            if fix_match:
                current_fix_finding = int(fix_match.group(1))
                continue

            status_match = FIX_STATUS_RE.match(line)
            if status_match and current_fix_finding is not None:
                raw_status = status_match.group(1).strip()
                fix_statuses[current_fix_finding] = (raw_status, "")
                continue

            issues_match = FIX_ISSUES_RE.match(line)
            if issues_match and current_fix_finding is not None:
                reason = issues_match.group(1).strip()
                if current_fix_finding in fix_statuses:
                    status = fix_statuses[current_fix_finding][0]
                    fix_statuses[current_fix_finding] = (status, reason)
                continue

    return findings_styles, fix_statuses


def normalize_status(raw_status: str) -> str:
    """Normalize Fix Summary status to schema values."""
    lower = raw_status.lower().strip()
    if lower.startswith("partially"):
        return "partial"
    if lower.startswith("applied"):
        return "applied"
    if lower.startswith("skipped"):
        return "skipped"
    return "applied"


def harvest_worktree(worktree_dir: Path) -> list[LogEntry]:
    """Harvest style usage data from a single worktree."""
    eval_file = worktree_dir / "EVALUATION.md"
    if not eval_file.exists():
        print(f"  SKIP: no EVALUATION.md")
        return []

    content = eval_file.read_text()
    findings_styles, fix_statuses = parse_evaluation(content)

    if not findings_styles:
        print(f"  SKIP: no style file references found")
        return []

    if not fix_statuses:
        print(f"  SKIP: no Fix Summary found")
        return []

    # Derive project name
    worktree_name = worktree_dir.name
    project = worktree_name.removesuffix("_style_fix")

    # Get base branch from the main project
    project_dir = RUST_DIR / project
    if project_dir.exists():
        base_branch = get_current_branch(project_dir)
    else:
        base_branch = "main"

    # Use EVALUATION.md mtime as timestamp
    mtime = eval_file.stat().st_mtime
    timestamp = datetime.fromtimestamp(mtime, tz=timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )

    # Group findings by style file
    style_findings: dict[str, list[FindingEntry]] = {}
    for finding_num, style_path in findings_styles.items():
        style_id, style_file, is_local = normalize_style_path(style_path)

        if style_id not in style_findings:
            style_findings[style_id] = []

        entry: FindingEntry = {"finding": finding_num, "status": "applied"}
        if finding_num in fix_statuses:
            raw_status, reason = fix_statuses[finding_num]
            entry["status"] = normalize_status(raw_status)
            if reason:
                entry["reason"] = reason

        style_findings[style_id].append(entry)

    # Build log entries
    entries: list[LogEntry] = []
    for style_id, findings in style_findings.items():
        # Re-derive style_file and local from style_id
        if style_id.startswith("local:"):
            parts = style_id.split(":", 2)
            style_file = parts[2] if len(parts) > 2 else style_id
            is_local = True
        else:
            # shared:rust/foo.md -> foo.md
            relative = style_id.removeprefix("shared:")
            style_file = Path(relative).name
            is_local = False

        log_entry: LogEntry = {
            "timestamp": timestamp,
            "style_id": style_id,
            "style_file": style_file,
            "local": is_local,
            "project": project,
            "base_branch": base_branch,
            "findings": findings,
        }
        entries.append(log_entry)

    return entries


def main() -> None:
    all_entries: list[LogEntry] = []

    # Find all _style_fix worktrees
    worktrees = sorted(RUST_DIR.glob("*_style_fix"))
    if not worktrees:
        print("No _style_fix worktrees found.")
        return

    print(f"Found {len(worktrees)} style_fix worktrees\n")

    for worktree_dir in worktrees:
        name = worktree_dir.name
        print(f"Processing {name}...")
        entries = harvest_worktree(worktree_dir)
        if entries:
            applied = sum(
                1
                for e in entries
                for f in e["findings"]
                if f["status"] == "applied"
            )
            total = sum(len(e["findings"]) for e in entries)
            print(
                f"  OK: {len(entries)} style(s), {total} finding(s) ({applied} applied)"
            )
            all_entries.extend(entries)
        print()

    if not all_entries:
        print("No data harvested.")
        return

    # Validate and write
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with open(LOG_FILE, "a") as f:
        for entry in all_entries:
            line = json.dumps(entry, separators=(",", ":"))
            # Self-validate
            try:
                json.loads(line)
            except json.JSONDecodeError:
                print(f"WARN: skipping malformed entry for {entry.get('project', '?')}")
                continue
            _ = f.write(line + "\n")
            written += 1

    print(f"Wrote {written} entries to {LOG_FILE}")


if __name__ == "__main__":
    main()
