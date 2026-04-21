---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-04-21]]'
tags:
- naming
- rust
---
## Spell out names

Identifiers should be readable without decoding. Abbreviation-only names force the reader to mentally expand every token. Spell out the words.

```rust
// bad — abbreviation soup
const MM_TO_M: f32 = 0.001;
const A4_H: f32 = 297.0;
let a4_h_m = A4_H * MM_TO_M;

// good — say what you mean
const MILLIMETERS_PER_METER: f32 = 0.001;
const A4_HEIGHT_MILLIMETERS: f32 = 297.0;
let a4_height = A4_HEIGHT_MILLIMETERS * MILLIMETERS_PER_METER;
```

Well-known single-word abbreviations (`max`, `min`, `len`, `idx`) are fine — the rule targets multi-abbreviation compounds where every word is shortened (`a4_h_m`, `ctrl_w`, `mm_to_m`).

### Sweep satellite identifiers

Expanding an abbreviation leaves derivatives stale: `ctrl_w_handler` next to a renamed `control_width`, format tokens, error message text, and doc comments built around the short form all read as mismatched until swept.