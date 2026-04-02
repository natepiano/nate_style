---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-31]]'
tags:
- rust
- visibility
---
## Leaf module visibility

Items re-exported by the parent facade must be `pub` — Rust requires `pub` at the source for `pub use` to work (`E0364`). Items that are not re-exported should be `pub(super)`.

```rust
// leaf module (e.g. utils/timer.rs)

// Re-exported by parent with `pub use` → must be `pub`
pub struct Timer { ... }

// NOT re-exported, only used by sibling modules → `pub(super)`
pub(super) const DUPLICATE_OFFSET: f32 = 0.2;
```

```rust
// facade (e.g. utils/mod.rs)
pub use timer::Timer;
// DUPLICATE_OFFSET is not listed — it stays internal to utils/
```

When the parent module is itself private, bare `pub` in children is bounded by that privacy — so `pub` is acceptable if the parent re-exports it and external code uses it.

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

**Tooling:** `cargo mend` detects this as `suspicious_pub` (warning). Run `cargo mend --fix-pub-use` to auto-fix cases where a stale parent `pub use` can be removed.

### Top-level private module exception

Use `pub(super)` for items that are shared with sibling modules but are not intended for facade
re-export. This visibility is intentional documentation and should not be widened to bare `pub`
solely to satisfy Clippy's `redundant_pub_crate` lint.

This is especially relevant for modules declared directly under `lib.rs` or `main.rs` with `mod`,
not `pub mod`. In that layout, bare `pub` is still bounded by the non-public module boundary, but
it loses the semantic signal that the item is meant for sibling use rather than facade export.

Use allows sparingly. Prefer fixing the code over suppressing the lint. When an allow is truly
required, choose the smallest scope that keeps the code readable. Avoid repetitive per-item allows
when a single crate- or module-level allow better expresses an intentional architectural policy.

If `clippy::redundant_pub_crate` conflicts with this rule, prefer a crate-level allow in
`Cargo.toml` when the crate uses this visibility policy broadly. Use a module- or file-level allow
only when the exception is genuinely local, rather than widening the item visibility.
