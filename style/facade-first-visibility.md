---
tags: [rust, visibility]
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
