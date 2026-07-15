# Browser Use — Cursor Plugin

Gives Cursor's agent a real browser via the Browser Use CLI. Bundles:

- **Skill** (`skills/browser-use/SKILL.md`): teaches the agent to drive Chrome (or a Browser Use Cloud browser) through the `browser-use` CLI — navigation, coordinate clicks, extraction, screenshots, cloud daemons.
- **MCP server** (`mcp.json`): registers `uvx browser-use@latest --cli-mcp`, a self-installing stdio server exposing `browser_exec` and `browser_screenshot` with a persistent Python helper namespace.

Only prerequisite on the user's machine: [uv](https://docs.astral.sh/uv/).

## Install

From the Cursor Marketplace: search for **Browser Use** and install.

For local development, symlink this directory into Cursor's local plugins folder and reload the window:

```bash
ln -s /path/to/plugins/cursor ~/.cursor/plugins/local/browser-use
```

Teams/Enterprise orgs can also import this repo as a team marketplace (Dashboard → Plugins → Team Marketplaces → Add Marketplace → Import from Repo); the root `.cursor-plugin/marketplace.json` points at this directory.

## Layout

```
cursor/
├── .cursor-plugin/plugin.json  # manifest
├── mcp.json                    # bundled MCP server config (stdio, self-installing via uvx)
├── skills/browser-use/SKILL.md # the skill
└── assets/logo.png
```

## Notes

- Local Chrome control requires enabling remote debugging once at `chrome://inspect/#remote-debugging`.
- Cloud browsers need `browser-use auth login` (the skill covers this).
