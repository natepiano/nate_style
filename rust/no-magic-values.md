---
date_created: "[[2026-04-06]]"
date_modified: "[[2026-05-03]]"
tags: [constants, rust]
mechanism: llm
---
## No magic values

Place all constants in `constants.rs` with descriptive names. When a module is a directory (e.g., `toasts/`), its constants belong in its own `constants.rs`, not in the parent's.

```rust
// bad
if port == 15702 { ... }

// good — in constants.rs
pub(super) const DEFAULT_BRP_PORT: u16 = 15702;

// good — at call site
if port == DEFAULT_BRP_PORT { ... }
```

Exceptions — leave in place:

- `impl Type { const FOO: ... = ...; }` — type-anchored, already named.
- Single-file binary targets (`examples/*.rs`, `benches/*.rs`, `build.rs`) — constants at the top of the file, after imports.
- `#[cfg(test)] mod tests` blocks (inline or as a sibling file) — constants at the top of the test module, after imports.

## File organization

Group constants into related sections with a `//` comment title for each section. Sort sections alphabetically by section name. Within each section, sort constants alphabetically by name.

Use `//` plain comments for section headers. Write headers in lowercase (proper nouns excepted) so they stand out as labels rather than reading like sentences. Use `///` doc comments on individual constants only when the value is not self-evident from the name.

Rustfmt does not reorder constants, so alphabetical order must be maintained manually.

Cross-cutting sections (e.g., "Actor physics velocity limits" spanning multiple entity types) are fine when the grouping adds clarity.

```rust
// bad -- unsorted sections, mixed concerns
pub(super) const SPACESHIP_MASS: f32 = 10.0;
pub(super) const MISSILE_SCALE: f32 = 2.5;
pub(super) const SPACESHIP_HEALTH: f32 = 5000.0;
pub(super) const MISSILE_MASS: f32 = 0.1;

// good -- sections with comment titles, sorted alphabetically
// Missile constants
pub(super) const MISSILE_MASS: f32 = 0.1;
pub(super) const MISSILE_SCALE: f32 = 2.5;

// Spaceship constants
pub(super) const SPACESHIP_HEALTH: f32 = 5000.0;
pub(super) const SPACESHIP_MASS: f32 = 10.0;

// good -- doc comment on a non-obvious value
// Nateroid constants
pub(super) const NATEROID_COLLIDER_MARGIN: f32 = 1.0 / 3.0;
/// Vertical vibration runs 30% faster than lateral, creating non-repeating
/// patterns.
pub(super) const NATEROID_VIBRATION_SPEED_MULT: f32 = 1.3;
```