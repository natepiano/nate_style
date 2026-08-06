---
date_created: '[[2026-04-10]]'
date_modified: '[[2026-08-06]]'
tags:
- rust
- visibility
mechanism: mend
mode: auto
lint: [overbroad_pub_crate, forbidden_pub_in_crate, narrow_to_pub_crate]
---
## Use the narrowest visibility that compiles

Pick the modifier that tells a reader the item's effective reach at a glance, and that is as restrictive as Rust allows given how the item is actually re-exported. From tightest to loosest:

1. **no modifier** (private to the module) — only used inside this file
2. **`pub(super)`** — siblings inside the parent module use it; nothing else. Not the parent's re-export of it — see the `pub(super) use` case below
3. **`pub(in crate::path)`** — declarations only, when a parent facade re-exports the item as `pub(super) use`; the path names the facade's parent boundary
4. **`pub(crate)`** — the parent facade re-exports it as `pub(crate) use`; reach is crate-wide and explicitly capped there
5. **`pub`** — the item is on an unbroken `pub use` chain from the crate root and is part of the library's external API

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

**The item is on a `pub use` chain that reaches the crate root** — it is part of the library's external API.

A declaration carried by a reachable public signature must also remain bare `pub`, even without a crate-root re-export chain.

The `pub(super) use` facade case does not require bare `pub`: use the exact `pub(in crate::path)`
rung below instead.

### When a `pub(super) use` facade needs `pub(in crate::path)`

Reach for `pub(in crate::path)` in exactly one situation: a parent module re-exports a declaration
with `pub(super) use`, which puts the declaration's required reach above the module it lives in.
`pub(super)` at the declaration is too narrow to compile; `pub` is wider than the truth.

```rust
// video_plane/plane/camera_panel.rs — parent carries it up one level
pub(in crate::video_plane) fn bind_fed_panels_to_producer_materials(...) { ... }

// video_plane/plane/mod.rs
mod camera_panel;
pub(super) use camera_panel::bind_fed_panels_to_producer_materials;

// video_plane/mod.rs — the consumer, one level above `plane`
```

The item lives in `video_plane::plane::camera_panel` and the facade lives in
`video_plane::plane`, so the path is `crate::video_plane`: the parent of the module holding the
facade, not one level above the item. It is two levels above `camera_panel`. With chained facades,
find the widest facade and use the parent of the module holding it; the distance can grow beyond
two levels. The path names who can see the item, not who owns it.

`pub(super)` on the declaration would only make it visible to `plane`, but the facade's
`pub(super) use` must be visible to `video_plane`. Rust rejects that wider re-export with E0364.
Bare `pub` compiles, but promises more access than the relationship requires; the exact
`pub(in crate::video_plane)` boundary tells the reader where access stops.

Always spell the path from `crate::`. `pub(in super::super)` can compile to the same boundary, but
requires counting levels and changes meaning when the file moves.

This is declarations only. A `use` line selects its own reach, so `pub(super)`, `pub(crate)`, and
`pub` already cover the reaches it can need. A field cannot be re-exported, so no facade can
justify `pub(in crate::path)` on a field.

Do not use this form to avoid moving an item. A long path, or a path through a module unrelated to
the item, says the item belongs elsewhere. It never widens access: `pub(in crate::a)` is narrower
than `pub(crate)` and `pub`. If it seems to unlock access, the intended decision may be a
`pub(crate) use` facade, which belongs on the `use` line.

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
| none | `pub(super)` | `overbroad_pub_crate` fires |
| `pub(super) use` | `pub(in crate::<facade parent>)` | fires — and `pub(super)` will not compile |
| `pub(crate) use` | `pub(crate)` | accepted |
| `pub use` to crate root | `pub` | does not compile — a bare `pub use` requires the declaration to be `pub` |

The `pub(super) use` row is the only case for this restricted path. Configure
`pub_in_path = "permitted"` or `"required"` (the default) to accept the exact boundary.

**Tooling:** `cargo mend` reports `overbroad_pub_crate` and `narrow_to_pub_crate` as warnings, and
`forbidden_pub_in_crate` as an error. Run `cargo mend --fix` to apply supported visibility rewrites.
