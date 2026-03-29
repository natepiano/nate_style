---
tags: [rust, project-setup]
---

## Workspace dependencies

Define all dependencies in the workspace `Cargo.toml`. Members reference them with `.workspace = true`.

```toml
# bad — version pinned in a member crate
[dependencies]
serde = { version = "1.0", features = ["derive"] }

# good — member defers to workspace
[dependencies]
serde = { workspace = true }
```
