---
date_created: "[[2026-04-06]]"
date_modified: "[[2026-05-05]]"
see_also: "[[when-to-split-a-module]]"
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

### Surface

Applies to numerics, strings naming domain entities (file names like `Cargo.toml` / `mod.rs`, path keywords `crate` / `super` / `self`, cargo target kinds, subcommands, CLI flags), format-spec literals (`{name:<40}`), and meaning-bearing char/byte literals. A familiar word is not exempt — `"Cargo.toml"` belongs in `constants.rs` once, not at every call site.

Exceptions — leave in place:

- `impl Type { const FOO: ... = ...; }` — type-anchored, already named.
- Single-file binary targets (`examples/*.rs`, `benches/*.rs`, `build.rs`) — constants at the top of the file, after imports.
- `#[cfg(test)] mod tests` blocks (inline or as a sibling file) — constants at the top of the test module, after imports.
- Typed `const fn` factory aliases — `const X: T = T::factory_fn();` where the RHS is a self-naming `const fn` call with no literals (e.g. `PlatformShortcutMode::current()`). The factory call is already the name; binding it to a constant adds a layer without adding information. Inline the call at each use site.

Don't lift a literal from an exempt site. If a constant ends up with no caller outside exempt scopes, delete the constant — adding code to keep it referenced is evasion (see `agent-must-review-allows.md`).

### Don't promote a flat module just to add `constants.rs`

A flat `foo.rs` keeps its constants in the parent directory's `constants.rs`, as a peer file. Do not convert `foo.rs` into `foo/mod.rs` + `foo/constants.rs` solely to satisfy the constants-rs rule — promoting a flat file to a directory module requires 2+ of the criteria in [[when-to-split-a-module]], and the constants rule alone is not one of them.

```text
# bad — split exists only to host the constant
input/
  keybindings/
    mod.rs              # was keybindings.rs
    constants.rs        # holds the one moved const

# good — peer constants.rs in the existing directory module
input/
  constants.rs          # holds keybindings' constant (pub(super))
  keybindings.rs        # imports from sibling
```

## File organization

Group constants into related sections with a `//` comment title for each section. Sort sections alphabetically by section name. Within each section, sort constants alphabetically by name.

Use `//` plain comments for section headers. Write headers in lowercase (proper nouns excepted; acronyms are also lowercased — e.g. `// rtt`, `// sdf rendering`, `// msdf rasterization`) so they stand out as labels rather than reading like sentences. Use `///` doc comments on individual constants only when the value is not self-evident from the name.

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