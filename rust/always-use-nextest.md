---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-04-06]]'
tags:
- rust
- tests
---
## Always use nextest

Use `cargo nextest run` instead of `cargo test`.

```bash
# bad
cargo test

# good
cargo nextest run
```