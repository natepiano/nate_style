---
tier: B
family: types
input_scope: file
approval: always
date_created: "[[2026-10-27]]"
date_modified: "[[2026-10-27]]"
see_also:
  - "[[enums-over-bool-for-owned-booleans]]"
  - "[[make-invalid-states-unrepresentable]]"
tags: [rust, types]
mechanism: llm
candidates:
  surface: partial
  uncovered: 'function arguments, return types, local accumulators'
  kind: struct_fields
  field_type_pattern: '^Option<'
---
## Enums over `Option` when `None` has a meaning

When `None` stands for a state of its own, not only "no value", use an enum whose variants name each state. `Option` says only present or absent; the reader must learn from other code what `None` means. Keep `Option` when `None` means "absent" and nothing more.

```rust
// bad — None means "inherit the workspace level"
struct Lints { level: Option<Level> }
let level = lints.level.unwrap_or(workspace.level);

// good
enum LintLevel { Inherit, Set(Level) }
```
