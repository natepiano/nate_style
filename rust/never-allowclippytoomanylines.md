---
date_created: "[[2026-04-03]]"
date_modified: "[[2026-04-07]]"
tags: [lints, rust]
group: allows
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

## orchestrator pattern
It is not helpful to just simply refactor a small number of lines to get under the limit. Often it's the case that a new change will come along that will once again push it over.

Many functions with too many lines have logical sections that can be broken apart - so that the calling function is merely an orchestrator. If you see this pattern you should fully break apart the function into the pieces that can be reliably orchestrated.

```rust
// bad
fn orchestrator(self) -> SomeType {
	// fn with >100 lines
	// returns a bool
	some_type_instance
}

// good - only the high level function calls remain
fn orchestrator(&self) -> SomeType {
	let some_this = do_this(&self);
	
	let some_that = do_that(some_this);
	
	construct_some_type(some_that)
}
```