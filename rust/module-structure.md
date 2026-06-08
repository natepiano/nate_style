---
date_created: "[[2026-06-08]]"
date_modified: "[[2026-06-08]]"
see_also: "[[module-roots-as-table-of-contents]]"
tags:
  - rust
  - modules
mechanism: llm
---
## Anchor type leads the file

A content file is organized around its anchor type — the type that anchors the module name (`ImageFile` in `image_file.rs`; "anchor type" is defined in `name-submodules-after-anchor-types.md`). Order top-down:

1. Imports (`imports-go-at-the-top-of-the-file.md`).
2. Constants — in `constants.rs`; single-file `examples/`, `benches/`, `build.rs` put them at the top after imports (`no-magic-values.md`).
3. Short field types and enum payloads — the vocabulary the anchor's fields use.
4. Anchor type, then its `impl` blocks (inherent before trait).
5. Free helper functions (no anchor type).
6. `#[cfg(test)] mod tests`.

A supporting type with a long `impl` is its own anchor: give it its own module rather than inlining it (`when-to-split-a-module.md`). Inlined field types stay short by that test. In a `mod.rs`, the table of contents comes first, then this order.

```rust
enum Extension { Png, Jpg }     // short field type — vocabulary first

pub struct ImageFile {          // anchor type
    extension: Extension,
}
impl ImageFile { ... }
impl Display for ImageFile { ... }

fn sniff_extension(bytes: &[u8]) -> Extension { ... }   // helper — last

#[cfg(test)]
mod tests { ... }
```
