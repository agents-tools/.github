# Changelog

## Unreleased

## 0.1.2

- Standardize member builds on the latest stable Xcode available to shared CI,
  with a matching `swift-tools-version`. Libraries and command-line tools
  support the three most recent released major generations of each declared
  platform. To upgrade, align `.github/swift-package.json`, package toolchain
  and platform declarations, and Homebrew macOS floors with the policy;
  current values are Xcode 26.6, Swift 6.3 and macOS 15.
- Use agents-tools/github-workflows for shared workflows and checks; callers
  adopt package aggregates and shared Homebrew validation. Organization
  profiles and presentation assets are rendered and checked locally.
  To upgrade, migrate callers and `.github/swift-package.json` using the
  [shared workflow README](https://github.com/agents-tools/github-workflows),
  replace profile and presentation workflow calls with the local commands in
  this repository's README, and verify replacement required contexts on a real
  consumer run before updating rulesets.
- Add github-workflows to the organization catalog and settings declaration.
- Declare `skill-cli/skill-cli.github.io`, the skill website, with the same
  settings and required contexts as the agents website.
- VERSIONING's release timing no longer describes how other repositories
  reference a release; the [workflow integration guide](docs/reference/workflow-integration.md)
  and each member's release reference own that.

## 0.1.1

- End the `.github` repository's About sentence with a period, like every
  member's; its catalog `about`, settings declaration and social preview match.

## 0.1.0

- Define shared maintenance, compatibility, versioning and release policy for
  the agents family: releases follow the governing delivery workflow, and the
  version change rides in the change's final pull request.
- Provide reusable policy, Swift package CI, presentation and profile
  workflows with caller contexts `policy / policy`, `validate / swift-package`,
  `presentation / presentation` and, for member dashboards, `check / profile`.
- Choose presentation checks from each caller's catalog `kind`: tools check
  their terminal and social preview; libraries, apps, distributions and
  `.github` check their social preview; website callers fail. Tools, libraries
  and apps commit a `logo/` directory whose catalog icons match the SHA-256
  receipts in `.github/design/icons/*/provenance.json`. Regenerated files
  upload as `presentation.tar` in the `presentation` artifact, laid out like
  the asset root.
- Publish the family DESIGN in Google's DESIGN.md format, with visual tokens
  for terminal demos, social previews and profiles, an app icon entry and
  framework logo entries. Fonts and icon layers live in `.github/design/`,
  with consumed icon copies recorded in `provenance.json`.
- Generate the organization profile and this repository's social preview from
  the catalog and DESIGN with the TypeScript presentation toolchain.
- Supply default community files and issue and pull-request templates.
- Include repository settings declarations and read-only membership, About,
  settings and policy checks in `scripts/`, and the workflow integration guide
  in `docs/reference/workflow-integration.md`.
