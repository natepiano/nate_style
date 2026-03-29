---
tags: [rust, style]
---

## Inline variables in format strings

Use inline variable names, not positional arguments. Field accesses and method calls cannot be inlined — use `{}` for those.

```rust
// bad
format!("Element index: {}", index)

// good
format!("Element index: {index}")

// field access — cannot inline, {} is correct
format!("failed to read {}", path.display())
format!("module `{}` not found", candidate.module_name)
```
