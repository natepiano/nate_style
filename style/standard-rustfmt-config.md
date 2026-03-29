---
tags: [rust, project-setup]
---

## Standard rustfmt config

Every repo has a `rustfmt.toml` at the workspace root with this exact config.

```toml
max_width = 100
comment_width               = 100
format_code_in_doc_comments = true
wrap_comments               = true
group_imports       = "StdExternalCrate"
imports_granularity = "Item"
reorder_imports     = true
enum_discrim_align_threshold = 50
struct_field_align_threshold = 50
fn_single_line             = true
match_block_trailing_comma = true
```
