---
date_created: '[[2026-06-01]]'
date_modified: '[[2026-06-01]]'
tags:
- bevy
- rust
mechanism: llm
mode: propose
---
## Extract observer guards into run conditions

Observers support `.run_if(...)` (bevy `0.19.0-rc.2`+, `ObserverSystemExt` in
prelude). When an observer opens with a world-state guard that early-returns,
propose lifting it into a condition so the body is the action, not the gate.

```rust
// before: guard buried in body
fn on_select(t: On<Select>, mode: Res<EditMode>, mut c: Commands) {
    if !mode.is_editing() { return; }
    c.entity(t.target()).insert(Highlight);
}
// after
world.add_observer(on_select.run_if(|mode: Res<EditMode>| mode.is_editing()));
```

### Only extract — and only when equivalent

- Conditions take no event input: guards reading the trigger/event
  (`if t.button != Left`) stay in the body. Only resource/state/component
  guards move.
- The guard must be a pure read-only early return — no `else`, no work on the
  skipped path, no mutation.
- Chained `.run_if(a).run_if(b)` does not short-circuit (keeps `Changed<T>`
  ticks live); don't split one decision across closures.

Propose per candidate; relocating a one-liner that doesn't clarify intent is
churn.
