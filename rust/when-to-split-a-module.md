---
date_created: "[[2026-04-10]]"
date_modified: "[[2026-04-19]]"
tags:
  - rust
  - modules
see_also:
  - "[[types-live-with-their-behavior]]"
  - "[[name-submodules-after-anchor-types]]"
  - "[[split-by-type-ownership]]"
---
## When to split a module into submodules

A flat `.rs` file should become a `module/mod.rs` with submodules when **two or more** of these are true:

1. **Multiple type clusters** -- the file defines 3+ top-level types (structs/enums) that don't appear in each other's field lists
2. **Mixed domains** -- the file contains logic that serves different concerns (e.g., git detection and Cargo parsing)
3. **Line count** -- the file exceeds ~500 lines of non-test code
4. **Independent testability** -- distinct sections would benefit from focused test modules

A single criterion alone is not enough. A 600-line file with one tightly coupled type cluster is fine. A 300-line file with three unrelated type clusters should split.

### Example: a file that should split

```text
# project.rs — 2121 lines, 6 unrelated type clusters

AbsolutePath, DisplayPath          ~90 lines   (path utilities)
GitOrigin, GitInfo, GitPathState  ~720 lines   (git detection)
ProjectType, CargoParseResult     ~360 lines   (cargo parsing)
RustProject, NonRustProject, ...  ~620 lines   (project types)
MemberGroup                        ~60 lines   (workspace members)
tests                              ~70 lines
```

This file hits all four criteria: 6 type clusters, 3+ distinct domains, 2000+ lines, and tests that could target individual domains.

### Example: a file that should not split

```text
# worktree_group.rs — 120 lines

WorktreeGroup<Kind>         primary struct
  impl WorktreeGroup        accessors, live_entry_count, renders_as_group
  impl Clone for ...        two Clone impls (Workspace, Package)
```

Only one type cluster, one domain, well under 500 lines. Splitting would create noise.

### Decision checklist

Before splitting, verify:

1. Can you name each proposed submodule with a domain noun? If not, the boundary may be artificial.
2. Are the type clusters independent -- no circular references between proposed submodules?
3. Does each proposed submodule have at least ~100 lines? Smaller than that, leave it in the parent.
