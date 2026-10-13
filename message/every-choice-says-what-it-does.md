---
date_created: "[[2026-10-13]]"
date_modified: "[[2026-10-13]]"
tags: [question]
mechanism: llm
test: "Does each option say what choosing it does, with exactly one recommendation and its reason?"
source: "~/.claude/docs/user_facing_explanation.md, the user's rule, in the doc since 2026-08-01: \"exactly one recommendation, with its reason\"; \"what each choice makes the system do\""
---
## Every choice says what it does

Describe what happens if each option is chosen. Recommend exactly one, with the reason tied to the user's goal or the failure it avoids.

### Bad
Action: Allow production_lifecycle.py promote-main and wrap in the nested-g2 showrunner, or say leave it unwrapped

### Good
Tonight's test of one showrunner under another passed, but auto mode refused its last step as a production deploy. That step finishes a production by copying its work to main (here a throwaway repo on this disk), so real productions will be refused too.

Allow (recommended): add a permission rule for that step, so real productions can finish.

Don't allow: natedev deletes the two test productions by hand.
