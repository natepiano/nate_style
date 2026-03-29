---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- rust
- style
---
## Never prefix unused fields or variables with `_`

Remove unused items entirely instead of silencing the warning.

```rust
// bad
struct Drag {
    _offset: Vec2,
    active: bool,
}

// good — remove the unused field
struct Drag {
    active: bool,
}
```