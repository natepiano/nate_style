---
date_created: '[[2026-04-10]]'
date_modified: '[[2026-05-14]]'
see_also: "[[leaf-module-visibility]]"
tags:
- rust
- visibility
mechanism: mend
mode: auto
lint: [forbidden_pub_crate, narrow_to_pub_crate]
---
## Use the narrowest visibility that compiles

Pick the modifier that tells a reader the item's effective reach at a glance, and that is as restrictive as Rust allows given how the item is actually re-exported. From tightest to loosest:

1. **no modifier** (private to the module) — only used inside this file
2. **`pub(super)`** — siblings inside the parent module use it; nothing else
3. **`pub(crate)`** — the parent facade re-exports it as `pub(crate) use`; reach is crate-wide and explicitly capped there
4. **`pub`** — there is an unbroken chain of `pub use` from the crate root, i.e. it is part of the library's external API

The rule for picking is mechanical: choose the narrowest modifier that still compiles given the actual re-export. Rust's E0364 caps this from below — a re-export cannot be wider than the source — so the parent's `pub(crate) use` forces the source to be at least `pub(crate)`, never narrower.

### Why `pub(crate)` at depth 3+ when the parent re-exports it that way

When the immediate parent module is declared `mod foo;` (private) — and it always is, because `pub mod` is forbidden by [[never-use-pub-mod]] — the long path `crate::foo::child::Item` is unreachable from outside `foo`'s subtree regardless of whether `Item` is `pub` or `pub(crate)`. The private `mod child;` declaration gates the path. So at depth 3+, `pub(crate)` and `pub` at the source site have identical effective reach. The difference is what the modifier communicates: `pub(crate)` says "at most crate-internal, definitely," while bare `pub` requires the reader to walk back up the module tree to learn the answer. The narrower modifier wins.

```rust
// keyboard/keys.rs — re-exported by mod.rs as `pub(crate) use`
pub(crate) fn send_keys_handler(...) { ... }   // tells you the cap at a glance

// keyboard/keys.rs — NOT re-exported, only used within keyboard/
pub(super) struct SendKeysRequest { ... }       // siblings only
```

```rust
// keyboard/mod.rs
mod keys;
pub(crate) use keys::send_keys_handler;
```

### When bare `pub` is required at depth 3+

Only when the item is on a `pub use` chain that reaches the crate root — i.e. it is part of the library's external API. In a binary crate, bare `pub` should essentially never appear at any depth.

### Examples of incorrect visibility

```rust
// bad — overly wide at depth 3+ when nothing re-exports it
// selection/operations/helpers.rs
pub(crate) fn build_label() -> String { ... }

// good — siblings-only, no re-export
pub(super) fn build_label() -> String { ... }
```

```rust
// bad — bare pub when parent caps at pub(crate)
// keyboard/keys.rs
pub fn send_keys_handler(...) { ... }
// keyboard/mod.rs
pub(crate) use keys::send_keys_handler;

// good — modifier matches the cap
// keyboard/keys.rs
pub(crate) fn send_keys_handler(...) { ... }
```

`cargo mend` enforces both directions: it flags `pub(crate)` that should be `pub(super)` (no re-export above it) and bare `pub` that should be `pub(crate)` (parent re-exports as `pub(crate) use`).