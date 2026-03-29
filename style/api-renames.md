---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- bevy
- rust
---
## API renames

Use the current names — the old forms no longer exist.

```rust
// bad → good
time.delta_seconds()    // → time.delta_secs()
time.elapsed_seconds()  // → time.elapsed_secs()
Parent                  // → ChildOf(Entity), access via .parent()
dir3.into()             // → dir3.as_vec3()   (Dir3 → Vec3)
ChildBuilder            // → ChildSpawnerCommands
e.despawn_descendants() // → e.despawn_children()
e.clear_children()      // → e.detach_all_children()
```