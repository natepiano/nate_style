---
date_created: '[[2026-04-29]]'
date_modified: '[[2026-04-29]]'
exceptions: text shaping
tags:
- rust
- style
- naming
- comments
mechanism: llm
pre_filter: '(?i)shape|honest'
---
## Avoid "shape" and "honest"

Drop the words **"shape"** and **"honest"** (and variations: `shaped`, `shapes`, `reshape`, `reshaped`, `honestly`, `to be honest`, etc.) from **both code and comments**. That includes identifiers (type names, function names, variables, fields, modules) and `//` / `///` comments. They're filler — they describe the writing, not the thing. State the claim directly.

### In code

```rust
// bad — "shaped" baked into the type name
struct CtxShapedArgs { /* ... */ }
fn handle_request_shaped_payload(p: RequestShapedPayload) { /* ... */ }

// good — name the thing
struct CtxArgs { /* ... */ }
fn handle_request_payload(p: RequestPayload) { /* ... */ }
```

### In comments

```rust
// bad — "shape" adds nothing
// ctx-shaped args
fn run(ctx: Ctx) { /* ... */ }

// good
// ctx args
fn run(ctx: Ctx) { /* ... */ }
```

```rust
// bad — "honestly" is filler
// honestly, this branch is unreachable in practice
unreachable!()

// good
// unreachable: caller validates the variant before dispatch
unreachable!()
```

### Exception: industry-standard terms

Leave domain terminology alone. `text shaping` / `shaper` (the typography pipeline step, e.g. HarfBuzz) is the canonical term — keep it in identifiers, types, and comments. Same rule for any other established term of art; the ban targets vague analogies, not domain vocabulary.

### Why

These words are LLM tics. "X-shaped" gets reached for as a vague analogy when the concrete noun would do, and "honest"/"honestly" is throat-clearing that signals nothing. A reader scanning code or comments wants the constraint, the invariant, or the surprise — not hedges or analogies. The user actively dislikes seeing these words; treat their presence as a defect.

### How to apply

When the urge to write "X-shaped" appears, name the thing instead:

- `ctx-shaped args` → `ctx args`
- `tree-shaped data` → `tree`
- `request-shaped payload` → `request payload`
- `CtxShapedArgs` → `CtxArgs`

When "honest"/"honestly" appears, delete it — the sentence reads better without it. If a clarifier is genuinely needed, use a concrete one (`actually`, `in practice`, `note:`) or rewrite to state the fact directly.

When reviewing existing code, flag every occurrence in identifiers and comments and propose renames/rewrites; don't leave them in place.
