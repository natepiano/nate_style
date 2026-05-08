---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-05-08]]'
tags:
- naming
- rust
mechanism: llm
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

Well-known single-word abbreviations (`max`, `min`, `len`, `idx`, `secs`, `ms`) are fine — the rule targets multi-abbreviation compounds where every word is shortened (`a4_h_m`, `ctrl_w`, `mm_to_m`). Match the host crate's spelling for unit suffixes (Bevy uses `delta_secs`, not `delta_seconds`).

Canonical industry acronyms count as single tokens: `Ux`, `Fps`, `Http`, `Url`, `Json`, `Sql`, `Api`, `regex`, `Fov`, `Msaa`, `Smaa`, `Taa`, `Hdr`, `Sdr`, etc. Keep `ProtectedUx`, `ShowFps`, `MsaaHdr`; do not expand.

Canonical process and CLI terms count as single tokens: keep `pid` for process IDs and `args` for command-line arguments, especially in public or serialized fields.

A binding may also mirror its type's snake_case name when the type abbreviates: `let orbit_cam: OrbitCam = …`, not `orbit_camera`. The type's spelling is canonical; satellite identifiers (params, format tokens) follow the binding.

### Sweep satellite identifiers

Expanding an abbreviation leaves derivatives stale: `ctrl_w_handler` next to a renamed `control_width`, format tokens, error message text, and doc comments built around the short form all read as mismatched until swept.
