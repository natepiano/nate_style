---
tags: [rust, patterns]
---

## Make functions `const fn` when possible

Mark functions `const fn` whenever the body permits it.

```rust
// bad
fn default_port() -> u16 {
    8080
}

// good
const fn default_port() -> u16 {
    8080
}
```
