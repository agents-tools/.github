# Versioning

## Tags

Versions use SemVer 2.0.0. Release tags are signed and annotated, named
`vX.Y.Z`, with the message `agents-tools/.github X.Y.Z`. A tagged version is never
moved, reused or decreased.

## When to release

Where a delivery workflow governs the project, it decides when to release;
otherwise:

Release once a change is complete: everything it needs, including
documentation, is merged and verified. A change that spans several pull
requests or repositories releases once, when all of it has landed, or at
milestones its owner names before the work starts. Its intermediate steps,
review fixes, documentation fixes and pin updates do not release on their own.

## Choosing the next version

### 0.x (initial development)

Anything may change at any time, without deprecation windows or a release
cadence. Breaking changes (removing or incompatibly changing a documented
interface) bump MINOR; everything else bumps PATCH.

Minor-bounded dependency ranges such as `"0.1.1"..<"0.2.0"` and caret semantics
treat `0.MINOR` as the boundary, so automatic updates never pull a breaking
change.

### 1.0.0

Release `1.0.0` when the owner decides the interface is stable and
compatibility is promised.

### 1.0 and later

Change an interface by adding the new form compatibly, keeping the old form
working and deprecating it. Remove the old form only in a planned major.

Breaking changes appear only in planned majors, on a roughly yearly cadence
like platform releases. A major may also mark a significant feature release.
Never cut a major because of a single change.

New features, including value or output changes consumers absorb without
changing their usage (such as regenerating outputs), bump MINOR. Fixes bump
PATCH.

Reset less significant components to zero when bumping MAJOR or MINOR.
Version numbers never tagged or published to users do not constrain the first
release, which may start at `0.1.0`.

## Version source

The version source is the Git tag.

Files that mirror it:

- None.

Update the source and its mirrors together in the release change.

## Changelog

Keep `CHANGELOG.md` with `## Unreleased` first, followed by `## X.Y.Z`
sections newest first. Describe what each version ships. Every breaking change
includes instructions for upgrading.
From `1.0` onward, record deprecations in the changelog and list a planned
major's removals beforehand.

## Release procedure

1. Choose the next version using the rules above.
2. In the change's final PR, set the version source and its mirrors, move the
   Unreleased entries into the new `## X.Y.Z` section, and leave an empty
   `## Unreleased` section at the top.
3. Run the repository checks and complete the ecosystem release preparation
   below. Resolve review findings before accepting the PR.
4. Squash merge the accepted PR.
5. Create the signed annotated tag with the name and message above on the
   accepted merge commit.
6. Publish the tag and verify that the remote tag's peeled commit equals the
   accepted merge commit.

For each release tag, verify that the version source at its commit matches the
tag's version and that `CHANGELOG.md` at that commit has the matching section.

