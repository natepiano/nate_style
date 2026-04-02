---
date_created: '[[2026-04-02]]'
date_modified: '[[2026-04-02]]'
tags:
- rust
- visibility
---
## Use directory modules for modules with children

If a module has submodules, put its root in `module/mod.rs`. Do not use `module.rs` alongside a sibling `module/` directory.

```text
# bad
src/tui/detail.rs
src/tui/detail/model.rs

# good
src/tui/detail/mod.rs
src/tui/detail/model.rs
```
