---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-31]]'
tags:
- lints
- rust
---
## Test module allow boilerplate

`expect_used`, `unwrap_used`, and `panic` are acceptable in test code. Every `#[cfg(test)] mod tests` block should carry:

```rust
#[cfg(test)]
#[allow(clippy::expect_used, reason = "tests should panic on unexpected values")]
#[allow(clippy::unwrap_used, reason = "tests should panic on unexpected values")]
#[allow(clippy::panic, reason = "tests should panic on unexpected values")]
mod tests {
```

This is pre-authorized boilerplate — the agent may apply it without user review.
