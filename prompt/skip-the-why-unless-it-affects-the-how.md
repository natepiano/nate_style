---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- prompt
- tokens
---
## Skip the why unless it affects the how

Cut context that doesn't change the agent's behavior. Focus on actionable instructions. Use clear conditionals without over-explanation.

```markdown
// bad — unnecessary context
Files are important because they contain information that we need to
process in order to generate the output the user expects...

// good
Process each file in ${DIRECTORY}

// bad — over-explained conditional
If the user provides arguments, which means they gave you something
when they called the command, then you should use those arguments...

// good
If $ARGUMENTS provided: use as ${FILE}. If $ARGUMENTS empty: ask user for path.
```
