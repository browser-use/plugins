# browser-use (Browser Use CLI 3.0)

Give Claude Code **direct browser control via CDP** through the
[Browser Use CLI 3.0](https://github.com/browser-use/browser-use#-cli). Claude drives your
real Chrome — or a Browser Use cloud browser — with short Python snippets: coordinate clicks,
screenshots, navigation, DOM extraction, raw CDP.

This plugin ships the `browser-use` skill from the
[browser-use library](https://github.com/browser-use/browser-use/blob/main/skills/browser-use/SKILL.md)
(the source of truth — the skill here is a verbatim copy of `skills/browser-use/SKILL.md` on `main`).
The CLI itself is a separate one-time install.

## How it works

```bash
browser-use <<'PY'
new_tab("https://example.com")
print(page_info())
PY
```

The CLI lets Claude control the browser via Python and manages the browser (a background
daemon attached to Chrome's CDP endpoint) for you.

## Setup

1. Install the plugin:
   ```bash
   claude plugin marketplace add browser-use/plugins
   claude plugin install browser-use@browser-use
   ```
2. Install the CLI (one-time):
   ```bash
   uv tool install --python 3.12 --upgrade browser-use
   ```
3. Allow Chrome remote debugging when prompted — the harness opens
   `chrome://inspect/#remote-debugging`; tick **"Allow remote debugging for this browser
   instance"** and click **Allow** on the popup.
4. Ask Claude to do something on the web, e.g.
   *"open Hacker News and summarize the top 5 Show HN posts."*

If anything fails, `browser-use --doctor` diagnoses the connection; setup details live in the
[install docs](https://github.com/browser-use/browser-harness/blob/main/install.md).

## Cloud browsers (optional)

Local Chrome needs no API key. For headless servers, parallel sub-agents, or isolated work,
the skill can start a [Browser Use cloud](https://cloud.browser-use.com) browser instead —
authenticate once with `browser-use auth login` (or set `BROWSER_USE_API_KEY`).
