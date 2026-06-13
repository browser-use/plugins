# Browser Use plugins

A self-contained marketplace of [Browser Use](https://browser-use.com) plugins for coding agents — drive a real browser, then edit the video of it.

Everything is managed in **this** repo. Each plugin is vendored here as a local-source directory; the plugins are thin skills that point at a one-time CLI/tool install. No changes to the upstream tool repos are required.

## Plugins

| Plugin | What it does | Upstream tool |
|---|---|---|
| **browser-harness** | Direct CDP browser control — coordinate clicks, screenshots, persistent Python session, local Chrome or Browser Use cloud. | [browser-use/browser-harness](https://github.com/browser-use/browser-harness) |
| **video-use** | Edit videos with a coding agent — transcript-driven cuts, color grade, subtitles, self-eval. | [browser-use/video-use](https://github.com/browser-use/video-use) |

Both ship **skills only**. The actual CLI/tool is a one-time install prerequisite documented in each plugin's `skills/<name>/references/install.md`; the skill then points at that install for its deeper docs and scripts.

## Install (Claude Code)

```bash
claude plugin marketplace add browser-use/plugins
claude plugin install browser-harness@browser-use
claude plugin install video-use@browser-use
```

## Layout

```
browser-harness/   vendored plugin (manifest + skill + install prereq)
video-use/         vendored plugin (manifest + skill + install prereq)
.claude-plugin/marketplace.json   Claude Code catalog (local sources "./browser-harness", "./video-use")
.grok-plugin/marketplace.json     xAI Grok catalog (local sources {type:local, path})
```

Two host-specific catalog files point at the same vendored directories — mirroring how upstream plugin repos ship parallel `.grok-plugin/` and `.claude-plugin/` dirs.

## Notes

- **Self-contained by design.** The skills are thin: they describe the tool, give the one-time install, and then reference the user's local checkout for heavy content (browser-harness's `interaction-skills/`, video-use's `helpers/`). So this repo never vendors that fast-moving code and never needs to re-sync it.
- **Grok:** Grok Build's built-in catalog is `xai-org/plugin-marketplace`; it does not add external marketplaces. This repo is the canonical source of truth and the Claude Code install target. To list in Grok, open per-plugin PRs to `xai-org/plugin-marketplace`.
