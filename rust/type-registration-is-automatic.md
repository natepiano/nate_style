---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- bevy
- rust
---
## Type registration is automatic

Bevy registers types automatically. Do not call `register_type` manually.

```rust
// bad
app.register_type::<MyComponent>();

// good — just derive Reflect
#[derive(Component, Reflect)]
struct MyComponent;
```