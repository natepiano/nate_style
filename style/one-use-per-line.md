---
tags: [rust, imports]
---

## One `use` per line

Never consolidate imports with braces.

```rust
// bad
use crate::movable::{Movable, DragState, Selected};

// good
use crate::movable::DragState;
use crate::movable::Movable;
use crate::movable::Selected;
```
