# Browser Use plugins

The [Browser Use](https://browser-use.com) plugin marketplace for **Claude Code**.

This repo is a catalog of Browser Use plugins for Claude Code. Most entries remote-source a plugin from its own repo (the source of truth lives there, no drift); some smaller plugins are colocated here as subdirectories. Support for other hosts (Grok, Codex, …) will be added later.

## Plugins

| Plugin | What it does | Source of truth |
|---|---|---|
| **browser-harness** | Direct CDP browser control — coordinate clicks, screenshots, persistent Python session, local Chrome or Browser Use cloud. | [browser-use/browser-harness](https://github.com/browser-use/browser-harness) |
| **qa** | QA-test a website or app and return a 1–5 quality score with evidence. Drives a Browser Use cloud browser and tunnels localhost automatically. Run as `/qa <url-or-localhost-port>`. | [`qa/`](./qa) (colocated; requires browser-harness) |

Both ship **skills only**. The `browser-harness` CLI is a one-time install prerequisite documented inside the plugin; `qa` runs through browser-harness, so install that first.

## Install

```bash
claude plugin marketplace add browser-use/plugins
claude plugin install browser-harness@browser-use
claude plugin install qa@browser-use          # adds /qa
```

## Layout

`.claude-plugin/marketplace.json` — the Claude Code catalog. Each entry is either remote-sourced (`source: { url }`) from a plugin's own repo, or colocated (`source: ./<dir>`) as a subdirectory of this repo.
