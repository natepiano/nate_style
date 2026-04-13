---
date_created: '[[2026-04-10]]'
date_modified: '[[2026-04-10]]'
group: visibility
tags:
- rust
- visibility
---
## No `pub(crate)` in nested modules

`pub(crate)` is acceptable in top-level modules (direct children of `main.rs` or `lib.rs`) where it says exactly what it means. In nested modules, use `pub(super)` or bare `pub` with facade re-exports — `pub(crate)` bypasses module boundaries.

```rust
// bad — nested module using pub(crate)
// selection/operations/helpers.rs
pub(crate) fn build_label() -> String { ... }

// good — use pub(super), let parent facade control exposure
pub(super) fn build_label() -> String { ... }
```

### When bare `pub` is required

`pub(super)` cannot be re-exported at wider visibility (E0364). If the parent facade re-exports an item as `pub(crate) use`, the source must be bare `pub`. The same applies to types that appear as fields of such structs (`private_interfaces`).

```rust
// keyboard/keys.rs — re-exported by mod.rs as pub(crate) use
pub fn send_keys_handler(...) { ... }        // must be pub (E0364)

// keyboard/keys.rs — NOT re-exported, only used within keyboard/
pub(super) struct SendKeysRequest { ... }    // pub(super) is correct
```

**Tooling:** `cargo mend` detects this as `forbidden_pub_crate` (error).