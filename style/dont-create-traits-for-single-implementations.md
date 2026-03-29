---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- patterns
- rust
---
## Don't create traits for single implementations

Extract a trait only when two or more types implement it.

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