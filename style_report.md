---
date_created: "[[2026-04-07]]"
date_modified: "[[2026-04-07]]"
tags:
  - report
  - style
---
# Style Report
## Style Usage History
| [[style_report_usage#Style\|Style]] | [[style_report_usage#Projects\|Projects]] | [[style_report_usage#Applied\|Applied]] | [[style_report_usage#Partial\|Partial]] | [[style_report_usage#Skipped\|Skipped]] | [[style_report_usage#Last Seen\|Last Seen]] | [[style_report_usage#Trend\|Trend]] |
|---|---|---|---|---|---|---|
| [[no-magic-values]] | 5 | 8 | 0 | 1 | 2026-04-07 10:06 | active |
| [[spell-out-names]] | 7 | 8 | 0 | 0 | 2026-04-07 10:06 | active |
| [[constants-file-organization]] | 5 | 8 | 0 | 0 | 2026-04-07 10:06 | active |
| [[cargo-toml-lints]] | 8 | 7 | 0 | 1 | 2026-04-07 10:06 | active |
| [[enums-over-bool-for-owned-booleans]] | 6 | 7 | 0 | 0 | 2026-04-07 10:06 | active |
| [[test-module-allow-boilerplate]] | 5 | 6 | 0 | 0 | 2026-04-07 10:06 | active |
| [[import-types-directly]] | 4 | 6 | 0 | 0 | 2026-04-07 10:06 | active |
| [[imports-go-at-the-top-of-the-file]] | 4 | 5 | 0 | 0 | 2026-04-07 10:06 | active |
| [[leaf-module-visibility]] | 6 | 5 | 0 | 1 | 2026-04-07 10:06 | active |
| [[use-a-context-struct-when-arguments-exceed-7]] | 3 | 3 | 1 | 0 | 2026-04-07 10:06 | active |
| [[import-the-module-for-functions-not-the-function-itself]] | 3 | 3 | 0 | 0 | 2026-04-07 10:06 | active |
| [[prefer-local-relative-imports]] | 3 | 3 | 0 | 0 | 2026-04-07 10:06 | active |
| [[backtick-names-in-comments]] | 2 | 3 | 0 | 0 | 2026-04-05 08:24 | active |
| [[collapse-if-let-with-inner-conditions]] | 3 | 3 | 0 | 0 | 2026-04-05 08:24 | active |
| [[no-pubcrate-in-nested-modules]] | 2 | 2 | 0 | 0 | 2026-04-04 08:39 | active |
| [[dont-repeat-type-name-in-fields]] | 2 | 2 | 0 | 0 | 2026-04-07 10:06 | active |
| [[import-constants-at-the-top]] | 2 | 2 | 0 | 0 | 2026-04-07 10:06 | active |
| [[prefer-functional-patterns]] | 2 | 2 | 0 | 0 | 2026-04-07 10:06 | active |
| [[module-roots-as-table-of-contents]] | 2 | 2 | 0 | 0 | 2026-04-07 10:06 | active |
| [[use-bevy_kana-in-all-bevy-crates]] | 1 | 1 | 0 | 0 | 2026-04-04 08:39 | active |
| [[cargo-toml-bevy-lints]] | 1 | 1 | 0 | 0 | 2026-04-04 16:51 | active |
| [[reflectcomponent-suffices-for-brp-mutation]] | 1 | 1 | 0 | 0 | 2026-04-05 08:24 | active |
| [[never-prefix-unused-fields-or-variables-with]] | 1 | 1 | 0 | 0 | 2026-04-05 08:24 | active |
| [[inline-variables-in-format-strings]] | 1 | 1 | 0 | 0 | 2026-04-05 08:24 | active |
| [[no-wildcard-reexports]] | 1 | 1 | 0 | 0 | 2026-04-05 08:24 | active |
| [[derive-test-values-from-production-constants]] | 1 | 1 | 0 | 0 | 2026-04-07 10:06 | active |
| [[dont-create-traits-for-single-implementations]] | 1 | 1 | 0 | 0 | 2026-04-07 10:06 | active |
| [[borrow-the-slice-not-the-container]] | 1 | 1 | 0 | 0 | 2026-04-07 10:06 | active |
| [[use-pubcrate-in-top-level-private-modules]] | 1 | 1 | 0 | 0 | 2026-04-07 10:06 | active |
## By Project
**bevy_brp** — 1 styles, 3 applied, 0 partial, 0 skipped
**bevy_catenary** — 13 styles, 58 applied, 1 partial, 3 skipped
**bevy_diegetic** — 12 styles, 64 applied, 0 partial, 3 skipped
**bevy_kana** — 2 styles, 13 applied, 0 partial, 1 skipped
**bevy_lagrange** — 5 styles, 19 applied, 1 partial, 0 skipped
**bevy_liminal** — 12 styles, 58 applied, 1 partial, 3 skipped
**bevy_window_manager** — 7 styles, 41 applied, 0 partial, 3 skipped
**cargo-mend** — 8 styles, 35 applied, 0 partial, 1 skipped
**cargo-port** — 7 styles, 25 applied, 0 partial, 1 skipped
**nateroids** — 10 styles, 56 applied, 0 partial, 3 skipped
**obsidian_knife** — 8 styles, 39 applied, 0 partial, 1 skipped
## Local Styles

### cargo-port

| [[style_report_usage#Style\|Style]] | [[style_report_usage#Applied\|Applied]] | [[style_report_usage#Partial\|Partial]] | [[style_report_usage#Skipped\|Skipped]] | [[style_report_usage#Last Seen\|Last Seen]] | [[style_report_usage#Trend\|Trend]] |
|---|---|---|---|---|---|
| [[frontend-boundaries]] | 1 | 0 | 0 | 2026-04-07 10:06 | active |

## Skips & Partial Applications

| Style | Project | Date | Reason |
|---|---|---|---|
| [[no-magic-values]] | bevy_diegetic | 2026-04-07 | Moving 28 constants across 9 files into 3 new constants.rs files risks compile errors alongside 11 other concurrent findings. |
| [[cargo-toml-lints]] | nateroids | 2026-04-04 | Binary crate intentionally allows cargo_common_metadata; style guide needs policy for binary crates. |
| [[leaf-module-visibility]] | bevy_diegetic | 2026-04-07 | All 5 items are structurally required to be pub because they appear in public interfaces. |
| [[use-a-context-struct-when-arguments-exceed-7]] | bevy_lagrange | 2026-04-07 | Bevy Query invariant lifetimes prevent bundling queries into a struct; only non-query params were bundled. |

*Generated 2026-04-07T10:36:21Z from 98 log entries across 11 projects*
