---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- rust
- style
---
## Backtick names in comments

Surround type, function, and variable names with backticks in comments.

```doc
// bad
/// Returns the Movable component for the given entity.

// good
/// Returns the `Movable` component for the given `Entity`.
```