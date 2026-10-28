---
tier: B
family: types
input_scope: crate
approval: always
date_created: "[[2026-10-03]]"
date_modified: "[[2026-10-16]]"
see_also: "[[enums-over-bool-for-owned-booleans]]"
tags: [rust, types, patterns]
mechanism: llm
candidates:
  surface: partial
  uncovered: 'multiline or async public signatures, error definitions, String error fields, Result-to-Option conversions'
  kind: regex
  pattern: '\bpub fn .*->\s*Option<'
---
## Public failures return named errors, not `Option`

A public function that can fail returns `Result<T, E>`, where `E` is a public error enum that names each way it fails. When `None` could mean "the bytes did not parse", "the asset did not load" or "that ID was never registered", the caller cannot tell which one happened. It cannot report the failure, so it falls back quietly.

- Each variant names one failure and carries the value that identifies it: the name, the ID, the path.
- Derive `thiserror::Error`. Wrap a lower-level error with `#[from]` or `#[source]` so the cause chain survives.
- Export the error beside the type whose functions return it.
- Never carry a failure as a `String` field (`error: String`). Give the field the error type.
- Never turn a `Result` into an `Option` with `.ok()` at a public boundary. That drops the reason.

```rust
// bad — None stands for several different failures
impl FontRegistry {
    pub fn register_font(&mut self, name: &str, data: &[u8]) -> Option<FontId> { ... }
    pub fn font_id_by_name(&self, name: &str) -> Option<FontId> { ... }
}

pub struct FontLoadFailed {
    pub path: String,
    pub error: String,
}

// good — each failure has a name and the data that identifies it
#[derive(Debug, Clone, thiserror::Error)]
pub enum FontParseError {
    #[error("font `{name}` is not a readable font face")]
    Unreadable { name: String },
}

#[derive(Debug, Clone, thiserror::Error)]
pub enum FontRegistrationError {
    #[error(transparent)]
    Unreadable(#[from] FontParseError),
}

#[derive(Debug, Clone, thiserror::Error)]
pub enum FontLookupError {
    #[error("no font family is registered as `{0}`")]
    UnknownFamilyName(String),
    #[error("no font family has ID {0:?}")]
    UnknownFamilyId(FontId),
}

impl FontRegistry {
    pub fn register_font(
        &mut self,
        name: &str,
        data: &[u8],
    ) -> Result<FontId, FontRegistrationError> { ... }

    pub fn font_id_by_name(&self, name: &str) -> Result<FontId, FontLookupError> { ... }
}

pub struct FontLoadFailed {
    pub path: String,
    pub error: FontLoadError,
}
```

### When `Option` is right

`None` is an ordinary answer with one meaning, and that meaning is not a failure:

- `first()`, `last()`, the `parent()` of a root;
- an optional setting that is unset;
- a lookup that asks whether something is there.

A lookup whose key should exist is different. That covers an ID the registry handed out, or a name the caller registered. When that key is missing, something failed, so the lookup returns a `Result`.

When `None` is an ordinary answer with a meaning of its own, name it with an enum instead of `Option`, as [[enums-over-bool-for-owned-booleans]] does for `bool`:

```rust
pub enum TextInkMeasurement {
    NoVisibleInk,
    Visible(TextInk),
}
```

### Not public, or not owned

- `pub(crate)` and private helpers may return `Option` inside the crate. The public function that calls them names the failure before a caller outside the crate sees it.
- Trait signatures we do not own keep their return type (`Iterator::next`).
