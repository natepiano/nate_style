---
clippy: single_component_path_imports
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- imports
- rust
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