---
tags: [rust, style]
---

## No magic values

Place all constants in `constants.rs` with descriptive names.

```rust
// bad
if port == 15702 { ... }

// good — in constants.rs
pub(super) const DEFAULT_BRP_PORT: u16 = 15702;

// good — at call site
if port == DEFAULT_BRP_PORT { ... }
```
