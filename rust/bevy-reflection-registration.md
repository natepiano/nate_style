---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-04-29]]'
tags:
- bevy
- rust
mechanism: llm
pre_filter: '\.register_type::<'
---
## Bevy reflection registration

For non-generic types, deriving `Reflect` plus a reflection-kind attribute (`#[reflect(Component)]`, `#[reflect(Resource)]`, etc.) is sufficient. Bevy auto-registers them at startup. **Do not call `app.register_type::<X>()` manually for non-generic types.**

```rust
// good — derive + reflect-kind attribute is enough; auto-registration covers it
#[derive(Component, Reflect)]
#[reflect(Component)]
struct Health(f32);

// bad — redundant, auto-registration already handled it
app.register_type::<Health>();
```

### Components for BRP mutation

`#[reflect(Component)]` is all that is needed for BRP component mutation. It both marks the type as a Component for reflection and triggers auto-registration. Do not add ceremony beyond it.

### Generic types — the exception

Bevy cannot auto-register generic types because there is no concrete instantiation to register at startup. Manually register the concrete monomorphizations you actually use:

```rust
// good — concrete monomorphization, manual registration is required
app.register_type::<MyGenericComponent<f32>>();
app.register_type::<MyGenericComponent<u32>>();
```

### What the agent must not do

- Add `app.register_type::<MyComponent>()` for any non-generic type that derives `Reflect` — auto-registration covers it.
- Add additional registration calls or trait derivations beyond `#[reflect(Component)]` for BRP mutation.

See the `bevy_reflect` docs on auto-registration: https://docs.rs/bevy/latest/bevy/reflect/index.html