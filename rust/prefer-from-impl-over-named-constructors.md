---
date_created: "[[2026-04-19]]"
date_modified: '[[2026-07-30]]'
tags: [rust, patterns]
mechanism: llm
candidates:
  kind: regex
  pattern: '\bfn from_\w+\s*\('
---
## Prefer `From`/`Into` impls over named constructor methods

When bridging a type boundary with a single-input, infallible conversion, implement `From` and let `Into` come for free — don't write a custom `from_xyz(T)` associated function.

```rust
// bad — named constructor for a boundary conversion
impl KeyPressState {
    const fn from_pressed(is_pressed: bool) -> Self {
        if is_pressed { Self::Pressed } else { Self::Released }
    }
}

let left = KeyPressState::from_pressed(key_input.pressed(KeyCode::ShiftLeft));

// good — `From` impl
impl From<bool> for KeyPressState {
    fn from(pressed: bool) -> Self {
        if pressed { Self::Pressed } else { Self::Released }
    }
}

let left: KeyPressState = key_input.pressed(KeyCode::ShiftLeft).into();
```

Call sites read as idiomatic Rust, compose with `impl Into<T>` parameter bounds, and get the standard `Into::into` blanket impl for free. `From` is the signal that says "this is a lossless, unambiguous conversion" — future readers recognize it on sight without looking up a custom constructor.

### `.into()` vs `Type::from(value)`

Both are idiomatic. Pick whichever makes the target type most visible at the call site:

- `value.into()` — when a binding annotation or function signature already names the target (`let left: KeyPressState = pressed.into();`).
- `Type::from(value)` — when there is no annotation to carry the target, especially inline in larger expressions (`let sample_mode = SampleMode::from(msaa);`).

`From::from(value)` (fully qualified) is only needed when neither shorter form can infer — rare.

### When a named constructor is still appropriate

Use a named constructor when `From` would be ambiguous or wrong:

- **Multiple interpretations of the same input type** — `Point::from_polar(f32, f32)` and `Point::from_cartesian(f32, f32)` take the same input types; neither should claim the `From<(f32, f32)>` slot.
- **Fallible conversions** — use `TryFrom`, not `From` and not a named infallible `fn`.
- **Conversions that need external context** — if the construction depends on state beyond the input, it isn't a `From`.
- **`const` contexts** — `From::from` can't be `const fn` on stable today. If the conversion must be usable in a `const` expression, a named `const fn` constructor is the only option.

### Not covered: required trait methods

This rule governs *inherent* associated functions. A trait that requires its implementors to construct `Self` owns that method's name — `Default::default`, `FromStr::from_str`, `FromIterator::from_iter`. Leave it alone, even when the signature matches `fn from_xyz(T) -> Self`.

```rust
// fine — the trait, not the type, names this
pub trait CascadeRootResource<A>: Resource {
    fn root(&self) -> A;
    fn from_root(root: A) -> Self;
}
```

Converting such a method into a `From` supertrait bound is a public API change, so it needs approval under [[public-api-changes-require-explicit-approval]] regardless. Weigh it on whether every implementor's `From<A>` would describe what the conversion does: a constructor that fills in fields the input doesn't carry is not the lossless conversion `From` advertises, and should stay a named trait method.

Renaming a method purely so it stops matching this rule's candidate pattern is evasion, not a fix — the same test [[agent-must-review-allows]] applies to suppressions: if you can't name what the renamed version does differently, don't rename it.
