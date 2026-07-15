# Browser Use plugins

The [Browser Use](https://browser-use.com) plugin marketplace for **Claude Code** and **Kimi Code**.

This repo is a catalog of Browser Use plugins for Claude Code, and doubles as the Browser Use plugin for Kimi Code CLI (see [`.kimi-plugin/`](./.kimi-plugin)). The plugins are self-sufficient: they install the CLI they run through on first use. Support for other hosts (Grok, Codex, …) will be added later.

## Plugins

| Plugin | What it does | How it works |
|---|---|---|
| **browser-use** | Give Claude a real browser — your Chrome or a Browser Use Cloud browser. Use it whenever a task involves a website or web app: browsing, scraping and data extraction, filling forms, testing sites, taking screenshots, automating web workflows. | MCP server (`uvx browser-use@latest --cli-mcp`) exposing the [Browser Use CLI 3.0](https://github.com/browser-use/browser-use#-cli) surface: `browser_exec` + `browser_screenshot`, with usage instructions served by the release itself — self-installing via uv, always current, nothing here to sync. |
| **qa** | QA-test a website or app and return a 1–5 quality score with evidence. Drives a Browser Use cloud browser and tunnels localhost automatically. Run as `/qa <url-or-localhost-port>`. | Colocated skill ([`qa/`](./qa)); runs through the `browser-harness` CLI and installs it itself if missing. |

## Install

Claude Code:

```bash
claude plugin marketplace add browser-use/plugins
claude plugin install browser-use@browser-use      # browser control (MCP server, self-installs via uvx)
claude plugin install qa@browser-use               # adds /qa
```

Kimi Code (inside the TUI):

```text
/plugins install https://github.com/browser-use/plugins
/reload
```

## Layout

`.claude-plugin/marketplace.json` — the Claude Code catalog. Each plugin is a colocated subdirectory (`source: ./<dir>`).

`.kimi-plugin/plugin.json` — the Kimi Code plugin manifest (Kimi installs one plugin per repo, resolved from the repo root). Declares the same `uvx --python 3.12 browser-use@latest --cli-mcp` MCP server plus a skill at [`.kimi-plugin/skills/browser-use/`](./.kimi-plugin/skills/browser-use).
