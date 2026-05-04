---
date_created: "[[2026-04-17]]"
date_modified: "[[2026-05-04]]"
tags: [naming, rust]
mechanism: llm
---
## Avoid repeated field affixes

When sibling fields all repeat the same prefix or suffix, the repetition adds noise without information.

```rust
// bad
struct Summary {
    error_count: usize,
    warning_count: usize,
}

// good
struct Summary {
    errors: usize,
    warnings: usize,
}
```

If wire-format names require repetition, use `#[serde(rename = "...")]` instead of baking it into the Rust API.

### Exception: unit suffixes

Unit suffixes (`_ms`, `_seconds`, `_bytes`) may repeat on raw numeric fields — the suffix carries unit info that would be lost if dropped.

```rust
struct PerfSnapshot {
    frame_ms:  f32,
    update_ms: f32,
}
```

### Sweep satellite identifiers

After dropping an affix, check helper methods, constructor params, and format tokens that still carry it: `errors_count_total()` alongside a renamed `errors` field, or `format!("{error_count}")` tokens, all go stale.
