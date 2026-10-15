#!/usr/bin/env python3
"""Fold the flight logs into the dossier's table. Deterministic (counts, digests);
walls are order-of-magnitude (shared Linux box)."""
import re, pathlib
rows = {}
for f in sorted(pathlib.Path("flights").glob("*.txt")):
    t = f.read_text()
    g = lambda k: (re.search(k + r" (\S+)", t) or [None, "?"])[1]
    rows.setdefault(f.stem, {})[
        "digest" if "digest" in t else "x"] = 0
    d = dict(
        digest=g("digest"), bpb=g("bytes_per_body"), dem=g("demotions").split()[0] if "demotions" in t else "?",
        pro=g("promotions"), hits=g("hits"), rnow=g("retained_now"), wall=g("wall_s"),
        rss=g("rss_mb"), kicks=g("kicks"), bodies=g("bodies"), ptotal=g("total_s"),
    )
    d["dem"] = re.search(r"demotions (\d+)", t).group(1)
    rows[f.stem] = d
print(f"{'arm':28} {'digest[:8]':9} {'bpb':6} {'dem':>8} {'promos':>9} {'hits':>9} {'rnow':>6} {'p_secs':>7} {'wall':>6} {'rss':>5}")
for k, d in rows.items():
    print(f"{k:28} {d['digest'][:8]:9} {d['bpb']:6} {int(d['dem']):8} {int(d['pro']):9} {int(d['hits']):9} {int(d['rnow']):6} {float(d['ptotal']):7.2f} {float(d['wall']):6.2f} {int(float(d['rss'])):5}")
print("\nIdentity checks (digest equal across arms of a scene):")
for scene in ["10000_coast_20000_1", "10000_coast_20000_7", "100000_coast_20000_1", "100000_coast_48000_1"]:
    ds = {a: rows.get(f"{a}_{scene}", {}).get("digest", "MISSING")[:16] for a in ["ctl", "seam", "retain", "retain2"]}
    ok = len(set(ds.values())) == 1 and "MISSING" not in ds.values()
    print(f"  {scene}: {'IDENTICAL ' + list(ds.values())[0] if ok else ds}")
