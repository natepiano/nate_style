---
date_created: "[[2026-04-17]]"
date_modified: "[[2026-04-17]]"
group: structs
tags: [naming, rust]
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
