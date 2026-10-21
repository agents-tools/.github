# Workflow integration

Members call reusable workflows at a reviewed **full 40-character commit SHA**.
A release pin adds its `# vX.Y.Z` comment; while a change to the standard is in
progress, members pin its commits by SHA alone. `agents-tools/.github` supplies family policy and
Swift CI; each organization's `.github` supplies presentation and profile
checks with its own DESIGN, fonts and catalog. `skill-cli/.github` adopts
family maintenance and versioning by reference and owns its organization
values. Workflows and Dependabot configuration are not inherited from community
defaults.

## Interfaces

| Workflow | Inputs | Job ID / result with the documented caller |
| --- | --- | --- |
| `policy.yml` | None; handles `pull_request`, `push` and `workflow_dispatch` events | `policy` / `policy / policy` |
| `swift-package-ci.yml` | Required string `runner`; optional `package-directory` (default `.`), `format-configuration` (default `.swift-format`) | `swift-package` / `validate / swift-package` |
| `presentation.yml` | Strings `runner` (default `ubuntu-24.04`), `executable-artifact` and `executable-path` (default empty; required only for tools), `assets` (default `.github/assets`) | `presentation` / `presentation / presentation` |
| `profile.yml` | Strings `mode` (default `public`, or `member`), `member` (default `profile/member.json`), `output` (default `profile/README.md`) | `profile` / `check / profile` for a member dashboard |

All require only `contents: read`, accept no caller secrets, and expose no outputs.
They use one sequential job each: any failed step fails the required context.
There is no skipped-success aggregate. Explicit permissions exist at workflow
and job scope; checkout credentials are not persisted. All external actions
are pinned to full SHAs; released actions carry their version comments, and an
unreleased toolchain commit is pinned by SHA alone.

