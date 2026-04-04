---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- rust
- visibility
---
## Prefer local-relative imports

Use `super::` for peers within the same parent. Use `crate::` when crossing into a different top-level domain or when the path would require `super::super::` or deeper.

```rust
// bad — unnecessarily global path for a peer import
use crate::app_tools::support::cargo_detector::TargetType;

// good — shows the local peer relationship
use super::cargo_detector::TargetType;
```

### Stop at one `super::`

`super::super::` and deeper chains are hard to reason about — the reader has to count hops to figure out where the import lands. When a single `super::` isn't enough, switch to an absolute `crate::` path.

```rust
// bad — cognitive load increases with each super::
use super::super::columns::ResolvedWidths;

// good — absolute path is immediately clear
use crate::tui::columns::ResolvedWidths;
```

**Tooling:** `cargo mend` detects over-qualified local paths as `shorten_local_crate_import` (warning) and deep `super::super::` chains as `replace_deep_super_import` (warning). Run `cargo mend --fix` to auto-fix both.