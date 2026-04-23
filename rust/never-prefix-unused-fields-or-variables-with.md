---
clippy: ignored_unit_patterns
date_created: '[[2026-04-07]]'
date_modified: '[[2026-04-22]]'
tags:
- rust
- style
---
## Never prefix unused fields or variables with `_`

Remove unused items entirely instead of silencing the warning.

```rust
// bad
struct Drag {
    _offset: Vec2,
    active: bool,
}

// good — remove the unused field
struct Drag {
    active: bool,
}
```

**Exception — RAII guards:** When a binding exists solely for its `Drop` impl (timers, lock guards, temp files), `let _name = ...` is the correct Rust idiom. The underscore prefix suppresses `unused_variable` while keeping the value alive until scope exit. Do not remove the underscore — without it, `rustc` warns. Do not remove the name — `let _ = ...` drops the value immediately.

```rust
// good — _timer lives until end of scope, Drop prints elapsed time
let _timer = Timer::new("analyze");

// bad — drops immediately, timer measures nothing
let _ = Timer::new("analyze");

// bad — rustc warns "unused variable: timer"
let timer = Timer::new("analyze");
```

**Required-but-unused function parameters:** When a parameter must remain in a function signature (trait-impl defaults, callback signatures, or derive-macro hooks like `Deserialize::deserialize`), use bare `_` instead of `_name`. The type annotation sitting next to the underscore already identifies what is being ignored — the name would only restate the type in worse form.

```rust
// bad — leading underscore on a signature-required parameter
async fn handle_impl(&self, _params: Self::Params) -> Result<Self::Output> { ... }
fn deserialize<D>(_deserializer: D) -> Result<Self, D::Error> { ... }

// good — type annotation identifies what is being ignored
async fn handle_impl(&self, _: Self::Params) -> Result<Self::Output> { ... }
fn deserialize<D>(_: D) -> Result<Self, D::Error> { ... }
```

This applies regardless of function length — reviewers encounter the signature before the body, and the type is always visible.

**Exception — the ignored type is `()`:** When the required-but-unused parameter's type is the unit type, use the unit-destructuring pattern `()` instead of bare `_`. Clippy's `ignored_unit_patterns` lint (part of `clippy::pedantic`, denied in most workspaces) fires on `_: ()` and requires `(): ()`. This commonly shows up in trait impls whose associated type is bound to `()`:

```rust
// bad — fires clippy::ignored_unit_patterns
async fn load(&self, reader: &mut dyn Reader, _: &Self::Settings, ...) -> ... { ... }

// good — unit-destructuring pattern
async fn load(&self, reader: &mut dyn Reader, (): &Self::Settings, ...) -> ... { ... }
```

The bare-`_` prescription above still governs every non-unit case; the `()` pattern is specifically for the unit type, because destructuring `()` costs nothing and clippy considers it more explicit than `_` when the matched type is already unit.

**Exception — observer triggers:** Bevy observer functions require a trigger parameter for their signature even when the body doesn't use it. Prefer a descriptive name that communicates the event — e.g., `_drag`, `_added`, `_clear_selection`. A generic `_trigger` is acceptable but a meaningful name improves readability at the call site.

**Evaluation note:** Code matching the RAII guard exception above is conforming — do not count it as a finding.