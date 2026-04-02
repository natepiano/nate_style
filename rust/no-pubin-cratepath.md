---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- rust
- visibility
---
## No `pub(in crate::path)`

If a change seems to require `pub(in crate::path)`, treat it as a design smell. Move the item to the nearest common parent instead.

```rust
// bad
pub(in crate::selection::operations) fn build_label() -> String { ... }

// good — move to the shared boundary
// selection/build_label.rs
pub(super) fn build_label() -> String { ... }
```

**Tooling:** `cargo mend` detects this as `forbidden_pub_in_crate` (error).