# agents-tools/.github

Organization profile and shared community standards for
[agents-tools](https://github.com/agents-tools).

GitHub uses the community files and issue and pull-request templates here
for repositories in the organization that lack their own. Repositories keep
their own CODEOWNERS, workflows, and repository-specific development
instructions.

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

Python 3 and its standard library are sufficient; there is no build step or
dependency installation. The membership check uses the public GitHub API.
Set `GITHUB_TOKEN` for authenticated read access, or use an authenticated
GitHub CLI session without printing the token:

```sh
GITHUB_TOKEN="$(gh auth token)" python3 Scripts/check
```

For local work without GitHub access, `python3 Scripts/check --offline`
skips only membership verification. CI runs the full check.
