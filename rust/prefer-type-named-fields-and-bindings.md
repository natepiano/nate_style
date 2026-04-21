---
date_created: "[[2026-04-17]]"
date_modified: "[[2026-04-21]]"
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

### Sweep satellite identifiers

Renaming a field under this rule leaves sibling code referencing the old term stale. Sweep in the same pass: helper functions over the same type (`outline_mode_label` → `outline_method_label`), adjacent bindings whose names carry the old term (`let outline_mode_name: &str = ...`), and format-string tokens. The rule applies to the original field; the meaning applies to the whole neighborhood of names that described it.
