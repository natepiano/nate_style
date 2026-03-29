---
date_created: '[[2026-03-29]]'
date_modified: '[[2026-03-29]]'
tags:
- imports
- rust
---
## Exception: `std::` paths are allowed inline

Standard library paths are short and universally recognized — no import required.

```rust
// both are fine
let map: std::collections::HashMap<String, i32> = std::collections::HashMap::new();

use std::collections::HashMap;
let map: HashMap<String, i32> = HashMap::new();
```