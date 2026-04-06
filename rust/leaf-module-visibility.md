---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-04-04]]'
tags:
- rust
- visibility
---
## Leaf module visibility

Items re-exported by the parent facade must be `pub` — Rust requires `pub` at the source for `pub use` to work (`E0364`). Items that are not re-exported should use restricted visibility.

### `pub(crate)` at the top level

In top-level modules — those declared directly in `main.rs` or `lib.rs`, whether as `src/foo.rs` or `src/foo/mod.rs` — `pub(super)` and `pub(crate)` are identical because `super` _is_ the crate root. Use `pub(crate)` because it says what it actually means. This applies to both binary and library crates.

```rust
// src/constants.rs (direct child of main.rs or lib.rs)

pub(crate) const DEATH_VELOCITY_EPSILON: f32 = 0.001;
```

### `pub(super)` everywhere else

In nested modules (anything deeper than top-level), use `pub(super)` to scope items to the parent module subtree. `pub(crate)` is forbidden here because it bypasses module boundaries.

```rust
// actor/constants.rs (nested under actor/)

// Re-exported by parent with `pub use` → must be `pub`
pub struct Timer { ... }

// NOT re-exported, only used by sibling modules → `pub(super)`
pub(super) const DUPLICATE_OFFSET: f32 = 0.2;
```

```rust
// actor/mod.rs
pub use timer::Timer;
// DUPLICATE_OFFSET is not listed — it stays internal to actor/
```

`cargo mend` enforces this distinction.

### Structurally-used types

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

**Tooling:** `cargo mend` detects this as `suspicious_pub` (warning) and internal-only facades as `internal_parent_pub_use_facade` (warning). Run `cargo mend --fix-pub-use` to auto-fix stale `pub use` re-exports.
