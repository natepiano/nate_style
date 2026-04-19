---
clippy: [expect_used, unwrap_used, panic]
date_created: '[[2026-04-10]]'
date_modified: '[[2026-04-10]]'
group: allows
tags:
- lints
- rust
- tests
---
## Test module allow boilerplate

`expect_used`, `unwrap_used`, and `panic` are acceptable in test code, but only add the `#[allow]` attributes that the test module actually needs. Do not add allows for lints that aren't triggered.

- Only add `#[allow(clippy::expect_used, ...)]` if the module uses `.expect()`
- Only add `#[allow(clippy::unwrap_used, ...)]` if the module uses `.unwrap()`
- Only add `#[allow(clippy::panic, ...)]` if the module uses `panic!`

```rust
// Example: test module that only uses .unwrap()
#[cfg(test)]
#[allow(clippy::unwrap_used, reason = "tests should panic on unexpected values")]
mod tests {
```

These are pre-authorized — the agent may apply the ones that are needed without user review. Do not add allows speculatively; they create cognitive load by implying the keywords are present when they are not.