---
tags: [rust, project-setup]
---

## Always use nextest

Use `cargo nextest run` instead of `cargo test`.

```bash
# bad
cargo test

# good
cargo nextest run
```
