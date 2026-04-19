---
date_created: "[[2026-04-17]]"
date_modified: "[[2026-04-19]]"
tags: [naming, rust]
---
## Prefer type-named fields and bindings

When a field or local binding stores a value of some type, prefer the snake_case form of that type name when it reads naturally.

```rust
// bad
struct SomeStruct {
    mode: ChangeMode,
}

let cfg = ValidatedConfig::default();

// good
struct SomeStruct {
    change_mode: ChangeMode,
}

let validated_config = ValidatedConfig::default();
```
