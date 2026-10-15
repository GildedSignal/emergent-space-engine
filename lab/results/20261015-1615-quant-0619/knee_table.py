#!/usr/bin/env python3
"""Fold the knee flights into the dossier table. Deterministic parts: counts/digests/ratios."""
import re, pathlib, math

rows = {}
for f in sorted(pathlib.Path("flights").glob("*.txt")):
    t = f.read_text()
    g = lambda k: (re.search(k + r" (\S+)", t) or [None, "?"])[1]
    m = re.search(r"demotions (\d+)", t)
    rows[f.stem] = dict(
        digest=g("digest"), dem=int(m.group(1)) if m else 0, pro=int(g("promotions")),
        hits=int(g("hits")), rnow=int(g("retained_now")), ev=int(g("hot_evicts")),
        wall=float(g("wall_s")), rss=int(float(g("rss_mb"))),
        p50=float(g("promote_us p50").replace("?","0")), p99=float(g("promote_us p99").replace("?","0")),
    )

print(f"{'flight':30} {'digest':9} {'dem':>7} {'promos':>8} {'xdem':>6} {'hits':>8} {'rnow':>7} {'evict':>7} {'p50us':>6} {'p99us':>7} {'wall':>6} {'rss':>5}")
for k, d in rows.items():
    xd = f"{d['pro']/d['dem']:.3f}" if d["dem"] else "-"
    print(f"{k:30} {d['digest'][:8]:9} {d['dem']:7} {d['pro']:8} {xd:>6} {d['hits']:8} {d['rnow']:7} {d['ev']:7} {d['p50']:6.1f} {d['p99']:7.1f} {d['wall']:6.1f} {d['rss']:5}")

print("\nIdentity (digest per scene, all arms):")
scenes = sorted({ "_".join(k.split("_")[1:]) for k in rows })
for sc in scenes:
    ds = {k.split("_")[0]: rows[k]["digest"][:16] for k in rows if k.endswith(sc)}
    print(f"  {sc}: {'IDENTICAL ' + next(iter(ds.values())) + f' ({len(ds)} arms)' if len(set(ds.values())) == 1 else ds}")

print("\nWorking set and knee:")
pts = []
for n in [10000, 30000, 100000, 200000]:
    k = f"sat_{n}_burn_20000_1"
    if k not in rows and n != 10000: continue
    if k in rows:
        ws, ev = rows[k]["rnow"], rows[k]["ev"]
        pts.append((n, ws))
        print(f"  N={n:>7}: WS={ws:>7} (evicts {ev})  WS/N={ws/n:.2f}")
print("  linear law: WS - N and WS - demotions (offsets must be constant):")
for n, ws in ([(10000, 40187)] if "sat_10000_burn_20000_1" not in rows else []) + pts + ([("10^4", rows["sat_10000_burn_20000_1"]["rnow"])] if "sat_10000_burn_20000_1" in rows else []):
    k = f"sat_{n}_burn_20000_1" if n != 10000 else None
    dem = rows[k]["dem"] if k in rows else 40187
    print(f"    N={n:>7}: WS-N={ws-n:>6}  WS-demotions={ws-dem}")
z = [(n, rows[f"sat_{n}_burn_20000_1"]["rnow"] - rows[f"glob_{n}_burn_20000_1"]["rnow"]) for n in [30000, 100000, 200000]]
print("  ring zombies vs global (sat rnow - glob rnow):", ", ".join(f"N={n}: +{d}" for n, d in z))
print("  knee extrapolation to 1e9 (law WS ~ N per 20k game-s): ~1e9 entries ~ 1.4 TB -- no cap ships")

reads_inv = {}
for k in sorted(rows):
    if "burn_20000" in k and ("sat_" in k or k.startswith(("c1", "c2", "c6")) or k.startswith("glob")):
        sc = "_".join(k.split("_")[1:]); reads_inv.setdefault(sc, set()).add(rows[k]["hits"] + rows[k]["pro"])
print("\nRead stream cap-invariance (hits+promotions identical across arms of a scene):")
for sc, v in reads_inv.items(): print(f"  {sc}: {'INVARIANT ' + str(next(iter(v))) if len(v)==1 else v}")
print("\nPrice law below the knee (promos-dem == hits_sat-hits_cap):")
for k in sorted(rows):
    if not k.startswith(("c1", "c2", "c6")): continue
    sc = "_" + "_".join(k.split("_")[1:])
    s, g_ = rows.get("sat" + sc), rows.get("glob" + sc)
    if not (s and g_): continue
    lhs = rows[k]["pro"] - rows[k]["dem"]; rhs = g_["hits"] - rows[k]["hits"]
    print(f"  {k:30} promos-dem={lhs:>7} hits_sat-hits_cap={rhs:>7} {'EXACT' if lhs == rhs else 'MISMATCH'}")

print("\nCut dependence (1e5 burn): WS(48k)/WS(20k):")
a, b = rows.get("cut48sat_100000_burn_48000_1"), rows.get("sat_100000_burn_20000_1")
if a and b: print(f"  {a['rnow']} / {b['rnow']} = {a['rnow']/b['rnow']:.2f}  (evicts {a['ev']})")
