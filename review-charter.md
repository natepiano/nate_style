---
date_created: '[[2026-07-07]]'
date_modified: '[[2026-07-07]]'
---
# Review charter

Shared value system for multi-agent review commands (`/api_review`, `/team_review`). Every review agent judges by these values and reports findings in this schema.

## Values (ranked — earlier wins a conflict)

1. **Ergonomics** — a caller guesses the right call from names alone; minimal steps, imports, type annotations.
2. **Uncompromising speed and performance** — never trade hot-path cost for surface sugar. A recommendation that adds runtime cost (allocation, clone, dynamic dispatch, copies at boundaries) must name that cost.
3. **Type-system leverage** — types encode invariants the compiler enforces; readability and changeability over cleverness.
4. **Simplicity** — fewer concepts, fewer entry points, less surface.

Tie-breaks: caller-side simplicity beats internal elegance; a real performance need beats surface sugar.

## Hard rules

- Rust subject → load the style guide first: `zsh ~/.claude/scripts/rust_style/load-rust-style.sh` (Read the saved file if a path is printed). Its rules — including `forbidden-words.md` and `dont-create-traits-for-single-implementations.md` — bind every word of every finding. No trait or generic recommendation may violate them.
- "The current design is right" and "reject" are valid verdicts. Ask of each recommendation: does it make the common call site simpler, or just different?
- allowlist/denylist, never the alternatives.

## Finding schema

Title / Where (paths + item names) / Class (`design-improvement` | `premise-challenge` | mechanical — when the command distinguishes) / Severity (critical | important | minor) / Problem (concrete — show the current call site or doc passage) / Impact / Recommendation (before/after sketch where it clarifies).
