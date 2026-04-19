---
clippy: [redundant_closure, redundant_closure_for_method_calls]
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- patterns
- rust
---
## Avoid redundant closures

Pass method references directly instead of wrapping them in a closure.

```rust
// bad
let names: Vec<_> = items.iter().map(|item| item.name()).collect();

// good
let names: Vec<_> = items.iter().map(Item::name).collect();
```

For `&str` → `String` conversions, use `String::from` rather than a closure or a fully-qualified trait path.

```rust
// bad — redundant closure
.map(|s| s.to_string())

// bad — unnecessarily verbose
.map(std::string::ToString::to_string)

// good
.map(String::from)
```