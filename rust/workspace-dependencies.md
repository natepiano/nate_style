---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-04-29]]'
tags:
- cargo
- rust
mechanism: llm
---
## Workspace dependencies

Pin every dependency's version in the workspace `Cargo.toml`. Members reference them with `workspace = true`, and may add per-crate `features = [...]` so each member compiles only the feature surface its own code uses.

```toml
# bad — version pinned in a member crate
[dependencies]
serde = { version = "1.0", features = ["derive"] }

# good
# workspace Cargo.toml
[workspace.dependencies]
serde = "1.0"

# member Cargo.toml
[dependencies]
serde = { workspace = true, features = ["derive"] }
```

If the workspace baseline needs `default-features = false` (or its own feature list), set it at the workspace, not on every member.

### Exception: dev/prod default-features mismatch

Cargo does not let an inheriting member override `default-features`. If one dep needs different `default-features` in `[dependencies]` and `[dev-dependencies]` of the same crate, member-pin the side that fights the workspace.

```toml
# workspace Cargo.toml — production needs defaults off.
[workspace.dependencies]
bevy = { version = "0.18.1", default-features = false }

# member Cargo.toml — dev-dep needs defaults on, so member-pin it.
[dependencies]
bevy = { workspace = true, features = ["bevy_pbr"] }

[dev-dependencies]
bevy = { version = "0.18.1", features = ["default_font"] }
```
