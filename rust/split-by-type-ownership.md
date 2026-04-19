---
date_created: "[[2026-04-10]]"
date_modified: "[[2026-04-19]]"
see_also:
  - "[[name-submodules-after-anchor-types]]"
  - "[[types-live-with-their-behavior]]"
tags: [modules, rust]
---
## Split along type ownership, not code shape

When splitting a module into submodules, draw boundaries around **type clusters**, not around code categories. Each submodule should own one type cluster: the primary type, its field types, its `impl` blocks, and the free functions that construct or operate on it.

### Bad: split by code shape

Separating types from functions or tests from code produces files that are coupled across every boundary. Every change touches multiple files.

```text
# bad -- all types in one file, all functions in another
project/
  mod.rs
  types.rs       # all structs and enums
  functions.rs   # all free functions
  tests.rs       # all tests
```

### Bad: one type per file

Over-splitting creates navigation overhead and empty-feeling files. A 30-line struct with a 20-line impl doesn't need its own file.

```text
# bad -- too granular
project/
  mod.rs
  absolute_path.rs    # 70 lines
  display_path.rs     # 20 lines
  git_origin.rs       # 30 lines
  git_info.rs         # 100 lines
  git_path_state.rs   # 40 lines
  ...12 more files
```

### Good: split by type ownership

Each submodule owns a cohesive type cluster. The calling function's type signature tells you which submodule it belongs to.

```text
# good -- each submodule owns a type cluster
project/
  mod.rs            # facade only
  paths.rs          # AbsolutePath, DisplayPath, home_relative_path
  git.rs            # GitOrigin, GitInfo, GitPathState, all detection functions
  cargo.rs          # ProjectType, ExampleGroup, from_cargo_toml, target collection
  types.rs          # RustProject<Kind>, NonRustProject, WorktreeGroup, RootItem
  member_group.rs   # MemberGroup, count_rs_files_recursive
```

### Where tests go after a split

Tests stay with the code they test. Each submodule gets its own `#[cfg(test)] mod tests` at the bottom. Do not create a separate `tests.rs` submodule -- it separates tests from the code they exercise and forces items to be more visible than necessary.

```rust
// git.rs -- tests at the bottom of the same file
fn detect_git_path_state(project_dir: &Path) -> GitPathState { ... }

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn git_repo_root_finds_ancestor_git_directory() { ... }
}
```

### Cross-reference check

Before finalizing boundaries, verify there are no circular dependencies between proposed submodules. If submodule A needs a type from B and B needs a type from A, the boundary is in the wrong place -- merge them or move the shared type to the parent.
