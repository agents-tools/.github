# Profile renderer

`render_profile.py` is copied byte for byte from
[`showxu/skills`](https://github.com/showxu/skills) at commit
`346d15b5d50197fe41d24727c977679ee1e61e6f`. It imports the sibling
`presentation.py`.

| Local file | Upstream path | SHA-256 |
| --- | --- | --- |
| `render_profile.py` | `skills/github-readme-design/scripts/render_profile.py` | `e1588ffc8a69cbe99041f2c733f62315e64315796c3ca353d5c2c917996b929e` |

The shared dependency and license are copied byte for byte from
[`showxu/skills`](https://github.com/showxu/skills) at commit
`ac178c7b85a0693b1595f1ac7e46945584a43375`:

| Local file | Upstream path | SHA-256 |
| --- | --- | --- |
| `presentation.py` | `skills/github-repo-steward/scripts/presentation.py` | `5b3a8164c9eed21ac6d34c2c476f492339ff71c4c138aacb5efac56145506d00` |
| `LICENSE` | `LICENSE` | `16cce2b404888067eb74891e05f2281837fef58c1cc73d50025cc460ceff8bf1` |

The files are MIT-licensed, copyright (c) 2026 showxu. The full upstream notice
is preserved in [LICENSE](LICENSE).

[`Scripts/render-profile.py`](../render-profile.py) runs it with
`profile/catalog.json` and `Brand/Profile/recipe.json`; `Scripts/check`
validates the catalog with it. The renderer and its input contract are owned
upstream; update it from `skills/github-readme-design/scripts/`, then
regenerate the profile.

## Updating

Review the upstream changes and select one full commit SHA for the renderer,
its dependencies and license. In this repository's task worktree, with
`SKILLS_CHECKOUT` pointing to a local `showxu/skills` checkout and
`REVISION` set to that reviewed commit, copy the original Git blobs:

```sh
git -C "$SKILLS_CHECKOUT" show "$REVISION:skills/github-readme-design/scripts/render_profile.py" > Scripts/vendor/render_profile.py
git -C "$SKILLS_CHECKOUT" show "$REVISION:skills/github-readme-design/scripts/presentation.py" > Scripts/vendor/presentation.py
git -C "$SKILLS_CHECKOUT" show "$REVISION:LICENSE" > Scripts/vendor/LICENSE
shasum -a 256 Scripts/vendor/render_profile.py Scripts/vendor/presentation.py Scripts/vendor/LICENSE
```

Do not patch the vendored files locally. Review imports for new upstream
dependencies, preserve their licensing, and update the revision and hashes
above together. Regenerate the profile and run its byte check and unit tests:

```sh
python3 Scripts/render-profile.py
python3 Scripts/render-profile.py --check
python3 -m unittest discover -s Tests
```

Commit source, provenance and any changed profile inputs and output together.
Review the generated public profile and the member dashboard in both themes.
