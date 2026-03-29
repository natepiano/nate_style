---
tags: [rust, patterns]
---

## Use a context struct when arguments exceed 7

When a function accumulates too many parameters, group related arguments into a struct. Bevy systems are exempt (they require owned params), but all other code should refactor.

```rust
// bad — too many loose arguments
fn render_child_item(
    app: &App,
    project: &RustProject,
    name: &str,
    disk_width: usize,
    ci_width: usize,
    origin_width: usize,
    sync_width: usize,
    lang_width: usize,
) -> ListItem<'static> { /* ... */ }

// good — related arguments grouped
struct ColumnWidths {
    disk:   usize,
    ci:     usize,
    origin: usize,
    sync:   usize,
    lang:   usize,
}

fn render_child_item(
    app: &App,
    project: &RustProject,
    name: &str,
    widths: &ColumnWidths,
) -> ListItem<'static> { /* ... */ }
```
