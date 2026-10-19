# Repository social cards

| Repository | Card | Title |
| --- | --- | --- |
| [agents-tools/cli](https://github.com/agents-tools/cli) | [cli/card.png](cli/card.png) | agents |
| [agents-tools/core](https://github.com/agents-tools/core) | [core/card.png](core/card.png) | core |
| [agents-tools/homebrew-tap](https://github.com/agents-tools/homebrew-tap) | [homebrew-tap/card.png](homebrew-tap/card.png) | homebrew-tap |

Each directory keeps its `recipe.json`, outlined `card.svg`, 1280×640
`card.png` and `card.layout.json` receipt. Recipes bind to
[DESIGN.md](../../DESIGN.md) by SHA-256 and use the licensed faces in
[Brand/Fonts](../Fonts/OFL.txt). The core icon and its source commit/digest
are retained in [core/SOURCE.md](core/SOURCE.md); tool cards use
[profile/assets/icon.png](../../profile/assets/icon.png).

Run from the repository root with
[github-repo-steward](https://github.com/showxu/skills/tree/master/skills/github-repo-steward)
installed and `rsvg-convert` available. Prepare the ignored environment:

```sh
SOCIAL_SKILL="$HOME/.agents/skills/github-repo-steward"
python3 -m venv .build/social-cards/venv
.build/social-cards/venv/bin/python -m pip install --no-cache-dir \
  -r "$SOCIAL_SKILL/scripts/requirements.txt" fonttools==4.67.0
```

Regenerate all three cards after updating their inputs and, when DESIGN changes,
each recipe's `design_sha256` to the SHA-256 of the final DESIGN.md:

```sh
for card in cli core homebrew-tap; do
  .build/social-cards/venv/bin/python "$SOCIAL_SKILL/scripts/render_social.py" \
    --spec "Brand/Social/$card/recipe.json" --output "Brand/Social/$card/card.svg"
  rsvg-convert -w 1280 -h 640 "Brand/Social/$card/card.svg" \
    -o "Brand/Social/$card/card.png"
done
```

Check the SVGs and layout receipts without rewriting them, then verify that
each PNG matches a fresh conversion:

```sh
for card in cli core homebrew-tap; do
  .build/social-cards/venv/bin/python "$SOCIAL_SKILL/scripts/render_social.py" \
    --spec "Brand/Social/$card/recipe.json" --output "Brand/Social/$card/card.svg" --check
  rsvg-convert -w 1280 -h 640 "Brand/Social/$card/card.svg" \
    -o ".build/social-cards/$card.png"
  cmp "Brand/Social/$card/card.png" ".build/social-cards/$card.png"
done
```

Review every PNG at full size and at 400 px wide, checking icon edges, text
wrapping and clipping against the layout receipt. The accepted PNG is the exact
bytes uploaded as that repository's social preview. Commit sources and exports
together; upload after the accepted source is merged. Remove the temporary PNGs
and environment in `.build/social-cards/` when finished.
