# browser-use

Give Claude Code a real browser — your Chrome or a [Browser Use Cloud](https://cloud.browser-use.com) browser — powered by the [Browser Use CLI 3.0](https://github.com/browser-use/browser-use#-cli).

## How it works

The plugin registers the Browser Use MCP server, self-installing and always current:

- `.mcp.json` launches `uvx browser-use@latest --cli-mcp` — uv fetches the latest stable release from PyPI on first use (the CLI bundles [browser-harness](https://github.com/browser-use/browser-harness) as a pinned dependency, so that's everything) and re-resolves the version on each session start.
- The server exposes the CLI 3.0 surface: **`browser_exec`** (drive the browser with Python — clicks, navigation, DOM extraction, raw CDP) and **`browser_screenshot`**, and ships its full usage instructions as native MCP server instructions, version-matched to the running release.

There is nothing here to sync when the library changes: no code, no skill text — just the launch config.

## Install

```bash
claude plugin marketplace add browser-use/plugins
claude plugin install browser-use@browser-use
```

Requires [uv](https://docs.astral.sh/uv/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`). Then just ask Claude to do something on the web, e.g. *"open Hacker News and summarize the top 5 Show HN posts."* For local Chrome control, allow remote debugging when Chrome prompts (`chrome://inspect/#remote-debugging` → "Allow remote debugging for this browser instance"). Cloud browsers are optional and authenticate via `browser-use auth login` or `BROWSER_USE_API_KEY`.
