---
date_created: "[[2026-04-19]]"
date_modified: "[[2026-05-03]]"
tags:
  - rust
  - modules
see_also:
  - "[[no-magic-values]]"
mechanism: llm
---
## Types live with their behavior

A type belongs in the module that owns its behavior — the module where its sole constructor, primary mutator, or single consumer already lives. When a file accumulates types that are "used elsewhere," that file has become a data dictionary instead of a unit of behavior. Before splitting such a file, relocate each type to the module that already owns its behavior, and only consider splitting what remains.

**Scope:** types and free helpers (functions, traits). Constants live in `constants.rs` — see `no-magic-values.md`. Types follow the relocation check below; free helpers without an anchor type follow the `support/` rule at the bottom of this file.

### The relocation check

For each type in a file, ask:

1. **Sole constructor?** Is there exactly one function (in another module) that builds this type? The type belongs there. Its constructor is its behavior.
2. **Single consumer?** Is there exactly one module that reads, mutates, or renders this type? The type belongs there — it is an intermediate state of that module's pipeline, not a standalone concept.
3. **Primary mutator?** If one module's methods mutate this type and other modules only read it, the type belongs with the mutator. Readers import from there.

If any of these is true, move the type. Only if a type has no single behavioral home — it is consumed roughly equally across several modules, or it is a public API surface — does it stay put.

### Worked example: extraction pipeline types

```text
# before -- data dictionary
src/
  types.rs          # public Outline API + ExtractedOutline + render cache resources
  extract.rs        # reads Outline, constructs ExtractedOutline, fills caches
  node.rs           # uses OutlineRenderGraphNode label
  lib.rs            # wires up observer configure_outline_camera_depth_texture
```

`ExtractedOutline::from_main_world` is called from exactly one place: `extract.rs`. The render cache resources (`ExtractedOutlineUniforms`, `ActiveOutlineModes`) are populated only by extraction systems. `OutlineRenderGraphNode` is a render-graph label consumed by `node.rs`. `configure_outline_camera_depth_texture` is an observer for `OutlineCamera` that runs once at spawn.

```text
# after -- types live with their behavior
src/
  outline.rs        # public Outline API (stays put — it is the public surface)
  extract.rs        # ExtractedOutline + from_main_world + render cache resources + extraction systems
  node.rs           # OutlineRenderGraphNode + OutlineNode (label alongside node)
  camera.rs         # OutlineCamera + configure_outline_camera_depth_texture observer
  lib.rs            # wires up the observer registered from camera.rs
```

Now each type's file is also the file that drives it. No relocation leaves a file where a type's behavior is "somewhere else."

### When this rule fires vs when splitting fires

The "when to split" rule asks *is this file too big to live in one place?* This rule asks *is this file in the wrong place?* Apply this rule first. If every type in a bloated file has a behavioral home elsewhere, splitting is unnecessary — the file dissolves into its siblings. Only when the residue is genuinely cohesive (one domain, no stronger home) does the split-decision rule fire.

### Non-goal: single-type-per-file

Relocation is not "one type per file." A module's natural home already contains other behavior. Relocating `ExtractedOutline` into `extract.rs` is correct precisely because `extract.rs` already owns its construction — it is not a new file, it is the existing owner.

### Parent-module naming follow-through

A module named `types/` or a file named `types.rs` is usually the signal that this rule has been skipped: the name admits that the file was organized by code shape ("here are the types") rather than by behavior. See the naming anti-patterns in the module-splitting anchor-types rule.

## Free functions and trait helpers — `support/`

Some helpers fail every relocation check above: a free function or trait that has no anchor type, no sole consumer, and is used by 2+ unrelated siblings of the same parent. Place these in a `support/` sibling at the relevant module level. `support/` is the only sanctioned exception to the `utils`/`helpers` anti-pattern list — it is reserved by name for items that have provably failed every other placement rule.

`support/` is recursive. `src/support/` for crate-wide helpers, `markdown_file/support/` for helpers shared across `markdown_file/`'s submodules, and so on. The qualifying test is the same at every level.

### Qualifying test

An item belongs in `<module>/support/` only if **all** are true:

1. **No anchor type.** The item is a free function or trait — not `impl SomeType`.
2. **No behavioral home.** The relocation check above gives no single sibling at the same level as sole constructor, single consumer, or primary mutator.
3. **Used by 2+ unrelated siblings of the same parent.** A helper used by exactly one sibling belongs with that sibling. A helper used by submodules of multiple unrelated parents belongs in the nearest common ancestor's `support/`.

`support/` may be a single file (`<module>/support.rs`) or a directory (`<module>/support/` with anchor-named children); the directory form follows `name-submodules-after-anchor-types.md` for its children. Domain-named children only — `support/escaping.rs`, `support/filesystem.rs` — never `support/helpers.rs` or `support/string_utils.rs`.

### What `support/` does not authorize

- Anchor-typed modules (`Timer`, `Sha256Cache`, `OutputFileWriter`) — they live with their domain or at top level, not inside `support/`.
- A single helper with one caller — relocate it.
- A `support/constants.rs` at any level — constants follow `no-magic-values.md` and live in the parent module's `constants.rs` (`src/constants.rs`, `markdown_file/constants.rs`, etc.), not nested inside `support/`.
