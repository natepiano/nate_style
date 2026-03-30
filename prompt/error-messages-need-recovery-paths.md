---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- prompt
- clarity
---
## Error messages need recovery paths

When something goes wrong, tell the user what failed and how to fix it. An error without a recovery path leaves the user stuck.

```markdown
// bad
If error occurs, handle it

// good
If file not found, inform user: "File ${FILE} not found at ${PATH}. Please verify the file exists and provide the correct path."
```
