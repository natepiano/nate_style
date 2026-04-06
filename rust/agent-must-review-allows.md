---
date_created: "[[2026-03-31]]"
date_modified: "[[2026-03-31]]"
tags:
  - lints
  - rust
---
## Agent must review all `#[allow]` with the user

The agent must never autonomously add an `#[allow(...)]` attribute or fill in a `reason` field. Every allow must be reviewed with the user to determine if there is a way to avoid the suppression entirely.

### Fix priority

Before adding or keeping any allow, the agent must work through this sequence:

1. **Remove it** — delete the allow and run clippy. If it passes, the allow was stale.
2. **Restructure** — if the lint still fires, find a way to fix the code that eliminates the need for the allow, without regressing code quality.
3. **Propose to the user** — if neither works, explain why the allow is unavoidable and propose a reason string. The user decides the final text.

### Why

`reason` fields are the signal that an allow was intentional. If the agent fills them in automatically, they lose that meaning — a machine-generated reason is no better than a bare allow.

### Exception: pre-authorized allows

Allows that are explicitly pre-authorized by the style guide — with exact lint name, scope, and reason text — may be applied without review. Currently pre-authorized:

- **Test module boilerplate** (`test-module-allow-boilerplate.md`): `expect_used`, `unwrap_used`, and `panic` in `#[cfg(test)]` modules — but only the ones actually triggered by code in the module

If the style guide does not explicitly say the agent can apply an allow, the agent must ask.
