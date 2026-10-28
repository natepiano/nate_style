---
tier: C
family: types
input_scope: crate
mechanism: llm
mode: propose
date_created: "[[2026-10-27]]"
date_modified: "[[2026-10-27]]"
see_also:
  - "[[behavior-lives-in-its-most-cohesive-crate]]"
  - "[[use-narrowest-visibility]]"
  - "[[public-api-changes-require-explicit-approval]]"
tags: [rust, types]
---
## Crate APIs expose behavior

A crate exposes what its callers need as named operations with ergonomic signatures. Callers state what they want. They never assemble the crate's internals to get it.

- Expose an operation, not the data needed to rebuild it. A `pub` field that callers read only to compute something the crate could compute is a missing method.
- Name the operation for what the caller wants (`fit_to`, `open`, `focus`), not for how the crate does it.
- Take the caller's types, and return a result the caller can use at once. A caller should not convert, unwrap or re-check what the crate already knows.
- Keep the surface small: one way to do each thing, and nothing public that has no caller.

```rust
// bad: the caller does the crate's work with its parts
let entry = registry.entries.iter().find(|entry| entry.id == id && entry.enabled);
let label = entry.map(|entry| format!("{} ({})", entry.name, entry.kind));

// good: the crate owns the lookup and the label
let label = registry.label(id);
```

A new or changed public API follows [[public-api-changes-require-explicit-approval]]: the user approves it.
