---
date_created: "[[2026-10-13]]"
date_modified: "[[2026-10-13]]"
tags: [all]
mechanism: llm
test: "Can a reader understand every name in this message from what the message itself says?"
source: "~/.claude/docs/user_facing_explanation.md, the user's rules, in the doc since 2026-08-24 and 2026-08-01: \"A report that repeats on a timer is read cold.\"; \"Behavior first, name second. If the name is not needed for the decision, omit it.\""
---
## The reader starts cold

Assume the user knows only this message. Explain each session, unit, phase, script, flag, commit or file by what it does, or drop its name.

### Bad
**Hana: nested-g2 wrap**

Action: Allow production_lifecycle.py promote-main and wrap in the nested-g2 showrunner, or say leave it unwrapped

nested-g2 wrap blocked: auto mode refused promote-main (local bare repo only) as Production Deploy.

### Good
**Auto mode blocks finishing a production**

Action: In natedev, reply allow or don't allow.

Tonight's test of one showrunner under another passed, but auto mode refused its last step as a production deploy. That step finishes a production by copying its work to main (here a throwaway repo on this disk), so real productions will be refused too.

Allow (recommended): add a permission rule for that step, so real productions can finish.

Don't allow: natedev deletes the two test productions by hand.
