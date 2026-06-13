---
date_created: "[[2026-04-17]]"
date_modified: '[[2026-06-12]]'
see_also: "[[prefer-type-named-fields-and-bindings]]"
tags: [naming, rust]
mechanism: llm
candidates:
  kind: field_affixes
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

### Exception: stable config keys

Fields may repeat a prefix when they intentionally mirror stable config keys or diagnostic names, such as `allow_pub_mod` and `allow_pub_items`.

### Exception: counts in mixed structs

A repeated `_count` suffix is information-bearing when the enclosing struct also stores non-count fields and dropping it would make the name read as the items being counted, not the count.

### Exception: type-named fields

Fields may repeat a suffix when the full name is the snake_case form of the stored type and reads naturally, such as `visibility_config: VisibilityConfig`.
If removing the shared affix would break a type-named field, keep the type-named field.

### Exception: state-specific value kinds

Fields may repeat a suffix when siblings store the same value kind in different states and trimming the suffix leaves relation-only names (`current`, `previous`, `last_in_window`); prefer renaming the enclosing type before deleting the value kind.

```rust
// bad
struct MouseTracker { current: Vec2, previous: Vec2 }

// good
struct MouseTracker { current_position: Vec2, previous_position: Vec2 }
```

### Exception: context-preserving identifiers

Keep the affix when dropping it leaves a generic field whose meaning is not clear from the enclosing type. Two patterns:

- **Disambiguating from sibling concerns:** `WatchInfo { watch_id }`, not `WatchInfo { id }`, when nearby code also handles entity IDs, task IDs, ports, or log paths.
- **Preserving value-kind on typed wrappers:** `FrameMetrics { frame_elapsed: Duration }`, not `FrameMetrics { frame: Duration }`, when the bare noun reads as the thing measured rather than the measurement of it. Same applies to `_at` / `_deadline` on `Instant`/`SystemTime` fields.

### Sweep satellite identifiers

After dropping an affix, check helper methods, constructor params, and format tokens that still carry it: `errors_count_total()` alongside a renamed `errors` field, or `format!("{error_count}")` tokens, all go stale.
