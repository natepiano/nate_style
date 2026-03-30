---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- prompt
- workflow
- interaction
---
## State communication and decision tracking

The user should always know where they are and what they've decided. Show position in multi-item flows, validate unexpected input, and track decisions for a final summary.

```markdown
// good — position awareness
"Finding 3 of 7: Missing error handler in parse_input"

// good — input validation
"Unrecognized response 'yep'. Please select from: approve, skip, deny"

// good — final summary
"Review complete. Applied: 3, Skipped: 2, Investigated: 1"
```
