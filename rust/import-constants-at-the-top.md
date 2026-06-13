---
date_created: '[[2026-04-10]]'
date_modified: '[[2026-06-12]]'
tags:
- constants
- imports
- rust
mechanism: llm
candidates:
  kind: regex
  pattern: '\b[a-z_][a-z0-9_]*::[A-Z][A-Z0-9_]{2,}\b'
  exclude_pattern: '^\s*(pub(\([^)]*\))?\s+)?use\s|\b(f32|f64|i8|i16|i32|i64|i128|isize|u8|u16|u32|u64|u128|usize|char|str|bool)::'
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
