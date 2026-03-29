---
tags: [rust, style]
---

## Backtick names in comments

Surround type, function, and variable names with backticks in comments.

```doc
// bad
/// Returns the Movable component for the given entity.

// good
/// Returns the `Movable` component for the given `Entity`.
```
