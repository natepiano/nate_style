---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- prompt
- structure
---
## Extract logical units into tagged sections

Break distinct steps or concepts into tagged sections, like extracting helper functions. If a block is 50+ lines or you'd add a comment like "Now we do X", it should be a tagged section. Each section gets a single, clear responsibility.

```markdown
// bad — 50-line monolithic instruction block
First do this, then do that, then check this, then...

// good — decomposed into focused sections
<ExecutionSteps>
    **STEP 1:** Execute <ParseInput/>
    **STEP 2:** Execute <ProcessFiles/>
    **STEP 3:** Execute <GenerateOutput/>
</ExecutionSteps>
```
