---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- patterns
- rust
---
## Methods that don't use `self` should be associated functions

If a method never references `self`, remove it from the signature and make it an associated function.

```rust
// bad — unused self
impl Formatter {
    fn fit_name_for_node(&self, node: &ProjectNode) -> usize {
        node.name.len()
    }
}

// good — associated function
impl Formatter {
    fn fit_name_for_node(node: &ProjectNode) -> usize {
        node.name.len()
    }
}
```