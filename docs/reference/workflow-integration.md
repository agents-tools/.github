# Workflow integration

[agents-tools/github-workflows](https://github.com/agents-tools/github-workflows)
owns reusable workflows, their scripts and tests, and their caller interfaces
for agents-tools and skill-cli. Each organization's `.github` repository owns
its community documents, settings declaration, catalog, DESIGN, fonts and icon
sources. This repository's thin callers select the shared implementation and
pass this repository at the commit under test as the organization data source.

## Organization data

- [MAINTENANCE.md](../../MAINTENANCE.md) declares repository settings and
  required contexts. Keep its table and JSON declaration in agreement.
- [profile/catalog.json](../../profile/catalog.json) lists public,
  non-archived, non-fork repositories except `.github`, with their live About
  descriptions. `organization.about` describes `.github` itself.
- [DESIGN.md](../../DESIGN.md), fonts and icon provenance own presentation
  inputs. Render profiles, member dashboards, social previews and terminal
  SVGs locally with `github-readme-design` and commit them with their inputs.
  Member dashboards use an explicit accepted `.github` revision for DESIGN
  and catalog, plus their own member input. See [README](../../README.md).

## Adopt and update pins

Pin callers to a full reviewed `agents-tools/github-workflows` commit. A
release pin includes its version comment; an in-progress change uses the SHA
alone. Keep related pins together in each member's reviewed change. Shared
implementation validation belongs in that repository.

Before rolling pins or activating rulesets, run a representative consumer at
the exact candidate workflow commit. Swift changes need a package run; CLI
demo changes need a fresh executable and terminal recording on its build
runner. Preserve each member's smoke and release validation. Record the run
URL, consumer head, shared commit, check names and GitHub Actions App ID
(`15368`) in the adoption PR. Local syntax checks do not establish this gate.

Required contexts are declared in
[Maintenance](../../MAINTENANCE.md#activation-and-required-checks). Apply a
ruleset only after its exact contexts have appeared and passed on a real run.
Preserve existing protection until the replacement is verified. Update the
declaration and table with context changes, then read back live settings
through the shared organization checker. It reports drift and unknowns without
applying settings; public mode does not establish administrative conformance.

After representative acceptance, advance other members through their reviewed
PRs. A newer shared default commit is an update observation, not permission
to repin. Tags and releases follow [VERSIONING.md](../../VERSIONING.md).
