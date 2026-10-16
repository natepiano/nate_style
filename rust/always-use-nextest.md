---
tier: B
family: values
input_scope: crate
date_created: '[[2026-03-29]]'
date_modified: "[[2026-10-16]]"
tags:
- rust
- tests
mechanism: llm
candidates:
  surface: partial
  uncovered: 'cargo test commands outside the configured file globs'
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