# rust_style

An opinionated Rust style guide used across all of my Rust and Bevy projects.

## Structure

- `style/` — Individual rule files covering imports, lints, patterns, visibility, project setup, and Bevy-specific conventions.
- `*.base` — [Obsidian Bases](https://help.obsidian.md/bases) views that filter rules by tag. For Humans.

## Usage

Rules are loaded by claude code via the [`/rust_style`](https://github.com/natepiano/claude_commands/blob/main/commands/rust-style.md) slash command before writing or reviewing Rust code.
