---
description: Route an agents-tools or skill-cli Swift package change to its change flow, versioning, CI and documentation owners.
---
## Package Route

- Read `README.md` and, when present, `CONTRIBUTING.md` before editing, and
  follow the organization
  [maintenance change flow](https://github.com/agents-tools/.github/blob/master/MAINTENANCE.md#change-flow).
- Before changing versions, dependencies, packaging or release workflows, read
  the organization [VERSIONING](https://github.com/agents-tools/.github/blob/master/VERSIONING.md)
  and `Documentation/Reference/Release.md`.
- `.github/swift-package.json` configures package validation; the required
  checks are `policy / policy` and `validate / result`. Keep shared workflow
  callers pinned to one full commit of agents-tools/github-workflows.
- Read toolchain and deployment minimums from `Package.swift` and
  `.github/swift-package.json` instead of restating them.
- Read `Documentation/README.md` before placing documentation and
  `Documentation/Architecture/README.md` before changing package structure.
