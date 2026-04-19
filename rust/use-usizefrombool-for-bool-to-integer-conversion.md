---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-04-19]]'
see_also: "[[prefer-from-impl-over-named-constructors]]"
tags:
- patterns
- rust
---
## Use `usize::from(bool)` for bool-to-integer conversion

Never use `if bool { 1 } else { 0 }` — use the standard `From` conversion.

```rust
// bad
let max_col = if has_targets { 1 } else { 0 };

// good
let max_col = usize::from(has_targets);
```