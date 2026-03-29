---
tags: [rust, patterns]
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
fn on_health_depleted(trigger: Trigger<HealthDepleted>, mut commands: Commands) {
    commands.entity(trigger.target()).despawn();
}
```
