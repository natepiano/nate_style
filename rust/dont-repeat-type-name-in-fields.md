---
date_created: "[[2026-03-31]]"
date_modified: "[[2026-03-31]]"
tags:
  - rust
  - naming
---
## Don't repeat the type name in fields

When every field in a struct shares a common prefix or suffix, the repetition adds noise without information — the struct name already provides that context. Name fields for what they hold, not what they belong to.

```rust
// bad — every field ends with _count
struct Summary {
    error_count:   usize,
    warning_count: usize,
    fixable_count: usize,
}

// good — the struct name provides context
struct Summary {
    errors:   usize,
    warnings: usize,
    fixable:  usize,
}
```

This is enforced by `clippy::struct_field_names`. If serialization requires specific key names, use `#[serde(rename = "...")]` rather than baking wire-format names into the Rust API.
