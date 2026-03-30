---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- bevy
- rust
---
## Messages are strongly discouraged

`MessageWriter` / `MessageReader` (the pre-0.17 "events" pattern) are effectively off-limits. The only exception is when many items accumulate in a single frame and batch iteration is genuinely superior.