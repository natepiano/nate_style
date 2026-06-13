---
date_created: '[[2026-04-06]]'
date_modified: '[[2026-06-12]]'
tags:
- tests
- rust
mechanism: llm
candidates:
  kind: test_literals
---
## Derive test values from production constants

Tests must not hardcode values that are derived from constants. Use the same constant or function the production code uses.

```rust
// bad — breaks silently if TOAST_WIDTH changes
assert!(width <= 58);

// good — stays correct automatically
assert!(width <= toast_body_width());
```
