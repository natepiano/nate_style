---
date_created: "[[2026-10-13]]"
date_modified: "[[2026-10-13]]"
tags: [all]
mechanism: llm
test: "After any Action: or No action needed. first line, does the message give what happened, why it matters to the user, then any action and where to take it?"
source: "Approved design, 2026-10-13, ~/.local/state/plan-backlog/2026-10-13-user-message-clarity.md: \"what happened, why it matters and what each choice does\"; user, 2026-10-08, ~/.claude/projects/-etc-nixos/memory/answer-in-a-few-lines.md: \"Can you permanently become more succinct ?\""
---
## What happened, why it matters, what you do

Give what happened, why it matters to the user, then what they do and where. Keep only the context needed to understand or act. A push's `Action:` line comes first, as the phone shows it; the body after it follows this order.

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
