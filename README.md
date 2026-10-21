# agents-tools/.github

Organization profile, brand and shared standards for
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
| `docs/reference/workflow-integration.md` | Reusable workflow interfaces, caller pins and required contexts |
| `.github/ISSUE_TEMPLATE/` | Bug and feature templates, plus security reporting guidance |
| `.github/pull_request_template.md` | Change summary, validation, and documentation prompts |
| `profile/catalog.json` | Profile content, repository kinds, titles, About descriptions and icons |
| `.github/assets/social-preview/social-preview.png` | Organization repository social preview |
| `profile/README.md` | Organization profile generated from the catalog |
| `profile/assets/` | Organization avatar and profile mark |
| `DESIGN.md` | Visual tokens in Google's DESIGN.md format, the app icon entry and framework logo entries |
| `.github/design/icons/agents/layers/` | App icon layer artwork |
| `.github/design/icons/*/provenance.json` | Verified icon outputs, consumed copies and SHA-256 digests |
| `.github/design/fonts/` | Variable font and its upstream license |
| `scripts/` | Presentation input resolver, policy generator and read-only repository/settings checks |
| `tests/` | Workflow, input resolver, provenance, policy, settings and repository metadata tests |
| `.github/workflows/` | Shared policy, Swift CI, presentation and profile checks, plus this repository's callers |
| `.github/dependabot.yml` | Weekly Actions dependency updates |
| `AGENTS.md` | Repository-specific agent guide |
| `LICENSE` | Repository license |

## Change the profile

Edit `profile/catalog.json`, then regenerate `profile/README.md` with the
pinned toolchain using the commands below. Commit the catalog and generated
README together. The catalog lists every public, non-archived repository of
the organization except `.github`. Each entry declares its `kind`, `title`,
verbatim repository `about`, plain-text `outcome` and README header `icon`.
The organization also declares its own `.github` repository's `about`.
Marks and icons may select light and dark images.

The profile workflow owns catalog validation and compares the generated
profile byte for byte. `scripts/check` reads membership fields and compares
membership and every `about` with GitHub in online and public modes; it lists
all description differences together. Offline mode skips these live checks.
The private `.github-private` dashboard uses the catalog and DESIGN at its
pinned profile workflow revision, with operational values in
`profile/member.json`.

The policy and settings checks use Python 3 and its standard library.
Public membership and About checks use the GitHub API with optional
`GITHUB_TOKEN` read access. Run:

```sh
python3 -B -m unittest discover -s tests -v
python3 scripts/check --offline
python3 scripts/check --public
python3 scripts/check
```

