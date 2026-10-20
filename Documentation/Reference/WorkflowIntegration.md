# Workflow integration

Members call reusable workflows at a reviewed **full 40-character commit
SHA** with a `# vX.Y.Z` comment. `agents-tools/.github` supplies family policy
and Swift CI; each organization's `.github` supplies presentation with its own
DESIGN and fonts. `skill-cli/.github` adopts family maintenance and versioning
by reference and owns its organization values. Workflows and Dependabot
configuration are not inherited from community defaults.

## Interfaces

| Workflow | Inputs | Job ID / result with the documented caller |
| --- | --- | --- |
| `policy.yml` | None; handles `pull_request`, `push` and `workflow_dispatch` events | `policy` / `policy / policy` |
| `swift-package-ci.yml` | Required string `runner`; optional `package-directory` (default `.`), `format-configuration` (default `.swift-format`) | `swift-package` / `validate / swift-package` |
| `presentation.yml` | Optional string `runner` (default `ubuntu-24.04`); required strings `executable-artifact`, `executable-path`; optional string `assets` (default `.github/assets`) | `presentation` / `presentation / presentation` |

All require only `contents: read`, accept no caller secrets, and expose no outputs.
They use one sequential job each: any failed step fails the required context.
There is no skipped-success aggregate. Explicit permissions exist at workflow
and job scope; checkout credentials are not persisted. All external actions
are pinned to full SHAs with version comments.

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

`Scripts/check-policy.py` owns policy behavior. Run
`python3 Scripts/sync-policy-workflow.py` after changing it and commit both the
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

Keep caller job IDs `policy`, `validate` and `presentation`, and omit a custom
job `name` if using the declared contexts. The workflow display names are not status-check
names. CLI validation also defines a local `smoke` job, and each tap defines a
local `homebrew` job; each must execute its actual repository-owned checks and
fail on failure. Do not create a placeholder passing job to activate rules.

The standards repositories use local `check` jobs and the reusable policy
workflow for their own checks; neither is a Swift package. Each uploads
`Tests/Fixtures/Presentation/demo` in a `presentation-fixture` job, then calls
its own presentation workflow with that artifact and the fixture assets.
Relative self-calls test the candidate implementation; external members use
full pins. Standards' push triggers cover all branches to validate proposed
shared changes before a PR; member callers above cover the default branch and
PRs.

Callers and callees both declare concurrency. Reusable groups have distinct
`shared-policy-` / `shared-swift-ci-` / `shared-presentation-` prefixes because
`github.workflow` is the caller's name inside a reusable workflow. Reusing the caller's group would
cancel the caller itself. Use each reusable workflow at most once per caller;
separate workflow names keep independent validation runs apart. See GitHub's
[reuse contract](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows)
and [concurrency contract](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency).

## Presentation caller

CLI repositories commit their scripted terminal demo under
`.github/assets/terminal/`:

```text
.github/assets/terminal/
├── script.yml
├── fixture/              # optional source files copied into the sandbox
├── recording.json        # generated transcript for review
├── terminal-light.svg
└── terminal-dark.svg
```

