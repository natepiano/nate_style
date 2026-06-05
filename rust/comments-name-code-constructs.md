---
date_created: '[[2026-06-04]]'
date_modified: '[[2026-06-04]]'
tags:
- comments
- rust
- style
mechanism: llm
mode: flag
---
## Comments name code constructs

Review comments for vague verbs and metaphors. When code has names, the comment must name the concrete type, field, enum variant, resource, component, buffer, or table.

```rust
// bad
/// One vertex-pulling batch entity per batch key; runs ride in GPU record
/// tables.

// good
/// One vertex-pulling batch entity per `BatchKey`; text runs are stored as
/// `RunRecord`s in `GlyphBatch::run_records` and uploaded to
/// `BatchGpu::run_table: Handle<ShaderBuffer>`.
```

Fix the whole nearby comment cluster, not only the first sentence that sounds vague.
