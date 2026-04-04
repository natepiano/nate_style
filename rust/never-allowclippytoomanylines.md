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

### Exception: trivial exhaustive matches

When a function is long only because it exhaustively matches many variants with trivial per-arm logic, the allow is acceptable with a reason:

```rust
// ok — 1:1 mapping, no logic
#[allow(clippy::too_many_lines, reason = "trivial 1:1 exhaustive variant mapping")]
pub const fn to_key_code(self) -> KeyCode { match self { ... } }

// ok — uniform constructor call per variant
#[allow(clippy::too_many_lines, reason = "trivial per-variant constructor calls")]
fn get_annotations(self) -> Annotation { match self { ... } }
```

### Never split exhaustive matches with `unreachable!()`

Splitting a match into sub-functions with `_ => unreachable!()` catch-alls trades compile-time exhaustiveness for a runtime panic. When a new variant is added, the compiler won't flag it — it silently reaches `unreachable!()` and crashes.

If a function is long solely due to exhaustive enum dispatch, do not split it mechanically. Either find a structural solution that preserves compile-time safety, or flag it for the user.

**Tooling:** `cargo mend` detects this as `forbidden_allow` (warning). Configurable in `mend.toml` via `[forbidden_allows]` with scope `"prod"`, `"test"`, or `"all"` (default).

**Agent rule:** The agent must never add this allow without user review. See `agent-must-review-allows.md`.