Policy validates PR titles on `pull_request` events and commit subjects using the types in
[MAINTENANCE](../../MAINTENANCE.md#change-flow). It checks new commit messages
and added lines for the declared forbidden attribution trailers, and added
lines for whitespace errors and conflict markers. The exact commit-message
line `Signed-off-by: dependabot[bot] <support@github.com>` is allowed only when
a read-only GitHub commit GET for that SHA confirms author `dependabot[bot]`
of type `Bot`, committer `web-flow`, and signature verification `verified: true`
with reason `valid`. Each qualifying commit is authenticated independently;
the PR author or triggering actor does not exempt other commits. The policy
step uses the automatic `github.token` as `GH_TOKEN` for this GET, needs no
additional permissions, and fails closed if authentication is unavailable.
All other attribution trailers remain forbidden, including other signoffs
on a Dependabot commit. PR titles and added lines have no exception; squash
merges still use the PR title and an empty body. Product names remain valid
content. PR diffs use the merge base. Checkout fetches all branch history.
Every topic-branch push validates commits in `origin/<default>..after`,
independently of `before`, including force pushes and new branches. Added lines
are compared with the merge base, or the default tip when histories are unrelated.
Default-branch pushes validate `before..after` and added lines in that diff
when the previous tip is available. This excludes commits reachable from the
previous tip even after a force push. If the previous tip is missing, policy
attempts to fetch it by SHA using the workflow token without persisting credentials.
If it cannot be fetched or `before` is zero, policy validates only `after` and
its added lines against its first parent (the empty tree for a root commit).
Push notices report the selected range and commit count, or the single-commit
fallback. Branch deletion pushes skip checkout and validation with a notice.
General signing enforcement belongs to the branch ruleset and maintainer
verification; the signature check above authenticates only the Dependabot
signoff exception.

Manual dispatch, directly or through a caller, validates the subject and
trailers of the selected ref's head commit from `GITHUB_SHA`, including the
authenticated Dependabot exception. It requires no PR title and does not
rescan ancestors or added lines because dispatch supplies no new-change range.
Both the shared policy workflow and its caller declare `workflow_dispatch`.
GitHub enables manual runs once the workflow exists on the default branch;
the dispatched ref chooses the commit to validate. See the
[dispatch event contract](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_dispatch).

`scripts/check-policy.py` owns policy behavior. Run
`python3 scripts/sync-policy-workflow.py` after changing it and commit both the
script and generated `policy.yml`. The workflow embeds the implementation at
the caller's pin; it does not execute a policy script from the consumer's PR.
Action pins and their version comments live only in the committed workflow.
The generator reads and preserves them, so a Dependabot `uses:` pin update
passes `--check` without regeneration or a matching generator edit. All other
workflow content remains generated and checked against its sources.
The embedded Python runs in isolated mode so consumer modules cannot shadow
its imports. Text additions are checked independently of consumer Git
attributes; binary blobs and submodule gitlinks have no source lines to scan.
Event strings are read as JSON, never interpolated into shell code. PR runs use
`pull_request`, not privileged `pull_request_target`.

Swift CI checks out the caller's event commit (the test merge commit on PRs),
records the installed compiler, runs strict `xcrun swift-format` lint, builds
debug, runs tests, builds release and runs `git diff --check`. The package
directory must contain `Package.swift`, `Sources`, `Tests` and the declared
formatter configuration. The caller chooses a compatible GitHub-hosted macOS
runner/toolchain from its own supported requirements; current family packages
use `macos-26`. The workflow does not assert a minimum-OS test matrix.

Tests unset `CODEX_HOME`, `CLAUDE_CONFIG_DIR`, `XDG_CONFIG_HOME`,
`XDG_STATE_HOME` and `XDG_CACHE_HOME`, preserving `HOME`, `TMPDIR` and `PATH`.
Builds use no caches. CLI executable smoke tests and Homebrew checks remain
member-owned jobs; retain them when adopting shared package validation.

These are development/PR workflows. They cancel superseded runs and must not
be called from release validation or publication. Release owners implement
fresh, cache-free validation without cancelling running or queued releases.

## Policy caller

Use `.github/workflows/source-policy.yml`. Replace the 40 zeros below with the
accepted shared commit; zeros are a placeholder, not a runnable pin. Replace
the default branch with the member's declared value if it differs.

```yaml
name: Source policy
on:
  push:
    branches: [master]
  pull_request:
    types: [opened, synchronize, reopened, edited]
  workflow_dispatch:
permissions:
  contents: read
concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true
jobs:
  policy:
    uses: agents-tools/.github/.github/workflows/policy.yml@0000000000000000000000000000000000000000 # vX.Y.Z
```

## Swift caller

Use a separate validation workflow such as `.github/workflows/ci.yml` and the
same reviewed shared pin. Validation excludes title-only edits; a conditional
skip on `edited` could replace a failing result on the same commit.

```yaml
name: CI
on:
  push:
    branches: [master]
  pull_request:
    types: [opened, synchronize, reopened]
  workflow_dispatch:
permissions:
  contents: read
concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true
jobs:
  validate:
    uses: agents-tools/.github/.github/workflows/swift-package-ci.yml@0000000000000000000000000000000000000000 # vX.Y.Z
    with:
      runner: macos-26
      package-directory: .
      format-configuration: .swift-format
```

Keep caller job IDs `policy`, `validate`, `presentation` and member-profile
`check`, and omit a custom job `name` if using the declared contexts. The
workflow display names are not status-check names. CLI validation also defines
a local `smoke` job, and each tap defines a local `homebrew` job; each must
execute its actual repository-owned checks and fail on failure. Do not create a
placeholder passing job to activate rules.

The standards repositories use local `check` jobs and the reusable policy
workflow for their own checks; neither is a Swift package. Each calls its own
presentation and profile workflows with default inputs to check its
organization preview and public profile. Relative self-calls test the candidate
implementation; external members use full pins. Standards' required contexts
remain `policy / policy` and `check`. Standards' push triggers cover all
branches to validate proposed shared changes before a PR; member callers above
cover the default branch and PRs.

Callers and callees both declare concurrency. Reusable groups have distinct
`shared-policy-`, `shared-swift-ci-`, `shared-presentation-` and
`shared-profile-` prefixes because `github.workflow` is the caller's name
inside a reusable workflow. Reusing the caller's group would cancel the caller
itself. Use each reusable workflow at most once per caller; separate workflow
names keep independent validation runs apart. See GitHub's [reuse
contract](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows)
and [concurrency
contract](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency).

## Presentation callers

The standard's catalog selects the expected assets for each caller:

| Catalog kind | Checked asset directories | Executable inputs |
| --- | --- | --- |
| `tool` | `logo`, `terminal`, `social-preview` | Both required |
| `library`, `app` | `logo`, `social-preview` | Both rejected |
| `distribution` | `social-preview` | Both rejected |
| Organization `.github` (implicit kind `organization`) | `social-preview` | Both rejected |
| `website` | None; calling the workflow fails with `kind website has no presentation assets` | Not applicable |

The caller owner must exactly match `organization.login`; any repository other
than `.github` must be in the catalog. Missing expected directories and a
terminal directory for a kind without terminal fail. Tools, libraries and apps
require a `logo/` directory under the asset root. Distributions, websites and
the organization use standard icons and reject a `logo/` directory. Repository
entries require `kind`, `title` and `about` after `icon`; `about` equals the live
repository description. The organization declares its `.github` repository
About in `organization.about`.

