---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- prompt
- clarity
---
## Trust the user environment

If a command specifies a tool, script, or path, it exists and works. The user has ensured this. Never suggest checking availability, validating prerequisites, or adding fallbacks for specified tools.

```markdown
// bad
Check if required scripts exist before using them
Validate Python/tool availability before execution
Verify directory permissions before writing

// good
Run: bash ~/.claude/scripts/example.sh "${WORKING_DIR}"
```
