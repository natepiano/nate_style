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

This part applies to Bevy 0.20.1; in 0.19.1 a panic does not reach the error handler.
For a fallible Bevy system, return `bevy::ecs::error::Result` and use `?` to convert `anyhow::Error` to `BevyError`.
Call `App::set_error_handler` once in the app to report unhandled system failures; a second call panics.
A system panic also reaches that handler: if `error.take_payload()` returns a payload, call `std::panic::resume_unwind(payload)` first.
A handler that only logs hides each system panic.
Otherwise log the error with `{:?}` to include the cause chain, at the level of `error.severity()`.
Log `Severity::Panic` with `error!`: an error converted by `?` has that severity unless `with_severity` sets another.
With this handler, a system that returns an error is logged and the app continues; only a real panic stops the app.
Do not end propagation with `.ok()` or a `warn!` or `error!` call that prints only the outer message.

```rust
fn report_system_error(mut error: BevyError, context: ErrorContext) {
    if let Some(payload) = error.take_payload() {
        std::panic::resume_unwind(payload);
    }
    error!("{context}: {error:?}");
}
```
