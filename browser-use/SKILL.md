---
name: browser-use
description: "Direct browser control via CDP for web interaction: automation, scraping, testing, screenshots, and site/app work."
---

# Browser Use

The `browser-use` CLI carries its own instructions, version-matched to the installed binary — the CLI is the source of truth, not this file. Run this once now and follow what it prints for the rest of the task:

```bash
browser-use skill
```

**Only if that fails because `browser-use` is not installed**, install it and retry (one-time, ~30s — don't make the user do it):

```bash
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh   # uv installer, only if missing
export PATH="$HOME/.local/bin:$PATH"
uv tool install --python 3.12 --upgrade browser-use                           # latest stable release from PyPI
browser-use skill
```

## If something goes wrong

- A later call can't find `browser-use` (fresh shells don't inherit the `export` above): prefix it with `export PATH="$HOME/.local/bin:$PATH"` or invoke `~/.local/bin/browser-use` directly.
- The CLI runs but can't reach a browser: run `browser-use --doctor` and follow its output.
- The install or `browser-use skill` itself fails: read https://github.com/browser-use/browser-use (the README's CLI section and `skills/browser-use/SKILL.md`) and https://github.com/browser-use/browser-harness/blob/main/install.md to diagnose and fix the setup yourself.
