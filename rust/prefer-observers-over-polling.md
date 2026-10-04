---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-10-04]]'
tags:
- bevy
- rust
mechanism: llm
mode: propose
---
## Prefer observers over polling

Use event-driven patterns instead of per-frame polling.

### Trigger at the authoritative source

Trigger the event once, in the deepest code that decides the state, and only
for the entities whose state changed. That emitter is the one authoritative
signal: no downstream system notices the change and triggers it again, and no
observer turns it into a second event for the same fact. Both directions are
events (off and on, dim and undim), each started by its own observer, and an
observer that often has nothing to do carries a run condition
(`extract-observer-run-conditions.md`).

```rust
// bad — a chain: a later system re-detects the change and re-emits it
fn read_switches(mut graph: ResMut<Graph>, ...) { graph.set_switched_off(off); }
fn notice_switches(graph: Res<Graph>, mut commands: Commands) {
    if graph.is_changed() { for tool in graph.switched_off() { commands.trigger(Dim(tool)); } }
}

// good — the code that decides the state emits it, once per changed tool
fn read_switches(mut graph: ResMut<Graph>, mut commands: Commands, ...) {
    for change in graph.set_switched_off(off) {
        commands.trigger(ToolSwitchChanged { tool: change.tool, state: change.state });
    }
}
```

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