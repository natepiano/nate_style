---
tags: [rust, patterns]
---

## If/else chains signal missing types

When branching on the same condition in multiple places, or when an if/else grows beyond two arms, introduce an enum to represent the states. Let `match` enforce exhaustiveness instead of relying on else branches to catch new cases.

```rust
// bad — stringly-typed branching, else hides bugs
fn apply(mode: &str, value: f32) -> f32 {
    if mode == "add" {
        value + 1.0
    } else if mode == "multiply" {
        value * 2.0
    } else {
        value // silent fallthrough when a new mode is added
    }
}

// good — compiler forces you to handle every variant
enum BlendMode {
    Add,
    Multiply,
}

fn apply(mode: BlendMode, value: f32) -> f32 {
    match mode {
        BlendMode::Add => value + 1.0,
        BlendMode::Multiply => value * 2.0,
    }
}
```
