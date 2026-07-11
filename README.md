# Browser Use plugins

The [Browser Use](https://browser-use.com) plugin marketplace for **Claude Code**.

This repo is a catalog of Browser Use plugins for Claude Code. Plugins are colocated here as subdirectories; where a plugin wraps an upstream skill, the source of truth is noted below. Support for other hosts (Grok, Codex, …) will be added later.

## Plugins

| Plugin | What it does | Source of truth |
|---|---|---|
| **browser-use** | Direct browser control via CDP with the [Browser Use CLI 3.0](https://github.com/browser-use/browser-use#-cli) — Claude drives your real Chrome or a Browser Use Cloud Browser through short Python snippets: coordinate clicks, screenshots, navigation, DOM extraction, raw CDP. | [`browser-use/`](./browser-use) (skill mirrored verbatim from [browser-use/browser-use `skills/browser-use`](https://github.com/browser-use/browser-use/tree/main/skills/browser-use)) |
| **qa** | QA-test a website or app and return a 1–5 quality score with evidence. Drives a Browser Use cloud browser and tunnels localhost automatically. Run as `/qa <url-or-localhost-port>`. | [`qa/`](./qa) (colocated) |

**browser-use** ships the skill; the `browser-use` CLI is a one-time install (`uv tool install --python 3.12 --upgrade browser-use`) documented inside the plugin. **qa** runs through the `browser-harness` CLI and installs it itself if missing.

## Install

```bash
claude plugin marketplace add browser-use/plugins
claude plugin install browser-use@browser-use      # CDP browser control (one-time CLI install)
claude plugin install qa@browser-use               # adds /qa
```

## Layout

`.claude-plugin/marketplace.json` — the Claude Code catalog. Each entry is a colocated plugin (`source: ./<dir>`) in a subdirectory of this repo.
