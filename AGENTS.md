# Agent Guide

Read `README.md` first.

- This repository owns organization data, documents and thin workflow callers.
  Reusable workflows and their checkers belong to
  [agents-tools/github-workflows](https://github.com/agents-tools/github-workflows).
- `MAINTENANCE.md` owns change flow, settings, required contexts, review and
  legacy exceptions. Update its JSON declaration and required-context table
  together. `VERSIONING.md` owns family version policy and release order.
- `docs/reference/workflow-integration.md` owns organization adoption policy
  and the real-run gate before activating rulesets or rolling workflow pins.
- Keep catalog membership equal to the organization's public, non-archived,
  non-fork repositories except `.github`. Every catalog `about` equals the
  live repository description, including `organization.about` for `.github`.
  Summaries state what the repository does for a visitor in one sentence.
- Render `profile/README.md` and social previews locally with the
  `github-readme-design` toolchain using the commands in `README.md`; commit
  inputs and generated outputs together. Private dashboards add their own
  member input to the catalog and DESIGN from an explicit standard commit.
- Read `DESIGN.md` before visual or asset work. It owns visual tokens and icon
  entries. Regenerate affected outputs after token or icon artwork changes.
  Record consumed icon copies and their digests in
  `.github/design/icons/*/provenance.json`. Tools use the app icon style;
  reusable libraries use the framework icon style.
- Keep community files and templates applicable to every agents-tools
  repository. Repository-specific build and test commands belong in each
  repository's README.
- Before handoff, run local DESIGN lint (zero errors and warnings), profile
  and social-preview checks, `actionlint`, and `git diff --check origin/master`.
  Run organization checks through `github-workflows`; report live drift and
  unknowns. Public checks do not establish administrative settings conformance.
