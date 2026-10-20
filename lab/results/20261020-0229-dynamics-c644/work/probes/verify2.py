#!/usr/bin/env python3
"""Checker2's independent re-derivation of the dossier's headline numbers, from raw
TSVs only (no reuse of analyze.py)."""
import math, sys

Q = 1 << 20
MU = 70 * (1 << 52)

def eps_of(x, y, kx, ky):
    return (kx * kx + ky * ky) / 2.0 - MU / math.hypot(x, y)

for arm in sys.argv[1:]:
    ev = {"D": [], "U": []}
    for l in open(f"{arm}.events.tsv"):
        p = l.split()
        ev[p[0]].append((int(p[1]), int(p[2]), int(p[3])))
    U = {b: t for t, b, _ in ev["U"]}
    D = {b: t for t, b, _ in ev["D"]}
    # snapshots per body
    snap = {}
    for l in open(f"{arm}.snap.tsv"):
        t, bid, ring, ct, cl, x, y, kx, ky = map(int, l.split())
        snap.setdefault(bid, []).append((t, ring, ct, cl, x, y, kx, ky))
    times = sorted({s[0][0] for s in snap.values()})
    last_t = max(s[-1][0] for s in snap.values())
    # 1. clamp among dead (snapshot-cumulative cl>0 at any snapshot <= tD)
    cl_dead = sum(1 for b, tD in D.items()
                  if any(r[0] <= tD and r[3] > 0 for r in snap[b]))
    # 2. U <= tD fraction
    ubd = sum(1 for b, tD in D.items() if b in U and U[b] <= tD)
    # 3. ring gradient: dead fraction per genesis ring (first vs last ring)
    rings = sorted({s[0][1] for s in snap.values()})
    per = {}
    for rg in rings:
        ids = [b for b, s in snap.items() if s[0][1] == rg]
        per[rg] = sum(1 for b in ids if b in D) / len(ids)
    # 4. tail hazard after 32k: deaths in (32k, end], per ch, vs fit lam
    late = sorted(t for t in D.values() if t > 32000)
    tail_lam = len(late) / (last_t - 32000) if last_t > 32000 else None
    # remnant: n_in after 32k min/max from global col 4
    g = [tuple(map(int, l.split())) for l in open(f"{arm}.global.tsv")]
    n_in_late = [r[4] for r in g if r[0] > 32000] or [0]
    late_ct = sum(r[1] for r in g if r[0] > g[-1][0] - 4096) / 4096
    # 5. leaver energy: last-snapshot eps - first-snapshot eps, for dead
    ddeps = []
    for b, tD in D.items():
        s = snap[b]
        e0 = eps_of(*s[0][4:8]); eL = eps_of(*s[-1][4:8])
        ddeps.append(eL - e0)
    pos = sum(1 for d in ddeps if d > 0)
    ddeps.sort()
    med = ddeps[len(ddeps) // 2] if ddeps else None
    # 6. survivors at final snapshot: radius distribution + core
    surv_r = []
    subq = 0
    for b, s in snap.items():
        if b in D:
            continue
        t, rg, ct, cl, x, y, kx, ky = s[-1]
        r = math.hypot(x, y)
        surv_r.append(r)
        if r < 0.5 * Q:
            subq += 1
    surv_r.sort()
    n = len(surv_r)
    med_r = surv_r[n // 2] / Q if n else None
    frac_core = sum(1 for r in surv_r if r < 2.1 * Q) / n if n else None
    # 7. lambda by own fit on ln N_alive vs t over deaths
    if D:
        dt = sorted(D.values())
        N0 = len(snap)
        pts = []
        for t in dt:
            alive = N0 - sum(1 for x in dt if x <= t)
            if alive > 0:
                pts.append((t, math.log(alive)))
        mx = sum(p[0] for p in pts) / len(pts); my = sum(p[1] for p in pts) / len(pts)
        sxx = sum((p[0] - mx) ** 2 for p in pts)
        sxy = sum((p[0] - mx) * (p[1] - my) for p in pts)
        lam = -sxy / sxx
        ss_res = sum((p[1] - (my - lam * (p[0] - mx))) ** 2 for p in pts)
        ss_tot = sum((p[1] - my) ** 2 for p in pts)
        r2 = 1 - ss_res / ss_tot
    else:
        lam = r2 = None
    print(f"== {arm} ==")
    print(f" dead {len(D)}  U {len(U)}  clamp-among-dead {cl_dead}")
    print(f" U<=tD {ubd}/{len(D)} = {ubd/len(D):.2f}" if D else " no D")
    print(f" ring dead% {rings[0]}:{per[rings[0]]:.2f} .. {rings[-1]}:{per[rings[-1]]:.2f}")
    print(" lam", lam, "r2", r2, " tail_lam(>32k)", tail_lam, "n_tail", len(late), "last_t", last_t)
    print(f" n_in(>32k) min {min(n_in_late)} max {max(n_in_late)}  late c/ch {late_ct:.0f}")
    print(f" leavers deps>0 {pos}/{len(ddeps)}  median +{med/1e9:.2f}e9" if ddeps else "")
    print(f" survivors {n}  med r {med_r:.1f}q  frac r<2.1q {frac_core:.2f}  r<0.5q {subq}")
