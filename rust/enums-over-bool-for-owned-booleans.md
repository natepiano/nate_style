---
date_created: "[[2026-04-17]]"
date_modified: "[[2026-05-07]]"
see_also: "[[dont-repeat-enum-domain-in-variant-names]]"
tags: [rust, types]
mechanism: llm
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

### Not owned

- **Wire-format single-value field.** A field hard-coded at every construction site (e.g. external spec requires it but the producer only writes one value) is not state — leave it `bool`. Introduce the enum only when both values actually appear.
- **Parsing scaffolding.** File-private `Raw*` structs that convert to a typed public struct via `impl From<Raw> for Pub` are deserialization-only. Apply the rule to the public type.

### Local accumulators count as owned

A local `let mut x: bool` that accumulates domain state — `dirty |= ...`, `any_failed |= ...`, `seen_match = seen_match || ...` — is owned the same way a return type or struct field is. Promote it to the enum; add an enum method for updating the accumulated state when the update logic is reused, nontrivial, or likely to gain states.

```rust
// bad — producer returns the enum, consumer keeps the bool
let mut dirty = false;
for item in items {
    dirty |= cache.upsert(item).is_changed();
}
if dirty { recompute(); }

// good — accumulator carries the same domain type
let mut dirty = CacheUpdate::Unchanged;
for item in items {
    dirty = dirty.merge(cache.upsert(item));
}
if dirty.is_changed() { recompute(); }
```

Short one-off updates may stay inline as long as the accumulator itself stays typed end-to-end.

### Avoid stutter in enum names

When naming the replacement enum, don't repeat the variant meaning in the type name:

```rust
// bad
enum CableDebugEnabled {
    Enabled,
    Disabled,
}

// good
enum DebugGizmos {
    Enabled,
    Disabled,
}
```

See [[dont-repeat-enum-domain-in-variant-names]].
