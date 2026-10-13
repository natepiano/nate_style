---
date_created: "[[2026-10-13]]"
date_modified: "[[2026-10-13]]"
tags: [question, reply]
mechanism: llm
test: "Does a question asked before appear at the end of this reply only as the number of open questions, while anything the user asked for is answered in full?"
source: "User, relayed 2026-10-12, ~/.claude/projects/-etc-nixos/memory/open-questions-as-a-count.md: \"your messages should just say 'there are {n} open questions for you' - that's it\""
---
## Ask once, then give the count

Ask a question once with enough context to answer. At the end of later replies, give only "There are N open questions for you." This limits the reminder, never an answer or explanation the user asked for. Give the questions in full again only when asked.

### Bad
The only open question is WESL: "prepare first" or "straight to the upgrade"?

### Good
There are 3 open questions for you.
