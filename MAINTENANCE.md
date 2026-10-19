# Maintenance

`agents-tools/.github` owns the shared engineering standard and reusable
workflows for the agents family. The declaration below covers the public
repositories in `agents-tools` and the related `skill-cli` organization.
`skill-cli/.github` adopts this standard by reference in its own reviewed
change, retaining its own identity, metadata and repository instructions.
Member adoption and live settings changes are separate from declaring this
standard. [VERSIONING.md](VERSIONING.md) owns releases; [DESIGN.md](DESIGN.md)
owns the agents-tools identity.

## Change flow

1. Work in a task-owned worktree on a topic branch based on the current remote
   default branch. Preserve published history and other contributors' work.
2. Keep one logical change per commit and pull request. Use Conventional
   Commit titles and subjects: `type(scope)!: subject`, with optional scope
   and `!`. Allowed types are `build`, `chore`, `ci`, `docs`, `feat`, `fix`,
   `perf`, `refactor`, `revert`, `style` and `test`.
3. Sign all new commits. Run the member's checks from its README and include
   results in the PR. Added lines must have no trailing whitespace, conflict
   markers or attribution trailers. Commit messages forbid `Co-authored-by`,
   `Signed-off-by`, `Generated-by`, `Generated-with`, `Made-with`,
   `Assisted-by` and `Powered-by` trailers. The sole exception is the exact
   line `Signed-off-by: dependabot[bot] <support@github.com>` on a commit
   authenticated through GitHub as authored by `dependabot[bot]` (Bot), with
   a valid verified signature and the `web-flow` committer. This exception
   applies only to that commit's message; PR titles, added lines and squash
   messages retain their restrictions. Unavailable authentication fails the
   check. Preserve authorship in Git's author fields and existing
   legal/provenance records.
4. Review the actual final head. Fix or answer every review finding on the PR
   and resolve every thread. Zero required approvals does not waive review.
5. Squash-merge only the reviewed head after all required contexts succeed.
   Use the PR title as the subject and explicitly pass an empty body, for
   example `gh pr merge <number> --squash --match-head-commit <sha> --subject '<PR title>' --body ''`.
   Verify the accepted commit and its signature. Delete merged branches.

External and bot-authored contributions are welcome. Their identities remain
their own; GitHub's verified squash signatures are valid accepted signatures.
Policy checks new commit subjects and content, not historical ancestors.

## Signing

Use the repository's existing local SSH signing configuration and registered
public signing key. Enable `commit.gpgsign` and `tag.gpgsign`, with
`gpg.format=ssh` and the local `user.signingkey`; do not publish a private key
or impose a workstation-specific path on contributors. Configure only the
task repository/worktree when configuration is needed. Verify local work with
`git verify-commit HEAD` and release tags with `git verify-tag <tag>`, using
the configured public allowed-signers file. GitHub must recognize the signing
key for new accepted commits.

## GitHub settings

The JSON declaration below is the settings checker's only source of expected
values. Common settings are expanded with each repository's branch, check
names, tag patterns, description and complete topic set. Repository-specific
metadata is intentional; the two organizations retain their own values.
Description changes should agree with the member's visitor-facing README
and any social card; catalog summaries may give additional context.

- Squash merge only; PR title as subject, blank body, delete merged branches.
- Read-only workflow token; workflows cannot approve PRs. Every workflow also
  declares its own permissions. No administrator credential is passed to CI.
- Private vulnerability reporting enabled in every public member.
- An active `Default branch` ruleset on `~DEFAULT_BRANCH`, no bypass actors,
  requiring PRs, zero approvals, resolved threads, signed commits, no force
  push or deletion, and the declared GitHub Actions contexts.
- For repositories that release: an active `Release tags` ruleset, no bypass
  actors, preventing update and deletion of the declared tag patterns.
  `refs/tags/[0-9]*.[0-9]*.[0-9]*` covers unprefixed `X.Y.Z` tags. It is a
  GitHub fnmatch protection glob, not a SemVer validator; the member's release
  checklist validates the exact version. `skill-cli/cli` uses `refs/tags/v*`.
  Taps and standards repositories have no release tags of their own.

### Activation and required checks

These are **adoption targets**, not a claim that protection is live. First
install the caller workflows, run them on a real candidate at the proposed
full SHA, and inspect `check-runs` for the exact names and GitHub Actions App
ID (`15368`). Only then apply the ruleset. Keep any existing protection until
its replacement is verified, and inspect overlapping legacy branch protection
before migration. Repository rulesets are used; organization-plan support is
not assumed. Never add a nonexistent context to a live ruleset.

