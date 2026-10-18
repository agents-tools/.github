# agents-tools/.github

Organization profile and shared community standards for
[agents-tools](https://github.com/agents-tools).

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
| `.github/ISSUE_TEMPLATE/` | Bug and feature templates, plus security reporting guidance |
| `.github/pull_request_template.md` | Change summary, validation, and documentation prompts |
| `profile/catalog.json` | Promise, navigation, and repository groups for the profile |
| `profile/README.md` | Organization profile generated from the catalog |
| `profile/assets/` | Organization avatar and profile mark |
| `DESIGN.md` | Brand colors, the agents app icon entry and framework logo entries |
| `Brand/Icon/` | App icon layer artwork |
| `Brand/Exports/agents/` | Icon Composer document generated from the app icon entry |
| `Scripts/` | Profile renderer and repository checks |
| `Tests/` | Profile tooling tests |
| `.github/workflows/ci.yml` | Automated tests and checks |
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

The catalog accepts an optional `mark` object (`path` to a repository file
and `alt` text) and an optional `quickstart` object (`title` and a list of
single-line `commands`). Omitted objects produce no markup.
An optional `mark.dark` path to a repository file selects a dark-mode image
using `<picture>`; `mark.path` remains the light-mode and fallback image.

Python 3 and its standard library are sufficient; there is no build step or
dependency installation. The membership check uses the public GitHub API.
Set `GITHUB_TOKEN` for authenticated read access, or use an authenticated
GitHub CLI session without printing the token:

```sh
GITHUB_TOKEN="$(gh auth token)" python3 Scripts/check
```

For local work without GitHub access, `python3 Scripts/check --offline`
skips only membership verification. CI runs the full check.

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
