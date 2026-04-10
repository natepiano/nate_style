---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-04-01]]'
tags:
- bevy
- rust
---
## Type registration is automatic

Bevy registers non-generic reflected types automatically. Do not call `register_type` manually
for non-generic types.

Generic types are the exception: register the concrete monomorphized instantiations you actually
use. See the `bevy_reflect` docs on auto registration:
https://docs.rs/bevy/latest/bevy/reflect/index.html

```rust
// bad — non-generic type
app.register_type::<MyComponent>();

// good — just derive `Reflect`
#[derive(Component, Reflect)]
struct MyComponent;

// good — generic concrete instantiation
app.register_type::<MyGenericComponent<f32>>();
```