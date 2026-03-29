---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- bevy
- rust
---
## Bundles are deprecated — use required components

Adding `Transform` automatically adds `GlobalTransform`. Spawn components directly.

```rust
// bad — bundle struct
commands.spawn(SpriteBundle { transform, ..default() });

// good — required components handle the rest
commands.spawn((Sprite::default(), transform));
```