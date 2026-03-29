---
tags: [rust, project-setup]
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
