#!/usr/bin/env python3
"""Encounter parity as a rate/survival process (chaos-shadowing direction 2).

Reads the events arms (truth disk-entry epochs) and plane arms (kill epochs) at
mu = 1e-3 (control) and mu = 1e-2, plus the rtol pair and the e846 cross-check.
Emits parity.txt: survival curves, first-event parity ratios, hazard windows,
recrossing counts, instrument controls, and the driver-check dead-set diff.
"""
import json, math, random, sys

R = sys.argv[1] if len(sys.argv) > 1 else "."
HORIZON = 512.0
N = 144
random.seed(20261018)

def load(name):
    rows = {}
    for line in open(f"{R}/{name}.jsonl"):
        v = json.loads(line.replace(":inf", ":0").replace(":NaN", ":0"))
        if "gave_up" in v and v["gave_up"]:
            v["_gaveup"] = True
        rows[(round(v["du"], 4), round(v["phi_deg"], 1))] = v
    return rows

def first_entries(ev):
    """(first entry epoch or None) per IC, ordered as the IC grid."""
    return {k: (v["entries"][0] if v.get("entries") else None) for k, v in ev.items()}

def first_kills(pl):
    return {k: (v["epoch_P"] if v.get("dead") else None) for k, v in pl.items()}

def survival(firsts, grid):
    """S(t): fraction of the ensemble with no first event by t."""
    n = len(firsts)
    return [sum(1 for f in firsts.values() if f is None or f > t) / n for t in grid]

def synodic_exposure(rows):
    """Total synodic periods elapsed per IC over the horizon: T/T_syn, T_syn = P/(1.5·|du|·band)."""
    band = {0.001: (8 * 0.001 / 3) ** 0.5, 0.01: (8 * 0.01 / 3) ** 0.5}
    tot = 0.0
    for k, v in rows.items():
        du = abs(k[0]) * band[round(v.get("mu", 0.001), 4)]
        tot += HORIZON * 1.5 * du  # horizon in synodic units (du=0 ICs: none in the grid)
    return tot

def boot(firsts, grid, draws=2000):
    """Bootstrap CI of S(t) over ICs."""
    vals = list(firsts.values())
    n = len(vals)
    out = [[] for _ in grid]
    for _ in range(draws):
        s = [random.choice(vals) for _ in range(n)]
        for i, t in enumerate(grid):
            out[i].append(sum(1 for f in s if f is None or f > t) / n)
    return [(sorted(o)[int(0.025 * len(o))], sorted(o)[int(0.975 * len(o))]) for o in out]

def rate(firsts, horizon):
    n = len(firsts)
    k = sum(1 for f in firsts.values() if f is not None)
    r = k / (n * horizon)
    # Poisson CI on the count
    lo = 0.5 * __import__("statistics").NormalDist().inv_cdf(0.025) ** 2 if k else 0.0
    import statistics
    z = statistics.NormalDist().inv_cdf(0.975)
    lo = max(0.0, k + z * z / 2 - z * math.sqrt(k + z * z / 4))
    hi = k + z * z / 2 + z * math.sqrt(k + z * z / 4)
    return k, n, r, lo / (n * horizon), hi / (n * horizon)


def syn_rate(firsts, rows):
    """First events per synodic period of exposure, with Poisson CI."""
    import statistics
    k = sum(1 for f in firsts.values() if f is not None)
    e = synodic_exposure(rows)
    z = statistics.NormalDist().inv_cdf(0.975)
    lo = max(0.0, k + z * z / 2 - z * math.sqrt(k + z * z / 4))
    hi = k + z * z / 2 + z * math.sqrt(k + z * z / 4)
    return k, e, k / e, lo / e, hi / e

def hazard(firsts, t0, t1):
    """Events in [t0,t1) per at-risk IC per P."""
    at = sum(1 for f in firsts.values() if f is None or f >= t1 or f >= t0)
    at_risk = sum(1 for f in firsts.values() if f is None or f >= t0)
    k = sum(1 for f in firsts.values() if f is not None and t0 <= f < t1)
    d = at_risk * (t1 - t0)
    return (k / d if d else float("nan")), k, at_risk

out = []
say = out.append

