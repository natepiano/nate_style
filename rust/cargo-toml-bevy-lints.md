---
date_created: '[[2026-04-06]]'
date_modified: '[[2026-04-06]]'
tags:
- bevy
- lints
- rust
---
## Cargo.toml Bevy-only lint allows

Bevy projects (and only Bevy projects) may add these allows to `[workspace.lints.clippy]`. Bevy systems and queries inherently produce complex types and long parameter lists that are impractical to refactor away, Bevy's prelude convention relies on wildcard imports, and Bevy reflect macros trigger false positives in `option_if_let_else`.

```toml
needless_pass_by_value = "allow" # Bevy systems require owned params
option_if_let_else     = "allow" # False positives with Bevy reflect macros
too_many_arguments     = "allow" # Bevy systems often require many params
type_complexity        = "allow" # Bevy query types are inherently complex
wildcard_imports       = "allow" # Bevy prelude convention
```

### Mixed workspaces

When a workspace contains both Bevy and non-Bevy crates, the Bevy-only allows live in `[workspace.lints.clippy]`. Cargo does not support per-member lint overrides — `lints.workspace = true` cannot be combined with a member-level `[lints.clippy]` section. Non-Bevy members inherit the Bevy allows; this is acceptable since they are permissive relaxations of pedantic lints, not warning suppressions.

Do not add Bevy-only allows to a workspace that has no Bevy dependency at all.