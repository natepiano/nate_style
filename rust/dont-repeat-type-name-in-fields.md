---
date_created: "[[2026-04-17]]"
date_modified: "[[2026-04-21]]"
see_also: "[[prefer-type-named-fields-and-bindings]]"
tags: [naming, rust]
---
## Don't repeat the type name in fields

The enclosing struct already provides the domain. Field names should describe the member, not restate the struct name.

```rust
// bad
struct Point {
    point_x: u32,
    point_y: u32,
}

// good
struct Point {
    x: u32,
    y: u32,
}
```

### Sweep satellite identifiers

After trimming the type prefix from a field, look for helpers and format tokens that still carry it: `point.point_x_delta()` or `format!("{point_x}")` next to a renamed `x` read as stale.
