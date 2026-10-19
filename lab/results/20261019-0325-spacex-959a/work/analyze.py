#!/usr/bin/env python3
"""Emit the run's table from the flight logs (one line per stat; the checker's entry point)."""
import re, sys, pathlib

def stat(text, key, fn):
    vals = [float(m) for m in re.findall(rf"{key}=([0-9.e+-]+)", text)]
    vals.sort()
    if not vals:
        return None
    return fn(vals)

def p50(v): return v[len(v)//2]
def mx(v): return v[-1]
def tot(v): return sum(v)

rows = []
for f in sorted(pathlib.Path(__file__).parent.glob("logs/*.log")):
    t = f.read_text()
    frames = re.findall(r"^SKYSERV .*f=(\d+) ", t, re.M)
    steady = "\n".join(l for l in t.splitlines() if re.match(rf"SKYSERV .*f=([2-9]|[1-9]\d+) ", l))
    d = dict(
        log=f.name,
        n_frames=len(frames),
        serve_p50=stat(t, "serve_ms", p50), serve_max=stat(t, "serve_ms", mx),
        near_p50=stat(t, "near_ms", p50), due_p50=stat(steady, "due_ms", p50),
        due_max=stat(t, "due_ms", mx),
        ops_max=stat(t, "sums_ops", mx), ops_steady_max=stat(steady, "sums_ops", mx),
        drift_max=stat(t, "sums_drift", mx),
        wrong=sum(int(x) for x in re.findall(r"wrong_cell=(\d+)", t)),
        cells_wrong=sum(int(x) for x in re.findall(r"cells_wrong=(\d+)", t)),
        missing=sum(int(x) for x in re.findall(r"missing=(\d+)", t)),
        extra=sum(int(x) for x in re.findall(r"extra=(\d+)", t)),
        tier_err=sum(int(x) for x in re.findall(r"tier_err=(\d+)", t)),
        digest_bad=len(re.findall(r"digest=0", t)),
        served_B=stat(t, "served_B", lambda v: sum(v)/len(v)),
        end=(re.findall(r"SKYSERV-END .*digest=([0-9a-f]+)", t) or ["-"])[0][:16],
    )
    rows.append(d)

cols = ["log","n_frames","serve_p50","serve_max","near_p50","due_p50","due_max","ops_max",
        "ops_steady_max","drift_max","wrong","cells_wrong","missing","extra","tier_err",
        "digest_bad","served_B","end"]
print(" ".join(cols))
for d in rows:
    print(" ".join(str(d[c]) for c in cols))
