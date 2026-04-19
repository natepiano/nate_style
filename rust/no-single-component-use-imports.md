---
clippy: single_component_path_imports
date_created: "[[2026-04-19]]"
date_modified: "[[2026-04-19]]"
group: import-style
tags: [imports, rust]
---
## No single-component `use` imports

A crate declared in `Cargo.toml` (or any other single-component path in scope) is already reachable by its root name from every file in the crate. Writing `use foo;` on its own line adds nothing and is rejected by `clippy::single_component_path_imports`.

```rust
// bad — redundant, clippy will reject
use syn;

let syntax = syn::parse_file(&text)?;

// good — just call through the crate name
let syntax = syn::parse_file(&text)?;
```

### Interaction with [[import-the-module-for-functions-not-the-function-itself]]

The module-import rule says to call free functions as `module::function()` rather than importing the free function directly. For items inside a crate the canonical form is `use crate::some_module;` + `some_module::function(...)`. For an **external crate's root**, there is no local `use` to write — the crate name is already the module, so call `external_crate::function(...)` inline.

```rust
// bad — redundant use plus module-qualified call
use syn;
let file = syn::parse_file(&text)?;

// bad — aliases the crate just to satisfy the module-import rule
use syn as syn_module;
let file = syn_module::parse_file(&text)?;

// good — no use line; crate name is already reachable
let file = syn::parse_file(&text)?;
```

### Tooling

`clippy::single_component_path_imports` is part of `clippy::all` (default warn; denied in most projects via workspace lints). When it fires, the fix is always to delete the offending `use` line — never to add an `#[allow]`.