| Repository | Required contexts after adoption | Release tag format / protection glob |
| --- | --- | --- |
| `agents-tools/.github` | `policy / policy`, `check` | None |
| `agents-tools/core` | `policy / policy`, `validate / swift-package` | `X.Y.Z` / `[0-9]*.[0-9]*.[0-9]*` |
| `agents-tools/cli` | `policy / policy`, `validate / swift-package`, `smoke`, `presentation / presentation` | `X.Y.Z` / `[0-9]*.[0-9]*.[0-9]*` |
| `agents-tools/homebrew-tap` | `policy / policy`, `homebrew` | None |
| `skill-cli/.github` | `policy / policy`, `check` | None |
| `skill-cli/cli` | `policy / policy`, `validate / swift-package`, `smoke`, `presentation / presentation` | `vX.Y.Z` / `v*` |
| `skill-cli/homebrew-tap` | `policy / policy`, `homebrew` | None |

The 2026-10-19 audits observed `Swift Package` and
`validate-commit-messages` in core, `Swift CLI` and
`validate-commit-messages` in both CLIs, and no check contexts in either tap.
The table defines their replacement interfaces. The CLIs retain executable
smoke validation in a member-owned `smoke` job; taps supply a member-owned
`homebrew` job for formula validation, installation and tests. Their commands
belong in the members. `.github` uses `check` for its Python validation.
Both CLIs also require `presentation / presentation` to verify their committed
Quick look SVGs against their recording and recipe using the pinned shared
renderer. Core and the taps have no recording. This repository exercises the
presentation workflow against a small test fixture in CI; that self-test does
not replace the member adoption run.
The [integration guide](Documentation/Reference/WorkflowIntegration.md)
defines caller names and the rollout gate. Shared Swift automation still
needs a representative member run before rollout.

Any setting, metadata, ruleset or required-context change updates this
declaration and its explanatory table in the **same PR** as the associated
workflow or governance change. After review and a real run, the authorized
maintainer applies the declared live change and records the readback in that
PR. `Scripts/check` reports differences without applying them. A pending
adoption remains reported drift, never an implicit exemption.

### Declaration

