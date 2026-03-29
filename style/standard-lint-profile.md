---
tags: [rust, lints]
---

## Standard lint profile

Deny all major Clippy groups and forbid fallible unwrapping. Place this in `[workspace.lints.clippy]` (or `[lints.clippy]` for standalone crates).

```toml
# [workspace.lints.clippy]
expect_used = "deny"
panic       = "deny"
unwrap_used = "deny"

all      = { level = "deny", priority = -1 }
cargo    = { level = "deny", priority = -1 }
nursery  = { level = "deny", priority = -1 }
pedantic = { level = "deny", priority = -1 }
```
