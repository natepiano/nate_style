---
date_created: "[[2026-04-05]]"
date_modified: "[[2026-04-17]]"
tags: [naming, rust]
---
## Name bindings to match parameters they feed

When a local binding is converted and passed directly as a function argument, name it after the parameter it becomes — not the source type it came from. This suppresses editor inlay hints and makes the conversion read naturally.

```rust
// bad — binding named after source type, editor shows inlay hint "actor_kind:"
for (portal, deaderoid) in portals_query.iter() {
    Boundary::draw_portal(
        ...,
        deaderoid.map_or(PortalActorKind::Nateroid, |_| PortalActorKind::Deaderoid),
    );
}

// good — binding named after the parameter it becomes
for (portal, actor_kind) in portals_query.iter() {
    Boundary::draw_portal(
        ...,
        actor_kind.map_or(PortalActorKind::Nateroid, |_| PortalActorKind::Deaderoid),
    );
}
```
