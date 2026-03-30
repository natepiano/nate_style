---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- prompt
- workflow
- structure
---
## Three or more steps need ExecutionSteps

Commands with 3+ sequential operations must have an `<ExecutionSteps>` block. Simple 2-step commands are exempt.

```markdown
// good — exact format
<ExecutionSteps>
    **EXECUTE THESE STEPS IN ORDER:**

    **STEP 1:** Execute <GatherInput/>
    **STEP 2:** Execute <ProcessData/>
    **STEP 3:** Execute <PresentResults/>
</ExecutionSteps>
```

Each step references a specific tagged section. The header "EXECUTE THESE STEPS IN ORDER" is mandatory.
