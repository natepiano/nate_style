---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-05-04]]'
tags:
- imports
- rust
mechanism: llm
---
## Import external-crate paths at the top, including `std::`

External-crate paths — `std::`, `core::`, third-party — get a `use` at the top
and bare names at the call site, same as intra-crate paths. Covers types
(`ratatui::Frame`), trait paths in `impl Trait for Type`
(`crate::pane::Hittable`), and enum variants
(`notify::WatcherKind::NullWatcher` → `use notify::WatcherKind;` +
`WatcherKind::NullWatcher`).

```rust
// before
fn count(m: &std::collections::HashMap<String, i32>) -> usize { m.len() }

// after
use std::collections::HashMap;
fn count(m: &HashMap<String, i32>) -> usize { m.len() }
```

Skipped when the import would shadow a name already in use (e.g. `Result::ok`
on prelude `Result` blocks `use io::Result;`).

**Tooling:** `cargo mend` detects this as `inline_path_qualified_type` (warning).
Run `cargo mend --fix` to auto-fix.
