---
tier: D
family: modules
input_scope: crate
mechanism: llm
mode: propose
scope: review
date_created: "[[2026-10-27]]"
date_modified: "[[2026-10-27]]"
see_also:
  - "[[crate-apis-expose-behavior]]"
  - "[[no-duplicate-implementations]]"
  - "[[types-live-with-their-behavior]]"
tags: [rust, modules]
---
## Behavior lives in its most cohesive crate

In a workspace, each behavior lives in the crate that has the most cohesion with it: the crate that owns the types, data and rules the behavior reads and changes. A crate that depends on it calls that behavior. It never does the owning crate's work itself.

We split crates for three reasons, and misplaced behavior defeats all three:

- **Encapsulation.** The owning crate keeps its invariants private. Work done outside it must reach into its internals or copy its rules.
- **Compile speed.** A change stays in one crate and rebuilds only what depends on it. Logic spread across crates makes one change rebuild several.
- **Comprehension.** A reader finds a behavior in the crate whose name says it, not in each caller.

```rust
// bad: the app crate computes the fit from the camera crate's fields
let distance = camera.bounds.radius() / (camera.fov * 0.5).tan() * camera.margin;
camera.target_distance = distance.clamp(camera.min_distance, camera.max_distance);

// good: the camera crate owns the fit; the app crate asks for it
camera.fit_to(bounds);
```

Signs of misplaced behavior: a dependent crate reads several fields of another crate's type to compute something about it; two dependent crates hold near-copies of the same logic; a dependent crate re-checks a rule the owning crate already holds.

The fix moves the behavior into the owning crate and gives it an API there (see [[crate-apis-expose-behavior]]). Remove the copies in every dependent crate in the same change. Move behavior down to a lower crate only when that crate owns it, never to share code that has no owner.
