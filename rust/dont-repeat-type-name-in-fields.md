---
date_created: "[[2026-04-17]]"
date_modified: "[[2026-05-20]]"
trigger_test: "field name begins with snake_case of struct name, not merely a shared domain word"
see_also: "[[prefer-type-named-fields-and-bindings]]"
tags: [naming, rust]
mechanism: llm
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

### When this rule fires

A field triggers this rule only when its name begins with the snake_case form of the enclosing struct's name (or a leading word thereof, when that word is the struct's primary noun — e.g. `Point` for `Point2D`, `Window` for `WindowConfig`).

Sharing a domain word with the struct is **not** enough. If the field name is the snake_case of its *type* and that string is not also the snake_case of the struct, the type-named form wins per [[prefer-type-named-fields-and-bindings]].

```rust
// good — `outline_method` is snake_case of the field's type (`OutlineMethod`),
// not snake_case of the struct's name (`outline_mode_toggle`). Sharing the
// word "outline" with the struct is incidental.
struct OutlineModeToggle {
    outline_method: OutlineMethod,
}

// bad — `outline_mode_toggle_method` would restate the struct's full name.
// (Hypothetical — included to show what the rule actually targets.)
```

### Exception: transparent collection wrappers

A one-field collection wrapper may use the collection noun when generic names would lose meaning: `struct ImageLinks { links: Vec<ImageLink> }`.

This does not allow repeating the full type name: `image_links`.

### Exception: context-preserving member names

Keep the repeated word when the enclosing type names a broader operation or container, not the field's specific role: `ViewportProjection { viewport_rect: Rect }`, not `rect`.

### Sweep satellite identifiers

After trimming the type prefix from a field, look for helpers and format tokens that still carry it: `point.point_x_delta()` or `format!("{point_x}")` next to a renamed `x` read as stale.
