---
date_created: "[[2026-04-06]]"
date_modified: "[[2026-05-02]]"
see_also: "[[constants-file-organization]]"
tags: [constants, rust]
mechanism: llm
---
## No magic values

Place all constants in `constants.rs` with descriptive names. When a module is a directory (e.g., `toasts/`), its constants belong in its own `constants.rs`, not in the parent's.

```rust
// bad
if port == 15702 { ... }

// good — in constants.rs
pub(super) const DEFAULT_BRP_PORT: u16 = 15702;

// good — at call site
if port == DEFAULT_BRP_PORT { ... }
```

Exceptions — leave in place:

- `impl Type { const FOO: ... = ...; }` — type-anchored, already named.
- Single-file binary targets (`examples/*.rs`, `benches/*.rs`) — constants at the top of the file, after imports.
- `#[cfg(test)] mod tests` blocks (inline or as a sibling file) — constants at the top of the test module, after imports.