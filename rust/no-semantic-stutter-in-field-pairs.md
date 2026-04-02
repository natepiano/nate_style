---
date_created: '[[2026-04-02]]'
date_modified: '[[2026-04-02]]'
tags:
- rust
- style
- naming
---
## No semantic stutter in field pairs

Treat semantic stutter as an API smell. If a field already names the feature, its type should
describe the state, mode, policy, or switch, not repeat the feature name.

```rust
// bad
touch_input: TouchInput::Enabled
trackpad_pinch_to_zoom: TrackpadPinchToZoom::Disabled

// better
touch_input: State::Enabled
touch_input: Mode::Enabled
touch_input: Switch::On

// best when the domain has a real concept
orientation: CameraOrientation::UpsideDown
time_source: TimeSource::Virtual
```

When replacing a `bool` with an enum, choose names that read naturally at the use site. If no
natural field/type pair exists, the API may be wrong and should be reconsidered instead of renamed
mechanically.
