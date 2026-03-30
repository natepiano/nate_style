---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- prompt
- structure
---
## Every reference needs a definition

Every `<TagName/>` reference must have exactly one `<TagName>...</TagName>` definition, and vice versa. References must appear before their definitions in file order (read the invocation context before the implementation). Cross-file references via shared workflows are valid — the definition lives in the callee file.

No orphaned definitions. No missing definitions. No duplicates.
