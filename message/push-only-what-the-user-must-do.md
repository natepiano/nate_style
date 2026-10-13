---
date_created: "[[2026-10-13]]"
date_modified: "[[2026-10-13]]"
tags: [push]
mechanism: llm
test: "Does this push name something only the user can do, or a finished-plan or ready-shots note?"
source: "User, 2026-10-05, ~/.claude/projects/-etc-nixos/memory/phone-push-must-be-actionable.md: \"The alert didn't make sense nor was it actionable\"; user, 2026-10-06, ~/.claude/projects/-home-natepiano-rust-cargo-liner/memory/hooks-speak-only-when-actionable.md: \"if it's redundant or incorrect and goes to the session it just fills its context for no good reason\"; ~/.claude/commands/showrunner/produce.md <Notify>: \"A unit's whole plan finished and merged; before/after shots ready for the user's review.\""
---
## Push only what needs the user

Push only for something only the user can do, or the <Notify> note cases: a whole plan finished and merged, or before/after shots ready for review. Send agent work to that agent by message.

### Bad
Phone push: "natedev: build caches swept" after the sweep restored free space.

### Good
Message the responsible session with the sweep result; send no phone push.
