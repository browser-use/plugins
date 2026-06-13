# Browser Use plugins

The [Browser Use](https://browser-use.com) plugin marketplace for **Claude Code**.

This repo is a thin index — it contains no plugin code, just a catalog that points at each plugin's own repo. Support for other hosts (Grok, Codex, …) will be added later.

## Plugins

| Plugin | What it does | Source of truth |
|---|---|---|
| **browser-harness** | Direct CDP browser control — coordinate clicks, screenshots, persistent Python session, local Chrome or Browser Use cloud. | [browser-use/browser-harness](https://github.com/browser-use/browser-harness) |

Ships **skills only**. The `browser-harness` CLI is a one-time install prerequisite documented inside the plugin.

## Install

```bash
claude plugin marketplace add browser-use/plugins
claude plugin install browser-harness@browser-use
```

## Layout

`.claude-plugin/marketplace.json` — the Claude Code catalog. Each entry remote-sources a plugin from its own repo; the source of truth lives there, so there's no drift.
