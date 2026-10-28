---
tier: C
family: types
input_scope: file
approval: always
date_created: "[[2026-10-27]]"
date_modified: "[[2026-10-27]]"
see_also:
  - "[[tests-live-with-the-type-under-test]]"
  - "[[always-use-nextest]]"
tags: [rust, types, tests]
mechanism: llm
---
## Test fixture ownership

A test that starts work which can outlive it owns that work through a fixture. Such work includes worker threads, supervisors, background runtimes, and process-global overrides of config, keymap, theme or cache paths. A helper never returns a bare app or handle while that work runs unowned.

The fixture's `Drop` releases in a fixed order:

1. Drop the app, so nothing sends new work.
2. Join or drain every worker. Do all of them, also after the first one fails.
3. Release override guards and remove temp paths.

```rust
// bad: the worker can still write to the temp dir after it is removed
fn app_with_workers() -> App { App::start(&config) }

// good: the fixture owns the app, the workers and the paths
struct WorkerFixture { app: Option<App>, workers: Vec<JoinHandle<()>>, _cache: TempDir }

impl Drop for WorkerFixture {
    fn drop(&mut self) {
        drop(self.app.take());
        let failures: Vec<_> = self.workers.drain(..).filter_map(|w| w.join().err()).collect();
        if !failures.is_empty() && !std::thread::panicking() { panic!("{} workers panicked", failures.len()); }
    } // `_cache` is removed after the workers stop
}
```

Quiet fixtures are the default: a helper starts no real workers or startup effects unless the test asks for them and then owns them.

Test helpers panic with context (`expect("load keymap fixture")`), and never call `std::process::abort()`.

Tests that use process-global fixtures must be stable under nextest. Either isolate the fixtures per process, or run that group with `--test-threads 1` and say why.