<!-- settings-declaration -->
```json
{
  "schema": 1,
  "defaults": {
    "repository": {
      "allow_squash_merge": true,
      "allow_merge_commit": false,
      "allow_rebase_merge": false,
      "delete_branch_on_merge": true,
      "squash_merge_commit_title": "PR_TITLE",
      "squash_merge_commit_message": "BLANK"
    },
    "workflow_token": {
      "default_workflow_permissions": "read",
      "can_approve_pull_request_reviews": false
    },
    "private_vulnerability_reporting": {
      "enabled": true
    },
    "branch_ruleset": {
      "name": "Default branch",
      "target": "branch",
      "enforcement": "active",
      "bypass_actors": [],
      "conditions": {
        "ref_name": {
          "include": [
            "~DEFAULT_BRANCH"
          ],
          "exclude": []
        }
      },
      "rules": [
        {
          "type": "deletion"
        },
        {
          "type": "non_fast_forward"
        },
        {
          "type": "required_signatures"
        },
        {
          "type": "pull_request",
          "parameters": {
            "allowed_merge_methods": [
              "squash"
            ],
            "required_approving_review_count": 0,
            "dismiss_stale_reviews_on_push": false,
            "require_code_owner_review": false,
            "require_last_push_approval": false,
            "required_review_thread_resolution": true
          }
        }
      ]
    },
    "status_checks": {
      "integration_id": 15368,
      "strict_required_status_checks_policy": false,
      "do_not_enforce_on_create": false
    },
    "tag_ruleset": {
      "name": "Release tags",
      "target": "tag",
      "enforcement": "active",
      "bypass_actors": [],
      "rules": [
        {
          "type": "update"
        },
        {
          "type": "deletion"
        }
      ]
    }
  },
  "repositories": {
    "agents-tools/.github": {
      "default_branch": "master",
      "description": "Organization profile, brand and shared standards for agents-tools",
      "topics": [],
      "required_checks": [
        "policy / policy",
        "check"
      ],
      "release_tag_patterns": []
    },
    "agents-tools/core": {
      "default_branch": "master",
      "description": "Swift libraries behind agents and skill: sources, locks, skills, instructions and watch.",
      "topics": [
        "agent-skills",
        "agents-md",
        "ai-agents",
        "swift",
        "swift-package"
      ],
      "required_checks": [
        "policy / policy",
        "validate / swift-package"
      ],
      "release_tag_patterns": [
        "refs/tags/[0-9]*.[0-9]*.[0-9]*"
      ]
    },
    "agents-tools/cli": {
      "default_branch": "master",
      "description": "A package manager for agent skills and instructions.",
      "topics": [
        "agent-skills",
        "agents-md",
        "ai-agents",
        "claude-code",
        "cli",
        "codex",
        "cursor",
        "gemini-cli",
        "opencode",
        "swift"
      ],
      "required_checks": [
        "policy / policy",
        "validate / swift-package",
        "smoke",
        "presentation / presentation"
      ],
      "release_tag_patterns": [
        "refs/tags/[0-9]*.[0-9]*.[0-9]*"
      ]
    },
    "agents-tools/homebrew-tap": {
      "default_branch": "master",
      "description": "Homebrew tap for agents",
      "topics": [
        "homebrew",
        "homebrew-tap"
      ],
      "required_checks": [
        "policy / policy",
        "homebrew"
      ],
      "release_tag_patterns": []
    },
    "skill-cli/.github": {
      "default_branch": "master",
      "description": "Organization profile, brand and shared standards for skill-cli",
      "topics": [],
      "required_checks": [
        "policy / policy",
        "check"
      ],
      "release_tag_patterns": []
    },
    "skill-cli/cli": {
      "default_branch": "master",
      "description": "A package manager for agent skills.",
      "topics": [
        "agent-skills",
        "ai-agents",
        "claude-code",
        "cli",
        "codex",
        "cursor",
        "gemini-cli",
        "opencode",
        "swift"
      ],
      "required_checks": [
        "policy / policy",
        "validate / swift-package",
        "smoke",
        "presentation / presentation"
      ],
      "release_tag_patterns": [
        "refs/tags/v*"
      ]
    },
    "skill-cli/homebrew-tap": {
      "default_branch": "master",
      "description": "Homebrew tap for skill-cli",
      "topics": [
        "homebrew",
        "homebrew-tap"
      ],
      "required_checks": [
        "policy / policy",
        "homebrew"
      ],
      "release_tag_patterns": []
    }
  }
}
```

## Advisory review

**Deferred: Codex code review.** The owner must connect both organizations,
select the intended repositories and enable review. Existing review receipts
in `skill-cli/cli` do not establish family-wide activation. After connection,
open a real applicable code PR in each organization's selected scope, verify
that review runs automatically on the final head, and record the PR URL,
reviewed SHA and provider settings in the adoption PR. Resolve the findings
and update this declaration of review status only after that verification.
Advisory review is not a required status context and does not replace human
review or resolved-thread enforcement. No new credentials or Apps are
provisioned by these workflows.

## Dependencies, licenses and shared automation

Each member with `Package.swift` configures Dependabot `swift` updates weekly.
Each member with Actions workflows configures `github-actions` updates weekly.
Dependabot files are repository-local and are not inherited. Updates follow
the same signed/reviewed change flow and preserve the release dependency
contract. Pin every external action and reusable workflow to a full commit
SHA, with a version comment for actions. The committed
`.github/workflows/policy.yml` owns its action pins and version comments;
`Scripts/sync-policy-workflow.py` reads and preserves them during regeneration.
Its version comments contain only dot-separated ASCII decimal numbers with an
optional `v` prefix, such as `# v1.2.3` or `# 1.2.3`.
Dependabot pin-only updates pass the generated-workflow check without edits
to the generator. Policy behavior remains owned by `Scripts/check-policy.py`;
changes to it require regeneration, and hand edits to the embedded policy or
generated workflow structure fail the check.
Consumers advance shared workflow pins through reviewed PRs after a
representative run; a pin lag observation alone is not a failed required
check. See the integration guide for pin comparison and updates.

Core, both CLIs and both taps are MIT-licensed. Each ships its own LICENSE;
GitHub does not inherit licenses. Preserve existing copyright and third-party
notices. Formula license metadata describes the packaged tool, not the tap's
own license. Community fallback and local build instructions retain the
ownership described in [README.md](README.md).

