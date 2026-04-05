---
date_created: "[[2026-03-29]]"
date_modified: "[[2026-03-31]]"
tags:
  - lints
  - rust
  - visibility
---
## Cargo.toml lint configuration

Place this in `[workspace.lints.clippy]` (or `[lints.clippy]` for standalone crates).

### Deny groups

Deny all major Clippy groups and forbid fallible unwrapping.

```toml
# [workspace.lints.clippy]
allow_attributes_without_reason = "deny"
expect_used                     = "deny"
panic                           = "deny"
unreachable                     = "deny"
unwrap_used                     = "deny"

all      = { level = "deny", priority = -1 }
cargo    = { level = "deny", priority = -1 }
nursery  = { level = "deny", priority = -1 }
pedantic = { level = "deny", priority = -1 }
```

### Universal allows

```toml
multiple_crate_versions = "allow" # Transitive deps — out of our control
redundant_pub_crate     = "allow" # cargo mend is the visibility authority, not clippy
```
