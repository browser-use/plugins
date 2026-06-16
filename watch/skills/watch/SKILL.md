---
name: watch
description: Monitor the user's Chrome in real time — network requests, console logs/errors, and user actions (clicks, form changes, navigations) — plus a dense screen recording. Use when the user wants you to "watch", "monitor", or "keep an eye on" their browser so you can later answer what happened ("what was that error?", "did the upload finish?", "why did checkout fail?"). You keep watching across turns and decide when to stop — when the user asks about what happened, stop, review, and answer.
---

# watch

Watch the user's Chrome so you can later tell them exactly what happened. You run a background monitor that records **two streams**:

- **Timeline** (`timeline.jsonl`) — your primary signal: network requests/responses, console logs + exceptions, and user actions (clicks, form `change`s with field identity + value *length* only, submits, navigations). This is *what* happened, timestamped.
- **Frames** (`frames/<epoch_ms>.png`) — a dense ~2.5 fps recording. This is *how it looked*. You consult it on demand by reading the frames around a timestamp — don't load the whole thing.

Captures **only Chrome** (the page's own CDP stream), needs **no screen-recording permission**, and is **not a daemon** — you start it and you stop it, within this session. Requires the `browser-harness` CLI on PATH (verify with `command -v browser-harness`; if missing, tell the user to install it — see https://github.com/browser-use/browser-harness).

## Start watching

When asked to watch/monitor, spawn the monitor **in the background** and confirm, then go quiet — it accumulates on its own while you're idle between turns.

```bash
MON="<absolute path to monitor.py next to this SKILL.md>"   # e.g. ${CLAUDE_PLUGIN_ROOT}/skills/watch/monitor.py
WATCH_DIR="/tmp/watch-$(date +%s)"; mkdir -p "$WATCH_DIR"
echo "$WATCH_DIR" > /tmp/watch-current        # so you can find it next turn
WATCH_DIR="$WATCH_DIR" browser-harness < "$MON"   # run this with run_in_background
```

Use the real absolute path to `monitor.py` in this skill's directory (you know where this SKILL.md lives; under a plugin it's `${CLAUDE_PLUGIN_ROOT}/skills/watch/monitor.py`). Run that last line as a **background** command. Tell the user: "Watching your Chrome — go do your thing, then ask me what happened." Do **not** poll or screenshot yourself between turns; the monitor handles it.

## When the user asks what happened

You decide this is the cue to stop (a question about what occurred = stop, review, answer). Then:

1. **Stop the monitor** cleanly: `touch "$(cat /tmp/watch-current)/STOP"` and give it ~1s to flush.
2. **Read the FULL structured timeline first — this is the authoritative record, the frames are not.** Always reconstruct from the complete event stream before looking at a single image:
   - **Every action** (`action` kind): clicks, typing, keys, scrolls, submits — the whole list, chronological, not a filtered subset.
   - **Every navigation** (`watch.tab` + `action.k=="nav"`): the tab/URL trail. **Searches and direct URL visits live here, not in actions** — a Google/address-bar search shows up only as a navigation whose URL holds the `q=` query (page listeners can't see omnibox typing). If you skip navigations you will miss searches and page-to-page movement.
   - **Network** (`net` / `net.fail`): statuses, failures, the API calls behind each step.
   ```bash
   D="$(cat /tmp/watch-current)"
   # full action + navigation trail, chronological — read ALL of it, don't pre-filter to a keyword
   python3 -c "
   import json,datetime
   for l in open('$D/timeline.jsonl'):
       e=json.loads(l); k=e['kind']; d=e['data']
       if k not in ('action','watch.tab'): continue
       ts=datetime.datetime.fromtimestamp(e['t']).strftime('%H:%M:%S')
       if k=='watch.tab': print(f'[{ts}] TAB  {d[\"url\"]}')
       else: print(f'[{ts}] {d.get(\"k\"):7} {d.get(\"target\",\"\")[:40]} {d.get(\"text\") or d.get(\"to\") or d.get(\"value\") or d.get(\"key\") or d.get(\"y\",\"\")}')
   "
   # network errors / notable statuses
   grep -E '"net.fail"|"status": [45][0-9][0-9]' "$D/timeline.jsonl"
   ```
   Build the answer from this complete picture. Each line has `t` (epoch seconds) → your index into the frames.
3. **Then use the images as extra help** — only for the few moments where a line needs visual detail (what a page/error/post actually looked like). List frames whose `<epoch_ms>` falls in `[t-3s, t+3s]` and `Read` that slice. Frames are supplementary confirmation, never the primary source, and never the whole `frames/` dir.
   ```bash
   T=<event epoch seconds>; lo=$(( (T-3)*1000 )); hi=$(( (T+3)*1000 ))
   for f in "$D"/frames/*.jpg; do n=$(basename "$f" .jpg); [ "$n" -ge "$lo" ] && [ "$n" -le "$hi" ] && echo "$f"; done
   ```
4. **Answer from the full timeline, backed by frames where useful** — include the navigation/search trail, e.g. "…then you searched Google for **shawn pan poop**, opened the first result, and `POST /api/x` returned **500** (frame `…188.jpg` shows the red toast)." Don't report only the in-page clicks; the searches and tab moves are part of "what I did."

Optional — if the user wants to watch it themselves, assemble an mp4 from the frame slice with ffmpeg (`ffmpeg -pattern_type glob -i '…/frames/*.jpg' clip.mp4`).

## Notes

- **Granular by design:** the recording is dense so playback shows motion (spinner → toast → redirect), but you only ever *read* the slice the question needs — the timeline tells you where to look.
- **Privacy:** raw keystrokes and input values are **not** captured — only field identity + value length, and password fields are redacted. Say so if the user asks.
- **Cleanup:** after answering, the monitor is already stopped (STOP sentinel). The session dir under `/tmp/watch-*` holds the frames/timeline until you or the user removes it.
- If the user says "keep watching" or asks something mid-stream, you may answer from the timeline without stopping — only stop when the episode is clearly over.
