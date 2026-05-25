---
date_created: '[[2026-04-10]]'
date_modified: '[[2026-05-25]]'
tags:
- rust
- visibility
mechanism: mend
mode: flag
lint: [suspicious_pub, unused_pub, internal_parent_pub_use_facade]
---
## Leaf module visibility

The visibility modifier at the source must match how the item is actually re-exported. Rust's E0364 caps from below — a re-export cannot be wider than the source — so the parent's re-export form determines the minimum modifier at the source. Pick the narrowest one that still satisfies E0364.

### Picking the modifier

| Parent re-export                         | Source modifier |
| ---------------------------------------- | --------------- |
| none (not re-exported, siblings only)    | `pub(super)`    |
| `pub(crate) use`                         | `pub(crate)`    |
| `pub use` (only if it chains to the crate root) | `pub`    |

```rust
// actor/constants.rs (nested under actor/)

// Re-exported by parent with `pub(crate) use` → modifier must match the cap
pub(crate) struct Timer { ... }

// NOT re-exported, only used by sibling modules → `pub(super)`
pub(super) const DUPLICATE_OFFSET: f32 = 0.2;
```

```rust
// actor/mod.rs
mod constants;
pub(crate) use constants::Timer;
// DUPLICATE_OFFSET is not listed — it stays internal to actor/
```

See [[use-narrowest-visibility]] for the full hierarchy and the reasoning behind allowing `pub(crate)` at depth 3+. See also [[use-pubcrate-in-top-level-private-modules]].

### Structurally-used types

If a `pub` item in a leaf module is not re-exported by the parent facade, it is only a candidate for narrowing. If it is structurally exposed through any public API position, including public function signatures, public fields of public structs, public enum variants, or nested public field graphs, it must remain `pub` and is not a style violation. Visibility-wider-than-private parameter types — including `Local<T>`, `Res<T>`, `ResMut<T>`, `Query<T>` in a `pub(crate) fn` — also count as structural exposure: `T` must be at least as visible as the function.

If a `pub` type in a leaf module appears only in the return type of a re-exported function and no external code imports it by name, do **not** re-export it — that triggers an unused-import warning. Leave it as `pub` (required by the compiler for the function signature) without a corresponding `pub use` in the facade.

```rust
// utils/file_utils.rs
pub struct RepositoryFiles {
    pub image_files:    Vec<PathBuf>,
    pub markdown_files: Vec<PathBuf>,
}
pub fn collect_repository_files(...) -> Result<RepositoryFiles, ...> { ... }
```

```rust
// utils/mod.rs — re-export the function, not the struct
pub use file_utils::collect_repository_files;
// RepositoryFiles is NOT re-exported — callers access it structurally
```

```rust
// caller — never names `RepositoryFiles`, just uses its fields
let files = utils::collect_repository_files(...)?;
let images = files.image_files;
```

Re-export the type only when external code would write `use crate::utils::RepositoryFiles`.