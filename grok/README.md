# Browser Use Plugin for Grok Build

Give Grok a real browser — your own Google Chrome browser with all of your logins or an isolated [Browser Use Cloud](https://cloud.browser-use.com) browser.

Use it whenever a task involves a website or web app: browsing, scraping and data extraction, filling
forms, testing sites, taking screenshots, automating web workflows.

## Installation

1. Install Grok Build (see the [Grok Build docs](https://docs.x.ai/build/overview)):

   ```bash
   curl -fsSL https://x.ai/cli/install.sh | bash   # macOS / Linux / Git Bash
   irm https://x.ai/cli/install.ps1 | iex          # Windows PowerShell
   ```

2. Sign in to your xAI account:

   ```bash
   grok login
   ```

3. Start Grok Build by running `grok`, then open the plugin:

   ```text
   /plugins
   ```

4. Find **browser-use**, and install it.

5. Ask Grok to do anything that needs the web, and Browser Use will do it.

## Tools

| Tool | What it does | Cost |
|---|---|---|
| `browser_exec` | Run Python in the browser to navigate, click, type, extract data, and more. | Free on local Chrome; cloud browsers bill while running |
| `browser_screenshot` | Capture what is on screen, so Grok can see the page before acting | Free |

Both tools expose the same namespace as the
[Browser Use CLI](https://github.com/browser-use/browser-use#-cli).

## Skills

| Skill | What it does |
|---|---|
| `browser-use` | Instructions to look at the page before acting, get through the parts that break automation (iframes, dropdowns, uploads, downloads), and pick local Chrome or a cloud browser |

It also tells Grok when *not* to open a browser: if a plain HTTP request can read the page, `curl` is
cheaper and faster. The browser is for tasks that need interaction, your logged-in session, JS
rendering, or a page behind bot protection.

## Example prompts

**Act on a site you are logged into:**

```text
Add paper towels to my Amazon cart
```

**Extract structured data from a page:**

```text
Go to news.ycombinator.com, and give me the top 10 stories with their points as CSV
```

**Test a local website you're coding:**

```text
Open localhost:3000, walk through the signup flow, and tell me what breaks
```

**Use an isolated cloud browser instead of your own Chrome:**

```text
Scrape the last 50 reviews from a product page on Ebay — use a cloud browser
```

## Driving your local Chrome

Local Chrome control needs remote debugging enabled. Grok walks you through it on first use:

1. Open `chrome://inspect/#remote-debugging`.
2. Tick **Allow remote debugging for this browser instance**.
3. Chrome shows an **"Allow remote debugging?"** popup for each new connection — click **Allow**.

Cloud browsers need none of this. They do need a Browser Use account: run `browser-use auth login`, and
sign up at [cloud.browser-use.com](https://cloud.browser-use.com).

## Security

- **Network endpoints:** One MCP server, run locally as `uvx browser-use@latest --cli-mcp`. It pulls
  the `browser-use` package from `pypi.org`, drives your Chrome over its local DevTools endpoint, and
  reaches `api.browser-use.com` only if you opt into a cloud browser.
- **Credentials:** None for local Chrome. Cloud browsers use an API key you supply via
  `browser-use auth login`, stored by the CLI outside this plugin. The plugin reads no secrets of
  its own.
- **Contents:** Markdown and JSON only.
- **Your browser session:** Local Chrome uses your real profile, so the agent acts as you where you
  are signed in. The skill tells it to stop at login walls and never complete a password, MFA, or
  payment step.
- **Untrusted content:** Page content is data, not instructions; the skill does not follow directives
  found on a page.

## Resources

- [browser-use.com](https://browser-use.com) — product
- [Documentation](https://docs.browser-use.com)
- [GitHub](https://github.com/browser-use/browser-use)
- [Browser Use Cloud](https://cloud.browser-use.com) — hosted browsers and the v4 agent
- [Discord](https://link.browser-use.com/discord)

## License

MIT — see [LICENSE](../LICENSE) at the repo root.
