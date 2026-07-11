# Browser Use plugins

The [Browser Use](https://browser-use.com) plugin marketplace for **Claude Code**.

This repo is a catalog of Browser Use plugins for Claude Code. The plugins are self-sufficient: they install the CLI they run through on first use. Support for other hosts (Grok, Codex, …) will be added later.

## Plugins

| Plugin | What it does | How it works |
|---|---|---|
| **browser-use** | Give Claude a real browser — your Chrome or a Browser Use Cloud browser. Use it whenever a task involves a website or web app: browsing, scraping and data extraction, filling forms, testing sites, taking screenshots, automating web workflows. | Thin wrapper around the [Browser Use CLI 3.0](https://github.com/browser-use/browser-use#-cli): installs the CLI if missing, then follows `browser-use skill` — the CLI's own instructions, version-matched to the installed binary, so nothing here drifts from upstream. |
| **qa** | QA-test a website or app and return a 1–5 quality score with evidence. Drives a Browser Use cloud browser and tunnels localhost automatically. Run as `/qa <url-or-localhost-port>`. | Colocated skill ([`qa/`](./qa)); runs through the `browser-harness` CLI and installs it itself if missing. |

## Install

```bash
claude plugin marketplace add browser-use/plugins
claude plugin install browser-use@browser-use      # browser control (CLI self-installs on first use)
claude plugin install qa@browser-use               # adds /qa
```

## Layout

`.claude-plugin/marketplace.json` — the Claude Code catalog. Each plugin is a colocated subdirectory (`source: ./<dir>`).
