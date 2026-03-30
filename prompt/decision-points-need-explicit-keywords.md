---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- prompt
- clarity
- interaction
---
## Decision points need explicit keywords

Every place the user must choose requires named keywords with clear actions. Never say "handle the response appropriately."

```markdown
// bad
Handle the user's response appropriately

// good
## Available Actions
- **approve** - Accept this change and continue
- **skip** - Skip this change and move to the next
- **stop** - Exit without further changes

Please select one of the keywords above.
```
