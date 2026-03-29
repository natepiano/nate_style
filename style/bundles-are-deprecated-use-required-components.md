---
tags: [rust, bevy]
---

## Bundles are deprecated — use required components

Adding `Transform` automatically adds `GlobalTransform`. Spawn components directly.

```rust
// bad — bundle struct
commands.spawn(SpriteBundle { transform, ..default() });

// good — required components handle the rest
commands.spawn((Sprite::default(), transform));
```
