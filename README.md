# Browser Use plugins

A marketplace of [Browser Use](https://browser-use.com) plugins for coding agents — drive a real browser, then edit the video of it.

This repo is a thin **index**: it doesn't contain plugin code, it points at each plugin's own repo, pinned to a commit. Each plugin stays the single source of truth in its own repository.

## Plugins

| Plugin | What it does | Source |
|---|---|---|
| **browser-harness** | Direct CDP browser control — coordinate clicks, screenshots, persistent Python session, local Chrome or Browser Use cloud. | [browser-use/browser-harness](https://github.com/browser-use/browser-harness) |
| **video-use** | Edit videos with a coding agent — transcript-driven cuts, color grade, subtitles, self-eval. | [browser-use/video-use](https://github.com/browser-use/video-use) |

Both ship **skills only**. Their CLIs / runtimes are one-time install prerequisites documented inside each plugin.

## Install (Claude Code)

```bash
claude plugin marketplace add browser-use/plugins
claude plugin install browser-harness@browser-use
claude plugin install video-use@browser-use
```

## Layout

- `.grok-plugin/marketplace.json` — xAI Grok catalog format (`source: url` + full `sha`).
- `.claude-plugin/marketplace.json` — Claude Code catalog format (`source: github` + `commit`).

Same plugin list, two host-specific source shapes — mirroring how upstream plugin repos ship parallel `.grok-plugin/` and `.claude-plugin/` directories.

## Status / TODO

- **video-use is temporarily pinned to a fork** (`ShawnPana/video-use@3e7cf02`) while [browser-use/video-use#65](https://github.com/browser-use/video-use/pull/65) (which adds the plugin manifest) is in review. Once it merges, repoint both marketplace files to `browser-use/video-use` at the merge commit.
- Grok note: Grok Build's built-in catalog is `xai-org/plugin-marketplace`; it does not add external marketplaces. This repo is the canonical source of truth and the Claude Code install target. To list in Grok, open per-plugin PRs to `xai-org/plugin-marketplace` pointing at the same repos/SHAs.
