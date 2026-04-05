---
date_created: "[[2026-03-29]]"
date_modified: "[[2026-03-29]]"
tags:
  - imports
  - rust
  - constants
---
## Import constants at the top

Constants follow the same rule as types — import at the top, use the bare name inline.

```rust
// bad
let margin = super::constants::ZOOM_TO_FIT_MARGIN;

// good
use super::constants::ZOOM_TO_FIT_MARGIN;

let margin = ZOOM_TO_FIT_MARGIN;
```