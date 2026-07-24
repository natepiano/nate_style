---
date_created: "[[2026-04-06]]"
date_modified: "[[2026-07-24]]"
see_also:
  - "[[when-to-split-a-module]]"
  - "[[constants-file-organization]]"
tags: [constants, rust]
mechanism: llm
---
## No magic values

Place all constants in `constants.rs` with descriptive names. When a module is a directory (e.g., `toasts/`), its constants belong in its own `constants.rs`, not in the parent's. For how to lay that file out, see [[constants-file-organization]].

```rust
// bad
if port == 15702 { ... }

// good — in constants.rs
pub(super) const DEFAULT_BRP_PORT: u16 = 15702;

// good — at call site
if port == DEFAULT_BRP_PORT { ... }
```

### The test

**Would changing the value change intent, or just break the math?** Intent → name it. Math → leave it inline.

That settles most literals that look magic and are not: counter starts (`0`), single steps (`+= 1`, `len - 1`), origins (`Vec3::new(0.0, y, 0.0)`), percentage divisors (`pct / 100.0`), range starts (`0..n`), and array dimensions or const generics in **type position** — `[u8; 32]` from `Sha256::Output`, `Vec3` → `[_; 3]`, `Mat4` → `[_; 16]`. Those last are structural facts about another type, not domain values.

Never invent a name to dodge a literal: no `FRAME_COUNTER_START = 0`, no `ONE_HUNDRED_PERCENT = 100.0`, and no `u32::MIN..rows` standing in for `0..rows` — that substitution is a longer way to write `0`.

### Surface

Applies to numerics, project/domain strings, cargo target kinds, subcommands, CLI flags, format-spec literals (`{name:<40}`), and meaning-bearing char/byte literals — **in expression position only**.

Exempt sites — leave the literal in place:

- **Fixed syntax spellings** that cannot vary — `"Cargo.toml"`, `"mod.rs"`, `"crate"`, `"super"`, `"self"`. A constant helps only when the value can change, is project-specific, or carries non-obvious policy.
- **`impl Type { const FOO: ... = ...; }`** — type-anchored, already named.
- **`#[cfg(test)] mod tests`** blocks, inline or as a sibling file — constants at the top of the test module, after imports.
- **Single-file binary targets** (`examples/*.rs`, `benches/*.rs`, `build.rs`) — constants at the top of the file, after imports. If the file is divided into banner-delimited subsystem sections (CAMERA / GROUND / GIZMO), each section's constants go at the top of the section that owns them instead, just above that section's types: a reader meeting `AXIS_LABEL_OFFSET` wants the gizmo context first. Constants-at-top stays the rule for genuinely single-subsystem files.
- **`include_str!` / `include_bytes!` path literals**, including wrapper macros like Bevy's `embedded_asset!` — Rust requires literal paths; do not duplicate them in `constants.rs`.
- **Typed `const fn` factory aliases** — `const X: T = T::factory_fn();` where the RHS is a self-naming `const fn` call with no literals (e.g. `PlatformShortcutMode::current()`). The call is already the name; inline it at each use site.
- **Grammatical glue** — English connectives and pluralization labels in description-builder chains (`.text("and")`, `.text("for")`, a `Phrase::File(1) => "file"` arm). This extends to any match arm pairing an enum variant with a short label where the match is that label's only consumer: the match is the dictionary for the enum, and lifting each arm to `constants.rs` creates names with no caller outside the match.
- **Format strings** — keep `format!("...{x:.1}")` inline. Do not lift to `const FMT: &str` and rewrite the call site as `FMT.replace("{x}", &format!("{:.1}", x))` — slower, less type-safe, no clearer.

Don't lift a literal out of an exempt site. If a constant ends up with no caller outside exempt scopes, delete it — adding code to keep it referenced is evasion (see `agent-must-review-allows.md`).

### One value per meaning, one constant

Same value + same meaning → one definition. If two modules need it, lift to the parent `constants.rs` and import from there.

Same value + distinct domains (`DEFAULT_VOLUME: f32 = 1.0`, `IDENTITY_SCALE: f32 = 1.0`) → keep separate; the name carries the domain that the value alone does not.

Don't add `_TEXT` / `_SINGULAR` / `_VALUE` to manufacture a second name for an existing value — rename the existing one if it doesn't fit.

`&str` is the default; never suffix `_STR`. Add a `_CHAR` companion only when a `char` is genuinely needed at a call site (e.g. `s.starts_with(PIPE_CHAR)`).

### Don't promote a flat module just to add `constants.rs`

A flat `foo.rs` keeps its constants in the parent directory's `constants.rs`, as a peer file. Converting `foo.rs` into `foo/mod.rs` + `foo/constants.rs` requires 2+ of the criteria in [[when-to-split-a-module]], and the constants rule alone is not one of them.

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
