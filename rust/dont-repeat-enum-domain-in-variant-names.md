---
date_created: "[[2026-04-17]]"
date_modified: '[[2026-06-12]]'
tags: [naming, rust]
mechanism: llm
candidates:
  kind: enum_variant_stutter
---
## Don't repeat the enum domain in variant names

The enum name already provides the domain. Variants should name the state or choice within that domain.

```rust
// bad
enum FluctuationEnabled {
    Enabled,
    Disabled,
}

// good
enum FluctuationMode {
    Enabled,
    Disabled,
}
```

### Exception: fixed compound terms

Keep the domain word when removing it would break an established compound term (`GameState::InGame`, `GameState::GameOver`, `TeleportStatus::JustTeleported`); otherwise keep variants state-only (`UploadStatus::Failed`, not `UploadStatus::UploadFailed`).

### Sweep satellite identifiers

Renaming the enum leaves bindings, field types, and helpers that embedded the old name stale: `set_fluctuation_enabled(...)` or a field `fluctuation_enabled: FluctuationMode` still carries the dropped term.
