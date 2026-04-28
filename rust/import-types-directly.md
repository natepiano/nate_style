---
date_created: '[[2026-04-10]]'
date_modified: '[[2026-04-28]]'
tags:
- imports
- rust
mechanism: mend
mode: auto
lint: inline_path_qualified_type
---
## Import types directly

Types (structs, enums, traits) are imported by name so they appear bare at the call site.

```rust
// bad — inline path in type position
fn spawn(query: Query<&crate::movable::Movable>) {}

// good
use crate::movable::Movable;

fn spawn(query: Query<&Movable>) {}
```

```rust
// bad — inline path in value position (enum variant comparison)
if settings.spawnability == actor_settings::Spawnability::Disabled {

// good
use super::actor_settings::Spawnability;

if settings.spawnability == Spawnability::Disabled {
```