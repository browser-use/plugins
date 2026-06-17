# Browser Use plugins

The [Browser Use](https://browser-use.com) plugin marketplace for **Claude Code**.

This repo is a catalog of Browser Use plugins for Claude Code. Most entries remote-source a plugin from its own repo (the source of truth lives there, no drift); some smaller plugins are colocated here as subdirectories. Support for other hosts (Grok, Codex, …) will be added later.

## Plugins

| Plugin | What it does | Source of truth |
|---|---|---|
| **browser-use** | Give Claude Code a hosted Browser Use cloud agent — spin up a stealth cloud browser and run long-horizon web tasks (browse, extract, fill forms, log in, solve CAPTCHAs) with the `browser-use-2.0` agent. No local Chrome or CLI; set `BROWSER_USE_API_KEY` (free). | [`browser-use/`](./browser-use) (colocated; hosted MCP) |
| **browser-harness** | Direct CDP browser control — coordinate clicks, screenshots, persistent Python session, local Chrome or Browser Use cloud. | [browser-use/browser-harness](https://github.com/browser-use/browser-harness) |
| **qa** | QA-test a website or app and return a 1–5 quality score with evidence. Drives a Browser Use cloud browser and tunnels localhost automatically. Run as `/qa <url-or-localhost-port>`. | [`qa/`](./qa) (colocated; requires browser-harness) |

**browser-use** is the zero-prerequisite cloud agent (just needs an API key). **browser-harness** and **qa** ship skills that run through the `browser-harness` CLI — a one-time install documented inside the plugin; install that first for those two.

## Install

```bash
claude plugin marketplace add browser-use/plugins
claude plugin install browser-use@browser-use      # hosted cloud agent (set BROWSER_USE_API_KEY)
claude plugin install browser-harness@browser-use
claude plugin install qa@browser-use               # adds /qa
```

## Layout

`.claude-plugin/marketplace.json` — the Claude Code catalog. Each entry is either remote-sourced (`source: { url }`) from a plugin's own repo, or colocated (`source: ./<dir>`) as a subdirectory of this repo.
