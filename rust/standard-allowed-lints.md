---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- lints
- rust
---
## Standard allowed lints

Allow only these lints, each for a specific reason.

```toml
multiple_crate_versions = "allow" # Transitive deps — out of our control
```

### Bevy-only additional allows

Bevy projects (and only Bevy projects) may also allow these lints. Bevy systems and queries inherently produce complex types and long parameter lists that are impractical to refactor away, Bevy's prelude convention relies on wildcard imports, and Bevy reflect macros trigger false positives in `option_if_let_else`.

```toml
needless_pass_by_value = "allow" # Bevy systems require owned params
option_if_let_else     = "allow" # False positives with Bevy reflect macros
too_many_arguments     = "allow" # Bevy systems often require many params
type_complexity        = "allow" # Bevy query types are inherently complex
wildcard_imports       = "allow" # Bevy prelude convention
```

Do not allow these in non-Bevy crates — refactor instead.