---
tier: E
input_scope: crate
date_created: '[[2026-04-15]]'
date_modified: "[[2026-11-22]]"
tags:
- rust
- api
- non-negotiable
mechanism: llm
---
## Public API changes require explicit approval

Style fixes, cleanup, and refactors must preserve the existing public API unless the user explicitly asks for or approves a breaking change.

Public API includes:
- exported types, functions, methods, constants, modules, fields, and re-exports
- trait impl availability that downstream code depends on
- constructor and builder entry points
- unit-struct plugin usage and other documented call shapes
- examples and README snippets presented as supported usage

If satisfying another style rule would require changing that surface, stop and ask instead of recommending or applying the breaking change.

Before you ask any public API question, including a proposed addition, answer these from the code:
1. Why must it exist? Start with the why in one short sentence: what a user or caller cannot do without it. "It exists already" (in the code, as a private type, on the trunk, in the plan) is a fact to name, never the why. Then name each thing that exists and could do the job. Check at least a model, a public item, the behavior on the trunk and a line of the plan. Say why each one cannot. A signature that takes `World` also says why no narrower Bevy form works (world-arguments-need-a-reason.md).
2. Is it an event? Say who reads the item, and when.
3. What is the code? Show the item beside its neighbours, with one real scenario.

The question to the user shows the why from check 1 for each API item.

Prefer API-preserving remediations:
- private wrapper types or plugins behind the existing entry points
- internal helper extraction or inlining
- facade-preserving delegation
- keeping documented/example call sites valid while restructuring internals

```rust
// bad — style refactor silently changes the public entry point
app.add_plugins(WindowManagerPlugin);
// becomes
app.add_plugins(WindowManagerPlugin::new());

// good — keep the public API, hide the refactor internally
pub struct WindowManagerPlugin;

impl Plugin for WindowManagerPlugin {
    fn build(&self, app: &mut App) {
        app.add_plugins(WindowManagerPluginCustomPath::default());
    }
}
```
