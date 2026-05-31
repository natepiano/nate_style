---
date_created: '[[2026-05-05]]'
date_modified: '[[2026-05-31]]'
exceptions: text shaping
tags:
- rust
- style
- naming
- comments
- non-negotiable
mechanism: llm
pre_filter: '(?i)shape|honest|carve|gloss|bite|biting|bitten|plain English|load-bearing|full stop|pull\w*\s+\w+\s+weight|blast\s+radius|hoist|in one breath|paper(s|ed|ing)?\s+over|pressure[\s-]+test(s|ed|ing)?|you(?:['']re|\s+are)[\s-]+right[\s-]+to[\s-]+be[\s-]+suspicious|sharp[\s-]+point|fair|clobber|this[\s-]+one(?:[\s-]+is|'?s)[\s-]+on[\s-]+me|rather[\s-]+than[\s-]+vibes?|seam(s|ed|ing)?|runnable[\s-]+instruments?|throat[\s-]+clearing|sharp[\s-]+edge(s)?|drive[\s-]+by(s)?|stat(e|es|ed|ing)[\s-]+plainly|wrinkl\w*|plain[\s-]+versions?|payoffs?'
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

### "hoist"

Forms: hoist, hoists, hoisted, hoisting. Metaphor that hides the operation. Name what actually moves and where: a declaration lifted out of a loop, a binding moved to an outer scope, an item promoted to a parent module, a check pulled before a branch.

Substitute: {lift, move up, move out, promote, extract, pull up, declare before use} — or name the concrete operation — or delete. **Not** elevate / raise / float up (same hedge).

### "in one breath"

Forms: in one breath. Filler that announces brevity instead of delivering it — the summary that follows already stands on its own.

Substitute: delete — or lead straight into the summary. **Not** in short / in a word / to put it simply (same hedge).

### "paper over"

regex: \bpaper(s|ed|ing)?\s+over\b

Forms: paper over, papers over, papered over, papering over. Metaphor that hides what the code actually does to compensate — name the concrete mechanism (a filter, a guard, a fallback) and where it runs.

Substitute: {compensates for, masks, works around, guards against} — or name the concrete mechanism — or delete. **Not** gloss over / cover up / patch over (same hedge).

### "pressure-test"

regex: \bpressure[\s-]+test(s|ed|ing)?\b

Forms: pressure test, pressure-test, pressure tested, pressure testing. Metaphor that hides what the check actually is — name the concrete test: which inputs, which failure modes, which edge cases the plan is run against.

Substitute: {test, stress, challenge, scrutinize, probe, validate} — or name the concrete check — or delete. **Not** stress-test / battle-test / kick the tires (same hedge).

### "you're-right-to-be-suspicious"

regex: \byou(?:['']re|\s+are)[\s-]+right[\s-]+to[\s-]+be[\s-]+suspicious\b

Forms: you're right to be suspicious, you are right to be suspicious. Sycophantic validation opener that flatters the reader before answering and adds no information.

Substitute: delete — answer the question or state the finding directly. **Not** good catch / great question / you're absolutely right / good instinct (same flattery).

### "sharp-point"

regex: \bsharp[\s-]+point\b

Forms: sharp point, sharp-point. Sycophantic validation that praises the reader's point as incisive instead of engaging with it.

Substitute: delete — address the point directly. **Not** good point / great point / astute observation (same flattery).

### "fair"

regex: \bfair\b

Forms: fair. Sycophantic validation that concedes or praises ("that's a fair point", "fair enough") instead of engaging with the argument.

Substitute: delete — address the point directly. **Not** good point / valid point / reasonable (same flattery).

### "clobber"

Forms: clobber, clobbers, clobbered, clobbering. Anachronistic, overly-familiar slang for overwriting a value — name the precise operation.

Substitute: {overwrite, replace} — or delete. **Not** trample / smash / blow away (same slang).

### "this-one-is-on-me"

