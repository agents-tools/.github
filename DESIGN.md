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
| `core` | Face `#6A63F0` to `#3B35D1`; bands `oklch(0.52 0.2 280)`, `oklch(0.6 0.19 302)`, `oklch(0.68 0.17 340)` | Core framework logo: an indigo face over violet and pink bands |

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
      "mode": "glow",
      "bands": 3,
      "face_colors": [
        "#6A63F0",
        "#3B35D1"
      ],
      "band_colors": [
        "oklch(0.52 0.2 280)",
        "oklch(0.6 0.19 302)",
        "oklch(0.68 0.17 340)"
      ],
      "custom_glyph": {
        "style": "fill",
        "d": "M0.022 -0.897 L0.029 -0.858 L0.037 -0.820 L0.045 -0.783 L0.054 -0.747 L0.063 -0.712 L0.073 -0.677 L0.083 -0.644 L0.093 -0.611 L0.104 -0.579 L0.115 -0.548 L0.127 -0.518 L0.139 -0.489 L0.153 -0.460 L0.165 -0.432 L0.179 -0.406 L0.194 -0.380 L0.208 -0.355 L0.224 -0.330 L0.239 -0.307 L0.255 -0.284 L0.272 -0.263 L0.289 -0.242 L0.306 -0.222 L0.324 -0.203 L0.343 -0.185 L0.361 -0.167 L0.381 -0.151 L0.401 -0.135 L0.421 -0.120 L0.442 -0.106 L0.463 -0.092 L0.485 -0.080 L0.506 -0.068 L0.529 -0.058 L0.552 -0.047 L0.576 -0.038 L0.600 -0.030 L0.624 -0.022 L0.640 -0.015 L0.646 -0.016 L0.652 -0.015 L0.657 -0.011 L0.661 -0.006 L0.662 0.000 L0.661 0.006 L0.657 0.011 L0.652 0.015 L0.646 0.016 L0.640 0.015 L0.624 0.022 L0.600 0.030 L0.576 0.038 L0.552 0.047 L0.529 0.058 L0.506 0.068 L0.485 0.080 L0.463 0.092 L0.442 0.106 L0.421 0.120 L0.401 0.135 L0.381 0.151 L0.361 0.167 L0.343 0.185 L0.324 0.203 L0.306 0.222 L0.289 0.242 L0.272 0.263 L0.255 0.284 L0.239 0.307 L0.224 0.330 L0.208 0.355 L0.194 0.380 L0.179 0.406 L0.165 0.432 L0.153 0.460 L0.139 0.489 L0.127 0.518 L0.115 0.548 L0.104 0.579 L0.093 0.611 L0.083 0.644 L0.073 0.677 L0.063 0.712 L0.054 0.747 L0.045 0.783 L0.037 0.820 L0.029 0.858 L0.022 0.897 L0.013 0.925 L0.016 0.931 L0.015 0.938 L0.012 0.944 L0.007 0.948 L0.000 0.950 L-0.007 0.948 L-0.012 0.944 L-0.015 0.938 L-0.016 0.931 L-0.013 0.925 L-0.022 0.897 L-0.029 0.858 L-0.037 0.820 L-0.045 0.783 L-0.054 0.747 L-0.063 0.712 L-0.073 0.677 L-0.083 0.644 L-0.093 0.611 L-0.104 0.579 L-0.115 0.548 L-0.127 0.518 L-0.139 0.489 L-0.153 0.460 L-0.165 0.432 L-0.179 0.406 L-0.194 0.380 L-0.208 0.355 L-0.224 0.330 L-0.239 0.307 L-0.255 0.284 L-0.272 0.263 L-0.289 0.242 L-0.306 0.222 L-0.324 0.203 L-0.343 0.185 L-0.361 0.167 L-0.381 0.151 L-0.401 0.135 L-0.421 0.120 L-0.442 0.106 L-0.463 0.092 L-0.485 0.080 L-0.506 0.068 L-0.529 0.058 L-0.552 0.047 L-0.576 0.038 L-0.600 0.030 L-0.624 0.022 L-0.640 0.015 L-0.646 0.016 L-0.652 0.015 L-0.657 0.011 L-0.661 0.006 L-0.662 0.000 L-0.661 -0.006 L-0.657 -0.011 L-0.652 -0.015 L-0.646 -0.016 L-0.640 -0.015 L-0.624 -0.022 L-0.600 -0.030 L-0.576 -0.038 L-0.552 -0.047 L-0.529 -0.058 L-0.506 -0.068 L-0.485 -0.080 L-0.463 -0.092 L-0.442 -0.106 L-0.421 -0.120 L-0.401 -0.135 L-0.381 -0.151 L-0.361 -0.167 L-0.343 -0.185 L-0.324 -0.203 L-0.306 -0.222 L-0.289 -0.242 L-0.272 -0.263 L-0.255 -0.284 L-0.239 -0.307 L-0.224 -0.330 L-0.208 -0.355 L-0.194 -0.380 L-0.179 -0.406 L-0.165 -0.432 L-0.153 -0.460 L-0.139 -0.489 L-0.127 -0.518 L-0.115 -0.548 L-0.104 -0.579 L-0.093 -0.611 L-0.083 -0.644 L-0.073 -0.677 L-0.063 -0.712 L-0.054 -0.747 L-0.045 -0.783 L-0.037 -0.820 L-0.029 -0.858 L-0.022 -0.897 L-0.013 -0.925 L-0.016 -0.931 L-0.015 -0.938 L-0.012 -0.944 L-0.007 -0.948 L0.000 -0.950 L0.007 -0.948 L0.012 -0.944 L0.015 -0.938 L0.016 -0.931 L0.013 -0.925 Z"
      },
      "glyph_rotation": -45,
      "glyph_scale": 0.34
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
