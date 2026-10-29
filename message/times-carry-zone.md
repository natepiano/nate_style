---
date_created: "[[2026-10-13]]"
date_modified: "[[2026-10-29]]"
tags: [all]
mechanism: llm
test: "Is each clock time in the user's zone, does it name that zone, and does it include its date when it is not today?"
source: "User, 2026-10-03, ~/.claude/projects/-etc-nixos/memory/name-the-time-zone.md: \"add the time zone you're reporting in when you say a time\"; user, 2026-10-12: \"switch all showrunners and units to return to communicating in EDT\"; user, 2026-10-29 (via the showrunner): yes, give times in the user's zone from user_zone.py"
---
## Times carry their zone

Give clock times in the user's zone and name the zone. Read the zone with `python3 ~/.claude/scripts/lib/user_zone.py`; it is EDT since 2026-10-28. Add the date when the time is not today.

### Bad
Mac rows as of the 12:14 sync.

### Good
Mac rows as of the 2026-10-12 12:14 EDT sync (in a report dated 2026-10-13).
