---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- lints
- rust
---
## Never `#[allow(clippy::too_many_lines)]`

Extract helper functions to bring the function under the line limit.

```rust
// bad
#[allow(clippy::too_many_lines)]
fn build_pipeline() { /* 200 lines */ }

// good
fn build_pipeline() {
    let layout = create_layout();
    let shaders = compile_shaders();
    assemble_pipeline(layout, shaders);
}
```