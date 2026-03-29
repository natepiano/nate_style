---
tags: [rust, lints]
---

## Never bare `#[allow(dead_code)]`

Remove the dead code instead of suppressing the warning. A bare `#[allow(dead_code)]` without a `reason` is always a violation.

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
