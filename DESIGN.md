# agents-tools Design

## Overview

The agents mark is a mecha crest holding a glint star: the V-shaped fin of
an anime robot's helmet arms the agent, and the star at its center stands for
intelligence. The same app icon is the organization avatar, the mark on the
organization profile and the mark of the `agents` CLI.

Reusable libraries use the framework icon style instead of the app icon
style, so a visitor can tell a tool from a component. The core library is an
isometric slab of three bands, one per module, with the same glint star on
its face.

The app icon is a Liquid Glass icon built in Icon Composer. Its Icon Composer
document and rendered assets are generated from the `app_icons` entry below,
and framework logos from the `icons` entries; change an entry or its artwork,
then regenerate.

## Colors

| Token | Value | Use |
| --- | --- | --- |
| `background` | `#3B35D1` | App icon background; Icon Composer derives its gradient from it |
| `fin` | `#FFC845` | Crest fin |
| `star` | `#FFFFFF` | Glint star |
| `core` | OKLCH hue 274 | Hue of the core framework logo |

## Iconography

The fin is translucent glass behind the star. The star's translucency is off,
so the gold fin never shows through it; the two still overlap with depth, and
the star keeps its shape in the dark, clear and tinted appearances.

```json
{
  "app_icons": {
    "agents": {
      "background": "#3B35D1",
      "gradient": true,
      "groups": [
        {
          "name": "Fin",
          "layers": [{"source": "Brand/Icon/fin.svg", "name": "Fin"}],
          "shadow": {"kind": "neutral", "opacity": 0.5},
          "translucency": {"enabled": true, "value": 0.35}
        },
        {
          "name": "Star",
          "layers": [{"source": "Brand/Icon/star.svg", "name": "Star"}],
          "shadow": {"kind": "neutral", "opacity": 0.5},
          "translucency": {"enabled": false, "value": 0}
        }
      ],
      "styles": {
        "liquid-glass": {"design_generation": 27}
      }
    }
  },
  "icons": {
    "core": {
      "hue": 274,
      "mode": "deepen",
      "bands": 3,
      "custom_glyph": {"style": "fill", "d": "M0 -0.95 C0.06 -0.3 0.2 -0.08 0.62 0 C0.2 0.08 0.06 0.3 0 0.95 C-0.06 0.3 -0.2 0.08 -0.62 0 C-0.2 -0.08 -0.06 -0.3 0 -0.95 Z"},
      "texture": "constellation",
      "glyph_rotation": -45,
      "glyph_scale": 0.36
    }
  }
}
```

| Output | Path |
| --- | --- |
| Icon Composer document | `Brand/Exports/agents/agents.icon` |
| Organization avatar, 1024 px | `profile/assets/avatar.png` |
| Profile mark, 512 px | `profile/assets/icon.png` |
| Core framework logo | `Documentation/Assets/Logo.svg` and `Logo.png` in agents-tools/core |
