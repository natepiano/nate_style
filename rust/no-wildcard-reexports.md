---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- rust
- visibility
---
## No wildcard re-exports

Don't use `pub use submod::*` in parent modules. Spell out each re-export explicitly so the facade is a readable table of contents.

```rust
// bad — hides what the module actually exports
pub use helpers::*;

// good — explicit list
pub use helpers::build_label;
pub use helpers::format_name;
```

**Tooling:** `cargo mend` detects this as `wildcard_parent_pub_use` (warning).
