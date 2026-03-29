---
tags: [rust, patterns]
---

## Use `usize::from(bool)` for bool-to-integer conversion

Never use `if bool { 1 } else { 0 }` — use the standard `From` conversion.

```rust
// bad
let max_col = if has_targets { 1 } else { 0 };

// good
let max_col = usize::from(has_targets);
```
