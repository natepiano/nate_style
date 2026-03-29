---
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