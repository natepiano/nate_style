---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- prompt
- clarity
---
## Name the tool and the pattern

When instructing an agent to search, read, or modify something, name the specific tool and its parameters. Generic instructions produce unreliable behavior.

```markdown
// bad
Search for the pattern in the codebase

// good
Use Grep tool with pattern "fn main" in directory ${PROJECT_ROOT}
```