for mu, tag, h, plfile in (("0.001", "mu3", 512.0, "pl-mu3"), ("0.01", "mu2", 4.0, "pl-mu2-4P")):
    ev = load(f"ev-{tag}")
    pl = load(plfile)
    fe = {k: (v["entries"][0] if v.get("entries") and v["entries"][0] <= h else None) for k, v in ev.items()}
    fk0 = first_kills(pl)
    fk = {k: (t if t is not None and t <= h else None) for k, t in fk0.items()}
    # Restrict the truth to the plane's completed ICs (a plane prefix is a job-order prefix).
    common = [k for k in pl if k in fe]
    fe = {k: fe[k] for k in common}
    n = len(common)
    if n < N:
        say(f"(plane completed {n}/{N} ICs in budget; parity on the common subset)")
    gaveup = [k for k, v in ev.items() if v.get("_gaveup")]
    say(f"events-arm gave-ups: {len(gaveup)}")
    # Channels
    ch = {}
    for v in pl.values():
        if v.get("dead"):
            ch[v["channel"]] = ch.get(v["channel"], 0) + 1
    say(f"plane channels: {ch}")
    # Counts and rates
    kt_s, e_t, rt_s, _, _ = syn_rate(fe, {k: v for k, v in ev.items() if k in fe})
    kp_s, e_p, rp_s, _, _ = syn_rate(fk, pl)
    say(f"per-synodic first-event rates (h={h:.0f} P, n={n}): truth {rt_s:.4f}/syn ({kt_s} events)  plane {rp_s:.4f}/syn ({kp_s})  ratio {rp_s/rt_s:.3f}")
    kt, _, rt, _, _ = rate(fe, h)
    kp, _, rp, _, _ = rate(fk, h)
    say(f"first events at h={h:.0f} P: truth {kt}/{n}  plane {kp}/{n}  parity ratio (per-P) {kp/kt:.3f}")
    # Survival curves
    grid = [x for x in (8 * i for i in range(1, 65)) if x <= h] or [h]
    st, sp = survival(fe, grid), survival(fk, grid)
    bt = boot(fe, grid)
    worst = max(range(len(grid)), key=lambda i: abs(st[i] - sp[i]))
    inside = all(lo - 0.02 <= p <= hi + 0.02 for (lo, hi), p, s in zip(bt, sp, st))
    pts = [p for p in (16, 64, 128, 256, int(h)) if p <= h] or [h]
    idx = {p: min(range(len(grid)), key=lambda i: abs(grid[i] - p)) for p in pts}
    say("S(t) — t: " + "  ".join(f"{p}" for p in pts) + "   (last point = parity horizon)")
    say("      truth: " + "  ".join(f"{st[idx[p]]:.3f}" for p in pts) + "   plane: " + "  ".join(f"{sp[idx[p]]:.3f}" for p in pts))
    say(f"max |dS| = {max(abs(a-b) for a,b in zip(st,sp)):.3f} at t={grid[worst]} P; plane inside truth's 95% band (+0.02 slack) everywhere: {inside}")
    # Hazard windows (full truth horizon; plane at its own h)
    h1, k1, r1 = hazard(fe, 0, 128)
    h2, k2, r2 = hazard(fe, 128, 512)
    say(f"truth hazard 0-128 P: {h1:.3e}/P ({k1} of {r1} at risk)   128-512 P: {h2:.3e}/P ({k2} of {r2})   ratio {(h1/h2 if h2 else float("inf")):.2f}")
    h1p, k1p, r1p = hazard(fk, 0, min(128, h))
    h2p, k2p, r2p = hazard(fk, min(128, h), h)
    say(f"plane hazard 0-{min(128, h):.0f} P: {h1p:.3e}/P ({k1p} of {r1p})   {min(128, h):.0f}-{h:.0f} P: {h2p:.3e}/P ({k2p} of {r2p})   ratio {(h1p/h2p if h2p else float("inf")):.2f}")
    # Recrossings
    ent = [len(v["entries"]) for v in ev.values() if v.get("entries")]
    say(f"truth entries total (full 512 P) {sum(ent)} on {len(ent)} crossing ICs; recrossers (>1 entry): {sum(1 for x in ent if x>1)}, max {max(ent)}")
    say(f"plane: kills {sum(1 for v in pl.values() if v.get('dead'))} (of {len(pl)} completed ICs), refused>0: {sum(1 for v in pl.values() if v.get('refused',0)>0)}")
    say("")

# P5: rtol pair at mu=1e-3
ev12, ev13 = load("ev-mu3"), load("ev-mu3fine")
f12, f13 = first_entries(ev12), first_entries(ev13)
k12 = sum(1 for f in f12.values() if f is not None)
k13 = sum(1 for f in f13.values() if f is not None)
agree = sum(1 for k in f12 if (f12[k] is None) == (f13[k] is None))
say(f"=== instrument: rtol 1e-12 vs 1e-13 (mu=1e-3) ===")
say(f"first-entry counts: {k12} vs {k13} (|d| = {abs(k12-k13)}); crossing-membership agrees on {agree}/144 ICs")
grid = [16 * i for i in range(1, 33)]
s12, s13 = survival(f12, grid), survival(f13, grid)
say(f"max |dS| between rtols: {max(abs(a-b) for a,b in zip(s12,s13)):.3f}")
scram = [k for k in f12 if f12[k] is not None and f13[k] is not None]
if scram:
    d = [abs(f12[k] - f13[k]) for k in scram]
    say(f"per-IC epoch scramble on the {len(scram)} both-crossing ICs: median {sorted(d)[len(d)//2]:.1f} P, max {max(d):.1f} P")
say("")

# Driver check: this tree's mu=1e-3 dead set vs e846's (wins.jsonl = their 47 dead ICs + refined epochs)
try:
    e846 = {}
    for line in open(f"{R}/e846/wins.jsonl"):
        v = json.loads(line)
        e846[(round(v["du"], 4), round(v["phi_deg"], 1))] = v
    mine = load("pl-mu3")
    dm = {k for k, v in mine.items() if v.get("dead")}
    de = set(e846)
    say("=== driver check (mu=1e-3 plane, 512 P) ===")
    say(f"this tree dead: {len(dm)}   e846 dead: {len(de)}   same set: {dm == de}")
    if dm != de:
        say(f"only-here: {sorted(dm - de)}")
        say(f"only-e846: {sorted(de - dm)}")
    shared = dm & de
    pairs = [(mine[k]["epoch_P"], e846[k]["epoch_P"]) for k in shared]
    dmax = max(abs(a - b) for a, b in pairs) if pairs else float("nan")
    say(f"epoch agreement on {len(shared)} shared dead ICs: max |d_epoch| = {dmax:.4f} P (P/64 resolution)")
except FileNotFoundError as e:
    say(f"(e846 wins.jsonl not available: {e})")

print("\n".join(out))
open(f"{R}/parity.txt", "w").write("\n".join(out) + "\n")
