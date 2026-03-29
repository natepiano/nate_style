---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- project-setup
- rust
---
## CI pattern

CI runs six jobs in this order of priority.

```bash
cargo +nightly fmt -- --check
taplo fmt --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo build --release --all-features --workspace --examples
cargo nextest run --all-features --workspace --tests
cargo mend --fail-on-warn
```