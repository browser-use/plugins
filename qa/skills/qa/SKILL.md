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

## Choose a backend (recommended: Browser Use v2 agent)

The test can run two ways — pick one (ask the user if it's unclear; **recommend v2** for real QA):

- **Browser Use v2 cloud agent — recommended, *built for QA*.** Hand the whole test to an autonomous Browser Use agent: it has a **judge** (pass/fail evaluation against expected behavior) and **structured output** (forces the 1–5 score schema), runs server-side, parallelizes, and returns step-by-step evidence with screenshots. **It spends Browser Use credits** (~$0.01/task + ~$0.006/step + $0.02/hr browser, from the account's monthly allowance). Flow: **`references/browser-use-v2.md`**.
- **Claude Code subagent — no task credits, full control.** You (or a spawned subagent) drive **browser-harness** on a cloud browser yourself, following the field-tested loop in **`references/methodology.md`**. Spends no Browser Use *task* credits — just cloud-browser time and your agent's own usage.

Default to **v2** (the judge + structured score is the right tool for scoring); fall back to the Claude subagent when the user would rather not spend credits or wants you driving directly. **Either way, `browser-harness` is required** — it's the key store for v2, and the test driver + localhost tunnel for the Claude path.

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
2. **Run the test with the chosen backend:**
   - **v2 agent** → read **`references/browser-use-v2.md`** and follow it: create the task (with `judge` + a 1–5 `structuredOutput` schema), poll to completion, and read the verdict from `judgeVerdict` + the structured score. A `localhost` target still needs a tunnel (the cloud agent can't reach localhost) — tunnel it per `methodology.md` and pass the public URL as `startUrl`.
   - **Claude subagent** → read **`references/methodology.md`** and follow it exactly: get/resolve the key, tunnel localhost, drive the cloud browser through the test loop with the field-tested gotchas (host-header rewrite, proxy-off, per-tab interstitial header, CORS-pinned APIs).
3. **Tear everything down** (stop the cloud browser so it stops billing; kill the tunnel). The v2 agent's one-off session auto-closes.
4. **Return the verdict**: lead with `Score: N/5`, then task, result, what worked, issues (tagged), edge cases tried, and evidence — using the rubric and output format in `references/methodology.md` (both backends report the same way; for v2, the score/verdict/evidence come from the agent's structured output + `steps`).

Scale effort to the ask: a quick "does X work?" is a few interactions and one score; "thoroughly QA this" warrants more flows and edge cases. Keep the verdict honest, specific, and reproducible.
