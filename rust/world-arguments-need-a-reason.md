---
tier: B
family: types
input_scope: file
date_created: "[[2026-11-22]]"
date_modified: "[[2026-11-22]]"
tags:
- bevy
- rust
- types
mechanism: llm
mode: propose
candidates:
  surface: whole
  kind: regex
  pattern: '&(''\w+\s+)?(mut\s+)?([a-z_]\w*::)*World\b'
see_also:
- "[[system-params-carry-their-behavior]]"
- "[[prefer-events-over-messages]]"
- "[[public-api-changes-require-explicit-approval]]"
---
## World Arguments Need a Reason

A function does not take `&mut World` or `&World` when a narrower Bevy form does the job.

The cost:
- `&mut World` makes each caller hold the whole world, so the caller runs alone.
- `&World` needs a `ParamSet` in a caller that also writes, and it blocks a parallel run with writers.
- Both hide what the function reads and changes.

Use the narrower form:
- A read or change by a system: the `Query` and `Res` it needs, or a `SystemParam` with methods.
- A change request: an event with an observer.
- A change of one entity: an entity event or `EntityCommands`.
- Work done once that needs many parameters: `commands.run_system_cached`.

```rust
// bad: each caller must hold the whole world to seat one cable end
pub fn seat_end(world: &mut World, cable: Entity, port: Entity) { ... }
// good: the caller triggers an event; an observer does the change
commands.trigger(SeatCableEnd { cable, port });

// bad: a read that blocks every writer
pub fn flying_plug_end(world: &World, cable: Entity) -> Option<Vec3> { ... }
// good: `cables` is `CableReads`, a SystemParam
cables.flying_plug_end(cable)
```

`World` stays only where Bevy gives nothing narrower:
1. The `apply` of a `Command`, `FromWorld::from_world`, and other signatures that Bevy or another crate owns.
2. An exclusive system that runs a schedule or a system and uses its result in the same call.
3. Work with component or resource types known only at run time: `ReflectComponent`, `ReflectResource`, access by `ComponentId`.
4. Tests, and setup called only from `Plugin::build` or `finish`.

Hooks and observers get `DeferredWorld` from Bevy; this rule does not cover it.
The doc comment of a function that keeps `World` names the case that applies.
A public signature with `World` goes to the user with that reason, in check 1.
