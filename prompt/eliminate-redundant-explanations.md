---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- prompt
- tokens
---
## Eliminate redundant explanations

Don't re-explain what a tool does — the tool description is sufficient. Don't add meta-commentary about the command's own structure. If the instruction is clear, stop writing.

```markdown
// bad — re-explains the tool
Use the Read tool to read the file. This will open the file and return its
contents so you can see what's inside.

// good
Use Read tool to read ${FILE}

// bad — meta-commentary
This section defines how you should handle errors, which is important for
maintaining a good user experience...

// good
[just provide the error handling instructions directly]
```
