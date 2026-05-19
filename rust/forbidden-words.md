---
date_created: '[[2026-05-05]]'
date_modified: '[[2026-05-18]]'
exceptions: text shaping
tags:
- rust
- style
- naming
- comments
- non-negotiable
mechanism: llm
pre_filter: '(?i)shape|honest|carve|gloss|bite|biting|bitten|plain English|load-bearing|full stop|pull\w*\s+\w+\s+weight|blast\s+radius'
---
## Forbidden words

Banned everywhere — prose, code, identifiers, comments, commits. **Permanent, non-negotiable.**

**Pre-send check:** scan every draft for each banned substring. If present, substitute the precise word. If no precise word fits, the sentence isn't making a claim — delete it. Don't surgically swap one word; rewrite the sentence.

**Counters:** hook hits are tracked in `~/.claude/state/forbidden-word-counts.json`, not in this guide. A rising local counter means the pre-send check failed.

### "honest"

Forms: honest, honestly, more/most honest, to be honest, in all honesty, the honest X, an honest Y. Bans apply to *things* (`an honest API`, `the design is more honest`) as well as claims. Smuggles in a virtue claim and implies the alternative is dishonest — both wrong moves.

Substitute: {direct, explicit, one-to-one, single-source-of-truth, simple, accurate} — or delete. **Not** truthfully / frankly / candidly.

### "shape"

regex: \b(reshaping|reshape|shapes|shaped|shape)\b
except: text shaping, shaper, text_shaping

Forms: shape, shaped, shapes, reshape, reshaping. Filler analogy. Name the concrete artifact: function, pattern, struct, enum, function signature, trait, type — and name it.

**Not** form / structure (same hedge, different letters).

**Exception:** `text shaping` / `shaper` (typography pipeline term, e.g. HarfBuzz) is canonical industry vocabulary — keep. The ban targets vague analogies, not domain terms. The `except:` line above is the machine-readable form parsed by the hook.

### "carve"

Forms: carve, carving, carved, carve-out, carve out. Metaphor that hides the operation. Pick the verb: **extract** (move body of code into a new home), **split** (one becomes two), **move** (single field relocates), **refactor** (behavior preserved), **introduce** (purely additive).

**Not** sculpt / tease apart (same hedge).

### "gloss"

Forms: gloss, glosses, glossed, glossing, glossary (when it means a short explanation). Pretentious jargon for plain-English explanation. Substitute: "plain-English explanation", "translation", "what it means in plain words", or "explanation".

**Not** annotation / summary when the job is *translating jargon into plain words* — name the job.

### "bite"

regex: \bbit(e|es|ing|ten)\b

Forms: bite, bites, biting, bitten. Metaphor that hides what actually happens. Pick the verb: **affects**, **hits**, **trips**, **trips up**, **fires on**.

Substitute: {affects, hits, trips, trips up, fires on} — or delete. **Not** stings / nips (same hedge).

### "plain English"

Forms: plain English. Filler that announces what the next clause already does — pure noise.

Substitute: delete. The sentence following the phrase already speaks plainly; the announcement adds nothing.

### "load-bearing"

regex: \bload-bearing\b

Forms: load-bearing. Metaphor that hides what actually depends on the thing. Name the dependency: which call site, invariant, test, or downstream consumer relies on it.

Substitute: {essential, required, depended-on, critical, relied-on} — or name the actual dependent. **Not** structural / foundational (same hedge).

### "full stop"

Forms: full stop, full-stop. Empty intensifier — adds emphasis without substance and signals the claim can't stand on its own.

Substitute: delete — or state the claim directly without the terminator. **Not** period / end of story / no exceptions (same hedge).

### "pulling its weight"

regex: \bpull(s|ed|ing)?\s+(its|their|his|her|my|your|our)\s+weight\b

Forms: pulling its weight, pulls its weight, pulled its weight, pull its weight, pulling their weight. Metaphor that hides whether the thing actually does its job. Name the concrete contribution: what function it serves, what it justifies, or what would break without it.

Substitute: {justifies its cost, does the work of X, is needed for Y} — or name the concrete dependent — or delete. **Not** earning its keep / carrying its weight / paying its way (same hedge).

### "dissolve"

Forms: dissolve, dissolves, dissolved, dissolving. Metaphor that hides what actually happens to the code — was the file deleted? Were its contents split out, moved, or inlined? Name the operation.

Substitute: {delete, remove, split, extract, inline, move} — or name the concrete operation. **Not** melt / evaporate / vanish (same hedge).

### "blast radius"

Forms: blast radius. Metaphor that hides what is actually affected. Name the concrete surface: which files, call sites, modules, or behaviors the change touches.

Substitute: {scope of change, affected call sites, files touched, surface area, what breaks} — or name the concrete dependents — or delete. **Not** footprint / impact (same hedge).

### Review pass

Flag every occurrence in identifiers, comments, and prose. Propose renames and rewrites — don't leave them in place.
