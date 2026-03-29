---
tags: [rust, visibility]
---

## Prefer local-relative imports

Use `super::` for peers within the same parent. Use `crate::` only when crossing into a different top-level domain.

```rust
// bad — unnecessarily global path for a peer import
use crate::app_tools::support::cargo_detector::TargetType;

// good — shows the local peer relationship
use super::cargo_detector::TargetType;
```
