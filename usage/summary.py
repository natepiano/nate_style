#!/usr/bin/env python3
"""Style guide usage summary.

Reads log.jsonl and outputs usage analytics with trend detection.

Usage:
    python3 summary.py [--since 30d] [--project foo] [--local] [--skips] [--style foo.md]
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from pathlib import Path
from typing import TypedDict
from typing import cast


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


class FailureEntry(TypedDict):
    timestamp: str
    project: str
    base_branch: str
    status: str  # "error"
    reason: str


class StyleStats(TypedDict):
    style_id: str
    style_file: str
    local: bool
    projects: set[str]
    applied: int
    partial: int
    skipped: int
    last_seen: datetime
    last_applied: datetime | None
    skip_details: list[tuple[str, str, str]]  # (project, timestamp, reason)


LOG_FILE = Path(__file__).parent / "log.jsonl"
NATE_STYLE_DIR = LOG_FILE.parent.parent
DAILY_REPORT = NATE_STYLE_DIR / "style_report.md"
DIARY_DIR = NATE_STYLE_DIR / "diary"

TREND_ACTIVE_DAYS = 14
TREND_DECLINING_DAYS = 60
TREND_BLOCKED_DAYS = 30


def parse_since(value: str) -> timedelta:
    """Parse a duration string like '30d', '2w', '6m' into a timedelta."""
    match = re.match(r"^(\d+)([dwm])$", value)
    if not match:
        msg = f"Invalid --since value: {value} (use e.g. 30d, 2w, 6m)"
        raise argparse.ArgumentTypeError(msg)
    amount = int(match.group(1))
    unit = match.group(2)
    if unit == "d":
        return timedelta(days=amount)
    if unit == "w":
        return timedelta(weeks=amount)
    # months approximated as 30 days
    return timedelta(days=amount * 30)


def _load_raw_entries() -> list[dict[str, object]]:
    """Load all JSONL entries as raw dicts."""
    if not LOG_FILE.exists():
        return []
    raw: list[dict[str, object]] = []
    for line in LOG_FILE.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            raw.append(json.loads(line))  # pyright: ignore[reportAny]
        except json.JSONDecodeError:
            continue
    return raw


def load_entries(
    since: timedelta | None = None,
    project: str | None = None,
) -> list[LogEntry]:
    """Load and filter JSONL entries (excludes failure entries)."""
    now = datetime.now(tz=timezone.utc)
    entries: list[LogEntry] = []

    for raw in _load_raw_entries():
        # Skip failure entries (they have a top-level "status" field)
        if "status" in raw:
            continue

        entry: LogEntry = cast(object, raw)  # pyright: ignore[reportAssignmentType]

        if project and entry["project"] != project:
            continue

        if since:
            ts = datetime.fromisoformat(
                entry["timestamp"].replace("Z", "+00:00")
            ).replace(tzinfo=timezone.utc)
            if now - ts > since:
                continue

        entries.append(entry)

    return entries


def load_failure_entries(since_days: int = TREND_ACTIVE_DAYS) -> list[FailureEntry]:
    """Load failure entries from the last N days."""
    cutoff = datetime.now(tz=timezone.utc) - timedelta(days=since_days)
    failures: list[FailureEntry] = []

    for raw in _load_raw_entries():
        if raw.get("status") != "error":
            continue

        entry: FailureEntry = cast(object, raw)  # pyright: ignore[reportAssignmentType]
        ts = datetime.fromisoformat(
            entry["timestamp"].replace("Z", "+00:00")
        ).replace(tzinfo=timezone.utc)
        if ts >= cutoff:
            failures.append(entry)

    return failures


def compute_stats(entries: list[LogEntry]) -> dict[str, StyleStats]:
    """Compute per-style statistics from log entries."""
    stats: dict[str, StyleStats] = {}

    for entry in entries:
        sid = entry["style_id"]
        ts = datetime.fromisoformat(
            entry["timestamp"].replace("Z", "+00:00")
        ).replace(tzinfo=timezone.utc)

        if sid not in stats:
            stats[sid] = StyleStats(
                style_id=sid,
                style_file=entry["style_file"],
                local=entry["local"],
                projects=set(),
                applied=0,
                partial=0,
                skipped=0,
                last_seen=ts,
                last_applied=None,
                skip_details=[],
            )

        s = stats[sid]
        s["projects"].add(entry["project"])
        if ts > s["last_seen"]:
            s["last_seen"] = ts

        for finding in entry["findings"]:
            status = finding["status"]
            if status == "applied":
                s["applied"] += 1
                if s["last_applied"] is None or ts > s["last_applied"]:
                    s["last_applied"] = ts
            elif status == "partial":
                s["partial"] += 1
                if s["last_applied"] is None or ts > s["last_applied"]:
                    s["last_applied"] = ts
                reason = finding.get("reason", "")
                if reason:
                    s["skip_details"].append(
                        (entry["project"], entry["timestamp"], reason)
                    )
            elif status == "skipped":
                s["skipped"] += 1
                reason = finding.get("reason", "")
                if reason:
                    s["skip_details"].append(
                        (entry["project"], entry["timestamp"], reason)
                    )

    return stats


def compute_trend(s: StyleStats, now: datetime) -> str:
    """Compute trend label for a style."""
    days_since_seen = (now - s["last_seen"]).days

    if days_since_seen <= TREND_ACTIVE_DAYS:
        # Check for blocked: seen recently but not applied recently
        if s["last_applied"] is None:
            return "blocked"
        days_since_applied = (now - s["last_applied"]).days
        if days_since_applied > TREND_BLOCKED_DAYS:
            return "blocked"
        return "active"

    if days_since_seen <= TREND_DECLINING_DAYS:
        return f"declining ({days_since_seen}d)"

    return f"retired? ({days_since_seen}d)"


def print_table(
    stats: dict[str, StyleStats],
    include_local: bool,
    show_skips: bool,
    style_filter: str | None,
) -> None:
    """Print the summary table."""
    now = datetime.now(tz=timezone.utc)

    # Filter
    items = list(stats.values())
    if not include_local:
        items = [s for s in items if not s["local"]]
    if style_filter:
        items = [s for s in items if style_filter in s["style_file"]]

    if not items:
        print("No matching style data found.")
        return

    # Sort by applied count descending
    items.sort(key=lambda s: s["applied"] + s["partial"], reverse=True)

    # Shared styles table
    shared = [s for s in items if not s["local"]]
    if shared:
        print_section("Shared Styles", shared, now, show_skips)

    # Local styles grouped by project
    local = [s for s in items if s["local"]]
    if local:
        print()
        print("Local Styles:")
        by_project: dict[str, list[StyleStats]] = {}
        for s in local:
            for p in sorted(s["projects"]):
                if p not in by_project:
                    by_project[p] = []
                by_project[p].append(s)

        for proj in sorted(by_project):
            print(f"  {proj}:")
            print_section(
                None, by_project[proj], now, show_skips, indent="    "
            )


def print_section(
    title: str | None,
    items: list[StyleStats],
    now: datetime,
    show_skips: bool,
    indent: str = "",
) -> None:
    """Print a section of the summary table."""
    if title:
        print(f"\n{title}:")

    # Column widths
    name_width = max(len(s["style_file"]) for s in items)
    name_width = max(name_width, 10)

    header = (
        f"{indent}{'Style File':<{name_width}}  "
        f"{'Projects':>8}  {'Applied':>7}  {'Partial':>7}  "
        f"{'Skipped':>7}  {'Last Seen':>10}  Trend"
    )
    print(header)
    print(f"{indent}{'-' * (len(header) - len(indent))}")

    for s in items:
        trend = compute_trend(s, now)
        last_seen_str = s["last_seen"].strftime("%Y-%m-%d %H:%M")
        proj_count = len(s["projects"])

        row = (
            f"{indent}{s['style_file']:<{name_width}}  "
            + f"{proj_count:>8}  {s['applied']:>7}  {s['partial']:>7}  "
            + f"{s['skipped']:>7}  {last_seen_str:>10}  {trend}"
        )
        print(row)

        if show_skips and s["skip_details"]:
            for proj, ts_str, reason in s["skip_details"]:
                ts_short = ts_str[:10]
                print(
                    f"{indent}  skip ({proj}, {ts_short}): \"{reason}\""
                )


def style_to_wikilink(style_file: str) -> str:
    """Convert a style filename to an Obsidian wikilink."""
    name = style_file.removesuffix(".md")
    return f"[[{name}]]"



def archive_existing_report() -> None:
    """Copy the existing style_report.md to the diary archive before overwriting."""
    if not DAILY_REPORT.exists():
        return

    # Read the existing report's date_modified to use for the archive filename
    content = DAILY_REPORT.read_text()
    archive_time = datetime.now(tz=timezone.utc)

    # Try to extract date_modified from frontmatter for the folder structure
    for line in content.splitlines():
        if line.startswith("date_modified:"):
            match = re.search(r"\[\[(\d{4}-\d{2}-\d{2})\]\]", line)
            if match:
                date_str = match.group(1)
                parts = date_str.split("-")
                if len(parts) == 3:
                    archive_time = archive_time.replace(
                        year=int(parts[0]),
                        month=int(parts[1]),
                        day=int(parts[2]),
                    )
            break

    year = archive_time.strftime("%Y")
    month = archive_time.strftime("%m")
    prefix = archive_time.strftime("%Y-%m-%d-%H-%M-%S")

    archive_dir = DIARY_DIR / year / month
    archive_dir.mkdir(parents=True, exist_ok=True)

    archive_path = archive_dir / f"{prefix} style_report.md"
    _ = archive_path.write_text(content)
    print(f"Archived {archive_path}")


def write_daily_report(entries: list[LogEntry]) -> None:
    """Write the full daily report with all sections."""
    archive_existing_report()
    stats = compute_stats(entries)
    now = datetime.now(tz=timezone.utc)
    today = now.strftime("%Y-%m-%d")
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    all_items = list(stats.values())
    all_items.sort(key=lambda s: s["applied"] + s["partial"], reverse=True)

    shared = [s for s in all_items if not s["local"]]
    local = [s for s in all_items if s["local"]]

    lines: list[str] = []
    lines.append("---")
    lines.append(f'date_created: "[[{today}]]"')
    lines.append(f'date_modified: "[[{today}]]"')
    lines.append("tags:")
    lines.append("  - report")
    lines.append("  - style")
    lines.append("---")
    lines.append("# Style Report")

    # Section 1: Overall usage
    if shared:
        lines.append("## Style Usage History")
        lines.append(
            "| [[style_report_usage#Style\\|Style]] | [[style_report_usage#Projects\\|Projects]] | [[style_report_usage#Applied\\|Applied]] | [[style_report_usage#Partial\\|Partial]] | [[style_report_usage#Skipped\\|Skipped]] | [[style_report_usage#Last Seen\\|Last Seen]] | [[style_report_usage#Trend\\|Trend]] |"
        )
        lines.append("|---|---|---|---|---|---|---|")
        for s in shared:
            trend = compute_trend(s, now)
            last_seen_str = s["last_seen"].strftime("%Y-%m-%d %H:%M")
            proj_count = len(s["projects"])
            wikilink = style_to_wikilink(s["style_file"])
            lines.append(
                f"| {wikilink} | {proj_count} | {s['applied']}"
                + f" | {s['partial']} | {s['skipped']}"
                + f" | {last_seen_str} | {trend} |"
            )

    # Section 2: Per-project breakdown
    project_stats: dict[str, list[StyleStats]] = {}
    for s in all_items:
        for p in sorted(s["projects"]):
            if p not in project_stats:
                project_stats[p] = []
            project_stats[p].append(s)

    if project_stats:
        lines.append("## By Project")
        for proj in sorted(project_stats):
            proj_items = project_stats[proj]
            applied = sum(s["applied"] for s in proj_items)
            partial = sum(s["partial"] for s in proj_items)
            skipped = sum(s["skipped"] for s in proj_items)
            lines.append(
                f"**{proj}** — {len(proj_items)} styles,"
                + f" {applied} applied, {partial} partial, {skipped} skipped"
            )

    # Section 3: Local styles
    if local:
        lines.append("## Local Styles")
        lines.append("")
        by_project: dict[str, list[StyleStats]] = {}
        for s in local:
            for p in sorted(s["projects"]):
                if p not in by_project:
                    by_project[p] = []
                by_project[p].append(s)

        for proj in sorted(by_project):
            lines.append(f"### {proj}")
            lines.append("")
            lines.append(
                "| [[style_report_usage#Style\\|Style]] | [[style_report_usage#Applied\\|Applied]] | [[style_report_usage#Partial\\|Partial]] | [[style_report_usage#Skipped\\|Skipped]] | [[style_report_usage#Last Seen\\|Last Seen]] | [[style_report_usage#Trend\\|Trend]] |"
            )
            lines.append("|---|---|---|---|---|---|")
            for s in by_project[proj]:
                trend = compute_trend(s, now)
                last_seen_str = s["last_seen"].strftime("%Y-%m-%d %H:%M")
                wikilink = style_to_wikilink(s["style_file"])
                lines.append(
                    f"| {wikilink} | {s['applied']}"
                    + f" | {s['partial']} | {s['skipped']}"
                    + f" | {last_seen_str} | {trend} |"
                )
            lines.append("")

    # Section 4: Skip/partial details
    all_skips: list[tuple[str, str, str, str]] = []  # (style, project, date, reason)
    for s in all_items:
        for proj, ts_str, reason in s["skip_details"]:
            all_skips.append((s["style_file"], proj, ts_str[:10], reason))

    if all_skips:
        lines.append("## Skips & Partial Applications")
        lines.append("")
        lines.append("| Style | Project | Date | Reason |")
        lines.append("|---|---|---|---|")
        for style, proj, date, reason in all_skips:
            wikilink = style_to_wikilink(style)
            lines.append(f"| {wikilink} | {proj} | {date} | {reason} |")
        lines.append("")

    # Section 5: Fix failures
    failures = load_failure_entries()
    if failures:
        lines.append("## Fix Failures")
        lines.append("")
        lines.append("| Project | Branch | Date | Reason |")
        lines.append("|---|---|---|---|")
        for f in failures:
            date = f["timestamp"][:10]
            lines.append(
                f"| {f['project']} | {f['base_branch']}"
                + f" | {date} | {f['reason']} |"
            )
        lines.append("")

    total_entries = len(entries)
    total_projects = len({e["project"] for e in entries})
    lines.append(
        f"*Generated {timestamp} from {total_entries} log entries"
        + f" across {total_projects} projects*"
    )
    lines.append("")

    _ = DAILY_REPORT.write_text("\n".join(lines))
    print(f"Wrote {DAILY_REPORT}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Style guide usage summary")
    _ = parser.add_argument("--since", type=str, help="Time window (e.g. 30d, 2w, 6m)")
    _ = parser.add_argument("--project", type=str, help="Filter by project name")
    _ = parser.add_argument(
        "--local", action="store_true", help="Include local styles"
    )
    _ = parser.add_argument(
        "--skips", action="store_true", help="Show skip/partial reasons"
    )
    _ = parser.add_argument("--style", type=str, help="Filter by style file name")
    _ = parser.add_argument(
        "--generate",
        action="store_true",
        help="Write Obsidian reports (style_report_usage.md + style_report.md)",
    )

    args = parser.parse_args()

    generate_mode: bool = cast(bool, args.generate)

    if generate_mode:
        entries = load_entries()
        if entries:
            write_daily_report(entries)
        else:
            print("No style usage data — skipping style_report.md")
        return

    since_raw: str | None = cast(str | None, args.since)
    since = parse_since(since_raw) if since_raw else None
    project: str | None = cast(str | None, args.project)
    entries = load_entries(since=since, project=project)

    if not entries:
        print("No style usage data found.")
        return

    stats = compute_stats(entries)
    include_local: bool = cast(bool, args.local)
    show_skips: bool = cast(bool, args.skips)
    style_filter: str | None = cast(str | None, args.style)
    print_table(stats, include_local, show_skips, style_filter)


if __name__ == "__main__":
    main()
