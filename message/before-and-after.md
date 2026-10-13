---
date_created: "[[2026-10-13]]"
date_modified: "[[2026-10-13]]"
tags: [all]
mechanism: llm
test: "Does the change say what the user sees before and after it?"
source: "~/.claude/docs/user_facing_explanation.md, the user's rule, in the doc since 2026-08-01: \"Behavior first, name second.\"; \"Never substitute a label for an explanation.\""
---
## Describe a change before and after

Describe a change by what the user sees before it and after it, before giving an implementation name.

### Bad
The recovery variants are `Disabled`, `ApplicationControlled`, and `FallbackAndReturn`.

### Good
Before: if the editor's monitor disappears, the editor is absent. After: it opens on another monitor and returns when the original display reconnects.
