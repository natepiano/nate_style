---
date_created: "[[2026-04-06]]"
date_modified: "[[2026-04-06]]"
group: constants
tags: [constants, rust]
---
## No magic values

Place all constants in `constants.rs` with descriptive names. When a module is a directory (e.g., `toasts/`), its constants belong in its own `constants.rs`, not in the parent's.

```rust
// bad
if port == 15702 { ... }

// good — in constants.rs
pub(super) const DEFAULT_BRP_PORT: u16 = 15702;

// good — at call site
if port == DEFAULT_BRP_PORT { ... }
```