The build job uploads the freshly built executable. Its dependent
`presentation` job calls the organization's standard at a reviewed full SHA
with a version comment. This follows the toolchain's
[member caller contract](https://github.com/showxu/skills/blob/ca4eee1bf838cfa81fa6de3912270c74e47c3e76/skills/github-readme-design/references/renderers.md#organization-standard-and-member-caller):

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

Replace the 40 zeros and version comment with the accepted standard commit
and tag. skill-cli members use
`skill-cli/.github/.github/workflows/presentation.yml` and their own built
executable path. `runner` must match the OS that built the executable; its
default is `ubuntu-24.04`. `executable-path` is relative to the uploaded
artifact and cannot be absolute or contain `..`. `assets` defaults to
`.github/assets`; the workflow reads its `terminal/` subdirectory.

With caller job ID `presentation` and no caller `name` override, the exact
required context is **`presentation / presentation`**. It runs on the caller's
event commit, including the test merge commit on PRs. Core and the taps have
no terminal demo and do not require this context.

The workflow validates GitHub's `job.workflow_sha`, then checks out the caller
under `caller/` and its own organization's `.github` under `standard/` at that
exact SHA, without persisted credentials. The SHA identifies the executing
reusable job, including relative self-calls, as documented in GitHub's
[`job` context](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#job-context).
An absent or invalid job SHA fails before checkout, preventing a default-branch
fallback. This interface targets GitHub.com, where that workflow identity is
available.

After downloading `executable-artifact` into the runner's temporary directory,
the workflow validates `executable-path` and restores its execute bit. The
pinned toolchain Action records `script.yml` against this executable in a fresh
sandbox, then renders and compares the recording and both SVGs byte for byte.
DESIGN and fonts come from `standard/DESIGN.md` and `standard/Brand/Fonts` at
`job.workflow_sha`. The Action and its locked parser version come from the
standard's Action pin; members select them through their single standard pin.
Organization DESIGN lint uses that same Action and parser.

Any drift fails the job. The failure artifact `presentation-terminal` holds
`presentation-terminal.tar`, an archive of the commit-ready `script.yml`,
optional `fixture/`, `recording.json` and both SVGs that preserves file modes
and dotfiles, when regeneration succeeds. Extract it with
`tar -xf presentation-terminal.tar -C .github/assets/terminal`, review the
recording and both appearances, and commit the files together. Invalid inputs or failed commands
also fail the job; if regeneration produced no files, artifact upload ignores
the missing directory. Local regeneration uses the same pinned package and
standard inputs as described in the toolchain's
[local instructions](https://github.com/showxu/skills/blob/ca4eee1bf838cfa81fa6de3912270c74e47c3e76/skills/github-readme-design/references/renderers.md#local-regeneration).

## Adopt and update pins

1. Review the shared diff and validate syntax, generated-policy agreement and
   behavioral tests in this repository. Resolve its default branch and full
   revision with `gh api repos/agents-tools/.github/commits/master --jq .sha`.
   A newer default SHA is an update observation, not permission to repin.
2. Prepare a representative consumer PR using the proposed full SHA, including
   a Swift member for Swift changes and a CLI re-recording against its freshly
   built executable on its own build runner for presentation changes. Preserve
   its local smoke/release checks.
   Inspect the real run at that exact candidate; do not claim consumer proof
   from static YAML checks or from a different pin. Before a broader wave,
   inspect current runner capacity and bound concurrent macOS jobs accordingly.
3. Read the check names with
   `gh api repos/OWNER/REPO/commits/HEAD_SHA/check-runs --paginate --jq '.check_runs[] | {name, conclusion, app: .app.id}'`.
   Require `policy / policy` plus the member's validation contexts listed in
   [MAINTENANCE](../../MAINTENANCE.md#activation-and-required-checks). Record the
   actual names, app IDs, run URL, accepted head and shared SHA in the adoption
   PR. Do not apply its ruleset until all required contexts have appeared on
   real runs and passed. Update the declaration if actual names differ.
4. After representative acceptance, advance the remaining callers through
   their own reviewed PRs. Compare every `uses: agents-tools/.github/...@SHA`
   in each member with the accepted pin and report path, observed SHA and
   proposed SHA. Include each organization's presentation workflow in this
   comparison. Resolve unavailable refs as unknown; do not auto-repin or
   fail a consumer solely because the shared default branch advanced.
5. Create signed, annotated standard tags only after this consumer gate and
   the owner's confirmation of each tag, under [VERSIONING](../../VERSIONING.md).
   Keep full SHA pins with their `# vX.Y.Z` comments; tags are never moved.
6. Change related caller pins together. A renamed required job updates the
   maintenance declaration and live ruleset only after its new context is
   verified. Read back settings with `python3 Scripts/check`; it never applies
   them. Dependabot's weekly Actions PRs use this same review and consumer gate.

`python3 Scripts/check --offline` checks local catalog, declaration and
generated files. CI uses `--public` to add public membership without attempting
administrative reads with its read-only token. Maintainers run the default
online check with their existing `gh` read access to both organizations.
