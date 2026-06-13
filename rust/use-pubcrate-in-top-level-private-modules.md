---
date_created: '[[2026-04-10]]'
date_modified: '[[2026-05-14]]'
see_also: "leaf-module-visibility, [[use-narrowest-visibility]]"
tags:
- rust
- visibility
mechanism: mend
mode: auto
lint: narrow_to_pub_crate
---
## Use `pub(crate)` in top-level private modules

In top-level modules — those declared directly in `main.rs` or `lib.rs`, whether as `src/foo.rs` or `src/foo/mod.rs` — items that are not re-exported by the crate root should use `pub(crate)` instead of bare `pub`.

At this level, `pub(super)` and `pub(crate)` are identical because `super` _is_ the crate root. Use `pub(crate)` because it says what it actually means. This applies to both binary and library crates.

Items that _are_ re-exported via `pub use` in `lib.rs` or `main.rs` must stay `pub` — Rust requires `pub` at the source to be at least as wide as any re-export (`E0364`).

```rust
// src/lib.rs
mod helpers;
pub use helpers::exported_fn;

// src/helpers.rs

// Re-exported by lib.rs → must be `pub`
pub fn exported_fn() {}

// NOT re-exported → use `pub(crate)`
pub(crate) fn internal_fn() {}

pub(crate) const DEATH_VELOCITY_EPSILON: f32 = 0.001;
```

Bare `pub` in this position is misleading — it suggests the item is part of the public API when it is not.

This is the top-level instance of the general rule: pick the narrowest modifier that the actual re-export allows. The same principle extends to nested modules — see [[use-narrowest-visibility]].