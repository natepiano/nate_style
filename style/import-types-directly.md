---
tags: [rust, imports]
---

## Import types directly

Types (structs, enums, traits) are imported by name so they appear bare at the call site.

```rust
// bad
fn spawn(query: Query<&crate::movable::Movable>) {}

// good
use crate::movable::Movable;

fn spawn(query: Query<&Movable>) {}
```
