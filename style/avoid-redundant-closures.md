---
tags: [rust, patterns]
---

## Avoid redundant closures

Pass method references directly instead of wrapping them in a closure.

```rust
// bad
let names: Vec<_> = items.iter().map(|item| item.name()).collect();

// good
let names: Vec<_> = items.iter().map(Item::name).collect();
```
