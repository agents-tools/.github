# agents-tools Design

## Overview

The agents mark is a homage to *Ghost in the Shell* by Masamune Shirow. The
agent is the ghost, a point of light; the tools around it are its shell, a
hexagon of glass. `agents` equips that shell with skills and instructions —
and lives in a shell itself.

Reusable libraries use the framework icon style instead of the app icon
style, so a visitor can tell a tool from a component. The core library is an
isometric slab of three bands, one per module, with the same star on its face.

The app icon is a Liquid Glass icon built in Icon Composer. Its Icon Composer
document and rendered assets are generated from the `app_icons` entry below,
and framework logos from the `icons` entries; change an entry or its artwork,
then regenerate.

## Colors

| Token | Value | Use |
| --- | --- | --- |
| `background` | `#3B35D1` | App icon background; Icon Composer derives its gradient from it |
| `shell` | `#1A1F5C` | Glass shell |
| `ghost` | `#FFFFFF` | Ghost star and its light |
| `spirit` | `#B57AFF`, `#FF7AD6` | Haze inside the shell |
| `core` | OKLCH hue 274 | Hue of the core framework logo |

## Iconography

```json
{
  "app_icons": {
    "agents": {
      "background": "#3B35D1",
      "gradient": true,
      "groups": [
        {
          "name": "Spirit",
          "shadow": {
            "kind": "layer-color",
            "opacity": 0.5
          },
          "translucency": {
            "enabled": true,
            "value": 0.4
          },
          "refractivity": {
            "enabled": true,
            "strength": 0.4,
            "depth": 0.16
          },
          "layers": [
            {
              "source": "Brand/Icon/spirit-a.svg",
              "name": "Spirit A",
              "fill": {
                "automatic-gradient": "#B57AFF"
              }
            },
            {
              "source": "Brand/Icon/spirit-b.svg",
              "name": "Spirit B",
              "fill": {
                "automatic-gradient": "#FF7AD6"
              },
              "opacity": 0.85
            }
          ]
        },
        {
          "name": "Bloom",
          "blend-mode": "plus-lighter",
          "specular": false,
          "shadow": {
            "kind": "none",
            "opacity": 0
          },
          "translucency": {
            "enabled": false,
            "value": 0
          },
          "layers": [
            {
              "source": "Brand/Icon/bloom-outer.svg",
              "name": "Bloom outer",
              "fill": {
                "solid": "#FFFFFF"
              },
              "opacity": 0.32
            },
            {
              "source": "Brand/Icon/bloom-inner.svg",
              "name": "Bloom inner",
              "fill": {
                "solid": "#FFFFFF"
              },
              "opacity": 0.65
            },
            {
              "source": "Brand/Icon/bloom-core.svg",
              "name": "Bloom core",
              "fill": {
                "solid": "#FFFFFF"
              },
              "opacity": 0.75
            }
          ]
        },
        {
          "name": "Shell",
          "shadow": {
            "kind": "layer-color",
            "opacity": 0.5
          },
          "translucency": {
            "enabled": true,
            "value": 0.55
          },
          "blur-material": 0.55,
          "refractivity": {
            "enabled": true,
            "strength": 0.8,
            "depth": 0.14
          },
          "layers": [
            {
              "source": "Brand/Icon/shell.svg",
              "name": "Shell",
              "fill": {
                "automatic-gradient": "#1A1F5C"
              }
            }
          ]
        },
        {
          "name": "Ghost",
          "blend-mode": "plus-lighter",
          "shadow": {
            "kind": "layer-color",
            "opacity": 0.5
          },
          "translucency": {
            "enabled": false,
            "value": 0
          },
          "refractivity": {
            "enabled": true,
            "strength": 0.2,
            "depth": 0.1
          },
          "layers": [
            {
              "source": "Brand/Icon/star.svg",
              "name": "Ghost",
              "fill": {
                "automatic-gradient": "#FFFFFF"
              },
              "fill-specializations": {
                "dark": {
                  "solid": "#FFFFFF"
                }
              }
            }
          ]
        }
      ],
      "styles": {
        "liquid-glass": {
          "design_generation": 27
        }
      }
    }
  },
  "icons": {
    "core": {
      "hue": 274,
      "mode": "deepen",
      "bands": 3,
      "custom_glyph": {
        "style": "fill",
        "d": "M0 -0.95 C0.06 -0.3 0.2 -0.08 0.62 0 C0.2 0.08 0.06 0.3 0 0.95 C-0.06 0.3 -0.2 0.08 -0.62 0 C-0.2 -0.08 -0.06 -0.3 0 -0.95 Z"
      },
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
