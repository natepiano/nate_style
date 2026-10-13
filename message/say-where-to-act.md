---
date_created: "[[2026-10-13]]"
date_modified: "[[2026-10-13]]"
tags: [push, question]
mechanism: llm
test: "Does each action name the machine and the session or terminal where the user takes it?"
source: "User rule, 2026-10-04, ~/.claude/commands/showrunner/produce.md <Notify>: \"what is blocked, the exact action, and on which machine\""
---
## Say where to act

Name the machine and the session or terminal where the user acts.

### Bad
To unblock it now: run `tmux attach -t shutdown`.

### Good
In a terminal on natedev, run `tmux attach -t shutdown` to open the stopped unit's session and answer its permission prompt.
