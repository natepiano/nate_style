---
tags: [guild/units, guild-event, head/units]
date_created: "[[2026-10-28]]"
date_modified: "[[2026-10-28]]"
---
## Find a failing test's cause before you scope its repair
When a phase breaks a test outside its files, compare the failing assertion with the text the phase now prints before you write the repair prompt. A printed report or message line is a contract with every script and test that reads it. Do not guess the cause file and limit the worker to that file.
Evidence: sdlc-roles phase 5, F009. Repair round 3 (20:10 EDT) limited the worker to `send.py` on a guess. The cause was the recipient line in `broadcast.py`, which `test_codex_winddown.py` pins at lines 303, 320 and 332. Round 3 made no edits; round 4 (20:15 EDT) targets `broadcast.py` and the test expectations.
Source: roles-unit report; run d739a3b3 `findings_state.json`, `board.log` 20:11 EDT and `phases/5/fix_prompt_3_test.md`, 2026-10-28.
