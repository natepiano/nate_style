---
date_created: "[[2026-04-19]]"
date_modified: "[[2026-04-19]]"
tags: [imports, rust]
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