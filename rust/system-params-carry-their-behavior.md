---
date_created: "[[2026-08-17]]"
date_modified: "[[2026-08-17]]"
tags:
  - bevy
  - rust
mechanism: llm
mode: propose
---
## SystemParam bundles carry their behavior

A `#[derive(SystemParam)]` struct earns its place when its impl is the last stop for its fields —
callers get back a resolved `Entity`, `Rect`, or `bool` and never touch a raw `Query`. A bundle
whose consumer unpacks it field by field into another function has only relocated the arity: the
params reappear one level down, and `#[allow(clippy::too_many_arguments)]` with them.

```rust
// before: a private helper already takes the bundle by reference
fn finalize_widget_anchor_state(
    demands: &Query<&AnchoredHere>, attachments: &Query<&AnchoredTo>, /* three more */
    panel: Entity, commands: &mut Commands,
) { ... }

// after: that signature was the struct
#[derive(SystemParam)]
struct PanelAnchorParticipation<'w, 's> { demands: Query<..>, attachments: Query<..>, /* three more */ }

impl PanelAnchorParticipation<'_, '_> {
    fn finalize(&self, panel: Entity, commands: &mut Commands) { ... }
}
```

### Where to look

- A helper already takes the params by reference — whoever wrote that signature already found the
  bundle. Strongest signal, and the only one that fires when no two systems share a param block.
  Drop `Commands` from that signature first; fewer than two params left and it stays a helper.
- Two or more systems running the same call sequence on the same params.
- One system past roughly eight params, where some subset of them is a coherent concept.

### Not a bundle

The module's central resource plus `Commands` recurring across systems — that is what every system
in the module looks like, not a concept. A narrowly-used param has to anchor the set. Counting
decides nothing in either direction: a one-field bundle with five callers can carry real behavior,
and a hub type shared by nine systems carries none. An impl with no callers is speculative API.

### Bounds

Keep `Commands` out of the bundle when a `&mut self` method would collide with a live field borrow;
take it as an argument. A `SystemParam` cannot be built from `&World`, so a test calling the old
free function becomes a one-shot system. Give the bundle its own module once its consumers span
files — otherwise leave it beside them.
