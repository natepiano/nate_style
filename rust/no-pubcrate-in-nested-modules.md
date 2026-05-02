---
date_created: '[[2026-04-10]]'
date_modified: '[[2026-05-02]]'
see_also: "[[leaf-module-visibility]]"
tags:
- rust
- visibility
mechanism: mend
mode: flag
lint: forbidden_pub_crate
---
## No `pub(crate)` in nested modules

`pub(crate)` is acceptable at depth ≤ 2 from the crate root (`crate::foo` or `crate::foo::bar` under a private parent) where the surrounding privacy already walls the item off. At depth 3+, use `pub(super)` or bare `pub` with facade re-exports — `pub(crate)` bypasses module boundaries.

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