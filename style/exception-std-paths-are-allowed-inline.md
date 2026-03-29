---
tags: [rust, imports]
---

## Exception: `std::` paths are allowed inline

Standard library paths are short and universally recognized — no import required.

```rust
// both are fine
let map: std::collections::HashMap<String, i32> = std::collections::HashMap::new();

use std::collections::HashMap;
let map: HashMap<String, i32> = HashMap::new();
```
