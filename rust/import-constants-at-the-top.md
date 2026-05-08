---
date_created: '[[2026-04-10]]'
date_modified: '[[2026-05-08]]'
tags:
- constants
- imports
- rust
mechanism: llm
---
## Import constants at the top

Module constants are imported at the top and used bare inline; inherent associated constants stay qualified (`Vec3::X`, `f32::EPSILON`).

```rust
// bad
let margin = super::constants::ZOOM_TO_FIT_MARGIN;

// good
use super::constants::ZOOM_TO_FIT_MARGIN;

let margin = ZOOM_TO_FIT_MARGIN;
```
