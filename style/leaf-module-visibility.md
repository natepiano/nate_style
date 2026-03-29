---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- rust
- visibility
---
## Leaf module visibility

In nested leaf modules, use `pub(super)` for parent-managed details. Use bare `pub` only for items the parent intentionally re-exports.

```rust
// bad — too broad for an internal constant
pub const DUPLICATE_OFFSET: f32 = 0.2;

// good — parent decides what to export
pub(super) const DUPLICATE_OFFSET: f32 = 0.2;
```

When the parent module is itself private, bare `pub` in children is bounded by that privacy — so `pub` is acceptable if the parent re-exports it and external code uses it.