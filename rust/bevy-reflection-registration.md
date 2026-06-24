---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-06-23]]'
tags:
- bevy
- rust
mechanism: llm
candidates:
  kind: regex
  pattern: '\.register_type::<'
---
## Bevy reflection registration

For non-generic types, `#[derive(Reflect)]` plus a reflection-kind attribute (`#[reflect(Component)]`, `#[reflect(Resource)]`, …) is enough — Bevy auto-registers them at startup (`reflect_auto_register`, a default feature). **Never call `app.register_type::<X>()` for a non-generic type.** `#[reflect(Component)]` alone also satisfies BRP component mutation; add nothing beyond it.

```rust
#[derive(Component, Reflect)]
#[reflect(Component)]
struct Health(f32);          // registered automatically

app.register_type::<Health>(); // bad — redundant
```

### Generic types — the only exception

Auto-registration cannot see generic types; register each concrete monomorphization you use:

```rust
app.register_type::<MyComponent<f32>>();
```
