---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-04-24]]'
tags:
- bevy
- rust
---
## Prefer observers over polling

Use event-driven patterns instead of per-frame polling.

```rust
// bad — runs every frame checking for changes
fn check_health(query: Query<&Health>) {
    for health in &query {
        if health.current == 0 { despawn_entity(); }
    }
}

// good — fires only when the event occurs
fn on_health_depleted(trigger: On<HealthDepleted>, mut commands: Commands) {
    commands.entity(trigger.target()).despawn();
}
```

### Exception: `Changed<T>` for in-place mutation

Observers fire on lifecycle (`Add`/`Insert`/`Replace`/`Remove`) and
explicit triggers — not on `Query<&mut C>` edits. Keep `Changed<T>`
for inspector-style mutation and for values written by another
schedule (e.g. `GlobalTransform`). Do **not** rewrite
`Changed<C>` into `On<Insert/Replace, C>`: it silently drops `&mut`
edits.