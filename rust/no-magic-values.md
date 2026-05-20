---
date_created: "[[2026-04-06]]"
date_modified: "[[2026-05-20]]"
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

Applies to numerics, project/domain strings, cargo target kinds, subcommands, CLI flags, format-spec literals (`{name:<40}`), and meaning-bearing char/byte literals — **in expression position only**.

Numerics in **type position** — `[T; N]` array dimensions, `T<N>` const generics — are out of scope: they are structural facts about another type (`Vec3` → `[_; 3]`, `Mat4` → `[_; 16]`, `[u8; 32]` from `Sha256::Output`), not domain values. Leave them inline.

Exceptions — leave in place:

- Fixed Rust/tooling syntax spellings that cannot vary — `"Cargo.toml"`, `"mod.rs"`, `"crate"`, `"super"`, `"self"` — stay inline. A constant only helps when the value can change, is project-specific, or carries non-obvious policy.
- `impl Type { const FOO: ... = ...; }` — type-anchored, already named.
- Single-file binary targets (`examples/*.rs`, `benches/*.rs`, `build.rs`) — constants at the top of the file, after imports.
- `#[cfg(test)] mod tests` blocks (inline or as a sibling file) — constants at the top of the test module, after imports.
- `include_str!` / `include_bytes!` path literals, including wrapper macros like Bevy's `embedded_asset!` — Rust requires literal paths; do not duplicate them in `constants.rs`.
- Typed `const fn` factory aliases — `const X: T = T::factory_fn();` where the RHS is a self-naming `const fn` call with no literals (e.g. `PlatformShortcutMode::current()`). The factory call is already the name; binding it to a constant adds a layer without adding information. Inline the call at each use site.
- English connectives and pluralization labels used in description-builder chains. Strings like `.text("and")`, `.text("for")`, or a `Phrase::File(1) => "file"` arm returning `"file"` / `"files"` are grammatical glue between domain words, not domain entities — leave inline at the call site.
- Match arms that pair an enum variant with a short label, where the match is the only consumer of those labels. Example: `impl Phrase { fn pluralize(&self) { match self { Self::File(1) => "file", Self::File(_) => "files", … } } }`. The match is the dictionary for the enum; lifting each label to `constants.rs` creates names with no caller outside the match.
- Init/identity literals — values dictated by the operation, not the domain: counter starts (`0`), single steps (`+= 1`, `- 1`, `+ 1`), origins (`Vec3::new(0.0, y, 0.0)`), arithmetic identities (`len - 1`, `pct / 100.0`). Test: would changing the value change *intent*, or just break the math? If the latter, leave inline. Do not lift to `FRAME_COUNTER_START = 0`, `COUNT_INCREMENT = 1`, `ZERO_F64 = 0.0`, `ORIGIN_X = 0.0`, `ONE_HUNDRED_PERCENT = 100.0`, `SAMPLE_INDEX_OFFSET = 1`.
- Range start of `0` — `0..n` stays inline. Do not write `T::MIN..n` (e.g. `u32::MIN..rows`) to dodge the literal; the substitution is a longer way to write `0`.
- Format strings — keep inline as `format!("...{x:.1}")`. Do not lift to `const FMT: &str = "...{x}"` and rewrite the call site as `FMT.replace("{x}", &format!("{:.1}", x))` — slower, less type-safe, no clearer.

Don't lift a literal from an exempt site. If a constant ends up with no caller outside exempt scopes, delete the constant — adding code to keep it referenced is evasion (see `agent-must-review-allows.md`).

### One value per meaning, one constant

Same value + same meaning → one definition. If two modules need it, lift to the parent `constants.rs` and import from there.

Same value + distinct domains (`DEFAULT_VOLUME: f32 = 1.0`, `IDENTITY_SCALE: f32 = 1.0`) → keep separate; the name carries the domain that the value alone does not.

Don't add `_TEXT` / `_SINGULAR` / `_VALUE` to manufacture a second name for an existing value — rename the existing one if it doesn't fit.

`&str` is the default; never suffix `_STR`. Add a `_CHAR` companion only when a `char` is genuinely needed at a call site (e.g. `s.starts_with(PIPE_CHAR)`).

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

Rustfmt does not reorder constants. On insert, re-verify the section is alphabetical end-to-end — do not trust visual placement near similar prefixes.

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
