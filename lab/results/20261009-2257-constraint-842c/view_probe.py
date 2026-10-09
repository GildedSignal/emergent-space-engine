#!/usr/bin/env python3
"""Probe the live plane's view JSON: what the gather actually emits per frame.

Starts the server, steps it like the player (60 Hz, rtf 100), then reports the
emitter mix: kinds, angular radii, distances — how many emitters are below any
plausible differentiation floor (pixel-scale angle, invisible flux).
"""
import json, subprocess, sys, time, urllib.request

PORT = 8799
FRAMES = int(sys.argv[1]) if len(sys.argv) > 1 else 300
proc = subprocess.Popen(
    ["/home/glmlab/lab-target-2/release/xtask", "universe", "--rtf", "100",
     "--members", sys.argv[2] if len(sys.argv) > 2 else "1600",
     "--port", str(PORT), "--seed", "7"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    time.sleep(1.5)
    last = None
    for n in range(FRAMES):
        t0 = time.time()
        req = urllib.request.Request(
            f"http://127.0.0.1:{PORT}/frame", data=b'{"keys":0,"throttle":0,"rtf":100}',
            headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=5) as r:
            last = json.load(r)
        wait = 1/60.0 - (time.time() - t0)
        if wait > 0:
            time.sleep(wait)
    v = last["frame"]
    seen = v["seen"]
    print(f"frames={FRAMES} server_ms={last['server_ms']:.2f} emitters={len(seen)}")
    import math
    rows = []
    for s in seen:
        rows.append((s["kind"], s.get("angular_radius", 0.0), s["light_seconds"],
                     s.get("luminosity", 0.0), s.get("shift", 1.0)))
    from collections import Counter
    print("by kind:", Counter(r[0] for r in rows))
    # a 1080p pixel at 60 deg fov is ~5.8e-4 rad; half-pixel floor 3e-4
    for floor in (1e-2, 1e-3, 3e-4, 1e-4):
        above = sum(1 for r in rows if r[1] >= floor)
        print(f"angular_radius >= {floor:g}: {above}/{len(rows)}")
    fl = sorted(r[3] for r in rows)
    print("luminosity: max %.3g median %.3g min %.3g" % (fl[-1], fl[len(fl)//2], fl[0]))
    ds = sorted(r[2] for r in rows)
    print("distance_ls: min %.3g median %.3g max %.3g" % (ds[0], ds[len(ds)//2], ds[-1]))
    json.dump(v, open(sys.argv[3] if len(sys.argv) > 3 else "view_last.json", "w"))
finally:
    proc.terminate()
    proc.wait()
