---
clippy: ptr_arg
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- patterns
- rust
---
## Borrow the slice, not the container

Function parameters should accept the borrowed slice form, not a reference to the owned type. The caller can always pass the owned type by reference — the reverse requires an unnecessary allocation.

```rust
// bad — forces callers to have an owned PathBuf
fn load_config(path: &PathBuf) -> Config { ... }
fn parse_name(name: &String) -> Name { ... }
fn process_items(items: &Vec<Item>) -> usize { ... }

// good — accepts any &Path, &str, or &[Item]
fn load_config(path: &Path) -> Config { ... }
fn parse_name(name: &str) -> Name { ... }
fn process_items(items: &[Item]) -> usize { ... }
```

| Owned type | Borrow as |
|---|---|
| `PathBuf` | `&Path` |
| `String` | `&str` |
| `Vec<T>` | `&[T]` |
| `Box<T>` | `&T` |
