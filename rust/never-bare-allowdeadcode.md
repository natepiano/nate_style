---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- lints
- rust
group: allows
---
## Never bare `#[allow(dead_code)]`

Remove the dead code instead of suppressing the warning. A bare `#[allow(dead_code)]` without a `reason` is always a violation.

**Enforced by:** `allow_attributes_without_reason = "deny"` in the Cargo.toml lint configuration (`cargo-toml-lints.md`). This applies to all `#[allow(...)]` attributes, not just `dead_code`.

**Agent rule:** The agent must never add an `#[allow]` or fill in a `reason` field without user review. See `agent-must-review-allows.md`.

When suppression is genuinely needed (e.g., fields required for deserialization, items used by derive macros), use the `reason` field to document why. The `reason` is the signal that the allow was intentional.

```rust
// bad — bare allow hides dead code
#[allow(dead_code)]
fn unused_helper() {}

// bad — remove the dead code instead
// good — delete it

// good — reason documents why the allow is needed
#[allow(dead_code, reason = "field required for v1 deserialization")]
version: u8,

// good — used by generated code that clippy can't see
#[allow(dead_code, reason = "used by ParamStruct/ResultStruct derive macros")]
pub struct FieldPlacementInfo { ... }
```