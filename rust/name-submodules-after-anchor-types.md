---
date_created: "[[2026-04-10]]"
date_modified: "[[2026-04-19]]"
see_also: "[[split-by-type-ownership]]"
tags:
  - rust
  - modules
---
## Anchor types drive submodule boundaries and names

When splitting a module, identify the **anchor type** for each submodule -- the primary type that everything else in the file serves. The anchor type determines both the boundary (what code goes in that submodule) and the filename.

### Anchor type submodules

If a submodule has one primary type that its `impl` blocks and helper functions all serve, name the submodule after that type in snake_case.

```text
# good -- submodule named after its anchor type
project/
  root_item.rs      # RootItem enum, impl RootItem, traversal helpers
  member_group.rs   # MemberGroup enum, impl MemberGroup
```

A function belongs with its anchor type if:
- Its first parameter borrows the anchor type (`&GitInfo`, `&mut RustProject<Kind>`)
- It constructs or returns the anchor type
- It exists solely to support the anchor type's `impl` blocks

### Domain cohort submodules

When a submodule contains several peer types of equal weight with no single anchor, name it after the domain.

```text
# good -- domain noun, multiple peer types
project/
  git.rs       # GitOrigin, GitInfo, GitPathState — all peers in the git domain
  paths.rs     # AbsolutePath, DisplayPath — both path newtypes
```

### Parent module naming

The parent module name should reflect the domain, not necessarily a single type. If the most-used type is `RootItem` (462 occurrences across the codebase) but the module also contains `RustProject`, `NonRustProject`, `GitInfo`, and `MemberGroup`, the parent name `project` captures the domain better than `root_item`.

### Example: splitting `project.rs`

```text
# bad -- parent named after one type
root_item/
  mod.rs

# good -- parent named after the domain
project/
  mod.rs            # facade: mod + pub use
  paths.rs          # anchor: AbsolutePath (+ DisplayPath, home_relative_path)
  git.rs            # cohort: GitOrigin, GitInfo, GitPathState, detection functions
  cargo.rs          # cohort: ProjectType, ExampleGroup, from_cargo_toml, target collection
  rust_project.rs   # anchor: RustProject<Kind> (+ NonRustProject, WorktreeGroup, RootItem, traversal)
  member_group.rs   # anchor: MemberGroup (+ count_rs_files_recursive)
```

### Naming anti-patterns

Avoid names that don't predict content:

```text
# bad -- generic dumping grounds
helpers.rs
utils.rs
common.rs
misc.rs
types.rs
model.rs
```

`types.rs` and `model.rs` describe code shape, not domain — they signal that types were grouped by what they *are* (data definitions) instead of what they *do*. When every submodule has an anchor type, the anchor's name is always more predictive than "types."
