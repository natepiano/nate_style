---
date_created: "[[2026-10-13]]"
date_modified: "[[2026-10-13]]"
tags: [push]
mechanism: llm
test: "Is the full body, including its action or no-action first line, fewer than 500 characters?"
source: "Approved design, 2026-10-13, ~/.local/state/plan-backlog/2026-10-13-user-message-clarity.md: \"a body under 500\"; \"body 454\""
---
## Keep the push body under 500 characters

Keep the entire push body under 500 characters, including the action or no-action first line. Cut detail that does not help the user understand or act.

### Bad
**shutdown has been stopped on a permission prompt since 01:32 EDT.** It's asking to read its own saved tool output at `~/.claude1/projects/…/tool-results/bm2daw4h8.txt`. That path is a symlink into `~/.claude/projects/…`, and Claude Code treats the target as outside the unit's allowed directories. Any unit on claude 1 that reads back a large saved output will hit the same prompt. […] To unblock it now: run `tmux attach -t shutdown` […] To stop it happening again: I recommend adding `Read(~/.claude/projects/**/tool-results/**)` to `permissions.allow` […]

### Good
Action: In natedev, reply allow or don't allow.

Tonight's test of one showrunner under another passed, but auto mode refused its last step as a production deploy. That step finishes a production by copying its work to main (here a throwaway repo on this disk), so real productions will be refused too.

Allow (recommended): add a permission rule for that step, so real productions can finish.

Don't allow: natedev deletes the two test productions by hand.
