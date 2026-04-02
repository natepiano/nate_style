---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
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

**Tooling:** `cargo mend` detects this as `prefer_module_import` (warning). Run `cargo mend --fix` to auto-fix by replacing function imports with module imports and qualifying call sites.