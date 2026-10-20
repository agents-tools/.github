---
version: alpha
name: agents-tools
description: Visual identity of the agents-tools organization and its repositories.
colors:
  primary: "#3B35D1"
  primary-dark: "#8F8AFF"
  ink: "#16143D"
  ink-dark: "#F1F0FF"
  terminal-surface: "#FBFBFE"
  terminal-surface-dark: "#0E0F24"
  terminal-bar: "#F0EFF8"
  terminal-bar-dark: "#16183A"
  terminal-border: "#DCDBEA"
  terminal-border-dark: "#2A2C55"
  terminal-output: "#3F3D5C"
  terminal-output-dark: "#C8C7E6"
  terminal-dim: "#67657F"
  terminal-dim-dark: "#8785AE"
  social-preview-background: "#F5F4FF"
  social-preview-muted: "#4F4C7A"
typography:
  terminal:
    fontFamily: Google Sans Code
    fontSize: 14px
    fontWeight: 400
    lineHeight: 21px
    fontVariation: "'MONO' 1"
  social-preview-title:
    fontFamily: Google Sans Code
    fontSize: 72px
    fontWeight: 700
    lineHeight: 82.8px
    fontVariation: "'MONO' 0"
  social-preview-owner:
    fontFamily: Google Sans Code
    fontSize: 28px
    fontWeight: 500
    lineHeight: 28px
    fontVariation: "'MONO' 0"
  social-preview-body:
    fontFamily: Google Sans Code
    fontSize: 32px
    fontWeight: 400
    lineHeight: 44px
    fontVariation: "'MONO' 0"
rounded:
  terminal: 10px
spacing:
  terminal-padding: 20px
  terminal-title-bar: 34px
  terminal-min-width: 560px
  hairline: 1px
  social-preview-padding: 64px
  social-preview-gap: 64px
  social-preview-stack: 24px
  social-preview-icon: 384px
  profile-header-icon: 128px
  profile-member-header-icon: 64px
  profile-row-icon: 40px
  profile-member-row-icon: 24px
components:
  terminal:
    backgroundColor: "{colors.terminal-surface}"
    textColor: "{colors.terminal-output}"
    typography: "{typography.terminal}"
    rounded: "{rounded.terminal}"
    padding: "{spacing.terminal-padding}"
    width: "{spacing.terminal-min-width}"
  terminal-dark:
    backgroundColor: "{colors.terminal-surface-dark}"
    textColor: "{colors.terminal-output-dark}"
  terminal-frame:
    backgroundColor: "{colors.terminal-border}"
    size: "{spacing.hairline}"
  terminal-frame-dark:
    backgroundColor: "{colors.terminal-border-dark}"
  terminal-title-bar:
    backgroundColor: "{colors.terminal-bar}"
    textColor: "{colors.terminal-dim}"
    height: "{spacing.terminal-title-bar}"
  terminal-title-bar-dark:
    backgroundColor: "{colors.terminal-bar-dark}"
    textColor: "{colors.terminal-dim-dark}"
  terminal-prompt:
    backgroundColor: "{colors.terminal-surface}"
    textColor: "{colors.primary}"
  terminal-prompt-dark:
    backgroundColor: "{colors.terminal-surface-dark}"
    textColor: "{colors.primary-dark}"
  terminal-command:
    backgroundColor: "{colors.terminal-surface}"
    textColor: "{colors.ink}"
  terminal-command-dark:
    backgroundColor: "{colors.terminal-surface-dark}"
    textColor: "{colors.ink-dark}"
  social-preview:
    backgroundColor: "{colors.social-preview-background}"
    textColor: "{colors.ink}"
    typography: "{typography.social-preview-title}"
    padding: "{spacing.social-preview-padding}"
    size: "{spacing.social-preview-icon}"
  social-preview-gap:
    width: "{spacing.social-preview-gap}"
    height: "{spacing.social-preview-stack}"
  social-preview-owner:
    backgroundColor: "{colors.social-preview-background}"
    textColor: "{colors.ink}"
    typography: "{typography.social-preview-owner}"
  social-preview-about:
    backgroundColor: "{colors.social-preview-background}"
    textColor: "{colors.social-preview-muted}"
    typography: "{typography.social-preview-body}"
  profile-header:
    size: "{spacing.profile-header-icon}"
  profile-member-header:
    size: "{spacing.profile-member-header-icon}"
  profile-row:
    size: "{spacing.profile-row-icon}"
  profile-member-row:
    size: "{spacing.profile-member-row-icon}"
