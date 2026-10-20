# Versioning

The agents family releases in dependency order: **core → both CLIs → both
Homebrew taps**. Each releasing repository has its own version. A change
releases only the affected dependency chain; versions need not match across
repositories.

| Repository | Version source | Release tag | Release owner/checklist |
| --- | --- | --- | --- |
| `agents-tools/.github` | Git tag | `vX.Y.Z` | This policy and the [consumer real-run gate](Documentation/Reference/WorkflowIntegration.md#adopt-and-update-pins) |
| `agents-tools/core` | Git tag | `X.Y.Z` | [Core release checklist](https://github.com/agents-tools/core/blob/master/Documentation/Reference/Release.md) |
| `agents-tools/cli` | `BuildInfo.version` in `Sources/CLI/EntryPoint.swift` | `X.Y.Z` | [agents release checklist](https://github.com/agents-tools/cli/blob/master/Documentation/Reference/Release.md) |
| `skill-cli/cli` | `BuildInfo.version` in `Sources/CLI/EntryPoint.swift` | `vX.Y.Z` | [skill release checklist](https://github.com/skill-cli/cli/blob/master/Documentation/Reference/Release.md) |
| `agents-tools/homebrew-tap` | Upstream CLI version in each formula | None of its own | [agents tap](https://github.com/agents-tools/homebrew-tap#readme); formula validation in the agents checklist |
| `skill-cli/homebrew-tap` | Upstream CLI version in each formula | None of its own | [skill tap](https://github.com/skill-cli/homebrew-tap#readme); formula validation in the skill checklist |

Both `.github` repositories publish signed, annotated SemVer tags `vX.Y.Z`
on the default branch after a reviewed merge that changes a consumed interface
or output. A reusable workflow interface break increments MAJOR; a DESIGN
change requiring members to regenerate increments MINOR; a change preserving
member output increments PATCH. Consumers pin the full commit SHA with a
`# vX.Y.Z` comment so Dependabot proposes upgrades.

Create each standard tag only after the
[consumer real-run gate](Documentation/Reference/WorkflowIntegration.md#adopt-and-update-pins)
passes and the owner confirms that tag. Tags are immutable and never moved.
Do not introduce a duplicate version declaration into core or a tap.

## Choosing versions

Core and both CLIs follow [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).
Compatible fixes increment PATCH; compatible functionality increments MINOR.
Breaking changes increment MAJOR from `1.0.0`, and MINOR during `0.x`.
Reset lower components when a higher component increases. Breaking changes
include incompatible public API, CLI flags/output/exit codes, declared file
formats or locations, and raised toolchain/platform requirements that exclude
existing consumers. Member checklists own the supported compatibility surface
and exact version validation. No new prerelease convention is introduced here.

During development a CLI may follow core's development branch as its member
policy permits. Before release, it selects a published core version and updates
its manifest and lockfile together. During core `0.x`, use the member's
minor-bounded dependency range; from `1.x`, compatible ranges stop at the next
major. Follow the linked checklists for resolution and migration validation.

## Notes and publication

Every releasing member (core and both CLIs) maintains `CHANGELOG.md` with an
`Unreleased` section. At release preparation, move the shipped changes into a
versioned section and retain `Unreleased` for subsequent work. Notes explain
behavior changes and migration steps. Taps document formula changes, selected
upstream release, archive digest and validation in their PRs; they do not
publish an independent CLI changelog or release version.

All new release tags are signed, annotated and immutable. Use the local signing
configuration, verify the signature and exact commit locally, then verify the
remote annotated tag's peeled commit before publishing. `--verify-tag` alone
proves existence, not the intended commit. The
[maintenance declaration](MAINTENANCE.md#activation-and-required-checks) owns
each protection glob and live activation gate.

Published commits, tags and release assets are never rewritten or replaced.
A tagged mistake requires a new patch or the larger compatibility bump.
Interrupted publication resumes at the same accepted tag and verifies existing
assets instead of overwriting them. Validate from a clean task/detached worktree
at the accepted commit, using fresh build paths, no caches and no cancellation
of running or queued releases. Development CI is not release validation.

The linked member checklists own build, executable smoke, artifact, signature,
consumer and tap installation checks. Release core first; update and validate
each CLI against it; publish both CLI releases before the coordinated tap
updates. Record the source commits, core pin, release identities, archive
digests and installation results in the release handoff. Publishing any
release or tap update requires its normal maintainer authorization.
