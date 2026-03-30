---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- prompt
- clarity
- variables
---
## Explicit $ARGUMENTS handling

Commands that accept arguments must handle both the provided and empty cases explicitly. Don't assume the user will always provide input.

```markdown
// bad
Use the provided arguments

// good
If $ARGUMENTS is provided:
- Set FILE = $ARGUMENTS
- Verify ${FILE} exists

If $ARGUMENTS is empty:
- Ask user: "Which file would you like to process?"
- Set FILE = user's response
```
