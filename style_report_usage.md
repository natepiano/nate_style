---
date_created: "[[2026-04-04]]"
date_modified: "[[2026-04-04]]"
---

# Style Report — Usage
## Terminal
```bash
# All shared styles, all time
python3 ~/rust/nate_style/usage/summary.py

# Filter by time window
python3 ~/rust/nate_style/usage/summary.py --since 30d

# Filter by project
python3 ~/rust/nate_style/usage/summary.py --project nateroids

# Include local styles
python3 ~/rust/nate_style/usage/summary.py --local

# Show skip/partial reasons
python3 ~/rust/nate_style/usage/summary.py --skips

# Detail view for a single style
python3 ~/rust/nate_style/usage/summary.py --style cargo-toml-lints.md

# Regenerate Obsidian reports
python3 ~/rust/nate_style/usage/summary.py --generate
```
## Claude Code
```
/style_usage
/style_usage --project nateroids
/style_usage --generate
```
## Schema
Log data is in `usage/log.jsonl`. See [[style_report]] for the latest report.
## Column Key
### Style
The style guide rule that was evaluated. Links to the style file in this vault.
### Projects
Number of distinct projects where this style has been applied or attempted.
### Applied
Total number of findings that were fully fixed across all projects and runs.
### Partial
Total number of findings that were partially fixed — some but not all instances were addressed. Each partial entry includes a reason explaining what was left undone.
### Skipped
Total number of findings that were not fixed at all. Each skip includes a reason — typically the cited code no longer exists or the fix would require a larger refactor.
### Last Seen
Most recent date this style appeared in any evaluation, regardless of outcome. Used for trend detection.
### Trend
How actively this style is being encountered:
- **active** — seen within the last 14 days
- **declining (Nd)** — last seen 14–60 days ago
- **retired? (Nd)** — not seen in 60+ days, candidate for archival
- **blocked** — seen recently but not successfully applied in the last 30 days, indicating friction
