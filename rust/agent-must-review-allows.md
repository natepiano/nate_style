---
date_created: '[[2026-03-31]]'
date_modified: '[[2026-03-31]]'
tags:
- agent
- lints
- rust
---
## Agent must review all `#[allow]` with the user

The agent must never autonomously add an `#[allow(...)]` attribute or fill in a `reason` field. Every allow must be reviewed with the user to determine if there is a way to avoid the suppression entirely.

### Why

`reason` fields are the signal that an allow was intentional. If the agent fills them in automatically, they lose that meaning — a machine-generated reason is no better than a bare allow. The user must decide:

1. Whether the allow is necessary at all (can the code be restructured instead?)
2. What the reason text should say

### Exception: pre-authorized allows

Allows that are explicitly pre-authorized by the style guide — with exact lint name, scope, and reason text — may be applied without review. Currently pre-authorized:

- **Test module boilerplate** (`test-module-allow-boilerplate.md`): `expect_used` and `panic` in `#[cfg(test)]` modules

If the style guide does not explicitly say the agent can apply an allow, the agent must ask.
