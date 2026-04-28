---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-04-27]]'
tags:
- patterns
- rust
mechanism: clippy
mode: auto
lint: [redundant_closure, redundant_closure_for_method_calls]
---
## Avoid redundant closures

This rule is clippy-owned. Do not raise findings by visual inspection — if clippy does not fire, the closure is not redundant. In particular, `|x| x.method()` is **not** redundant when `method` is reached via `Deref` (e.g. a newtype wrapper around `Vec3` with no inherent `length` method); there is no `Wrapper::method` reference to substitute.

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