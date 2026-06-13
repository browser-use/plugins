# video-use — one-time install prerequisite

This is a **one-time prerequisite**, not part of the regular AI workflow. Do it once; after that, just drop footage in a folder and start editing.

## Install

```bash
git clone https://github.com/browser-use/video-use ~/Developer/video-use
cd ~/Developer/video-use
uv sync                         # or: pip install -e .
brew install ffmpeg             # required
brew install yt-dlp             # optional, for downloading online sources
cp .env.example .env
$EDITOR .env                    # ELEVENLABS_API_KEY=...  (grab one at elevenlabs.io/app/settings/api-keys)
```

Optionally register the skill with your agent so it auto-loads:

```bash
ln -sfn ~/Developer/video-use ~/.claude/skills/video-use   # Claude Code
# ln -sfn ~/Developer/video-use ~/.codex/skills/video-use  # Codex
```

That clone is the "checkout" the skill refers to — its root `SKILL.md` holds the production rules and `helpers/` holds the editing scripts.

## Use

Point your agent at a folder of raw takes and ask, e.g. "edit these into a launch video." It inventories the sources, proposes a strategy, waits for your OK, then produces `edit/final.mp4` next to your sources.
