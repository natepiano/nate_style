---
date_created: '[[2026-04-11]]'
date_modified: '[[2026-04-19]]'
see_also: "[[module-roots-as-table-of-contents]]"
tags:
- rust
- bevy
- modules
---
## Bevy plugin definitions live with their struct

A plugin's struct and `impl Plugin for` must live in the same module root — `lib.rs`, `main.rs`, `mod.rs`, or a flat `module.rs` file. Never delegate plugin build logic to a submodule via a builder function.

The plugin should appear after the table of contents (after all `mod` declarations and `pub use` re-exports).

```rust
// bad — lib.rs delegates its own plugin build to a submodule
impl Plugin for WindowManagerPlugin {
    fn build(&self, app: &mut App) {
        observers::build_plugin(app, path, persistence);
    }
}

// good — lib.rs owns its plugin build inline
impl Plugin for WindowManagerPlugin {
    fn build(&self, app: &mut App) {
        app.add_plugins(MonitorPlugin)
            .insert_resource(config)
            .add_observer(observers::on_managed_window_added)
            .add_systems(Update, systems::save_window_state);
    }
}
```

### When a module defines a plugin

A module defines a plugin when it needs to register things with the Bevy app — systems, observers, resources, gizmo groups, etc. Modules that only export types, constants, or pure logic do not need a plugin.

This applies equally to directory submodules (`mod.rs`), flat files (`module.rs`), and crate roots (`lib.rs`, `main.rs`).

### Directory submodules are the registration point for their domain

A `mod.rs` that represents a Bevy feature domain defines a plugin. This plugin is the natural place to register everything the domain needs — including items from its children. When a child only contributes a system or a couple of observers, the parent's plugin registers them directly. Don't create a child plugin for trivial registration.

```rust
// camera/mod.rs — registers its domain, including small child contributions
pub(crate) struct CameraPlugin;

impl Plugin for CameraPlugin {
    fn build(&self, app: &mut App) {
        // child with substantial registration — its own plugin
        app.add_plugins(ZoomPlugin)
            // child with one observer — register directly
            .add_observer(zoom_to_target::on_zoom_to_target)
            // child with one system — register directly
            .add_systems(Update, tracking::update_camera_tracking);
    }
}

// camera/zoom_to_target.rs — one observer, no plugin needed
pub(super) fn on_zoom_to_target(trigger: Trigger<ZoomToTarget>, ...) { ... }

// camera/zoom.rs — enough registration to warrant its own plugin
pub(super) struct ZoomPlugin;

impl Plugin for ZoomPlugin {
    fn build(&self, app: &mut App) {
        app.init_gizmo_group::<FocusGizmo>()
            .init_resource::<ZoomTarget>()
            .init_resource::<FocusSettings>()
            .add_systems(Update, handle_zoom);
    }
}
```

### No builder functions

Submodules must not export `build_plugin()`, `register_systems()`, or similar functions that accept `&mut App`. If a submodule has enough wiring to need an `&mut App`, it should be its own plugin.

```rust
// bad — submodule exports a builder function
// observers.rs
pub(crate) fn build_plugin(app: &mut App, path: PathBuf) { ... }

// good — submodule defines a plugin struct
// observers.rs
pub(super) struct ObserverPlugin;
impl Plugin for ObserverPlugin { ... }
```

### Visibility

- Top-level plugins (registered in `main.rs` or `lib.rs`): `pub(crate)`, or `pub` if re-exported from a library crate
- Child plugins (registered by a parent plugin): `pub(super)`
