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

## Dependency: browser-harness (required)

This skill runs the test through **browser-harness** — a separate plugin + CLI. It is not optional; QA must run on a real Browser Use cloud browser, never the user's local Chrome.

**Before anything else, verify it's available:**

```bash
command -v browser-harness && browser-harness <<'PY'
print("browser-harness OK")
PY
```

If `browser-harness` is **not** on `PATH`, stop and tell the user to install it, then resume:
- Plugin: `claude plugin install browser-harness@browser-use`
- CLI (one-time): see the browser-harness skill's `references/install.md` (it's a `uv`/pip install of the `browser-harness` package). Repo: https://github.com/browser-use/browser-harness

Do not attempt to QA with anything other than browser-harness + a cloud browser.

## Procedure

1. **Confirm the target is reachable** (`curl -s -o /dev/null -w "%{http_code}" <url>`), and identify what the app is (title, README) so you can frame a sensible test task.
2. **Read `references/methodology.md`** in this skill directory and follow it exactly. It defines: how to get a Browser Use API key (or self-sign-up), how to tunnel a localhost app and point a cloud browser at it, the field-tested gotchas (host-header rewrite, proxy-off, the per-tab interstitial header, CORS-pinned APIs), the test loop, the 1-5 rubric, and the output format.
3. **Run the test**, then **tear everything down** (stop the cloud browser so it stops billing; kill the tunnel).
4. **Return the verdict**: lead with `Score: N/5`, then task, result, what worked, issues (tagged), edge cases tried, and screenshot evidence — exactly as `references/methodology.md` specifies.

Scale effort to the ask: a quick "does X work?" is a few interactions and one score; "thoroughly QA this" warrants more flows and edge cases. Keep the verdict honest, specific, and reproducible.
