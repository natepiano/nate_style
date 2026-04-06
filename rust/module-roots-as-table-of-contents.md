---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-04-05]]'
tags:
- rust
- visibility
---
## Module roots as table of contents

Module roots (`mod.rs`, `lib.rs`) should only declare submodules and export the public API via `pub use`. No other logic.

```rust
// good — mod.rs as clean table of contents
mod constants;
mod duplicate;
mod helpers;

pub use constants::ZOOM_TO_FIT_MARGIN;
pub use duplicate::DuplicatePlugin;
```

### Exceptions

**Module-name type:** If a module defines a type whose name matches the module name (e.g., `ImageFile` in `image_file/mod.rs`), that type and its `impl` blocks may live in `mod.rs`. The module exists to define that type, so it belongs at the root. Supporting types should still be moved to leaf files when the module is large enough to warrant the split.

**Bevy plugin:** Bevy projects may also define the plugin (`impl Plugin for ...`) in `mod.rs`, since the plugin wires together the module's submodules and is conceptually part of the facade. The plugin should appear after the table of contents (after all `mod` declarations and `pub use` re-exports).
