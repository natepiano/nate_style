---
date_created: '[[2026-04-10]]'
date_modified: '[[2026-04-10]]'
group: import-style
tags:
- imports
- rust
---
## Import the module for functions, not the function itself

Free functions are called as `module::function()` so the origin is clear at the call site.

```rust
// bad
use crate::brp_tools::execute_brp_method;

let result = execute_brp_method(method, params, port).await?;

// good
use crate::brp_tools;

let result = brp_tools::execute_brp_method(method, params, port).await?;
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

**Tooling:** `cargo mend` detects this as `prefer_module_import` (warning). Run `cargo mend --fix` to auto-fix by replacing function imports with module imports and qualifying call sites.