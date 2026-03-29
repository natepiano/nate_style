---
tags: [rust, imports]
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