The default online mode also needs an authenticated `gh` session that can
read declared repository settings across both organizations. CI uses
`--public` with its read-only token and skips administrative settings. Run the
default check before handoff and report drift and unavailable observations;
it never mutates GitHub. See [Maintenance](MAINTENANCE.md#read-only-verification).

## Change the Standard

Follow [Maintenance](MAINTENANCE.md) for change flow and declarations,
[Versioning](VERSIONING.md) for release policy, and
[Workflow integration](docs/reference/workflow-integration.md) for
shared workflow interfaces and adoption. After editing `scripts/check-policy.py`
or its workflow generator, run `python3 scripts/sync-policy-workflow.py` and
commit the generated workflow too.

Before handoff, run the offline and online checks, unit tests, `actionlint`
(or parse every workflow as YAML when unavailable), and `git diff --check
origin/master`. Member settings activation and workflow pin rollouts require
the real consumer evidence described in the integration guide.

## Change the design and regenerate assets

`DESIGN.md` owns the visual tokens in Google's DESIGN.md front matter and the
icon entries. Read it before visual or asset work. The same pinned TypeScript
toolchain lints DESIGN and renders profiles, social previews and terminals. Use
the package at `9e5d7268232b78f5fbef21ccfb9e3a079f2ef7e3` (`v0.1.0`) in the
ignored `.build/presentation-toolchain`, following its [local regeneration
contract](https://github.com/showxu/skills/blob/9e5d7268232b78f5fbef21ccfb9e3a079f2ef7e3/skills/github-readme-design/references/renderers.md#local-regeneration):

```sh
toolchain_commit='9e5d7268232b78f5fbef21ccfb9e3a079f2ef7e3' # v0.1.0
toolchain_dir="$PWD/.build/presentation-toolchain"
mkdir -p "$toolchain_dir"
curl -fsSL "https://api.github.com/repos/showxu/skills/tarball/$toolchain_commit" \
  -o "$toolchain_dir/source.tar.gz"
archive_root="$(tar -tzf "$toolchain_dir/source.tar.gz" | sed -n '1s,/.*,,p')"
tar -xzf "$toolchain_dir/source.tar.gz" -C "$toolchain_dir" --strip-components=4 \
  "$archive_root/skills/github-readme-design/scripts"
tar -xzf "$toolchain_dir/source.tar.gz" -C "$toolchain_dir" --strip-components=1 \
  "$archive_root/LICENSE"
node --version # Must match the copied .node-version; use that runtime below.
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

DESIGN lint requires zero errors and zero warnings. The icon above is the
catalog mark's light-page image. Public profile commands omit member input and
catalog revision. These commands generate the organization's own assets;
members keep their previews in their own `.github/assets/social-preview/`.
Uploading the PNG in GitHub Settings remains a separate manual step.

Regenerate every output that reads changed DESIGN tokens or icon artwork,
review the outputs, and commit sources and outputs together. CI's local
`presentation` and `profile` calls check the organization's preview and public
profile. Reuse the package directory for a pin, replace its contents when
changing pins, and remove download and dependency outputs when finished.

## Change the Icons

Icons are generated from `DESIGN.md` with the
[apple-app-icon-design](https://github.com/showxu/skills/tree/master/skills/apple-app-icon-design)
and
[apple-framework-icon-design](https://github.com/showxu/skills/tree/master/skills/apple-framework-icon-design)
skills. Native Liquid Glass rendering needs macOS with Xcode's Icon Composer
and `rsvg-convert`.

For the agents app icon, edit its entry or the artwork in
`.github/design/icons/agents/layers/`, then run from this repository, with
`APP_ICONS` set to that skill's `scripts/app_icons.py`:

```sh
python3 "$APP_ICONS" DESIGN.md --name agents --lint
rm -rf .build/icon .build/icon-document
python3 "$APP_ICONS" DESIGN.md --name agents --style liquid-glass --out .build/icon
python3 "$APP_ICONS" DESIGN.md --name agents --style liquid-glass --out .build/icon-document --document-only
```

Review `.build/icon/contact-sheet.png` and open the generated `.icon` in Icon
Composer. The document stays in ignored scratch. Copy the consumed outputs
to their owners:

| Generated | Consumed copy |
| --- | --- |
| `.build/icon/web/avatar-1024.png` | `profile/assets/avatar.png` |
| `.build/icon/web/icon-512.png` | `profile/assets/icon.png` |
| `.build/icon/web/icon-512.png` | `.github/assets/logo/logo.png` in agents-tools/cli |

Record each consumed copy in `.github/design/icons/agents/provenance.json`:
its repository, path, generator output path and SHA-256, together with the
skill name, full skill commit, exact command, renderer version and verification
date. For a drift check, regenerate into `.build/icon` with the recorded skill
commit and renderer, then compare the output digests with the receipt:

```sh
python3 -B - <<'PYTHON'
import hashlib
import json
from pathlib import Path

receipt = json.loads(Path(".github/design/icons/agents/provenance.json").read_text())
for copy in receipt["copies"]:
    output = Path(".build/icon") / copy["output"]
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    if digest != copy["sha256"]:
        raise SystemExit(f"Icon drift: {copy['repository']}: {copy['path']}")
PYTHON
```

Repository tests compare every `profile/assets/` file with its receipt;
member presentation checks verify each caller-owned catalog icon against the
receipts at the pinned standard.

Framework logos for libraries are generated with that skill's
`scripts/design_icons.py`, as `DESIGN_ICONS`:

```sh
python3 "$DESIGN_ICONS" DESIGN.md --lint
rm -rf .build/logos
python3 "$DESIGN_ICONS" DESIGN.md --out .build/logos --name core --png
```

The generators write only new output directories, so remove the previous
`.build` outputs first. Copy `core.svg` and `core.png` to
`.github/assets/logo/logo.svg` and `.github/assets/logo/logo.png` in
agents-tools/core, then check them from this repository with
`python3 "$DESIGN_ICONS" DESIGN.md --check "core=<core checkout>/.github/assets/logo/logo.svg"`.
Record both core copies in `.github/design/icons/core/provenance.json` with
the same fields. Compare their generated digests with that receipt, using
`.build/logos` as the output root.
The organization avatar on GitHub is uploaded from `profile/assets/avatar.png`.
