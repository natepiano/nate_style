---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- prompt
- structure
- variables
---
## Consistent placeholder syntax

Use `${SCREAMING_SNAKE_CASE}` for all template variables. Declare them at the top of the file or section with `NAME = value`. These are documentation placeholders for AI agents, not shell variables.

The sole exception is `$ARGUMENTS` — this is a special replacement value handled by Claude Code and must never use `${ARGUMENTS}`.

```markdown
// bad — inconsistent
Process $FILE then check {output} and use ${result}

// good — uniform
MAX_RETRIES = 3
BASE_PORT = 30001
MAX_PORT = ${BASE_PORT + MAX_RETRIES - 1}

Process ${FILE} on port ${BASE_PORT}
Arguments from user: $ARGUMENTS
```
