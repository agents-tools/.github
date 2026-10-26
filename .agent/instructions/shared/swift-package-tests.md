---
description: Keep agents-tools and skill-cli package tests isolated from the machine's agent and Git configuration.
---
## Test Isolation

- Run tests with an isolated `HOME` and with `CODEX_HOME`, `CLAUDE_CONFIG_DIR`
  and the `XDG_*` variables unset; never inherit agent or Git configuration.
- Create Git fixtures with an explicit initial branch, and remove every
  fixture and temporary directory a test creates.
