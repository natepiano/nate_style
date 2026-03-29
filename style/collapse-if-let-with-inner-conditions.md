---
tags: [rust, patterns]
---

## Collapse `if let` with inner conditions

When an `if let` immediately contains another `if`, merge them with `&&`.

```rust
// bad
if let Some(rect) = cache.scan_log {
    if rect.contains(pos) {
        handle_click(rect);
    }
}

// good
if let Some(rect) = cache.scan_log
    && rect.contains(pos)
{
    handle_click(rect);
}
```
