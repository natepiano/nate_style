---
date_created: '[[2026-05-05]]'
date_modified: '[[2026-06-23]]'
exceptions: text shaping
tags:
- rust
- style
- naming
- comments
- non-negotiable
mechanism: llm
pre_filter: '(?i)shape|honest|carve|gloss|bite|biting|bitten|plain English|load-bearing|full stop|pull\w*\s+\w+\s+weight|blast\s+radius|hoist|in one breath|paper(s|ed|ing)?\s+over|pressure[\s-]+test(s|ed|ing)?|you(?:[\x27]re|\s+are)[\s-]+right[\s-]+to[\s-]+be[\s-]+suspicious|sharp[\s-]+point|fair|clobber|this[\s-]+one(?:[\s-]+is|\x27?s)[\s-]+on[\s-]+me|rather[\s-]+than[\s-]+vibes?|seam(s|ed|ing)?|runnable[\s-]+instruments?|throat[\s-]+clearing|sharp[\s-]+edge(s)?|drive[\s-]+by(s)?|stat(e|es|ed|ing)[\s-]+plainly|wrinkl\w*|plain[\s-]+versions?|payoffs?|spelunk\w*|clear[\s-]+eyed|hand[\s-]*wav(e|es|ed|ing)|worth[\s-]+naming[\s-]+precisely|let[\s-]+me[\s-]+ground|no[\s-]+metaphors?|worth[\s-]+getting[\s-]+exact|rather[\s-]+than[\s-]+guess(es|ing|ed)?|ground(ed|ing)|the[\s-]+tells?|the[\s-]+clean[\s-]+models?|worth[\s-]+flagging|evaporat\w*|conspir\w*|rid(e|es|ing|den)|rode|that(?:[\s-]+is|\x27?s)[\s-]+on[\s-]+me|it(?:[\s-]+is|\x27?s)[\s-]+worth|let[\s-]+me[\s-]+be[\s-]+exact|one[\s-]+decisive[\s-]+run(s)?|then[\s-]+a[\s-]+real[\s-]+fork(s)?|not[\s-]+another[\s-]+guess(es)?|guess|measur(e|es|ed|ing),?[\s-]+not[\s-]+infer(s|red|ring)?|worth[\s-]+anything|direct[\s-]+answer(s)?|truthful'
---
## Forbidden words

Banned everywhere — prose, code, identifiers, comments, commits. **Permanent, non-negotiable.** For each match: delete the word, or name the concrete thing (function, type, mechanism, cause, measurement). Never swap in a near-synonym.

### Register — the generative rule

Two tests, every sentence:

1. **Deletion test** — if the sentence survives removal with no loss of information, cut it. Kills trailers, self-grading, journey narration, stakes-building.
2. **Literal-mechanism test** — replace imagery (gambling, cooking, levers) with the cause, measurement, call site, or data. "The honest answer" → "The answer".

Target register: lab notebook.

### Banned terms

The list below is the source the matcher parses. Each `### "stem"` is one banned term; an optional `regex:` line overrides the default matcher and an optional `except:` line carves out domain-legitimate uses.

### "honest"

### "shape"

regex: \b(reshaping|reshape|shapes|shaped|shape)\b
except: text shaping, shaper, text_shaping

### "carve"

### "gloss"

### "bite"

regex: \bbit(e|es|ing|ten)\b

### "plain English"

### "load-bearing"

regex: \bload-bearing\b

### "full stop"

### "pulling its weight"

regex: \bpull(s|ed|ing)?\s+(its|their|his|her|my|your|our)\s+weight\b

### "dissolve"

### "blast radius"

### "hoist"

### "in one breath"

### "paper over"

regex: \bpaper(s|ed|ing)?\s+over\b

### "pressure-test"

regex: \bpressure[\s-]+test(s|ed|ing)?\b

### "you're-right-to-be-suspicious"

regex: \byou(?:['']re|\s+are)[\s-]+right[\s-]+to[\s-]+be[\s-]+suspicious\b

### "sharp-point"

regex: \bsharp[\s-]+point\b

### "fair"

regex: \bfair\b

### "clobber"

### "this-one-is-on-me"

regex: \bthis[\s-]+one(?:[\s-]+is|'?s)[\s-]+on[\s-]+me\b

### "rather-than-vibes"

regex: \brather[\s-]+than[\s-]+vibes?\b

### "seam"

regex: \bseam(s|ed|ing)?\b

### "runnable-instrument"

regex: \brunnable[\s-]+instruments?\b

### "throat-clearing"

regex: \bthroat[\s-]+clearing\b

### "sharp-edge"

regex: \bsharp[\s-]+edge(s)?\b

### "drive-by"

regex: \bdrive[\s-]+by(s)?\b

### "stated-plainly"

regex: \bstat(e|es|ed|ing)[\s-]+plainly\b

### "wrinkle"

### "plain-version"

regex: \bplain[\s-]+versions?\b

### "payoff"

### "spelunking"

### "clear-eyed"

regex: \bclear[\s-]+eyed\b

### "hand-waving"

regex: \bhand[\s-]*wav(e|es|ed|ing)\b

### "worth-naming-precisely"

regex: \bworth[\s-]+naming[\s-]+precisely\b

### "let-me-ground"

regex: \blet[\s-]+me[\s-]+ground\b

### "no-metaphors"

regex: \bno[\s-]+metaphors?\b

### "worth-getting-exact"

regex: \bworth[\s-]+getting[\s-]+exact\b

### "rather-than-guess"

regex: \brather[\s-]+than[\s-]+guess(es|ing|ed)?\b

### "grounded"

regex: \bground(ed|ing)\b

### "the-tell"

regex: \bthe[\s-]+tells?\b

### "the-clean-model"

regex: \bthe[\s-]+clean[\s-]+models?\b

### "worth-flagging"

regex: \bworth[\s-]+flagging\b

### "evaporate"

### "conspiracy"

regex: \bconspir(e|es|ed|ing|acy|acies|ator|ators|atorial|atorially)\b

### "ride"

regex: \brid(e|es|ing|den)\b|\brode\b

### "that's-on-me"

regex: \bthat(?:[\s-]+is|'?s)[\s-]+on[\s-]+me\b

### "it's-worth"

regex: \bit(?:[\s-]+is|'?s)[\s-]+worth\b

### "let-me-be-exact"

regex: \blet[\s-]+me[\s-]+be[\s-]+exact\b

### "one-decisive-run"

regex: \bone[\s-]+decisive[\s-]+run(s)?\b

### "then-a-real-fork"

regex: \bthen[\s-]+a[\s-]+real[\s-]+fork(s)?\b

### "not-another-guess"

regex: \bnot[\s-]+another[\s-]+guess(es)?\b

### "guess"

### "measure-not-infer"

regex: \bmeasur(e|es|ed|ing),?[\s-]+not[\s-]+infer(s|red|ring)?\b

### "worth-anything"

regex: \bworth[\s-]+anything\b

### "direct-answer"

regex: \bdirect[\s-]+answer(s)?\b

### "truthful"
