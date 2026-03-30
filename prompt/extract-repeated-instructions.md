---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- prompt
- tokens
- structure
---
## Extract repeated instructions

If the same instruction appears 2+ times, extract it into a tagged section and reference it. Same operation should be done the same way throughout the command.

```markdown
// bad — "wait for user" repeated in steps 3, 7, 12, and 15
**STEP 3:** Present options. Wait for user response.
...
**STEP 7:** Present findings. Wait for user response.

// good — extracted and referenced
**STEP 3:** Present options. Execute <WaitForUserResponse/>
...
**STEP 7:** Present findings. Execute <WaitForUserResponse/>
```
