---
date_created: "[[2026-04-19]]"
date_modified: "[[2026-04-19]]"
see_also: "[[when-to-split-a-module]]"
tags:
  - rust
  - modules
---
## Collapse split modules that grow thin

A split module is not a permanent shape. When refactoring — relocating types to their behavioral home, deleting dead code, merging redundant submodules — a previously-split module may be left with only one cluster inside. Collapse it back to a single file.

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

Delete `project/mod.rs`, rename `project/paths.rs` to `project.rs`, and drop the `pub use paths::*;` re-exports. Call sites do not change — the crate-level re-export surface is preserved because the items keep their paths through the parent.

### Splitting-then-unsplitting is normal

A module's shape should track its current contents, not its historical peak. A split that was justified at 600 lines with three clusters is no longer justified at 150 lines with one cluster. Treating the split as permanent preserves scaffolding that no longer holds anything up.

### What not to do

- **Do not preserve empty facades.** A `mod.rs` that only re-exports one child's items adds a navigation hop for zero benefit.
- **Do not leave `pub use child::*;` behind for compatibility.** Rename the single remaining child back to the parent name. The module system does not need a forwarding shim.
- **Do not collapse to hide incomplete relocation.** If you collapsed because you could not figure out where the types belonged, you skipped the relocation rule. Go back to it.
