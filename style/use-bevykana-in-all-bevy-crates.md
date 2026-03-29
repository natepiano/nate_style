---
tags: [rust, bevy]
---

## Use `bevy_kana` in all Bevy crates

All Bevy crates should depend on `bevy_kana`. It provides three categories of utilities.

### Semantic math newtypes

Use `Position`, `Displacement`, and `Velocity` instead of raw `Vec3` for struct fields and function signatures where the semantic meaning is clear.

```rust
// bad — what does this Vec3 represent?
pub struct Portal {
    pub position: Vec3,
}

// good — self-documenting
pub struct Portal {
    pub position: Position,
}
```

Newtypes act like `Vec3` through `Deref` — `.x`, `.length()`, `.normalize()` all work. Use `*position` to extract the inner `Vec3` at Bevy API boundaries (e.g., `Transform::from_trs`).

Leave as `Vec3`: scale values, direction vectors, AABB extents, internal math locals, and anything used in `const` context.

See `~/rust/nateroids/` and `~/rust/bevy_catenary/` for reference implementations.

### Numeric cast traits

Use `ToF32`, `ToI32`, `ToU32`, `ToUsize` instead of bare `as` casts with `#[allow(clippy::cast_*)]`.

```rust
// bad — scattered allow annotations
#[allow(clippy::cast_precision_loss)]
let t = i as f32 / n as f32;

// good — intent is explicit, allow is centralized in bevy_kana
let t = i.to_f32() / n.to_f32();
```

These traits replace the following clippy allows:

| Clippy lint | bevy_kana trait |
|---|---|
| `cast_precision_loss` | `ToF32` |
| `cast_possible_truncation` | `ToI32`, `ToU32`, `ToUsize` |
| `cast_sign_loss` | `ToU32`, `ToUsize` |
| `cast_possible_wrap` | `ToI32` |

### Input macros (binaries only)

The `input` feature (opt-in, not default) reduces `bevy_enhanced_input` boilerplate.

**`action!` replaces the three-line derive pattern:**

```rust
// before — repeated for every action
#[derive(InputAction)]
#[action_output(bool)]
pub struct CameraHome;

// after
action!(CameraHome);
```

**`event!` generates a BRP-compatible event:**

```rust
// before
#[derive(Event, Reflect, Default)]
#[reflect(Event)]
pub struct PauseEvent;

// after
event!(PauseEvent);

// also supports payload fields
event!(ZoomToTarget { entity: Entity });
```

**`bind_action_system!` wires an action → event → command in one line:**

```rust
// before — manual observer boilerplate
app.add_observer(
    |_: On<Start<PauseSwitch>>, mut commands: Commands| {
        commands.trigger(PauseEvent::default());
    },
)
.add_observer(|_: On<PauseEvent>, mut commands: Commands| {
    commands.run_system_cached(pause_command);
});

// after
bind_action_system!(app, PauseSwitch, PauseEvent, pause_command);
```

The intermediate event decouples input from commands, making commands triggerable via BRP's `world.trigger_event`.

**`Keybindings` builder** handles modifier keys and platform differences (Cmd vs Ctrl):

```rust
use bevy_kana::Keybindings;

let kb = Keybindings::new::<ShiftModifier>(ctx, settings);
kb.spawn_key::<CameraHome>(ctx, KeyCode::F12);
kb.spawn_shift_key::<InspectCamera>(ctx, KeyCode::KeyC);
kb.spawn_platform_key::<Save>(ctx, KeyCode::KeyS); // Cmd+S on macOS, Ctrl+S elsewhere
```