regex: \bthis[\s-]+one(?:[\s-]+is|'?s)[\s-]+on[\s-]+me\b

Forms: this one is on me, this one's on me. Performative self-blame that gestures at accountability instead of stating the error and the fix.

Substitute: delete — or state the error and the fix directly. **Not** my bad / my fault / mea culpa (same performative blame).

### "rather-than-vibes"

regex: \brather[\s-]+than[\s-]+vibes?\b

Forms: rather than vibes, rather-than-vibes, rather than vibe. Superfluous filler — it can be removed from any sentence with no loss of meaning.

Substitute: delete. **Not** instead of vibes / not just vibes / over vibes (same filler).

### "seam"

regex: \bseam(s|ed|ing)?\b

Forms: seam, seams, seamed, seaming. Metaphor that hides the concrete boundary — name the actual interface, module boundary, API edge, or join point between the two pieces.

Substitute: {interface, boundary, module boundary, API edge, join point, junction} — or name the concrete edge — or delete. **Not** fault line / fissure / crack (same metaphor).

### "runnable-instrument"

regex: \brunnable[\s-]+instruments?\b

Forms: runnable instrument, runnable-instrument, runnable instruments. Vague pairing that names neither what runs nor what it measures — name the concrete artifact.

Substitute: {test, example, binary, demo} — or name the concrete artifact. **Not** executable instrument / runnable tool (same vague pairing).

### "throat-clearing"

regex: \bthroat[\s-]+clearing\b

Forms: throat clearing, throat-clearing. Filler that labels a preamble as throat-clearing instead of just deleting the preamble and stating the point.

Substitute: delete — lead with the point. **Not** preamble / hedging / to be clear (same filler).

### "sharp-edge"

regex: \bsharp[\s-]+edge(s)?\b

Forms: sharp edge, sharp-edge, sharp edges. Metaphor that hides the concrete failure mode — name what actually goes wrong: the API that panics on empty input, the field that silently drops data, the call that's easy to misorder.

Substitute: {pitfall, hazard, easy-to-misuse API, the failure mode} — or name the concrete failure mode — or delete. **Not** rough edge / gotcha / rough spot (same metaphor).

### "drive-by"

regex: \bdrive[\s-]+by(s)?\b

Forms: drive-by, drive by, drive-bys. Metaphor that hides what actually happened — a contribution or change made without context or follow-through. Name the concrete action: an unsolicited edit, a one-off comment, a quick fix with no test.

Substitute: {unsolicited, one-off, quick, ad-hoc, unrequested} — or name the concrete action — or delete. **Not** hit-and-run / fly-by / drive-thru (same metaphor).

### "stated-plainly"

regex: \bstat(e|es|ed|ing)[\s-]+plainly\b

Forms: stated plainly, stated-plainly, state plainly, states plainly, stating plainly. Superfluous filler — it announces directness instead of delivering it, and can be removed from any sentence with no loss of meaning.

Substitute: delete — lead straight into the claim. **Not** put plainly / simply put / to put it plainly (same filler).

### "wrinkle"

Forms: wrinkle, wrinkles, wrinkled, wrinkling, a real wrinkle. Filler metaphor that hides the actual complication — name the concrete issue: the edge case, the caveat, the dependency that breaks the simple version.

Substitute: {complication, snag, edge case, caveat, catch} — or name the concrete issue — or delete. **Not** quirk / kink / twist (same metaphor).

### "plain-version"

regex: \bplain[\s-]+versions?\b

Forms: the plain version, plain version, plain-version, plain versions. Filler that announces a simpler restatement instead of delivering it — name the concrete thing being simplified, or just give the simpler statement.

Substitute: {the simple case, the base case, the unadorned form, without X} — or name the concrete thing — or delete. **Not** the simpler version / the basic version / the stripped-down version (same filler).

### "payoff"

Forms: payoff, payoffs, the payoff, here's the payoff. Filler that announces a reward or result is coming instead of just stating the result — name the concrete benefit or outcome.

Substitute: {the result, the benefit, what you get, the outcome} — or name the concrete outcome — or delete. **Not** the upshot / the win / the reward (same filler).

### Review pass

Flag every occurrence in identifiers, comments, and prose. Propose renames and rewrites — don't leave them in place.
