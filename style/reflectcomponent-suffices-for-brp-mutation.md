---
tags: [rust, bevy]
---

## `#[reflect(Component)]` suffices for BRP mutation

For BRP component mutation, `#[reflect(Component)]` is all that is needed — it handles type registration.

```rust
#[derive(Component, Reflect)]
#[reflect(Component)]
struct Health(f32);
```
