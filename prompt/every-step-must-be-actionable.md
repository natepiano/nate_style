---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- prompt
- clarity
---
## Every step must be actionable

Every instruction must name what to do, what tool to use, and what the target is. Vague directives produce inconsistent agent behavior.

```markdown
// bad — vague
Review the file and make appropriate changes

// good — actionable
Use Read tool to read ${FILE}, identify unused imports, then use Edit tool to remove them
```
