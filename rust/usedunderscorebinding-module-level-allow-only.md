---
clippy: used_underscore_binding
date_created: '[[2026-04-10]]'
date_modified: '[[2026-04-10]]'
group: allows
tags:
- lints
- rust
---
## `used_underscore_binding` — module-level allow only

Clippy fires false positives on enum variant fields (e.g., `Routed { planner: Planner }`). When this happens, suppress it on the `mod` declaration in the parent module — never in `Cargo.toml`.

```rust
// good — scoped to the module that triggers it
#[allow(clippy::used_underscore_binding, reason = "false positive on enum variant fields")]
mod enums;
```

See `~/rust/bevy_catenary/src/routing/mod.rs` and `~/rust/bevy_catenary/src/plugin/mod.rs` for examples.

**Agent rule:** The agent must not add this allow without user review, even for known false positives. See `agent-must-review-allows.md`.