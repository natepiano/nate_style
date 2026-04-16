---
date_created: '[[2026-04-15]]'
date_modified: '[[2026-04-15]]'
tags:
- rust
- api
- non-negotiable
---
## Public API changes require explicit approval

Style fixes, cleanup, and refactors must preserve the existing public API unless the user explicitly asks for or approves a breaking change.

Public API includes:
- exported types, functions, methods, constants, modules, fields, and re-exports
- trait impl availability that downstream code depends on
- constructor and builder entry points
- unit-struct plugin usage and other documented call shapes
- examples and README snippets presented as supported usage

If satisfying another style rule would require changing that surface, stop and ask instead of recommending or applying the breaking change.

Prefer API-preserving remediations:
- private wrapper types or plugins behind the existing entry points
- internal helper extraction or inlining
- facade-preserving delegation
- keeping documented/example call sites valid while restructuring internals

```rust
// bad — style refactor silently changes the public entry point
app.add_plugins(WindowManagerPlugin);
// becomes
app.add_plugins(WindowManagerPlugin::new());

// good — keep the public API, hide the refactor internally
pub struct WindowManagerPlugin;

impl Plugin for WindowManagerPlugin {
    fn build(&self, app: &mut App) {
        app.add_plugins(WindowManagerPluginCustomPath::default());
    }
}
```
