# browser-use (Browser Use Cloud agent)

Give Claude Code a **hosted Browser Use cloud agent**. Once installed, Claude can spin up a
stealth cloud browser and run **long-horizon web tasks** — browse, extract data, fill forms,
log in, solve CAPTCHAs — driven by the `browser-use-2.0` agent.

No local Chrome, no CLI. It connects to the hosted Browser Use MCP server, so the browser runs
entirely on [Browser Use Cloud](https://browser-use.com) with anti-detection, residential
proxies, and automatic CAPTCHA solving built in.

## Tools this adds

- **`browser_task`** — spin up a cloud browser and run an agent task to completion
- **`monitor_task`** — track a running task's status + step-by-step agent reasoning
- **`list_browser_profiles`** — reuse persistent logins (cookies/sessions) across runs
- **`list_skills` / `execute_skill`** — run fast pre-built workflows without a full browser
- **`get_cookies`** — pull profile cookies for authenticated skills

## Setup

1. Install the plugin:
   ```bash
   claude plugin marketplace add browser-use/plugins
   claude plugin install browser-use@browser-use
   ```
2. Set your API key (get a free one at
   [cloud.browser-use.com](https://cloud.browser-use.com/settings?tab=api-keys&new=1)):
   ```bash
   export BROWSER_USE_API_KEY=bu_...
   ```
3. Ask Claude to do something on the web, e.g.
   *"use browser-use to find the top 5 Show HN posts today and summarize them."*

## No key yet?

Your agent can provision a free account itself — no signup form:

1. `POST https://api.browser-use.com/cloud/signup` → returns a challenge
2. solve the challenge, `POST https://api.browser-use.com/cloud/signup/verify` → returns a `bu_` key
3. set it as `BROWSER_USE_API_KEY`

See the [stealth browsers](https://browser-use.com/stealth-browsers) page and
[docs](https://docs.browser-use.com/cloud/guides/mcp-server) for details.
