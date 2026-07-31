---
date_created: '[[2026-04-10]]'
date_modified: '[[2026-07-30]]'
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
2. **`pub(super)`** — siblings inside the parent module use it; nothing else. Not the parent's re-export of it — see the `pub(super) use` case below
3. **`pub(crate)`** — the parent facade re-exports it as `pub(crate) use`; reach is crate-wide and explicitly capped there
4. **`pub`** — either the item is on an unbroken `pub use` chain from the crate root (part of the library's external API), or the parent facade re-exports it as `pub(super) use`, which leaves no narrower modifier that compiles

The rule for picking is mechanical: choose the narrowest modifier that still compiles given the actual re-export. Rust's E0364 caps this from below — a re-export cannot be wider than the source — so the parent's `pub(crate) use` forces the source to be at least `pub(crate)`, never narrower.

### Why `pub(crate)` at depth 3+ when the parent re-exports it that way

When the immediate parent module is declared `mod foo;` (private) — and it always is, because `pub mod` is forbidden by never-use-pub-mod — the long path `crate::foo::child::Item` is unreachable from outside `foo`'s subtree regardless of whether `Item` is `pub` or `pub(crate)`. The private `mod child;` declaration gates the path. So at depth 3+, `pub(crate)` and `pub` at the source site have identical effective reach. The difference is what the modifier communicates: `pub(crate)` says "at most crate-internal, definitely," while bare `pub` requires the reader to walk back up the module tree to learn the answer. The narrower modifier wins.

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

Two cases, and only these two.

**The item is on a `pub use` chain that reaches the crate root** — it is part of the library's external API.

**The parent facade re-exports it as `pub(super) use`**, carrying it up to the grandparent but no further. Here every narrower modifier is unavailable: `pub(super)` at the declaration is narrower than the parent's own re-export of it and fails E0364, while `pub(crate)` and `pub(in path)` are both forbidden by policy. That leaves `pub`, which is not a widening — the private `mod` chain still caps the real reach, and the facade's `use` line is where a reader learns how far it goes.

```rust
// video_plane/plane/camera_panel.rs — parent carries it up one level
pub fn bind_fed_panels_to_producer_materials(...) { ... }

// video_plane/plane/mod.rs
mod camera_panel;
pub(super) use camera_panel::bind_fed_panels_to_producer_materials;  // the cap lives here

// video_plane/mod.rs — the consumer, one level above `plane`
```

In a binary crate, bare `pub` should otherwise essentially never appear at any depth.

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

`cargo mend` enforces every direction of this rule, and which way it points depends entirely on how the parent re-exports the item:

| Parent's re-export | Correct declaration | If you write `pub(crate)` |
|---|---|---|
| none | `pub(super)` | `forbidden_pub_crate` fires |
| `pub(super) use` | `pub` | `forbidden_pub_crate` fires — and `pub(super)` will not compile |
| `pub(crate) use` | `pub(crate)` | accepted |
| `pub use` to crate root | `pub` | `narrow_to_pub_crate` fires the other way, on bare `pub` |

The middle row is the one that reads as a contradiction if you only see the diagnostic: mend rejects `pub(crate)` and Rust rejects `pub(super)`, so `pub` is correct by elimination.

**Tooling:** `cargo mend` detects this as `forbidden_pub_crate` (error) and `narrow_to_pub_crate` (warning). Run `cargo mend --fix` to auto-fix `narrow_to_pub_crate`; `forbidden_pub_crate` is fix-manually.