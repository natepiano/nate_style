---
tags: [rust, bevy]
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
