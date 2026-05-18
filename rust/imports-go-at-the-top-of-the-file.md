---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-05-17]]'
tags:
- imports
- rust
mechanism: mend
mode: auto
---
## Imports go at the top of the file

Never scatter `use` statements through the body of a file.

```rust
// bad
fn example() {
    use crate::movable::Movable;
    let m = Movable::default();
}

// good
use crate::movable::Movable;

fn example() {
    let m = Movable::default();
}
```

**Tooling:** `cargo mend` detects this as `imports_at_top` (warning). Run
`cargo mend --fix` to lift the `use` to the top of the enclosing file or
inline module. Uses with attributes (such as `#[cfg(...)]`) and globs are
left in place. Bare-name collisions with existing top-level imports are
detected and skipped.