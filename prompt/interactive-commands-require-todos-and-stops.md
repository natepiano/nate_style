---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- prompt
- workflow
- interaction
---
## Interactive commands require todos and stops

Every interactive command needs three things:

1. **TodoWrite before interaction** — one todo per decision point, mark in_progress when presenting, completed after user responds
2. **Keywords at column 0** — no indentation, bolded, with action descriptions
3. **Explicit STOP** — after presenting keywords, the command must stop and wait. Never proceed without user input or assume defaults.

```markdown
// bad — keywords buried in prose
You can choose to apply, skip, or stop...

// good — column 0, bolded, with descriptions
## Available Actions
- **apply** - Execute the suggested changes
- **skip** - Skip this change and continue
- **stop** - Exit without further changes

Please select one of the keywords above.
```
