---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- rust
- visibility
---
## Never use `pub mod`

Declare modules with `mod`, then explicitly export with `pub use`.

```rust
// bad
pub mod some_module;

// good
mod some_module;
pub use some_module::SomeType;
pub use some_module::SomeOtherType;
```

**Exception:** `pub mod prelude;` is allowed to follow Bevy/Rust ecosystem conventions.