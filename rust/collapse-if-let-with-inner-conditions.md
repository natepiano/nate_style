---
clippy: [collapsible_if, collapsible_match]
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- patterns
- rust
---
## Collapse `if let` with inner conditions

When an `if let` block contains **only** another `if` (no sibling statements), merge them with `&&`.

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

### Exception: outer `if let` with an `else` branch

Do not collapse when the outer `if let` has its own `else`. Merging the inner condition with `&&` routes the "pattern matched, inner condition was false" case into the `else` — silent behavior change, not a refactor.

```rust
// bad — collapse would change semantics
if let Some(mut r) = cached {
    if r.value != pos {
        r.value = pos;
    }
} else {
    commands.insert(new_component(pos));
}
```

Here `Some` + `value == pos` is a no-op in the original. Collapsed with `&&`, it falls into the `else` and re-inserts on every tick where the value is unchanged. Leave the nested form, or restructure with a `match` + guards if the nesting bothers you:

```rust
match cached {
    Some(mut r) if r.value != pos => r.value = pos,
    Some(_) => {}
    None => commands.insert(new_component(pos)),
}
```

Clippy's `collapsible_if` already declines to suggest the collapse in this shape; if you find yourself overriding it by hand, that's the signal.