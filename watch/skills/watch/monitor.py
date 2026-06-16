# Background Chrome monitor for the /watch skill — v3.
# Follows the ACTIVE tab across all tabs; actions pushed via CDP binding (nav-proof, immediate).
# Run via:  WATCH_DIR=/tmp/watch-XXXX browser-harness < monitor.py   (backgrounded)
# Writes:   $WATCH_DIR/frames/<epoch_ms>.jpg   (dense recording of whichever tab is in front)
#           $WATCH_DIR/timeline.jsonl          (actions + console + network, tagged with tab url)
# Stop:     touch $WATCH_DIR/STOP
# Captures ONLY Chrome, no OS permission. Privacy: input is length-only; passwords redacted; no raw text.

import os, time, json, base64, glob

WATCH_DIR = os.environ["WATCH_DIR"]
FRAMES = os.path.join(WATCH_DIR, "frames"); os.makedirs(FRAMES, exist_ok=True)
TL = open(os.path.join(WATCH_DIR, "timeline.jsonl"), "a", buffering=1)
STOP = os.path.join(WATCH_DIR, "STOP")
INTERVAL = float(os.environ.get("WATCH_INTERVAL", "0.4"))
MAX_AGE = float(os.environ.get("WATCH_MAX_AGE", "1800"))

# Listeners push each action through the __watchEmit CDP binding the instant it happens —
# so a click that triggers a navigation is captured before the page unloads.
BOOT = r"""
(function(){
  if (window.__watch__) return; window.__watch__ = 1;
  var emit=function(o){ try{ o.t=Date.now()/1000; o.url=location.href;
    if (window.__watchEmit) { window.__watchEmit(JSON.stringify(o)); }      // fresh pages: instant, nav-proof
    else { (window.__watchLog=window.__watchLog||[]).push(o);               // pre-existing pages: buffer, polled
           if(window.__watchLog.length>1000) window.__watchLog.shift(); } }catch(e){} };
  var d=function(el){ if(!el||!el.tagName) return ''; var s=el.tagName;
    if(el.id)s+='#'+el.id; if(el.name)s+='[name='+el.name+']';
    if(typeof el.className==='string'&&el.className)s+='.'+el.className.split(' ')[0]; return s; };
  var val=function(t){ return (t.type==='password')?'<redacted>':((t.value||'').length+' chars'); };
  document.addEventListener('click',function(e){emit({k:'click',target:d(e.target),text:(e.target.innerText||'').slice(0,60)});},true);
  document.addEventListener('submit',function(e){emit({k:'submit',target:d(e.target),action:e.target.action||''});},true);
  document.addEventListener('change',function(e){emit({k:'change',target:d(e.target),value:val(e.target)});},true);
  document.addEventListener('input',function(e){var t=e.target; clearTimeout(t.__wt);
    t.__wt=setTimeout(function(){emit({k:'type',target:d(t),value:val(t)});},600);},true);
  document.addEventListener('keydown',function(e){ if(['Enter','Escape','Tab'].indexOf(e.key)>=0)
    emit({k:'key',key:e.key,target:d(e.target)});},true);
  var st; window.addEventListener('scroll',function(){ if(st)return;
    st=setTimeout(function(){emit({k:'scroll',y:Math.round(window.scrollY||0)}); st=null;},800);},true);
  ['error','warn'].forEach(function(lvl){ var o=console[lvl];
    console[lvl]=function(){ try{emit({k:'console.'+lvl,args:[].slice.call(arguments).map(String).slice(0,5)});}catch(e){}
      return o.apply(console,arguments);};});
  var last=location.href; setInterval(function(){ if(location.href!==last){emit({k:'nav',from:last,to:location.href}); last=location.href;} },300);
})();
"""

cdp("Target.setAutoAttach", autoAttach=True, flatten=True, waitForDebuggerOnStart=False)
sessions = {}

def page_targets():
    return [t for t in cdp("Target.getTargets")["targetInfos"]
            if t["type"] == "page" and not t["url"].startswith(("devtools://", "chrome://"))]

def ev(sid, expr):
    return cdp("Runtime.evaluate", session_id=sid, expression=expr, returnByValue=True).get("result", {}).get("value")

def rec(kind, data):
    TL.write(json.dumps({"t": time.time(), "kind": kind, "data": data}) + "\n")

def attach(t):
    sid = cdp("Target.attachToTarget", targetId=t["targetId"], flatten=True)["sessionId"]
    cdp("Runtime.enable", session_id=sid)
    cdp("Runtime.addBinding", session_id=sid, name="__watchEmit")          # nav-proof action channel
    try: cdp("Network.enable", session_id=sid)
    except Exception: pass
    try: cdp("Page.enable", session_id=sid)                                # so every full navigation is logged
    except Exception: pass
    cdp("Page.addScriptToEvaluateOnNewDocument", session_id=sid, source=BOOT)   # arm future docs
    try: ev(sid, BOOT)                                                          # arm current doc
    except Exception: pass
    sessions[t["targetId"]] = sid
    rec("watch.tab", {"url": t["url"]})
    return sid

rec("watch.started", {"dir": WATCH_DIR})
while not os.path.exists(STOP):
    now = time.time()
    tgts = page_targets()
    live = {t["targetId"] for t in tgts}
    for tid in [k for k in sessions if k not in live]:
        sessions.pop(tid, None)
    active = None
    for t in tgts:
        sid = sessions.get(t["targetId"]) or attach(t)
        try:
            if ev(sid, "document.visibilityState") == "visible":
                foc = ev(sid, "document.hasFocus()")
                if active is None or foc:
                    active = sid
        except Exception:
            pass
        # poll JS-side buffer too — covers tabs already open before watching started
        try:
            buf = ev(sid, "JSON.stringify((window.__watchLog||[]).splice(0))")
            if buf and buf != "[]":
                for o in json.loads(buf):
                    rec("action", o)
        except Exception:
            pass
    # one drain covers ALL attached sessions: actions (bindingCalled) + network
    try:
        for e in drain_events():
            m = e.get("method", "")
            if m == "Runtime.bindingCalled" and e["params"].get("name") == "__watchEmit":
                try: rec("action", json.loads(e["params"]["payload"]))
                except Exception: pass
            elif m == "Page.frameNavigated":
                fr = e["params"].get("frame", {})
                if not fr.get("parentId"):                                  # main frame only (full nav / search)
                    rec("nav", {"url": fr.get("url")})
            elif m == "Runtime.exceptionThrown":
                ed = e["params"].get("exceptionDetails", {}); rec("page.error", {"text": ed.get("text")})
            elif m == "Network.responseReceived":
                r = e["params"].get("response", {}); rec("net", {"status": r.get("status"), "url": r.get("url")})
            elif m == "Network.loadingFailed":
                rec("net.fail", {"error": e["params"].get("errorText"), "type": e["params"].get("type")})
    except Exception:
        pass
    if active:
        try:
            shot = cdp("Page.captureScreenshot", session_id=active, format="jpeg", quality=60)
            if shot.get("data"):
                open(os.path.join(FRAMES, "%d.jpg" % int(now * 1000)), "wb").write(base64.b64decode(shot["data"]))
        except Exception:
            pass
    if int(now) % 12 == 0:
        cutoff = (now - MAX_AGE) * 1000
        for f in glob.glob(os.path.join(FRAMES, "*.jpg")):
            try:
                if int(os.path.basename(f)[:-4]) < cutoff: os.remove(f)
            except Exception: pass
    time.sleep(INTERVAL)

rec("watch.stopped", {})
TL.close()
print("watch monitor stopped:", WATCH_DIR)
