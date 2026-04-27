---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-04-26]]'
tags:
- rust
- visibility
---
## No `pub(in <path>)`

Restricted-visibility paths — `pub(in crate::...)`, `pub(in super::super)`, any `pub(in ...)` — are a design smell. The path encodes a layering boundary that belongs in the module tree. Move the item to the nearest common parent and use `pub(super)`.

```rust
// bad
pub(in crate::selection::operations) fn build_label() -> String { ... }
pub(in super::super) fn build_label() -> String { ... }

// good — relocate, then plain pub(super) reaches every legitimate caller
pub(super) fn build_label() -> String { ... }
```

**Tooling:** `cargo mend` detects the absolute form as `forbidden_pub_in_crate` (error). The relative form is not yet caught — flag manually during review until mend grows `forbidden_pub_in_path`.
