---
tier: C
family: types
input_scope: crate
mechanism: llm
mode: propose
see_also: "[[public-failures-return-named-errors]]"
tags: [rust, types]
date_created: "[[2026-11-19]]"
date_modified: "[[2026-11-19]]"
---
## App Errors Carry Context With anyhow

Use `anyhow::Result` in the app crate to propagate crate failures to the report.
At each level, add `.context(...)` or `.with_context(...)` to identify the operation that failed.
For library errors, see [[public-failures-return-named-errors]].

```rust
// Bad
fn load_scene(path: &Path) -> Option<Scene> {
    scene_store::load(path).ok()
}

// Good
use anyhow::Context;

fn load_scene(path: &Path) -> anyhow::Result<Scene> {
    scene_store::load(path).with_context(|| format!("load scene {}", path.display()))
}
```

For a fallible Bevy system, return `bevy::ecs::error::Result` and use `?` to convert `anyhow::Error` to `BevyError`.
Call `App::set_error_handler` once in the app to report unhandled system failures.
Log the error with `{:?}` in that handler to include the cause chain.
Do not end propagation with `.ok()` or a `warn!` or `error!` call that prints only the outer message.
