---
date_created: "[[2026-04-10]]"
date_modified: "[[2026-05-03]]"
tags:
  - rust
  - modules
see_also:
  - "[[types-live-with-their-behavior]]"
mechanism: llm
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

### Where the original file goes

Splitting is a replacement, not a layering. The flat file either becomes `module/mod.rs` or disappears entirely:

1. **Rename to `module/mod.rs`** if a facade is genuinely useful -- module docs, cross-cluster impls, or re-exports that differ from the parent's.
2. **Delete** if the parent's `mod.rs` can declare the new submodules directly (e.g. `mod font_features;` in `layout/mod.rs` instead of hidden inside a leftover `types.rs`).

Never keep the original file as a shell that declares the new modules via `#[path = "peer_file.rs"]`. That preserves the original name as an empty intermediary and forces every use to hop through it. When in doubt, pick (2) -- a facade is only useful if it hides something.

## Collapse split modules that grow thin

A split module is not a permanent shape. When refactoring -- relocating types to their behavioral home, deleting dead code, merging redundant submodules -- a previously-split module may be left with only one cluster inside. Collapse it back to a single file.

### When to collapse

Collapse a `module/` directory back to `module.rs` when any of the following is true:

1. **Only one submodule has meaningful content** after relocation. A facade over a single child file is pure overhead.
2. **The remaining cluster fits under ~500 lines** and is one domain. The original split-decision criteria no longer hold.
3. **Every surviving submodule is a thin data file** (one small type, few impl lines). You were probably holding the split open for an anchor-type that has since moved elsewhere.

### What collapse looks like

```text
# before -- residue after relocation
project/
  mod.rs            # facade: mod paths; pub use paths::*;
  paths.rs          # AbsolutePath, DisplayPath — only cluster left

# after
project.rs          # AbsolutePath, DisplayPath — inlined, no facade
```

Delete `project/mod.rs`, rename `project/paths.rs` to `project.rs`, and drop the `pub use paths::*;` re-exports. Call sites do not change -- the crate-level re-export surface is preserved because the items keep their paths through the parent.

### Splitting-then-unsplitting is normal

A module's shape should track its current contents, not its historical peak. A split that was justified at 600 lines with three clusters is no longer justified at 150 lines with one cluster. Treating the split as permanent preserves scaffolding that no longer holds anything up.

### What not to do

- **Do not preserve empty facades.** A `mod.rs` that only re-exports one child's items adds a navigation hop for zero benefit.
- **Do not leave `pub use child::*;` behind for compatibility.** Rename the single remaining child back to the parent name. The module system does not need a forwarding shim.
- **Do not collapse to hide incomplete relocation.** If you collapsed because you could not figure out where the types belonged, you skipped the relocation rule. Go back to it.
