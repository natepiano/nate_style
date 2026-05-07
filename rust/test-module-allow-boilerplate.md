---
date_created: '[[2026-04-10]]'
date_modified: '[[2026-05-07]]'
see_also: "[[agent-must-review-allows]]"
tags:
- lints
- rust
- tests
mechanism: llm
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

### Verify before flagging stale

A site is stale only if the allow's lint list contains a lint whose pattern (`.unwrap(`, `.expect(`, `panic!(`) has zero matches in the target scope. Each Locations entry must name the lint to strip — e.g. `src/foo.rs:N — strip clippy::panic` — so a claim that names a lint not in the allow cannot be written.