---
tags: [rust, visibility]
---

## No `pub(crate)` in nested modules

`pub(crate)` is only acceptable at **crate root** in **library crates** to keep items out of the external API. Everywhere else, use `pub(super)` or bare `pub` with facade re-exports.

```rust
// bad — nested module using pub(crate)
// selection/operations/helpers.rs
pub(crate) fn build_label() -> String { ... }

// good — use pub(super), let parent facade control exposure
pub(super) fn build_label() -> String { ... }
```
