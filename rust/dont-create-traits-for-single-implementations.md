---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-07-07]]'
tags:
- patterns
- rust
mechanism: llm
candidates:
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