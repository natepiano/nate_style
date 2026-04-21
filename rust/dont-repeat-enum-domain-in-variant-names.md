---
date_created: "[[2026-04-17]]"
date_modified: "[[2026-04-21]]"
tags: [naming, rust]
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

### Sweep satellite identifiers

Renaming the enum leaves bindings, field types, and helpers that embedded the old name stale: `set_fluctuation_enabled(...)` or a field `fluctuation_enabled: FluctuationMode` still carries the dropped term.
