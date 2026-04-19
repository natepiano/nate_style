---
clippy: [manual_map, needless_collect, manual_find]
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- patterns
- rust
---
## Prefer functional patterns

Use combinators like `map_or_else` instead of `match`/`if let` when the arms are simple expressions.

```rust
// bad
let label = match result {
    Ok(val) => format!("found: {val}"),
    Err(e) => format!("error: {e}"),
};

// good
let label = result.map_or_else(|e| format!("error: {e}"), |val| format!("found: {val}"));
```