Run the local DESIGN, profile and social-preview checks in
[README.md](README.md#change-the-profile-and-design), `actionlint`, and
`git diff --check origin/master`. Run organization checks through
`agents-tools/github-workflows` and report drift or unknown observations.

Use the local signing configuration and verify the signature and exact commit
locally. Before publishing release assets, verify the remote annotated tag's
peeled commit; `--verify-tag` alone proves existence, not the intended commit.
The [maintenance declaration](MAINTENANCE.md#activation-and-required-checks)
owns each protection glob and live activation gate.

Ecosystem builds, packages, stores and consumer installation checks belong to
the release owners and checklists in the [members table](#members).

## Family release order

The agents family releases in dependency order: **core → both CLIs → both
Homebrew taps**. Each releasing repository has its own version. A change
releases only the affected dependency chain; versions need not match across
repositories.

Both `.github` standards and `agents-tools/github-workflows` release
independently, starting at `v0.1.0`. They publish signed, annotated SemVer tags
`vX.Y.Z` on the default branch once a
change to a consumed interface or output is complete, as
[When to release](#when-to-release) states. Create each tag only after
the
[consumer real-run gate](docs/reference/workflow-integration.md#adopt-and-update-pins)
passes and the owner confirms that tag. Consumers pin a release's full commit
SHA with a `# vX.Y.Z` comment so Dependabot proposes upgrades; while a change
is in progress, members pin its commits by SHA alone.

## Members

| Repository | Version source | Release tag | Release owner/checklist |
| --- | --- | --- | --- |
| `agents-tools/.github` | Git tag | `vX.Y.Z` | This policy and the [consumer real-run gate](docs/reference/workflow-integration.md#adopt-and-update-pins) |
| `agents-tools/github-workflows` | Git tag | `vX.Y.Z` | [Shared workflows](https://github.com/agents-tools/github-workflows) and the consumer real-run gate |
| `agents-tools/core` | Git tag | `X.Y.Z` | [Core release checklist](https://github.com/agents-tools/core/blob/master/Documentation/Reference/Release.md) |
| `agents-tools/cli` | `BuildInfo.version` in `Sources/CLI/EntryPoint.swift` | `X.Y.Z` | [agents release checklist](https://github.com/agents-tools/cli/blob/master/Documentation/Reference/Release.md) |
| `skill-cli/.github` | Git tag | `vX.Y.Z` | [Standard README](https://github.com/skill-cli/.github/blob/master/README.md) and the [consumer real-run gate](docs/reference/workflow-integration.md#adopt-and-update-pins) |
| `skill-cli/cli` | `BuildInfo.version` in `Sources/CLI/EntryPoint.swift` | `vX.Y.Z` | [skill release checklist](https://github.com/skill-cli/cli/blob/master/Documentation/Reference/Release.md) |
| `agents-tools/homebrew-tap` | Upstream CLI version in each formula | None of its own | [agents tap](https://github.com/agents-tools/homebrew-tap#readme); formula validation in the agents checklist |
| `skill-cli/homebrew-tap` | Upstream CLI version in each formula | None of its own | [skill tap](https://github.com/skill-cli/homebrew-tap#readme); formula validation in the skill checklist |

Do not introduce a duplicate version declaration into core or a tap. Every
releasing member (core, both CLIs, both `.github` standards and
`agents-tools/github-workflows`) maintains `CHANGELOG.md` under the common
changelog policy above.

## Documented interfaces

The family's documented interfaces are:

- Public library API.
- CLI commands, flags, exit codes and documented machine-readable output.
  Human-readable output is not an interface.
- Declared file formats and locations.
- Supported toolchain and platform requirements, including requirements whose
  increase would exclude existing consumers.
- For `agents-tools/github-workflows`, reusable workflow inputs, outputs,
  configuration schemas and caller context names.
- For both `.github` standards, declared organization data formats and the
  DESIGN token names renderers read.

A DESIGN value change that members absorb by regenerating is not breaking.
Member checklists own the supported compatibility surface and exact version
validation. Prerelease conventions remain member-owned.

## Platforms and toolchains

- Members compile and test with the latest stable Xcode available to the
  shared CI, through one entry in the `compilers` list of
  `.github/swift-package.json`. `swift-tools-version` equals that Xcode's Swift
  version.
- Libraries support the three most recent formally released major generations
  of each platform they declare; standalone command-line tools support the two
  most recent. Count actual releases, not version numbers.
- Building against the latest SDK checks API availability for every supported
  system at compile time. CI runs tests on its current macOS host, not on older
  systems.
- As of Xcode 26.6 the values are Swift 6.3, macOS 15 for `agents-tools/core`
  and macOS 26 for both CLIs. Homebrew formulae declare the CLI's macOS floor.
  Raising a floor is a breaking change under
  [Documented interfaces](#documented-interfaces); existing releases keep their
  original requirements.

## Dependency rules

During development a CLI may follow core's development branch as its member
policy permits. Before release, it selects a published core version and updates
its manifest and lockfile together. During core `0.x`, members depend on core
with a minor-bounded range; from core `1.x`, compatible ranges stop at the
next major. Follow the linked checklists for resolution and migration
validation.

## Family publication

Published commits, tags and release assets are never rewritten or replaced.
A tagged mistake requires a new patch or the larger compatibility bump.
Interrupted publication resumes at the same accepted tag and verifies existing
assets instead of overwriting them. Validate from a clean task/detached worktree
at the accepted commit, using fresh build paths, no caches and no cancellation
of running or queued releases. Development CI is not release validation.

The linked member checklists own build, executable smoke, artifact, signature,
consumer and tap installation checks. Release core first; update and validate
each CLI against it; publish both CLI releases before the coordinated tap
updates. Taps document formula changes, selected upstream release, archive
digest and validation in their PRs; they do not publish an independent CLI
changelog or release version.

Record the source commits, core pin, release identities, archive digests and
installation results in the release handoff. Publishing any release or tap
update requires its normal maintainer authorization.
