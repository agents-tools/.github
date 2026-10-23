# agents-tools/.github

Organization profile, brand and shared standards for
[agents-tools](https://github.com/agents-tools). Reusable workflows and their
checkers live in [agents-tools/github-workflows](https://github.com/agents-tools/github-workflows),
shared by agents-tools and skill-cli.

GitHub uses `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`,
`SUPPORT.md`, and the issue and pull-request templates here as defaults for
repositories in the organization that lack their own. `GOVERNANCE.md` is
linked from CONTRIBUTING; GitHub does not inherit it. The organization
profile, `AGENTS.md` and `LICENSE` are local to this repository. Members keep
their own CODEOWNERS, workflows and development instructions.

## Contents

| Path | Contents |
| --- | --- |
| Community documents and `.github/ISSUE_TEMPLATE/` | Contribution, conduct, security, support and issue defaults |
| `.github/pull_request_template.md` | Change, validation and documentation prompts |
| `GOVERNANCE.md` | Maintainer responsibilities, scope and decision records |
| `MAINTENANCE.md` | Change flow, signing, settings declarations, required checks and legacy exceptions |
| `VERSIONING.md` | Version policy and family release order |
| `docs/reference/workflow-integration.md` | Organization data and workflow adoption policy |
| `profile/catalog.json` | Membership, profile content, About descriptions and icons |
| `profile/README.md` | Locally generated public profile |
| `profile/assets/` | Organization avatar and profile mark |
| `.github/assets/social-preview/social-preview.png` | Locally generated social preview |
| `DESIGN.md` | Visual tokens and icon entries |
| `.github/design/` | Icon artwork, provenance receipts, fonts and licenses |
| `.github/workflows/` | Policy and organization callers, with the local `check` aggregate |
| `.github/dependabot.yml` | Weekly Actions dependency updates |
| `AGENTS.md`, `LICENSE` | Repository instructions and license |

## Change the standard

Follow [Maintenance](MAINTENANCE.md) for change flow and declarations,
[Versioning](VERSIONING.md) for releases, and
[Workflow integration](docs/reference/workflow-integration.md) for adoption.
Workflow interfaces, checker implementation and their tests belong to
[github-workflows](https://github.com/agents-tools/github-workflows).

CI calls its `organization.yml` with this repository at the commit under test.
Public mode compares catalog membership and About descriptions; the local
`check` aggregate succeeds only when that call succeeds. Source policy uses
an allowlist for supported agent names and the authenticated Dependabot
exception. Before handoff, run `actionlint`, `git diff --check origin/master`,
and the local presentation checks below. For administrative settings, use the
shared organization workflow's online check with authenticated read access and report
drift or unknown observations. See
[read-only verification](MAINTENANCE.md#read-only-verification).

## Change the profile and design

Edit `profile/catalog.json`, then regenerate `profile/README.md` locally.
The catalog lists every public, non-archived, non-fork repository except
`.github`. Each entry declares `kind`, `title`, the verbatim repository
`about`, a plain-text `outcome` and its README header `icon`. The organization
declares its own `.github` repository's `about`. Icons may select light and
dark images. Commit the catalog and generated README together.

`DESIGN.md` owns the visual tokens and icon entries. Read it before changing
assets. Profiles, member dashboards, social previews and terminal SVGs use the
local `github-readme-design` toolchain. The private dashboard combines DESIGN
and catalog from an explicit `.github` commit with its `profile/member.json`.
Regenerate every output affected by a token, catalog or icon change and commit
sources and outputs together.

Use toolchain commit `db02bcb24426f4add0393444f868f1bffdf06f9d` with Node
24.22.0. Prepare the package in ignored `.build/presentation-toolchain` using
its [local regeneration instructions](https://github.com/showxu/skills/blob/db02bcb24426f4add0393444f868f1bffdf06f9d/skills/github-readme-design/references/renderers.md#local-regeneration),
then run:

```sh
toolchain_dir="$PWD/.build/presentation-toolchain"
npm ci --ignore-scripts --omit=dev --prefix "$toolchain_dir"
node "$toolchain_dir/src/cli.ts" design lint --design DESIGN.md
node "$toolchain_dir/src/cli.ts" profile render \
  --design DESIGN.md --catalog profile/catalog.json --out profile/README.md
node "$toolchain_dir/src/cli.ts" profile check \
  --design DESIGN.md --catalog profile/catalog.json --out profile/README.md
node "$toolchain_dir/src/cli.ts" social-preview render \
  --design DESIGN.md --fonts .github/design/fonts --catalog profile/catalog.json \
  --repository .github --icon profile/assets/icon.png \
  --out .github/assets/social-preview/social-preview.png
node "$toolchain_dir/src/cli.ts" social-preview check \
  --design DESIGN.md --fonts .github/design/fonts --catalog profile/catalog.json \
  --repository .github --icon profile/assets/icon.png \
  --assets .github/assets/social-preview
```

DESIGN lint requires zero errors and warnings. Public profile commands omit
member input and catalog revision. Review generated markup and images before
committing. Uploading the social preview in GitHub Settings is a separate
manual step. Reuse the package directory and remove build outputs after use.

## Change the icons

Generate icons from `DESIGN.md` with
[apple-app-icon-design](https://github.com/showxu/skills/tree/master/skills/apple-app-icon-design)
and [apple-framework-icon-design](https://github.com/showxu/skills/tree/master/skills/apple-framework-icon-design).
The agents artwork lives in `.github/design/icons/agents/layers/`; native
Liquid Glass rendering needs macOS, Xcode's Icon Composer and `rsvg-convert`.
Use ignored `.build/icon` and `.build/logos` for the generators' outputs and
review the contact sheet and Icon Composer document before copying assets.

| Generated output | Consumed copy |
| --- | --- |
| `web/avatar-1024.png` | `profile/assets/avatar.png` |
| `web/icon-512.png` | `profile/assets/icon.png` and agents-tools/cli's `.github/assets/logo/logo.png` |
| `core.svg`, `core.png` | agents-tools/core's `.github/assets/logo/logo.svg` and `.github/assets/logo/logo.png` |

For each consumed copy, record its repository, path, generator output and
SHA-256 in `.github/design/icons/*/provenance.json`, together with the skill,
full skill commit, exact command, renderer version and verification date.
Regenerate with the recorded toolchain and compare generated and consumed
digests with the receipt when checking provenance. Commit artwork and updated
copies together, and remove scratch outputs when finished. The organization
avatar on GitHub is uploaded from `profile/assets/avatar.png`.
