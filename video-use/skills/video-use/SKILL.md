---
name: video-use
description: Edit any video by conversation. Transcribe, cut, color grade, generate overlay animations, burn subtitles — for talking heads, montages, tutorials, travel, interviews. No presets, no menus. Ask questions, confirm the plan, execute, iterate, persist. Production-correctness rules are hard; everything else is artistic freedom. Requires the one-time video-use install (see references/install.md).
---

# video-use

Edit videos with a coding agent. The LLM never watches the video — it *reads* it: a packed word-level transcript (`takes_packed.md`) is the primary surface, and a filmstrip + waveform PNG is rendered only at decision points. Cuts come from speech boundaries and silence, never frame-dumping.

## Prerequisite (one-time — NOT part of the AI workflow)

This skill is instructions only. video-use needs the repo cloned plus `ffmpeg` and an ElevenLabs API key. If `ffmpeg` or the cloned repo aren't present, do the one-time setup in [references/install.md](references/install.md) first. Installing clones the full `video-use` repo (the "checkout" below) and registers its skill.

## The full skill and scripts live in your video-use checkout

The authoritative production rules, the editing craft, and the pipeline are in the checkout's root **`SKILL.md`** — read it and follow it exactly. The editing scripts (`transcribe.py`, `render.py`, `timeline_view.py`, …) are in the checkout's **`helpers/`** — always read them before running; that's where the real logic lives. Animation overlays are covered by the checkout's `skills/manim-video/` skill.

## The loop

Ask → confirm the strategy → execute → self-eval the rendered output at every cut boundary → persist session memory in `project.md`. Never touch the cut without strategy approval. All outputs live in `/edit/` next to the user's sources; the skill directory stays clean.
