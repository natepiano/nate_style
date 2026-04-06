---
date_created: "[[2026-04-05]]"
date_modified: "[[2026-04-06]]"
tags:
  - rust
  - visibility
  - types
---
## Module roots as table of contents

Module roots (`mod.rs`, `lib.rs`) should only declare submodules and export the public API via `pub use`. No other logic.

```rust
// good — mod.rs as clean table of contents
mod history;
mod paths;
mod types;

pub use history::CacheUsage;
pub use paths::project_dir;
```

### Exceptions

**Module-name type and its field types:** If a module defines a type whose name matches the module name (e.g., `ImageFile` in `image_file/mod.rs`), that type and its `impl` blocks may live in `mod.rs`. The module exists to define that type, so it belongs at the root.

Types that appear as fields of the primary type or as enum variant payloads — plus their `impl` blocks — may also live in `mod.rs`, because you cannot read the primary type's definition without them. This is a structural test: if a type is referenced in the primary type's field list, it qualifies. Types that are merely topically related but independently constructed (separate components, resources, settings, gizmo groups) belong in leaf files.

```rust
// dimension_lock/mod.rs — DimensionLock is the module-name type

// LockAxis and TravelState qualify: they are field types of DimensionLock.
pub(super) enum LockAxis { X, Y, Z }
pub(super) enum TravelState { Centered, Positive { last_good: f32 }, ... }

pub struct DimensionLock {
    axis:         LockAxis,    // ← field type, lives here
    travel_state: TravelState, // ← field type, lives here
    // ...
}

// DimensionLockSettings is a separate Resource — leaf file.
// DimensionLockGizmo is a separate gizmo group — leaf file.
```

**Bevy plugin:** Bevy projects may also define the plugin (`impl Plugin for ...`) in `mod.rs`, since the plugin wires together the module's submodules and is conceptually part of the facade. The plugin should appear after the table of contents (after all `mod` declarations and `pub use` re-exports).
