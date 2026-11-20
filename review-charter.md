---
date_created: '[[2026-07-07]]'
date_modified: '[[2026-10-01]]'
---
# Review charter

Shared value system for multi-agent review commands (`/api_review`, `/team_review`). Every review agent judges by these values and reports findings in this schema.

## Values

The three gods (`<ThreeGods>` in `~/.claude/docs/decision_criteria.md`, user rule 2026-10-01), above a floor of correctness. We believe in them; kitschy, we know. A reviewer judges every line by them, not only the lines a rule names. Earlier wins a conflict:

1. **Simple** — few concepts, few entry points, a small surface. A caller finds the right call from names alone, with minimal steps, imports and type annotations.
2. **Fast** — never trade hot-path cost for surface sugar. A recommendation that adds runtime cost (allocation, clone, dynamic dispatch, copies at boundaries) must name that cost.
3. **Beautiful** — reads cleanly: the right names, one idiom, the style guide followed, and types that encode invariants the compiler enforces.

In an API review the gods rule, and two means serve them most often: good ergonomics, and leverage of the type system.

Tie-break: caller-side simplicity beats internal elegance.

## Hard rules

- Rust subject → load the style guide first: `zsh ~/.claude/scripts/rust_style/load-rust-style.sh` (Read the saved file if a path is printed). Its rules — including `dont-create-traits-for-single-implementations.md` — bind every word of every finding. No trait or generic recommendation may violate them.
- "The current design is right" and "reject" are valid verdicts. Ask of each recommendation: does it make the common call site simpler, or just different?
- allowlist/denylist, never the alternatives.

## Finding schema

Title / Where (paths + item names) / Class (`design-improvement` | `premise-challenge` | mechanical — when the command distinguishes) / Severity (critical | important | minor) / Problem (concrete — show the current call site or doc passage) / Impact / Recommendation (before/after sketch where it clarifies).
