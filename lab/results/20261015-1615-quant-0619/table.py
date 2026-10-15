#!/usr/bin/env python3
"""Fold the flight logs into the dossier's table. Deterministic (counts, digests);
walls are order-of-magnitude (shared Linux box)."""
import re, pathlib

rows = {}
for f in sorted(pathlib.Path("flights").glob("*.txt")):
    t = f.read_text()
    g = lambda k: (re.search(k + r" (\S+)", t) or [None, "?"])[1]
    dem = re.search(r"demotions (\d+)", t)
    rows[f.stem] = dict(
        digest=g("digest"), bpb=g("bytes_per_body"), dem=int(dem.group(1)) if dem else 0,
        pro=int(g("promotions")), hits=int(g("hits")), rnow=int(g("retained_now")),
        ev=int(g("hot_evicts")), ctotal=float(g("total_s")), wall=float(g("wall_s")),
        rss=int(float(g("rss_mb"))),
    )

print(f"{'flight':34} {'digest[:8]':9} {'bpb':>5} {'dem':>7} {'promos':>8} {'×dem':>5} {'hits':>8} {'share':>6} {'rnow':>6} {'evicts':>7} {'c_s':>6} {'wall':>6} {'rss':>5}")
for k, d in rows.items():
    reads = d["hits"] + d["pro"]  # demoted reads (seam arm: promos == reads)
    share = f"{d['hits']/reads*100:.1f}" if reads else "  -"
    xd = f"{d['pro']/d['dem']:.2f}" if d["dem"] else "  -"
    print(f"{k:34} {d['digest'][:8]:9} {d['bpb']:>5} {d['dem']:7} {d['pro']:8} {xd:>5} {d['hits']:8} {share:>6} {d['rnow']:6} {d['ev']:7} {d['ctotal']:6.2f} {d['wall']:6.2f} {d['rss']:5}")

print("\nIdentity checks (digest equal across arms of a scene):")
for scene in ["10000_coast_20000_1", "10000_burn_20000_1", "100000_coast_20000_1", "100000_coast_48000_1"]:
    stems = [s for s in rows if s.endswith(scene)]
    ds = {s.split("_")[0]: rows[s]["digest"][:16] for s in stems}
    extra = {s.split("_")[0]: rows[s]["digest"][:16] for s in stems if s.startswith(("hot512", "hot65536", "hot16384"))}
    ds.update(extra)
    ok = len(set(ds.values())) == 1 and len(ds) >= 4
    print(f"  {scene}: {'IDENTICAL ' + list(ds.values())[0] + f' ({len(ds)} arms)' if ok else ds}")

print("\nAssertions (checker's gold bar), per hot arm:")
for arm, cap in [("hot", 4096), ("hot16384", 16384)]:
    for scene in ["100000_coast_20000_1", "10000_burn_20000_1", "100000_coast_48000_1"]:
        k, c = f"{arm}_{scene}", rows.get(f"ctl_{scene}")
        h, s = rows.get(k), rows.get(f"seam_{scene}")
        if not (h and c and s):
            continue
        reads = h["hits"] + h["pro"]
        dem = s["dem"]  # demotions and the belt's own reads (one per demotion) live on the seam arms
        a = [
            ("digest", h["digest"] == c["digest"]),
            ("rnow<=cap", h["rnow"] <= cap),
            ("rss<=seam+10%", h["rss"] <= s["rss"] * 1.10),
            ("promos<=dem+belt", h["pro"] <= dem + dem),
            ("hits>=80%", h["hits"] >= 0.80 * reads),
        ]
        print(f"  {k:38} " + " ".join(f"{n}:{'PASS' if ok else 'fail'}" for n, ok in a))
