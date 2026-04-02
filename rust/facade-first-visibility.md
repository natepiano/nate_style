---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- rust
- visibility
---
## Facade-first visibility

Module roots (`mod.rs`, `lib.rs`) should only declare submodules, export the public API via `pub use`, and define the plugin. No other logic.

```rust
// good — mod.rs as clean table of contents
mod constants;
mod duplicate;
mod helpers;

pub use constants::ZOOM_TO_FIT_MARGIN;
pub use duplicate::DuplicatePlugin;
```

**Tooling:** `cargo mend` detects internal-only facades as `internal_parent_pub_use_facade` (warning). Run `cargo mend --fix-pub-use` to auto-fix facades that are only consumed within the parent's subtree.