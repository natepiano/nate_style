---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-04-06]]'
tags:
- bevy
- rust
---
## Use `bevy_kana` in all Bevy crates

All Bevy crates should depend on `bevy_kana`.

**`bevy_kana` is an internal dependency.** Library crates must never leak `bevy_kana` types through their public API.

### Public API boundary

Only standard types cross the public API boundary (`pub` struct fields, `pub` fn args/returns, `pub use` re-exports):

- **Struct fields**: `Vec3`, not `Position`
- **Function args**: `impl Into<Vec3>`
- **Return types**: `Vec3`
- **Never** `pub use` re-export bevy_kana types

### Internal code

Internal functions use bevy_kana newtypes freely. Use `impl Into<Position>` for parameters so callers can pass either `Vec3` or `Position` without manual wrapping. Return newtypes directly — callers dereference (`*position`) when storing into a public `Vec3` field.

```rust
// internal — accepts Vec3 or Position, returns Position
pub(crate) fn lerp_focus(from: impl Into<Position>, to: impl Into<Position>) -> Position {
    let from = from.into();
    let to = to.into();
    // ...
}

// caller stores into public Vec3 field
pan_orbit.focus = *lerp_focus(pan_orbit.focus, pan_orbit.target_focus);
```

### Semantic math newtypes

Use `Position`, `Displacement`, `Velocity` for internal struct fields where the semantic meaning matters. Leave as `Vec3`: scale, direction vectors, AABB extents, math locals, `const` context.

### Numeric cast traits

Use `ToF32`, `ToI32`, `ToU32`, `ToUsize` instead of `as` casts with `#[allow(clippy::cast_*)]`.

### Input macros (binaries only)

The `input` feature reduces `bevy_enhanced_input` boilerplate: `action!`, `event!`, `bind_action_system!`, `Keybindings` builder. See `~/rust/nateroids/` for reference.
