---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- imports
- rust
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