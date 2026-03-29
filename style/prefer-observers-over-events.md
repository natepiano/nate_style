---
tags: [rust, bevy]
---

## Prefer observers over events

Use observers paired with `Event` / `EntityEvent`. Only reach for events with `EventReader` when there is a clear batch or timing requirement.

```rust
// bad — default to message-style event reading
fn handle_click(mut reader: EventReader<ClickEvent>) {
    for event in reader.read() { /* ... */ }
}

// good — observer fires per-event automatically
app.add_observer(on_click);
fn on_click(trigger: Trigger<ClickEvent>, mut commands: Commands) { /* ... */ }
```
