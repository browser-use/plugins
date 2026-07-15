# Browser Use plugin for Kimi Code CLI

Give [Kimi Code CLI](https://github.com/MoonshotAI/kimi-code) a real browser — your Chrome or a [Browser Use Cloud](https://cloud.browser-use.com) browser — powered by the [Browser Use CLI 3.0](https://github.com/browser-use/browser-use#-cli).

## Install

Inside the Kimi Code TUI:

```text
/plugins install https://github.com/browser-use/plugins
/reload
```

Requires [uv](https://docs.astral.sh/uv/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`). Then just ask Kimi to do something on the web, e.g. *"open Hacker News and summarize the top 5 Show HN posts."* For local Chrome control, allow remote debugging when Chrome prompts (`chrome://inspect/#remote-debugging` → "Allow remote debugging for this browser instance"). Cloud browsers are optional and authenticate via `browser-use auth login` or `BROWSER_USE_API_KEY`.

## How it works

Kimi Code resolves the plugin manifest from `.kimi-plugin/plugin.json` at the repo root, which declares two surfaces:

- **MCP server** — launches `uvx --python 3.12 browser-use@latest --cli-mcp`; uv fetches the latest stable release from PyPI on first use and re-resolves the version on each session start. The server exposes the CLI 3.0 surface: **`browser_exec`** (drive the browser with Python — clicks, navigation, DOM extraction, raw CDP) and **`browser_screenshot`**, and ships its full usage instructions as native MCP server instructions, version-matched to the running release.
- **Skill** — `skills/browser-use/SKILL.md` teaches direct `browser-use` CLI usage (heredoc exec in a shell) for sessions where the MCP server is disabled or a shell workflow is preferred.

The skill text is adapted from `browser-use skill` output (`browser_use/skills/browser-use/SKILL.md` in the main repo); keep them in sync when the upstream skill changes.
