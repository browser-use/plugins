# browser-use

Give Claude Code a real browser — your Chrome or a [Browser Use Cloud](https://cloud.browser-use.com) browser — powered by the [Browser Use CLI 3.0](https://github.com/browser-use/browser-use#-cli).

## How it works

The plugin is a thin, self-sufficient wrapper around the CLI:

1. The skill triggers on any web/browser task.
2. If the `browser-use` CLI isn't installed, Claude installs it (one `uv tool install`; the CLI bundles [browser-harness](https://github.com/browser-use/browser-harness) as a pinned dependency, so that's everything).
3. Claude runs `browser-use skill`, which prints the CLI's own usage instructions — always version-matched to the installed binary — and follows them.

Because the instructions live in the CLI rather than in this repo, there is nothing here to sync when the library changes: `SKILL.md` is a ~15-line bootstrap that never drifts.

## Install

```bash
claude plugin marketplace add browser-use/plugins
claude plugin install browser-use@browser-use
```

Then just ask Claude to do something on the web, e.g. *"open Hacker News and summarize the top 5 Show HN posts."* No other setup — the CLI installs itself on first use. For local Chrome control, allow remote debugging when Chrome prompts (`chrome://inspect/#remote-debugging` → "Allow remote debugging for this browser instance"). Cloud browsers are optional and authenticate via `browser-use auth login` or `BROWSER_USE_API_KEY`.
