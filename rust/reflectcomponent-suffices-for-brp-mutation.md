---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- bevy
- rust
---
## `#[reflect(Component)]` suffices for BRP mutation

For BRP component mutation, `#[reflect(Component)]` is all that is needed — it handles type registration.

```rust
#[derive(Component, Reflect)]
#[reflect(Component)]
struct Health(f32);
```