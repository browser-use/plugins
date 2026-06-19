# Browser Use v2 agent backend (recommended for QA)

Run the QA test as an autonomous **Browser Use cloud agent** instead of driving browser-harness
step by step. It's purpose-built for QA: a **judge** evaluates pass/fail against expected
behavior, and **structured output** forces the 1–5 score. It runs server-side, parallelizes, and
returns step-by-step evidence (screenshots + actions).

**Cost / credits:** the v2 agent spends Browser Use credits — about **$0.01 per task + ~$0.006 per
step (LLM) + $0.02/hr browser**, drawn from the account's monthly allowance. (The Claude-subagent
backend in `methodology.md` spends no Browser Use *task* credits.) Recommend v2 for real QA; fall
back to the Claude subagent to avoid credits.

> Note: the docs label the v2 API "legacy" and steer new projects to v3 — but the **`judge` +
> structured-output** evaluation features QA needs live on v2 (`POST /api/v2/tasks`), so that's
> what this backend uses.

## The endpoints

- **Create:** `POST https://api.browser-use.com/api/v2/tasks` → `202 {id, sessionId}`
- **Poll:** `GET https://api.browser-use.com/api/v2/tasks/{id}` → `status` ∈ `created → started →
  finished | failed | stopped`, plus `output`, `judgeVerdict`, `judgement`, `steps[]`, `cost`.
- Auth header on both: `X-Browser-Use-API-Key`.

## Key resolution — via browser-harness (it stores the key)

The v2 API authenticates with `BROWSER_USE_API_KEY` — the same key `methodology.md` step 0 resolves
(browser-harness's `.env`, the process env, or self-signup). The cleanest way to use
*browser-harness's stored key* is to run the calls **inside a `browser-harness` heredoc**, where
the key is already loaded into `os.environ` — no separate plumbing, no re-exporting. (Plain `curl`
with `$BROWSER_USE_API_KEY` also works if it's exported. The v2 task itself runs on a Browser Use
cloud browser, so no local Chrome is needed for the test — browser-harness here is just the key
store + HTTP runtime.)

## Flow: create → poll → report

Fill in `task`, `startUrl` (the public URL — tunnel a localhost target first), and
`judgeGroundTruth` (what success looks like), then run:

```bash
browser-harness <<'PY'
import os, json, time, urllib.request, urllib.error
KEY = os.environ.get("BROWSER_USE_API_KEY")
assert KEY, "no BROWSER_USE_API_KEY — resolve it per methodology.md step 0"
BASE = "https://api.browser-use.com/api/v2"

def call(method, path, body=None):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(body).encode() if body is not None else None,
        method=method,
        headers={"X-Browser-Use-API-Key": KEY, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"v2 API {e.code}: {e.read().decode()[:300]}")

# 1-5 score schema (structuredOutput must be a *stringified* JSON schema)
SCORE_SCHEMA = json.dumps({
    "type": "object",
    "properties": {
        "score":   {"type": "integer", "minimum": 1, "maximum": 5},
        "verdict": {"type": "string"},
        "worked":  {"type": "array", "items": {"type": "string"}},
        "issues":  {"type": "array", "items": {"type": "string"}},
    },
    "required": ["score", "verdict"],
})

created = call("POST", "/tasks", {
    "task": "QA TASK HERE — e.g. 'Add an item to the cart, go to checkout, and report whether "
            "it completes. Score 1-5 (5=flawless, 1=broken) with what worked and any issues.'",
    "startUrl": "https://PUBLIC-URL-UNDER-TEST",          # tunnel localhost first; pass the public URL
    "judge": True,
    "judgeGroundTruth": "SUCCESS LOOKS LIKE — e.g. 'An order-confirmation / thank-you page is shown.'",
    "structuredOutput": SCORE_SCHEMA,
    "maxSteps": 60,
    # optional: "llm": "browser-use-2.0", "vision": True,
    #           "sessionSettings": {"proxyCountryCode": "us", "enableRecording": True}
})
tid = created["id"]
print("created task", tid, "session", created["sessionId"], flush=True)

while True:                                               # poll to a terminal state
    t = call("GET", "/tasks/" + tid)
    if t["status"] in ("finished", "failed", "stopped"):
        break
    time.sleep(5)

print(json.dumps({
    "status":       t["status"],
    "score_output": t.get("output"),       # the structuredOutput JSON → the 1-5 score object
    "judgeVerdict": t.get("judgeVerdict"),  # True = passed the ground-truth check, False = failed
    "judgement":    t.get("judgement"),     # judge's reasoning (stringified JSON report)
    "cost_usd":     t.get("cost"),          # what this run spent
    "num_steps":    len(t.get("steps") or []),
}, indent=2))
PY
```

## Mapping the result to the verdict

Report exactly as `methodology.md`'s output format, sourced from the agent's result:

- **`Score: N/5`** ← the `score` field of the structured `output`.
- **Result / pass-fail** ← `judgeVerdict` (true = met the ground truth, false = didn't); the agent's
  `isSuccess` is its self-report and is less reliable — prefer `judgeVerdict`.
- **What worked / issues** ← the structured `worked` / `issues` arrays, cross-checked against
  `judgement` (the judge's reasoning).
- **Evidence** ← `steps[]`: each has `url`, `screenshotUrl`, `actions`, `nextGoal`. Cite the
  screenshot URLs of the key moments.
- **Cost** ← surface `cost` so the user sees what the run spent.

## Gotchas

- **`structuredOutput` is a *string*** — pass `json.dumps(schema)`, not the schema object.
- **localhost isn't reachable** by the cloud agent — tunnel it (ngrok, per `methodology.md`) and
  pass the public `startUrl`; for a free-ngrok host, tell the agent in the `task` to click through
  any "You are about to visit" interstitial.
- **`429 TooManyConcurrentActiveSessionsError`** — the account hit its concurrent-session cap
  (Free = 3); wait or stop other sessions.
- **`maxSteps`** caps the run — bump it for multi-step flows, but it also caps cost.
