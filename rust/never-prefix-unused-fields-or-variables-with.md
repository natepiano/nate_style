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

**Exception — RAII guards:** When a binding exists solely for its `Drop` impl (timers, lock guards, temp files), `let _name = ...` is the correct Rust idiom. The underscore prefix suppresses `unused_variable` while keeping the value alive until scope exit. Do not remove the underscore — without it, `rustc` warns. Do not remove the name — `let _ = ...` drops the value immediately.

```rust
// good — _timer lives until end of scope, Drop prints elapsed time
let _timer = Timer::new("analyze");

// bad — drops immediately, timer measures nothing
let _ = Timer::new("analyze");

// bad — rustc warns "unused variable: timer"
let timer = Timer::new("analyze");
```