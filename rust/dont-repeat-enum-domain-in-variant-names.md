---
date_created: "[[2026-04-17]]"
date_modified: "[[2026-04-17]]"
group: enums
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
