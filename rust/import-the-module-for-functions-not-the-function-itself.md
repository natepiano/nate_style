---
date_created: '[[2026-04-10]]'
date_modified: '[[2026-04-10]]'
group: import-style
tags:
- imports
- rust
---
## Import the module for functions, not the function itself

**IMPORTANT:** Review the Tooling section at the end before making changes for this guideline.

Free functions are called as `module::function()` so the origin is clear at the call site.

```rust
// bad
use crate::brp_tools::execute_brp_method;

let result = execute_brp_method(method, params, port).await?;

// good
use crate::brp_tools;

let result = brp_tools::execute_brp_method(method, params, port).await?;
```

Inline qualified paths like `super::task::run()` or `crate::module::run()` are not the preferred form when a local module import would be clear. Import the module at the top of the file, then call the function through that import.

```rust
// bad — inline qualified path instead of a module import
let result = super::task::start_entity_watch_task(entity, types, port).await?;

// good
use super::task;

let result = task::start_entity_watch_task(entity, types, port).await?;
```

When the module is a grandparent peer (would require `super::super::`), use `crate::` for the module import instead. See `prefer-local-relative-imports.md` for why.

```rust
// bad — super::super:: for the module import
use super::super::render;

render::format_bytes(bytes);

// good — crate:: path for grandparent peers
use crate::tui::render;

render::format_bytes(bytes);
```

**Tooling:** `cargo mend` detects this as `prefer_module_import` (warning). First run `cargo mend` and evaluate what it reports for this rule. If `cargo mend` indicates that a fix is available, you may then run `cargo mend --fix` and review the resulting changes to confirm it fixed this issue correctly before making any manual edits.
