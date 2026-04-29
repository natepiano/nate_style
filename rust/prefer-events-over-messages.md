---
date_created: '[[2026-03-30]]'
date_modified: '[[2026-04-28]]'
tags:
- bevy
- rust
mechanism: llm
mode: propose
pre_filter: '\bMessage(Reader|Writer)<'
---
## Prefer events over messages

In current Bevy (0.18+), the **`Event`** / **`EntityEvent`** trait pairs with observers and fires synchronously — the reaction runs immediately at command-flush, in the same frame. The **`Message`** trait (pre-0.17 "events" pattern, read via `MessageReader`) is polled per-frame and runs whenever the consuming system happens to schedule. Default to events with observers; reach for messages only when there is a clear batch or timing requirement.

```rust
// bad — message polling: handler runs whenever the consuming system schedules
fn handle_click(mut reader: MessageReader<ClickMessage>) {
    for msg in reader.read() { /* ... */ }
}

// good — observer fires synchronously at command-flush
app.add_observer(on_click);
fn on_click(trigger: Trigger<ClickEvent>, mut commands: Commands) { /* ... */ }
```

### Exceptions — when messages are still right

- **Batch accumulation** — many items pile up per frame and batch iteration in a single system pass is genuinely simpler than per-item observer dispatch.
- **Timing requirement** — the reaction must run in a specific schedule slot, not synchronously at the producer's command-flush.

Both cases require weighing tradeoffs (synchrony vs. batching, latency vs. ordering). This is why the rule is `mode: propose` — the LLM should surface candidate sites for the user to weigh in on, never auto-rewrite a `MessageReader` into an observer.