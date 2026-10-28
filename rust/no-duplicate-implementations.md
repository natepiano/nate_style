---
tier: C
family: types
input_scope: crate
mechanism: llm
mode: propose
date_created: "[[2026-10-27]]"
date_modified: "[[2026-10-27]]"
see_also:
  - "[[one-mechanism-per-behavior]]"
  - "[[no-magic-values]]"
tags: [rust, types]
---
## No duplicate implementations

Each behavior has one implementation. A second copy of logic, a type, a helper or a data table that already exists is a defect, even when each copy works. Reuse or extend the existing one.

Two near-copies that differ only in data become one function over that data. Two types with the same fields and meaning become one type.

```rust
// bad: the same clamp in two places
fn clamp_zoom(z: f32) -> f32 { z.max(MIN_ZOOM).min(MAX_ZOOM) }
fn limit_zoom(z: f32) -> f32 { z.clamp(MIN_ZOOM, MAX_ZOOM) }

// good: one implementation, used by every caller
fn clamp_zoom(zoom: f32) -> f32 { zoom.clamp(MIN_ZOOM, MAX_ZOOM) }
```

Before adding code, search for an existing implementation of the same behavior. Never add a second one to avoid changing the first. Changing the first is the fix.
