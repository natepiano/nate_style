---
tier: B
family: types
input_scope: crate
date_created: '[[2026-03-29]]'
date_modified: "[[2026-10-16]]"
tags:
- patterns
- rust
mechanism: llm
candidates:
  surface: partial
  uncovered: 'same-named traits in separate modules, mutually exclusive implementations for one type'
  kind: single_impl_traits
---
## Don't create traits for single implementations

Extract a trait only when two or more types implement it.

Exception: a trait that is a deliberate extension point for downstream crates — external implementers count even when none exist in-crate. The trait's doc comment must state that intent.

```rust
// bad — trait exists for one struct
trait Processor {
    fn process(&self);
}
impl Processor for AudioProcessor { ... }

// good — just put the method on the struct
impl AudioProcessor {
    fn process(&self) { ... }
}
```