---

# agents-tools Design

## Overview

The agents mark is a homage to *Ghost in the Shell* by Masamune Shirow. The
agent is the ghost, a point of light; the tools around it are its shell, a
hexagon of glass. `agents` equips that shell with skills and instructions —
and lives in a shell itself.

Reusable libraries use the framework icon style instead of the app icon
style, so a visitor can tell a tool from a component. The core library is an
isometric slab of three bands, one per module, with the same star on its face.

This file follows Google's [DESIGN.md format](https://github.com/google-labs-code/design.md)
(`version: alpha`). Every token lives in the front matter; the sections below
explain intent and cite token names instead of values. CI lints this file
with the official `@google/design.md` parser and rejects any error or warning.
`github-readme-design`'s toolchain renders terminal demos, social previews and
the organization profiles from these tokens through the same parser. Change a
token, then regenerate every output that reads it.

## Colors

`primary` is the app icon's indigo. It marks what a reader acts on: the
terminal prompt and, on the website, links and accents. `primary-dark` lifts
the same hue for dark surfaces.

`ink` is a deep indigo for titles and commands, so text keeps the family's hue
instead of a neutral black; `ink-dark` is its counterpart on dark surfaces.

The `terminal-*` colors build a quiet window around the session: a near-white
surface, a slightly deeper title bar and a hairline border in light, and the
shell's night blue in dark. Output is one step softer than commands, so the
eye goes to what was typed; `terminal-dim` is reserved for the window title.

The `social-preview-*` colors are the card's pale lavender ground and the
muted tone of its About sentence.

