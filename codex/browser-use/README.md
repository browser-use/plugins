# browser-use (Codex plugin)

Give [Codex](https://developers.openai.com/codex) a **hosted Browser Use cloud agent**. Codex
can spin up a stealth cloud browser and run **long-horizon web tasks** — browse, extract data,
fill forms, log in, solve CAPTCHAs — driven by the `browser-use-2.0` agent.

No local Chrome, no CLI. It connects to the hosted Browser Use MCP, so the browser runs on
[Browser Use Cloud](https://browser-use.com) with anti-detection, residential proxies, and
automatic CAPTCHA solving built in.

## Install

```bash
codex plugin marketplace add browser-use/plugins
codex plugin add browser-use@browser-use
```

The plugin's marketplace entry uses `"authentication": "ON_INSTALL"`, so Codex prompts for your
Browser Use API key at install. Get a free key at
[cloud.browser-use.com](https://cloud.browser-use.com/settings?tab=api-keys&new=1). The key is
sent as the `x-browser-use-api-key` header (via `env_http_headers` → `BROWSER_USE_API_KEY`).

## Tools

- `browser_task` — spin up a cloud browser and run an agent task to completion
- `monitor_task` — track a running task's status + step-by-step agent reasoning
- `list_browser_profiles` — reuse persistent logins (cookies/sessions) across runs
- `list_skills` / `execute_skill` — run fast pre-built workflows without a full browser
- `get_cookies` — pull profile cookies for authenticated skills

## Layout

```
codex/browser-use/
├── .codex-plugin/plugin.json   # manifest → points at .mcp.json
├── .mcp.json                   # hosted Browser Use MCP (url + env_http_headers)
└── README.md
```

The Codex catalog entry lives in [`.agents/plugins/marketplace.json`](../../.agents/plugins/marketplace.json) at the repo root.
