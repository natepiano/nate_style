---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- patterns
- rust
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