A tool commits these assets under its asset root:

```text
.github/assets/
├── logo/
│   └── logo.png              # or logo-light.png and logo-dark.png
├── terminal/
│   ├── script.yml
│   ├── fixture/              # optional source files copied into the sandbox
│   ├── recording.json        # generated transcript for review
│   ├── terminal-light.svg
│   └── terminal-dark.svg
└── social-preview/
    └── social-preview.png
```

The build job uploads the freshly built executable. Its dependent
`presentation` job calls the organization's standard at a reviewed full SHA,
with the version comment of a release. This follows the toolchain's [member caller
contract](https://github.com/showxu/skills/blob/9e5d7268232b78f5fbef21ccfb9e3a079f2ef7e3/skills/github-readme-design/references/renderers.md#organization-standard-and-member-caller):

```yaml
jobs:
  build:
    runs-on: macos-26
    steps:
      # Check out and build the product here.
      - uses: actions/upload-artifact@cf430e030ddbb5b0abf93d22962f4752f3646cd9 # v7.0.2
        with:
          name: executable
          path: .build/release/agents
  presentation:
    needs: build
    uses: agents-tools/.github/.github/workflows/presentation.yml@0000000000000000000000000000000000000000 # vX.Y.Z
    with:
      runner: macos-26
      executable-artifact: executable
      executable-path: agents
```

Replace the 40 zeros with the accepted standard commit, and the version
comment with its release version or nothing for an unreleased commit. skill-cli members use
`skill-cli/.github/.github/workflows/presentation.yml` and their own built
executable path. `runner` must match the OS that built the executable; its
default is `ubuntu-24.04`. `executable-path` is relative to the uploaded
artifact and cannot be absolute or contain `..`. `assets` defaults to
`.github/assets` and must be caller-relative without `..` segments.

A library such as core calls without executable inputs; apps and distributions
use the same form:

```yaml
jobs:
  presentation:
    uses: agents-tools/.github/.github/workflows/presentation.yml@0000000000000000000000000000000000000000 # vX.Y.Z
```

With caller job ID `presentation` and no caller `name` override, the context
is **`presentation / presentation`**. Core and the taps have no terminal demo;
this workflow checks their logos (libraries) and social previews. Their existing required-context
declarations remain unchanged until member adoption passes its real-run gate.

The workflow validates GitHub's `job.workflow_sha`, then checks out the caller
under `caller/` and its own organization's `.github` under `standard/` at that
exact SHA, without persisted credentials. The SHA identifies the executing
reusable job, including relative self-calls, as documented in GitHub's [`job`
context](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#job-context).
An absent or invalid SHA fails before checkout. The caller checkout uses the
event commit, including the test merge commit on PRs. This interface targets
GitHub.com, where that workflow identity is available.

`scripts/presentation-inputs.py` runs from the pinned standard and resolves
kind, catalog selector and local icons. Catalog icons (or the organization's
`mark` for `.github`) must use
`https://raw.githubusercontent.com/<organization>/<repository>/HEAD/<path>`:
`.github` resolves in `standard/`, and a member's own repository resolves in
`caller/`. Other hosts, owners, repositories and refs, queries, fragments,
absolute paths, `..` segments and missing files fail with the URL named.
Every icon file resolved in the caller, including both light and dark
variants, must match a `copies` entry for that repository and path in the
standard's `.github/design/icons/*/provenance.json`, with identical SHA-256.
A missing or mismatched receipt fails naming the file. The light-page icon is
the rendering input. Repository tests verify every standard `profile/assets/`
file against its receipt, including avatars that are not rendering inputs.

For a tool, the workflow downloads `executable-artifact`, validates the path
and restores its execute bit. The pinned toolchain records the terminal
script against that executable in a fresh sandbox, then compares the recording
and both SVGs byte for byte. For every accepted kind it renders and compares
the social preview PNG. DESIGN, fonts and catalog come from
`standard/DESIGN.md`, `standard/.github/design/fonts` and `standard/profile/catalog.json`
at `job.workflow_sha`. The standard's Action pin selects the toolchain and its
locked parser; members select all these inputs through their standard pin.
Organization DESIGN lint uses that same Action and parser.

Any drift fails the job. Failure artifact `presentation` holds
`presentation.tar`, with regenerated `terminal/` and/or `social-preview/`
subdirectories laid out like the asset root. The tar preserves file modes and
hidden files. Extract it with `tar -xf presentation.tar -C .github/assets`,
review and commit the files together. Invalid inputs or failed commands also
fail; when no files were generated, archival and upload skip the absent output.
Local regeneration uses the same pinned package and standard inputs as
described in the toolchain's [local
instructions](https://github.com/showxu/skills/blob/9e5d7268232b78f5fbef21ccfb9e3a079f2ef7e3/skills/github-readme-design/references/renderers.md#local-regeneration).
Uploading the social preview in GitHub Settings remains manual.

## Profile callers

The profile workflow uses the same caller and pinned-standard checkout
contract. It validates `mode` (`public` or `member`) and the full
`job.workflow_sha` before any checkout. `member` and `output` are relative
paths in the caller, without `..` segments; they cannot escape that checkout.
The default `output` is `profile/README.md`.

Public mode uses only the standard's DESIGN and catalog. The organization's
own CI calls the workflow locally with no inputs. A `.github-private` member
dashboard calls from a job named `check`:

```yaml
jobs:
  check:
    uses: agents-tools/.github/.github/workflows/profile.yml@0000000000000000000000000000000000000000 # vX.Y.Z
    with:
      mode: member
```

skill-cli dashboards use `skill-cli/.github/.github/workflows/profile.yml`.
Replace the zeros with the accepted standard commit, and the version comment
with its release version or nothing for an unreleased commit. Member mode reads `profile/member.json` by default and supplies
`job.workflow_sha` as `catalog-revision`; public mode supplies neither member
input nor catalog revision to the Action. Member JSON keeps `maintenance` and
`repositories`; remove its `catalog` binding. The single workflow pin selects
DESIGN, catalog and toolchain together.

The Action validates the catalog and compares generated Markdown bytes with
the caller's output. On drift, artifact `profile` contains the regenerated
Markdown file; copy it to the declared output path, review and commit it. An
absent artifact directory is skipped. The member context is **`check / profile`**.
Update the member's maintenance declaration and live ruleset for that context
only after it has appeared and passed on a real run under the activation gate.

## Adopt and update pins

1. Review the shared diff and validate syntax, generated-policy agreement and
   behavioral tests in this repository. Resolve its default branch and full
   revision with `gh api repos/agents-tools/.github/commits/master --jq .sha`.
   A newer default SHA is an update observation, not permission to repin.
2. Prepare a representative consumer PR using the proposed full SHA, including
   a Swift member for Swift changes and a CLI re-recording against its freshly
   built executable on its own build runner for presentation changes affecting
   tools. The organization preview self-call cannot prove the tool path. Cover
   the social-preview and profile paths with their real callers at the same
   candidate commit, including a member dashboard for member-mode changes.
   Preserve local smoke/release checks.
   Inspect the real run at that exact candidate; do not claim consumer proof
   from static YAML checks or from a different pin. Before a broader wave,
   inspect current runner capacity and bound concurrent macOS jobs accordingly.
3. Read the check names with `gh api
   repos/OWNER/REPO/commits/HEAD_SHA/check-runs --paginate --jq '.check_runs[]
   | {name, conclusion, app: .app.id}'`. Require `policy / policy` plus the
   member's validation contexts listed in
   [MAINTENANCE](../../MAINTENANCE.md#activation-and-required-checks). Record
   the actual names, app IDs, run URL, accepted head and shared SHA in the
   adoption PR. Do not apply its ruleset until all required contexts have
   appeared on real runs and passed. Update the declaration if actual names
   differ.
4. After representative acceptance, advance the remaining callers through their
   own reviewed PRs. Compare every `uses: agents-tools/.github/...@SHA` in each
   member with the accepted pin and report path, observed SHA and proposed SHA.
   Include each organization's presentation workflow in this comparison, along
   with profile workflow callers. Resolve unavailable refs as unknown; do not
   auto-repin or fail a consumer solely because the shared default branch
   advanced.
5. When the change is complete, create signed, annotated standard tags only
   after this consumer gate and the owner's confirmation of each tag, under
   [VERSIONING](../../VERSIONING.md), then move callers to the release pins
   with their `# vX.Y.Z` comments in one pass. Tags are never moved.
6. Change related caller pins together. A renamed required job updates the
   maintenance declaration and live ruleset only after its new context is
   verified. Read back settings with `python3 scripts/check`; it never applies
   them. Dependabot's weekly Actions PRs use this same review and consumer gate.

`python3 scripts/check --offline` reads catalog membership fields and checks
the declaration and generated policy. The profile workflow owns catalog
validation and generated-profile comparison. CI uses `--public` to compare
public membership and repository About descriptions without attempting
administrative reads with its read-only token. Maintainers run the default
online check with their existing `gh` read access to both organizations.
