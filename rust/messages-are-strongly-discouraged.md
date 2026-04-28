---
date_created: '[[2026-03-30]]'
date_modified: '[[2026-04-28]]'
tags:
- bevy
- rust
mechanism: llm
mode: propose
---
## Messages are strongly discouraged

`MessageWriter` / `MessageReader` (the pre-0.17 "events" pattern) are effectively off-limits. The only exception is when many items accumulate in a single frame and batch iteration is genuinely superior.