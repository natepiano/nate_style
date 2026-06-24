---
date_created: '[[2026-06-23]]'
date_modified: '[[2026-06-23]]'
see_also: '[[module-structure]]'
tags:
- tests
- rust
mechanism: llm
---
## Tests live with the type under test

A `#[cfg(test)] mod tests` belongs in the file of the **primary type it exercises**, even when the test constructs other types to do so. Identify the type whose behavior the test asserts and put the test there — never collect tests in the crate root, a sibling module, or wherever the imports happen to be shortest.

Pick by what is asserted, not what is referenced: a test that builds an `App` and asserts on `OrbitCamInputPhase` ordering lives in `system_sets.rs` (which defines that phase), not in `lib.rs`.