App icon and framework logo colors are defined by their entries in
[Iconography](#iconography).

## Typography

One family, Google Sans Code, carries every lettering role. Its `MONO` axis
switches between a monospaced and a proportional design and `wght` sets the
weight; each typography token selects both. Terminal sessions and code are set
monospaced so output keeps its column grid; titles, labels and body text are
set proportional, which reads more compactly at display sizes.

Rendered lettering, terminal sessions included, is converted to glyph outlines
from `Brand/Fonts/GoogleSansCode[MONO,wght].ttf`, so every reader sees the same
letterforms and widths whatever fonts they have installed. The font is
Google Sans Code v7.001 from the
[googlefonts/googlesans-code](https://github.com/googlefonts/googlesans-code)
release archive (SHA-256
`eebba2a438882396e8530cad6d6cb80182b0afb6e9e0ad07b7340359a53ba2e9`), licensed
under the SIL Open Font License 1.1 (`Brand/Fonts/OFL.txt`).

The website reads static `MONO` 0 instances,
`Brand/Fonts/GoogleSansCodeProportional-{Regular,Medium,Bold}.ttf`, which
`python3 Brand/Fonts/instantiate.py` reproduces byte for byte.

## Layout

A terminal window is never narrower than `terminal-min-width` and grows with
its widest line. Its maximum is the width of GitHub's README column, a
platform limit the renderer enforces: a session that does not fit is
shortened, never scaled down. The title bar is `terminal-title-bar` tall, the
session sits `terminal-padding` from every edge, and one empty line separates
commands.

### Social preview canvas

A social preview fills GitHub's 1280×640 canvas. The icon is a
`social-preview-icon` square set `social-preview-padding` from the left edge,
and the text column starts `social-preview-gap` after it. Owner, title and
About stack `social-preview-stack` apart, centered vertically. Text is never
cut: a long title shrinks, then breaks at a hyphen or slash, and the About
sentence wraps.

### Organization profile

The public profile (`profile/README.md`) and the member dashboard in the
private `.github-private` repository are rendered by `github-readme-design`'s
toolchain from `profile/catalog.json`. The umbrella mark is a
`profile-header-icon` square on the public profile and a
`profile-member-header-icon` square on the dashboard; repository icons use
`profile-row-icon` and `profile-member-row-icon`.

| Field | Source |
| --- | --- |
| Row icon | The logo in that repository's README header; the tap and the website use the agents mark |
| Outcome | One plain-text sentence per repository in the catalog |

## Elevation & Depth

Presentation surfaces are flat: no shadows, gradients or blur. A terminal
window stands apart from the page by its hairline frame alone. Depth belongs
to the app icon, whose glass is defined in Iconography.

## Shapes

Terminal windows use the `terminal` corner radius, a soft corner that echoes
the app icon without imitating its continuous curve. The title bar carries no
window buttons: the session is the subject, not a desktop.

## Components

Each component is a presentation role. The light appearance carries the base
name; the dark appearance adds `-dark` and lists only the properties that
change, which renderers merge over the base.

| Component | Role |
| --- | --- |
| `terminal` | Window body, output text and the terminal typography |
| `terminal-frame` | Hairline outline and the separator under the title bar |
| `terminal-title-bar` | Title band and the session title |
| `terminal-prompt` | The `$ ` before each command |
| `terminal-command` | Command text |
| `social-preview` | Card ground, padding, icon square and repository title |
| `social-preview-gap` | Gap after the icon and between the text blocks |
| `social-preview-owner` | Owner label |
| `social-preview-about` | About sentence |
| `profile-header`, `profile-member-header` | Umbrella mark on the public profile and the member dashboard |
| `profile-row`, `profile-member-row` | Repository icons on the public profile and the member dashboard |

### Social preview

| Field | Source |
| --- | --- |
| `owner` | The organization login, `agents-tools` |
| `title` | The catalog entry's `title`, the repository's README title: `agents` for cli, `core` for core, `homebrew-tap` for the tap; the organization `name` for `.github` |
| `about` | The catalog entry's `about`, the repository's About sentence and README tagline, complete and unchanged |
| `icon` | The catalog entry's light-page icon: the agents app icon for cli, the tap and `.github`; the framework logo SVG for core |

Each repository commits its card at
`.github/assets/social-preview/social-preview.png`, and its presentation check
compares it with a fresh render from this file at the pinned standard.

### Website

The website maps its roles to tokens and defines no colors or faces of its own.

| Role | Light | Dark |
| --- | --- | --- |
| `page` | `social-preview-background` | `terminal-surface-dark` |
| `surface` | `terminal-surface` | `terminal-bar-dark` |
| `border` | `terminal-border` | `terminal-border-dark` |
| `text` | `ink` | `ink-dark` |
| `muted` | `social-preview-muted` | `terminal-output-dark` |
| `accent` | `primary` | `primary-dark` |

| Use | Typography |
| --- | --- |
| Headings | `social-preview-title` |
| Body | `social-preview-body` |
| Labels and navigation | `social-preview-owner` |
| Code and terminal | `terminal` |

## Do's and Don'ts

- Do change a value only in the front matter, then regenerate every output
  that reads it.
- Do keep a terminal session short enough to fit GitHub's README column at
  actual size.
- Do select light and dark images with `<picture>` and
  `prefers-color-scheme`.
- Don't restate token values in prose; cite token names.
- Don't ship live text in rendered images; outline it.
- Don't add window buttons, shadows or gradients to terminal windows.
- Don't use `primary` for body text or large fills; it marks what a reader
  acts on.

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
| Core framework logo | `.github/assets/logo/logo.svg` and `.github/assets/logo/logo.png` in agents-tools/core |
