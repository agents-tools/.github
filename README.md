# agents-tools/.github

Organization profile and shared engineering and community standards for
[agents-tools](https://github.com/agents-tools). This repository owns the
reusable workflows for the agents family; `skill-cli` adopts the standard by
reference with its own organization values.

GitHub uses `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`,
`SUPPORT.md`, and the issue and pull-request templates here as defaults for
repositories in the organization that lack their own.

`GOVERNANCE.md` is hosted here and linked from `CONTRIBUTING.md`; GitHub
does not inherit it. The organization profile, its tooling, `AGENTS.md`, and
`LICENSE` are local to this repository. Repositories keep their own
CODEOWNERS, workflows, and repository-specific development instructions.

## Contents

| Path | Contents |
| --- | --- |
| `CODE_OF_CONDUCT.md` | Community behavior and enforcement |
| `CONTRIBUTING.md` | Contribution and pull-request conventions |
| `SECURITY.md` | Private vulnerability reporting and security scope |
| `SUPPORT.md` | Where to ask for help and what to include |
| `GOVERNANCE.md` | Maintainer responsibilities, scope, and decision records |
| `MAINTENANCE.md` | Change flow, signing, declared settings, review and legacy exceptions |
| `VERSIONING.md` | Version sources, immutable tags, changelogs and release order |
| `Documentation/Reference/WorkflowIntegration.md` | Reusable workflow interfaces, caller pins and required contexts |
| `.github/ISSUE_TEMPLATE/` | Bug and feature templates, plus security reporting guidance |
| `.github/pull_request_template.md` | Change summary, validation, and documentation prompts |
| `profile/catalog.json` | Promise, account description, navigation, repository groups, outcomes and icons for the profile |
| `profile/README.md` | Organization profile generated from the catalog |
| `profile/assets/` | Organization avatar and profile mark |
| `DESIGN.md` | Brand colors, the agents app icon entry and framework logo entries |
| `Brand/Icon/` | App icon layer artwork |
| `Brand/Exports/agents/` | Icon Composer document generated from the app icon entry |
| [`Brand/Social/`](Brand/Social/README.md) | Repository social cards, recipes, layout receipts and regeneration commands |
| `Brand/Profile/recipe.json` | Profile tokens resolved from DESIGN.md |
| `Scripts/` | Profile/policy generators, [vendored renderers](Scripts/vendor/README.md) and read-only repository/settings checks |
| `Tests/` | Profile, policy, settings and presentation tests and fixtures |
| `.github/workflows/` | Shared policy, Swift CI and presentation checks, plus this repository's callers |
| `.github/dependabot.yml` | Weekly Actions dependency updates |
| `AGENTS.md` | Repository-specific agent guide |
| `LICENSE` | Repository license |

## Change the Profile

Edit `profile/catalog.json`, then regenerate the profile and run the checks:

```sh
python3 Scripts/render-profile.py
python3 -m unittest discover -s Tests
python3 Scripts/check
```

Commit the catalog and generated README together. The catalog must list
every public, non-archived repository in the organization except `.github`.
The check validates the catalog, detects generated-profile drift, and
compares membership with GitHub.

`Scripts/render-profile.py` runs the vendored shared renderer from
`github-readme-design`, which owns the catalog contract and layout: each
repository row has a plain-text `outcome` and the `icon` shown in its README
header, and optional fields cover the website, a quick start, the account
`description` and the maintainer line. The member dashboard in the private
`.github-private` repository renders from this catalog at a pinned revision.

Python 3 and its standard library are sufficient for local checks. The public
membership check uses the GitHub API with optional `GITHUB_TOKEN` read access.
The full online check also needs an authenticated `gh` session that can read
the declared repositories' settings in both organizations:

```sh
python3 Scripts/check
```

For local work without GitHub access, `python3 Scripts/check --offline`
validates local files and skips all network reads. CI runs
`python3 Scripts/check --public` with its read-only token: local checks and
public membership, without administrative settings. Run the default check
before handoff and report settings drift and unavailable observations; it
never mutates GitHub. See [Maintenance](MAINTENANCE.md#read-only-verification).

## Change the Standard

Follow [Maintenance](MAINTENANCE.md) for change flow and declarations,
[Versioning](VERSIONING.md) for release policy, and
[Workflow integration](Documentation/Reference/WorkflowIntegration.md) for
shared workflow interfaces and adoption. After editing `Scripts/check-policy.py`
or its workflow generator, run `python3 Scripts/sync-policy-workflow.py` and
commit the generated workflow too.

Before handoff, run the offline and online checks, unit tests, `actionlint`
(or parse every workflow as YAML when unavailable), and `git diff --check
origin/master`. Member settings activation and workflow pin rollouts require
the real consumer evidence described in the integration guide.

## Change the Icons

Icons are generated from `DESIGN.md` with the
[apple-app-icon-design](https://github.com/showxu/skills/tree/master/skills/apple-app-icon-design)
and
[apple-framework-icon-design](https://github.com/showxu/skills/tree/master/skills/apple-framework-icon-design)
skills. Native Liquid Glass rendering needs macOS with Xcode's Icon Composer
and `rsvg-convert`.

For the agents app icon, edit its entry or the artwork in `Brand/Icon/`, then
run from this repository, with `APP_ICONS` set to that skill's `scripts/app_icons.py`:

```sh
python3 "$APP_ICONS" DESIGN.md --name agents --lint
rm -rf .build/icon .build/icon-document
python3 "$APP_ICONS" DESIGN.md --name agents --style liquid-glass --out .build/icon
python3 "$APP_ICONS" DESIGN.md --name agents --style liquid-glass --out .build/icon-document --document-only
```

Review `.build/icon/contact-sheet.png` and open the generated `.icon` in Icon
Composer, then replace the committed outputs:

| Generated | Committed |
| --- | --- |
| `.build/icon-document/` | `Brand/Exports/agents/` |
| `.build/icon/web/avatar-1024.png` | `profile/assets/avatar.png` |
| `.build/icon/web/icon-512.png` | `profile/assets/icon.png` |

`python3 "$APP_ICONS" DESIGN.md --name agents --style liquid-glass --check Brand/Exports/agents --document-only`
reports drift between the entry and the committed document.

Framework logos for libraries are generated with that skill's
`scripts/design_icons.py`, as `DESIGN_ICONS`:

```sh
python3 "$DESIGN_ICONS" DESIGN.md --lint
rm -rf .build/logos
python3 "$DESIGN_ICONS" DESIGN.md --out .build/logos --name core --png
```

The generators write only new output directories, so remove the previous
`.build` outputs first. Copy `core.svg` and `core.png` to
`Documentation/Assets/Logo.svg` and `Logo.png` in agents-tools/core, then
check them from this repository with
`python3 "$DESIGN_ICONS" DESIGN.md --check "core=<core checkout>/Documentation/Assets/Logo.svg"`.
The organization avatar on GitHub is uploaded from `profile/assets/avatar.png`.
