---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- rust
- style
---
## Omit `return` in expression position

Rust's last expression is the return value. Never use explicit `return` in match arms, closures, or final expressions.

```rust
// bad
match origin {
    Some(url) => return format_url(url),
    None => return String::new(),
}

// good
match origin {
    Some(url) => format_url(url),
    None => String::new(),
}
```