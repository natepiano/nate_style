---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-04-06]]'
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
fn on_health_depleted(trigger: Trigger<HealthDepleted>, mut commands: Commands) {
    commands.entity(trigger.target()).despawn();
}
```