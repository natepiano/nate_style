---
date_created: '[[2026-03-30]]'
date_modified: '[[2026-03-30]]'
tags:
- bevy
- rust
---
## Messages are strongly discouraged (consultation only)

> **Not a style-fix rule.** This guideline requires case-by-case judgement about Bevy API capabilities (e.g. whether a type derives `Event` vs `Message`). It must only be applied during interactive consultation with the user, never during automated style evaluation or style-fix processes.

`MessageWriter` / `MessageReader` (the pre-0.17 "events" pattern) are effectively off-limits. The only exception is when many items accumulate in a single frame and batch iteration is genuinely superior.