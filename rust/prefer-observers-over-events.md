---
date_created: '[[2026-03-30]]'
date_modified: '[[2026-03-30]]'
tags:
- bevy
- rust
---
## Prefer observers over events (consultation only)

> **Not a style-fix rule.** Whether an observer can replace an event/message depends on the concrete Bevy type (e.g. `Message` vs `Event` trait). This guideline must only be applied during interactive consultation with the user, never during automated style evaluation or style-fix processes.

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