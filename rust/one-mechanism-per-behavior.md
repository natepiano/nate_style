---
tier: C
family: types
input_scope: crate
mechanism: llm
mode: propose
date_created: "[[2026-10-27]]"
date_modified: "[[2026-10-27]]"
see_also:
  - "[[no-duplicate-implementations]]"
  - "[[if-else-chains-signal-missing-types]]"
tags: [rust, types]
---
## One mechanism per behavior

A shared path, such as open, layout or return, never branches on which kind of thing it handles. The differences between kinds come from data that each kind supplies, such as its members, bounds and face, or from one trait method. They never come from `if this is a Screen` checks inside the shared code.

```rust
// bad: the shared layout knows each kind
fn layout(scope: &StagedScope) -> Layout {
    match scope { StagedScope::Screen(e) => screen_layout(e), StagedScope::FrameTime(e) => frame_time_layout(e) }
}

// good: each kind supplies its data; one layout reads it
fn layout(assembly: &Assembly) -> Layout { Layout::from_members(&assembly.members, assembly.bounds) }
```

A branch for one kind in a shared path is a design change, and it needs the user's approval. Never add one to get one kind's result right.

The way back follows the same rule: close, escape and nested close return to where open began, by one rule for every kind.
