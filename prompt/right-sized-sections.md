---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- prompt
- structure
---
## Right-sized sections

Balance between too many tiny sections and too few large ones. A section should represent a coherent unit of work, not a single operation or an entire workflow.

```markdown
// bad — too granular
<OpenFile/>
<ReadLine/>
<CloseFile/>

// bad — too coarse
<DoEverything/>

// good — coherent unit
<ProcessFileContents/>
```
