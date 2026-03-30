---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- prompt
- structure
---
## Cross-reference with self-closing tags

Use `<TagName/>` to invoke a defined section. Never use vague references like "as described earlier" or "follow the steps from above."

```markdown
// bad
Follow the validation steps described in the section above

// good
Execute <ValidationSteps/>
```
