# Terminal presentation renderer

These files are copied byte for byte from
[`showxu/skills`](https://github.com/showxu/skills) at commit
`ac178c7b85a0693b1595f1ac7e46945584a43375`:

| Local file | Upstream path | SHA-256 |
| --- | --- | --- |
| `render_terminal.py` | `skills/github-repo-steward/scripts/render_terminal.py` | `67f367cac9f205318c477c3aa5443046b5be62e9cfd15f4d7cc73499f388555b` |
| `presentation.py` | `skills/github-repo-steward/scripts/presentation.py` | `5b3a8164c9eed21ac6d34c2c476f492339ff71c4c138aacb5efac56145506d00` |
| `LICENSE` | `LICENSE` | `16cce2b404888067eb74891e05f2281837fef58c1cc73d50025cc460ceff8bf1` |

The renderer imports the sibling `presentation.py`; both use only Python's
standard library. They are MIT-licensed, copyright (c) 2026 showxu. The full
upstream notice is preserved in [LICENSE](LICENSE).

The [presentation workflow](../../.github/workflows/presentation.yml) checks
out this repository at its own `job.workflow_sha` and runs this copy against
the caller's recording, recipe and committed SVGs. It requires no skill
installation in the member's CI. The
[integration guide](../../Documentation/Reference/WorkflowIntegration.md#presentation-caller)
owns the caller interface and pin mechanism.

## Updating

Review the upstream changes and select one full commit SHA for the renderer,
its dependencies and license. In this repository's task worktree, with
`SKILLS_CHECKOUT` pointing to a local `showxu/skills` checkout and
`REVISION` set to that reviewed commit, copy the original Git blobs:

```sh
git -C "$SKILLS_CHECKOUT" show "$REVISION:skills/github-repo-steward/scripts/render_terminal.py" > Scripts/vendor/render_terminal.py
git -C "$SKILLS_CHECKOUT" show "$REVISION:skills/github-repo-steward/scripts/presentation.py" > Scripts/vendor/presentation.py
git -C "$SKILLS_CHECKOUT" show "$REVISION:LICENSE" > Scripts/vendor/LICENSE
shasum -a 256 Scripts/vendor/render_terminal.py Scripts/vendor/presentation.py Scripts/vendor/LICENSE
```

Do not patch the vendored files locally. Review imports for any new upstream
dependencies, preserve their licensing, and update the revision and hashes
above together. Run the unit tests and fixture check. If an accepted upstream
change alters rendering, regenerate and inspect both fixture SVGs:

```sh
python3 -B Scripts/vendor/render_terminal.py --record Tests/Fixtures/Presentation/record.json --spec Tests/Fixtures/Presentation/recipe.json --output-dir Tests/Fixtures/Presentation
python3 -B Scripts/vendor/render_terminal.py --record Tests/Fixtures/Presentation/record.json --spec Tests/Fixtures/Presentation/recipe.json --output-dir Tests/Fixtures/Presentation --check
```

Commit source, provenance and any changed fixtures together. Verify the real
CI run, then follow the integration guide's representative consumer gate
before advancing member pins. Members regenerate their recordings with the
same accepted renderer before adopting a revision that changes output.
