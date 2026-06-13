---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-06-12]]'
tags:
- rust
- tests
mechanism: llm
candidates:
  kind: regex
  pattern: '\bcargo test\b'
  globs: ['*.sh', '*.rs', '*.md', '*.yml', '*.yaml', '*.toml', 'justfile', 'Makefile']
---
## Always use nextest

Use `cargo nextest run` instead of `cargo test`.

```bash
# bad
cargo test

# good
cargo nextest run
```