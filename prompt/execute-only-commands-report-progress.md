---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- prompt
- workflow
---
## Execute-only commands report progress

Non-interactive commands that run to completion need: progress updates for operations taking 3+ seconds, a clear completion confirmation, and actionable error messages on failure. For 5+ step processes, use todos even without interaction.

```markdown
// bad — silent execution
[runs for 30 seconds with no output]

// good
"Searching for pattern... Found 23 matches. Processing..."
"Command complete. Processed 15 files, made 43 changes."
"Error: File 'config.json' not found at path X. Please verify the file exists."
```
