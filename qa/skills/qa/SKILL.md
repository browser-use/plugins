---
name: qa
description: QA-test a website or web app and return a 1-5 quality score (5 = flawless, 1 = broken) with evidence. Use when the user wants to test, QA, evaluate, score, or "check how good" a site, page, flow, or app — including a local dev server (e.g. "qa test localhost:5173", "does the checkout work?", "rate this landing page"). Drives a real Browser Use cloud browser, tunneling localhost automatically.
---

# QA

Drive a website with a real browser, judge how well it does the thing the user asked about, and return a **score from 1 (broken) to 5 (excellent)** with evidence. The deliverable is a verdict, not a screenshot dump.

## Inputs

From the user's invocation (the text after `/qa`, or their message):
- **Target** — a URL (`https://…`) or a local dev server (`localhost:5173`, `:3000`, "the app on 5173"). **Required** — if absent, ask for it before doing anything else.
- **What to test** (optional) — a flow or focus ("the signup", "search + filters"). If omitted, test the most obvious happy path and say so in the report.

## Single flow vs. fan-out (decide this first)

**Scale the approach to the ask:**

- **Testing one flow / one thing?** Don't bother with subagents — **drive `browser-harness` directly** yourself, following `references/methodology.md`. That's the right, lowest-overhead tool for a single test, and it's how the rest of this skill works.
- **Testing many flows / a lot at once?** **Fan out to subagents — one per flow — so they run in parallel.** Here the user has a choice of subagent type (ask if unclear; **recommend v2**):
  - **Browser Use v2 cloud agents — recommended.** Each flow becomes an autonomous v2 task with **`judge`** (pass/fail) + **`structuredOutput`** (1–5 score), running server-side and **in parallel**, returning step-by-step screenshot evidence. **Spends Browser Use credits** (~$0.01/task + ~$0.006/step + $0.02/hr browser). Per-task flow + how to fan out: `references/browser-use-v2.md`.
  - **Your harness's built-in subagents** — spawn Claude Code subagents (the Agent tool), each driving `browser-harness` through `references/methodology.md`. No Browser Use *task* credits; uses your agent's own usage.

Rule of thumb: **one flow → browser-harness directly; many flows → subagents (v2 recommended).** Either way `browser-harness` is required — as the direct driver, the subagent driver, the v2 key store, and the localhost tunnel.

## Dependency: browser-harness (required)

This skill runs the test through **browser-harness** — a separate plugin + CLI. It is not optional; QA must run on a real Browser Use cloud browser, never the user's local Chrome.

**Before anything else, verify it's available:**

```bash
command -v browser-harness && browser-harness <<'PY'
print("browser-harness OK")
PY
```

If `browser-harness` is **not** on `PATH`, stop and tell the user to install it, then resume:
- Plugin: install the `browser-harness` plugin for your agent — `claude plugin install browser-harness@browser-use` (Claude Code) or `codex plugin add browser-harness@browser-use` (Codex)
- CLI (one-time): see the browser-harness skill's `references/install.md` (it's a `uv`/pip install of the `browser-harness` package). Repo: https://github.com/browser-use/browser-harness

Do not attempt to QA with anything other than browser-harness + a cloud browser.

## Procedure

1. **Confirm the target is reachable** (`curl -s -o /dev/null -w "%{http_code}" <url>`), and identify what the app is (title, README) so you can frame a sensible test task.
2. **Run it, scaled to the ask** (see "Single flow vs. fan-out" above):
   - **One flow** → drive **browser-harness directly** per `references/methodology.md`: resolve the key, tunnel localhost, and run the test loop with the field-tested gotchas (host-header rewrite, proxy-off, per-tab interstitial header, CORS-pinned APIs).
   - **Many flows → fan out, one subagent per flow:**
     - **v2 agents (recommended)** → per `references/browser-use-v2.md`, create one task per flow (each with `judge` + a 1–5 `structuredOutput` schema), poll them all, and collect the verdicts. A `localhost` target still needs a tunnel (the cloud agent can't reach localhost) — tunnel it and pass the public `startUrl`.
     - **Claude subagents** → spawn one Agent per flow, each following `references/methodology.md` on browser-harness.
3. **Tear down** what you started — only the **one-flow / Claude** paths have anything to stop (cloud browser + tunnel). A v2 task on a public URL has nothing to tear down (its one-off session auto-closes).
4. **Return the verdict**: lead with `Score: N/5`, then task, result, what worked, issues (tagged), edge cases, and evidence — per the rubric and output format in `references/methodology.md`. **Fanning out?** Give a per-flow `Score: N/5` line and an **overall score that reflects the weakest critical path** (don't average a broken flow up because others passed).

Scale effort to the ask: a quick "does X work?" is a few interactions and one score; "thoroughly QA this" warrants more flows and edge cases. Keep the verdict honest, specific, and reproducible.
