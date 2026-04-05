---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- lints
- rust
---
## Enums over `bool` for owned booleans

Booleans only encode on/off. Enums capture intent, are extensible, and prevent `match`-on-bool code. This applies everywhere we own the type: struct fields, function arguments, and return types.

```rust
// bad — struct field
struct CableConfig {
    double_sided: bool,
}

// bad — function arguments that control branching
fn detail_layout_spec(has_git: bool, has_targets: bool) -> DetailLayoutSpec {
    match has_git {
        true => { /* ... */ },
        false => { /* ... */ },
    }
}

// good — enums for struct fields
enum SideMode {
    Outside,
    Inside,
    Both,
}

struct CableConfig {
    side_mode: SideMode,
}

// good — enums for function arguments
enum GitPresence {
    Available,
    Missing,
}

enum TargetPresence {
    Available,
    Missing,
}

fn detail_layout_spec(git: GitPresence, targets: TargetPresence) -> DetailLayoutSpec {
    match git {
        GitPresence::Available => { /* ... */ },
        GitPresence::Missing => { /* ... */ },
    }
}
```

### Avoid stutter in enum names

When naming the replacement enum, don't repeat the variant meaning in the type name:

```rust
// bad — "Enabled" stutters with "CableDebugEnabled"
CableDebugEnabled::Enabled

// good — type describes the domain, variant describes the state
DebugGizmos::Enabled
```

See [[no-semantic-stutter-in-field-pairs]].
