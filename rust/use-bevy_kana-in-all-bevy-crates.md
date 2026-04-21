---
clippy: [cast_precision_loss, cast_possible_truncation, cast_sign_loss, cast_possible_wrap]
date_created: '[[2026-04-07]]'
date_modified: '[[2026-04-07]]'
tags:
- bevy
- rust
---
## Use `bevy_kana` in all Bevy crates

All Bevy crates should depend on `bevy_kana`.

**Exception:** If a crate has no possible uses of the `bevy_kana` public API (no spatial math, no numeric casts, no input macros), skip the dependency.

**`bevy_kana` is an internal dependency.** Library crates must never leak `bevy_kana` types through their public API.

### Public API boundary

Only standard types cross the public API boundary (`pub` struct fields, `pub` fn args/returns, `pub use` re-exports):

- **Struct fields**: `Vec3`, not `Position`
- **Function args**: `impl Into<Vec3>`
- **Return types**: `Vec3`
- **Never** `pub use` re-export bevy_kana types

**Why `impl Into<Vec3>` on args.** `bevy_kana::Position` (and its siblings) implement `From<Position> for Vec3` (via `Deref`-free conversion) and `From<Vec3> for Position`. Accepting `impl Into<Vec3>` at the boundary means callers who already work in `bevy_kana` newtypes can pass them directly — no `*position` dereferencing, no visible bridging — while callers who work in `Vec3` pass them unchanged. The public signature stays newtype-free and callers on either side pay nothing.

### Prefer `impl Into<Vec3>` over `const fn` at the public boundary

On public constructors and public free functions, an `impl Into<Vec3>` parameter is more valuable than `const fn` usability. `From::from` is not `const fn` on stable, so the two are mutually exclusive — and most public constructors aren't called from `const` contexts anyway.

Default to dropping `const` to gain the `impl Into<Vec3>` affordance. Keep `const fn` only when the constructor is actually used inside a `const` expression (associated `const` items, array initializers, `static`s) — and in those rare cases, take `Vec3` directly.

```rust
// good — public API takes impl Into<Vec3>, drops const
impl Anchor {
    pub fn new(position: impl Into<Vec3>) -> Self {
        Self { position: position.into(), direction: None }
    }
}

// also good — const fn kept because it's used in a const expression elsewhere
impl Obstacle {
    pub const fn unit_at_origin() -> Self {
        Self { half_extents: Vec3::splat(0.5), position: Vec3::ZERO, rotation: Quat::IDENTITY }
    }
}
```

See `prefer-from-impl-over-named-constructors.md` for the `const fn` / `From` tension in the general case.

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