---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-04-25]]'
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

### Exception: racing a deferred-producer sibling

`On<Add, T>` fires synchronously at command-flush, before any later
system runs. If the reaction needs a sibling resource that another
producer creates *after* the insert, the observer wins the race and
sees nothing. Canonical case: `commands.spawn((Window, Marker))` —
`bevy_winit` creates the OS-level `NSWindow`/`HWND` later, so an
`On<Add, Marker>` observer that touches the OS handle gets `None`.
Poll `Added<Marker>` in the stage where the producer has run.