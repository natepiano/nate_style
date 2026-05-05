---
date_created: '[[2026-05-05]]'
date_modified: '[[2026-05-05]]'
exceptions: text shaping
tags:
- rust
- style
- naming
- comments
- non-negotiable
mechanism: llm
pre_filter: '(?i)shape|honest|carve|gloss'
---
## Forbidden words

Banned everywhere — prose, code, identifiers, comments, commits. **Permanent, non-negotiable.**

**Pre-send check:** scan every draft for each banned substring. If present, substitute the precise word. If no precise word fits, the sentence isn't making a claim — delete it. Don't surgically swap one word; rewrite the sentence.

**Counters:** increment when the user has to point a word out again. A rising counter means the pre-send check failed.

### "honest" — counter: 10

Forms: honest, honestly, more/most honest, to be honest, in all honesty, the honest X, an honest Y. Bans apply to *things* (`an honest API`, `the design is more honest`) as well as claims. Smuggles in a virtue claim and implies the alternative is dishonest — both wrong moves.

Substitute: {direct, explicit, one-to-one, single-source-of-truth, simple, accurate} — or delete. **Not** truthfully / frankly / candidly.

### "shape" — counter: 20

Forms: shape, shaped, shapes, reshape, reshaping. Filler analogy. Name the concrete artifact: function, pattern, struct, enum, function signature, trait, type — and name it.

**Not** form / structure (same hedge, different letters).

**Exception:** `text shaping` / `shaper` (typography pipeline term, e.g. HarfBuzz) is canonical industry vocabulary — keep. The ban targets vague analogies, not domain terms.

### "carve" — counter: 3

Forms: carve, carving, carved, carve-out, carve out. Metaphor that hides the operation. Pick the verb: **extract** (move body of code into a new home), **split** (one becomes two), **move** (single field relocates), **refactor** (behavior preserved), **introduce** (purely additive).

**Not** sculpt / tease apart (same hedge).

### "gloss" — counter: 1

Forms: gloss, glosses, glossed, glossing, glossary (when it means a short explanation). Pretentious jargon for plain-English explanation. Substitute: "plain-English explanation", "translation", "what it means in plain words", or "explanation".

**Not** annotation / summary when the job is *translating jargon into plain words* — name the job.

### Review pass

Flag every occurrence in identifiers, comments, and prose. Propose renames and rewrites — don't leave them in place.