Development CI uses the uncached baseline. A cache proposal must first record
a cost/latency threshold and repeated comparable cold, warm and disabled
measurements, including restore/save costs. Release builds use fresh paths,
no caches and no automatic cancellation of running or queued publication.

## Legacy exceptions

The 2026-10-19 read-only member audits identified the following published
unsigned commits. They are accepted legacy signature exceptions in each named
repository. They stay published exactly as they are; all new work is signed.
Identical SHAs in core and skill-cli are separate repository coverage entries,
reflecting their shared history.

| Repository | SHA | Subject |
| --- | --- | --- |
| `agents-tools/core` | `87917b99b857b1fc7a16ca3b02c74356709aeba9` | chore: prepare 0.2.1 release |
| `agents-tools/core` | `0f6c05b5416d48bcbfb4ce0d069be55f77459eb9` | fix: diagnose shared installations for selected agents |
| `agents-tools/core` | `5679b75681c9346f6f8243eb0626eee295bd8e37` | chore: merge origin/master before validating install diagnostics |
| `agents-tools/core` | `9dd6a1ce6b4b6dc6f1da1f0f4aadfaa64de81d12` | fix: stop doctor false positives and allow removing records with missing files |
| `agents-tools/core` | `4722385279154b57653f2e7cccd143f182e848bd` | chore: prepare 0.2.0 release |
| `agents-tools/core` | `6588d9b983f349d2cc035969dc48632c91e40bc4` | feat: add editable local skill installs and doctor diagnostics |
| `agents-tools/core` | `ffd8897ba8978f0e27362fbe677912b6c93ac01c` | chore: initial commit |
| `skill-cli/cli` | `87917b99b857b1fc7a16ca3b02c74356709aeba9` | chore: prepare 0.2.1 release |
| `skill-cli/cli` | `0f6c05b5416d48bcbfb4ce0d069be55f77459eb9` | fix: diagnose shared installations for selected agents |
| `skill-cli/cli` | `5679b75681c9346f6f8243eb0626eee295bd8e37` | chore: merge origin/master before validating install diagnostics |
| `skill-cli/cli` | `9dd6a1ce6b4b6dc6f1da1f0f4aadfaa64de81d12` | fix: stop doctor false positives and allow removing records with missing files |
| `skill-cli/cli` | `4722385279154b57653f2e7cccd143f182e848bd` | chore: prepare 0.2.0 release |
| `skill-cli/cli` | `6588d9b983f349d2cc035969dc48632c91e40bc4` | feat: add editable local skill installs and doctor diagnostics |
| `skill-cli/cli` | `ffd8897ba8978f0e27362fbe677912b6c93ac01c` | chore: initial commit |
| `skill-cli/homebrew-tap` | `16aaf2d3e978a76a16599af003e7e2fde1e38299` | chore: update skill-cli formula to 0.2.1 |
| `skill-cli/homebrew-tap` | `47854d4b80779a55a6bfc3b2dbd25689dead7d75` | chore: update skill-cli formula to 0.2.0 |
| `skill-cli/homebrew-tap` | `8a00824ec671adea64087bfa9132289a7f6b1449` | chore: initial commit |

Two GitHub-signed bootstrap subjects are also retained as published subject
exceptions: `agents-tools/cli` at
`3053d187d044444fcb12527060ae3f7d3783c9d2` and
`agents-tools/homebrew-tap` at
`f0ee0f598004cd9f7d42f51f971769b17ee47c71`, both `Initial commit`.
These are not unsigned-commit exceptions.

## Read-only verification

Run `python3 Scripts/check` using an authenticated `gh` session with read
access to repository settings across both organizations. It compares merge
settings, token defaults, full repository/inherited rulesets, private reporting,
descriptions and topics for every declared member. All GitHub calls are GETs;
it never applies a setting. `DRIFT` includes expected and observed values;
`UNKNOWN` denotes an inaccessible endpoint or missing field. Exit 0 means
observed conformance, 1 means drift/local validation failure, and 2 means an
unknown observation (with any drift still printed).

`--offline` validates local sources without network access. `--public` adds
public catalog membership but skips administrative settings; this is the
read-only workflow-token CI mode. Neither mode claims live settings conformity.
The settings check does not prove App activation, commit signatures throughout
history, effective issue-template rendering or consumer installation; those
remain explicit adoption/release verification steps.

GitHub owns the [ruleset API](https://docs.github.com/en/rest/repos/rules) and
[ref-pattern syntax](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository).
