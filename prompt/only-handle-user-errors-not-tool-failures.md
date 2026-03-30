---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- prompt
- clarity
---
## Only handle user errors, not tool failures

Focus error handling on user input mistakes and edge cases. Don't add handling for core tool failures (Read, Write, Task, Edit), system-level file operations, disk space, permissions, or timeout specifications. These indicate environmental issues beyond command scope.

```markdown
// bad
Handle Task tool failure or unexpected output format
Add error handling for file write failures, disk space, or permissions
Add timeout handling for tool operations

// good
If user provides invalid file path, display error and ask for correction
If $ARGUMENTS contains no .rs files, inform user: "No Rust files found in the given path"
```
