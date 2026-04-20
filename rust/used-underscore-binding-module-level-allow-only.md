---
clippy: used_underscore_binding
date_created: '[[2026-04-10]]'
date_modified: '[[2026-04-19]]'
see_also: "[[agent-must-review-allows]]"
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

### Exception: single-file crate roots

For single-file crate roots — `examples/*.rs`, `src/bin/*.rs`, `benches/*.rs`, and standalone binaries with no submodules — a crate-level `#![allow]` at the top of the file is the accepted form. These files are intentional single-file demonstrations; splitting them into submodules purely to scope this allow fights what the file is.

```rust
// good — crate-root allow on a single-file example
#![allow(clippy::used_underscore_binding, reason = "false positive on enum variant fields")]

// ...the rest of examples/foo.rs...
```

Do **not** wrap the file body in an inline `mod foo { ... }` block to "move the allow off the crate root" — that narrows nothing in practice and adds an indentation layer to the whole file.

**Agent rule:** The agent must not add this allow without user review, even for known false positives. See `agent-must-review-allows.md`.