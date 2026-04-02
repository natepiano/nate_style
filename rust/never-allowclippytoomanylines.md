---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- lints
- rust
---
## Never `#[allow(clippy::too_many_lines)]` in production code

Extract helper functions to bring the function under the line limit. Tests are exempt — long test functions are often clearer than artificially split ones.

```rust
// bad — production code
#[allow(clippy::too_many_lines)]
fn build_pipeline() { /* 200 lines */ }

// good — extract helpers
fn build_pipeline() {
    let layout = create_layout();
    let shaders = compile_shaders();
    assemble_pipeline(layout, shaders);
}

// ok — test code
#[test]
#[allow(clippy::too_many_lines)]
fn test_full_pipeline() { /* long integration test */ }
```

**Tooling:** `cargo mend` detects this as `forbidden_allow` (warning). Configurable in `mend.toml` via `[forbidden_allows]` with scope `"prod"`, `"test"`, or `"all"` (default).

**Agent rule:** The agent must never add this allow without user review. See `agent-must-review-allows.md`.