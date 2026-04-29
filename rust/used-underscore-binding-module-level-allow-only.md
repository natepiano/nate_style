---
date_created: '[[2026-04-10]]'
date_modified: '[[2026-04-29]]'
see_also: "[[agent-must-review-allows]]"
tags:
- lints
- rust
mechanism: clippy
mode: propose
lint: used_underscore_binding
---
## `used_underscore_binding` — module-level allow only

Clippy fires false positives on macro-expanded code where derive macros (e.g. Bevy's `Reflect`, `Component`, observer macros) generate underscore-prefixed bindings that the expansion then uses. Common on enum variant fields like `Routed { planner: Planner }`. Suppress it with an inner `#![allow(...)]` at the top of the file that triggers it — never in `Cargo.toml`. Promote to a parent `mod.rs` only when two or more sibling submodules would each need the same allow.

```rust
// good — inner allow in the file that triggers it
// src/panel/modes.rs
#![allow(clippy::used_underscore_binding, reason = "false positive on enum variant fields")]
```

### Exception: single-file crate roots

For single-file crate roots — `examples/*.rs`, `src/bin/*.rs`, `benches/*.rs`, and standalone binaries with no submodules — a crate-level `#![allow]` at the top of the file is the accepted form. These files are intentional single-file demonstrations; splitting them into submodules purely to scope this allow fights what the file is.

```rust
// good — crate-root allow on a single-file example
#![allow(clippy::used_underscore_binding, reason = "false positive on enum variant fields")]

// ...the rest of examples/foo.rs...
```

Do **not** wrap the file body in an inline `mod foo { ... }` block to "move the allow off the crate root" — that narrows nothing in practice and adds an indentation layer to the whole file.
