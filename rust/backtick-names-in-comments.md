---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-04-29]]'
tags:
- rust
- style
mechanism: clippy
mode: flag
lint: doc_markdown
---
## Backtick names in `///` doc comments

Surround type, function, and variable names with backticks **in `///` doc comments**, so rustdoc renders them as inline code and intra-doc links resolve. Regular `//` comments don't need backticks.

```doc
// bad
/// Returns the Movable component for the given entity.

// good
/// Returns the `Movable` component for the given `Entity`.
```

### Exception: commented-out code

Leave identifiers bare in commented-out code — backticks would make un-commenting a syntax error.