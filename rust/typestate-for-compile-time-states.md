---
tier: C
family: types
input_scope: file
mechanism: llm
mode: propose
see_also:
  - "[[make-invalid-states-unrepresentable]]"
  - "[[enums-over-option-when-none-has-meaning]]"
tags: [rust, types, patterns]
date_created: "[[2026-11-19]]"
date_modified: "[[2026-11-19]]"
---
## Typestate for States Known at Compile Time

When an operation is valid only in some states of a value, and the code knows the state at compile time, use the typestate pattern. Give each state its own type. Make each transition a method that consumes the value and returns the type of the next state. Then a call in the wrong state does not compile, and no runtime check is needed.

Use it for a builder with required steps, or for a session or connection lifecycle.

```rust
// bad — every call checks the state at run time
struct Connection { socket: Socket, authenticated: bool }
impl Connection {
    fn send(&mut self, message: &Message) -> Result<(), Error> {
        if !self.authenticated { return Err(Error::NotAuthenticated); }
        self.socket.write(message)
    }
}

// good — only an authenticated connection has `send`
struct Connection { socket: Socket }
struct Authenticated { socket: Socket }
impl Connection {
    fn authenticate(self, token: &Token) -> Result<Authenticated, Error> { ... }
}
impl Authenticated {
    fn send(&mut self, message: &Message) -> Result<(), Error> { self.socket.write(message) }
}
```

Limit: when the state comes from data at run time (a value read from a file, a message, or a database row), the compiler cannot know it. Use an enum whose variants carry each state's data.
