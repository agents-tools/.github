# Changelog

## Unreleased

- Check social previews and organization profiles with the TypeScript
  toolchain. DESIGN front matter carries the social preview and profile
  tokens, the profile workflow validates the catalog, and this repository
  commits its own social preview.
- Choose presentation checks from each caller's catalog `kind`: tools check
  their terminal and social preview; libraries, apps, distributions and
  `.github` check their social preview; website callers fail. Regenerated
  files upload as `presentation.tar` in the `presentation` artifact, laid out
  like the asset root.
- Add the reusable `profile.yml` for the public profile and member dashboards.
- Compare every catalog `about` with the live repository description in the
  public and online checks.
- Remove the terminal presentation fixture from this repository's CI; a tool's
  run at the candidate commit proves the tool path before pins roll.

Upgrading from 0.1.0:

- Add `kind`, `title` and the verbatim `about` to each catalog repository, and
  `about` to `organization`.
- Commit each member's card at
  `.github/assets/social-preview/social-preview.png`, rendered as described in
  `README.md`. Tools keep `.github/assets/terminal/` and pass both executable
  inputs; other kinds call `presentation.yml` without them; websites do not
  call it.
- Member dashboards call `profile.yml` with `mode: member` from a job named
  `check`, drop `catalog` from `profile/member.json` and remove their vendored
  renderer. Their required context becomes `check / profile` after it appears
  on a real run.
- Replace `Scripts/render-profile.py`, the vendored renderers and recipes with
  the toolchain commands in `README.md`.

## 0.1.0

- Define shared maintenance, compatibility, versioning and release policy for
  the agents family.
- Provide reusable policy, Swift package CI and presentation workflows with
  caller contexts `policy / policy`, `validate / swift-package` and
  `presentation / presentation`.
- Publish the family DESIGN in Google's DESIGN.md format, with visual tokens,
  an app icon entry and framework logo entries.
- Supply default community files and issue and pull-request templates.
- Generate the organization profile from its catalog with the shared renderer.
- Include repository settings declarations and read-only profile, settings and
  policy checks.
