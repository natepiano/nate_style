---
tier: C
family: types
input_scope: file
date_created: "[[2026-10-18]]"
date_modified: "[[2026-10-19]]"
tags: [rust, types, patterns]
mechanism: llm
mode: propose
see_also:
  - "[[enums-over-bool-for-owned-booleans]]"
  - "[[if-else-chains-signal-missing-types]]"
---
## Make invalid states unrepresentable

When a type can hold a combination of values that must never occur, change the type so that combination cannot be built. Do not guard against it at runtime: no `debug_assert!`, early `return`, or fallback value such as `""` for the state the type allows.

- **Fields valid only together:** one enum whose variants carry them, not parallel `Option`s, flags, or a kind field beside optional payloads.
- **Limits on a value:** a private field and one checked constructor; after construction, no code checks it again.
- **Operations valid in one state:** give that state its own type.

```rust
// bad — target_name must be Some only for FinderKind::Target
struct FinderItem { kind: FinderKind, target_name: Option<String> }

// good
enum FinderItem { Project, Target { name: String } }
```
