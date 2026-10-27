---
tier: C
family: values
input_scope: crate
date_created: '[[2026-03-29]]'
date_modified: "[[2026-10-27]]"
tags:
- patterns
- rust
mechanism: llm
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

Leave a plain two-way `if`/`else` that turns a `bool` into an enum where outside data enters, for example `impl From<bool> for TargetSupport`. That code is the boundary the type rules ask for, not a branch to fold.
