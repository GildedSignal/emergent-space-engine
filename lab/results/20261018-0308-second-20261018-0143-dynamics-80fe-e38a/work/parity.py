#!/usr/bin/env python3
"""Encounter parity as a rate/survival process (chaos-shadowing direction 2), second author:
adds the certificate's NEGATIVE CONTROL (a deliberately coarser, skipping plane must fail),
the mu=1e-2 full-horizon truth numbers, the at-risk (censored) exposure definition, and the
recrossing join against e846's kept-crossers.

Reads (regen.sh produces them): ev-mu2/ev-mu3/ev-mu3fine (truth disk-entry epochs at 512 P),
pl-mu3{,-s5,-s3} (plane kills at mu=1e-3, 512 P, step 7/5/3), pl-mu3-4P-s{9,7,5,3} (the knob
arms: kicks/P per step), pl-mu2-4P-s{9,7,5,3} (the mu=1e-2 burst), e846/wins.jsonl (the driver
check) and e846/oracle.jsonl (the kept-crosser join). Emits parity.txt.
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
    return {k: (v["entries"][0] if v.get("entries") else None) for k, v in ev.items()}

def first_kills(pl):
    return {k: (v["epoch_P"] if v.get("dead") else None) for k, v in pl.items()}

def survival(firsts, grid):
    n = len(firsts)
    return [sum(1 for f in firsts.values() if f is None or f > t) / n for t in grid]

BAND = {0.001: (8 * 0.001 / 3) ** 0.5, 0.01: (8 * 0.01 / 3) ** 0.5}

def syn_per_P(rows):
    """Synodic periods elapsed per P for each IC: T_syn = P/(1.5·|du|·band) => syn/P = 1.5·|du|·band."""
    return {k: 1.5 * abs(k[0]) * BAND[round(v.get("mu", 0.001), 4)] for k, v in rows.items()}

def synodic_exposure(rows, horizon=HORIZON, firsts=None):
    """Total synodic exposure. Full-horizon (no censoring) when firsts is None; at-risk
    (censored at each IC's first event) when firsts is given — the frozen statistic uses the
    at-risk form, the full-horizon form is kept for continuity with 80fe."""
    spp = syn_per_P(rows)
    if firsts is None:
        return sum(horizon * s for s in spp.values())
    return sum((horizon if firsts.get(k) is None else min(horizon, firsts[k])) * s for k, s in spp.items())

def boot(firsts, grid, draws=2000):
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
    return k, n, k / (n * horizon)

def syn_rate(firsts, rows, horizon=HORIZON, censored=False):
    """First events per synodic period of exposure, with Poisson CI."""
    import statistics
    k = sum(1 for f in firsts.values() if f is not None)
    e = synodic_exposure(rows, horizon, firsts if censored else None)
    z = statistics.NormalDist().inv_cdf(0.975)
    lo = max(0.0, k + z * z / 2 - z * math.sqrt(k + z * z / 4))
    hi = k + z * z / 2 + z * math.sqrt(k + z * z / 4)
    return k, e, k / e, lo / e, hi / e

def hazard(firsts, t0, t1):
    at_risk = sum(1 for f in firsts.values() if f is None or f >= t0)
    k = sum(1 for f in firsts.values() if f is not None and t0 <= f < t1)
    d = at_risk * (t1 - t0)
    return (k / d if d else float("nan")), k, at_risk

out = []
say = out.append

# ---------------------------------------------------------------- control mu=1e-3
mu, tag, h, plfile = "0.001", "mu3", 512.0, "pl-mu3"
ev = load(f"ev-{tag}")
pl = load(plfile)
fe = {k: (v["entries"][0] if v.get("entries") and v["entries"][0] <= h else None) for k, v in ev.items()}
fk = {k: (t if t is not None and t <= h else None) for k, t in first_kills(pl).items()}
common = [k for k in pl if k in fe]
fe = {k: fe[k] for k in common}
fk = {k: fk[k] for k in common}
n = len(common)
if n < N:
    say(f"(plane completed {n}/{N} ICs in budget; parity on the common subset)")
say(f"=== mu=1e-3, h={h:.0f} P, n={n} (the 80fe control, must reproduce) ===")
gaveup = [k for k, v in ev.items() if v.get("_gaveup")]
say(f"events-arm gave-ups: {len(gaveup)}")
ch = {}
for v in pl.values():
    if v.get("dead"):
        ch[v["channel"]] = ch.get(v["channel"], 0) + 1
say(f"plane channels: {ch}")
kt_s, e_t, rt_s, _, _ = syn_rate(fe, {k: v for k, v in ev.items() if k in fe}, censored=False)
kp_s, e_p, rp_s, _, _ = syn_rate(fk, pl, censored=False)
kt_c, e_tc, rt_c, _, _ = syn_rate(fe, {k: v for k in ev.items() if k in fe}, censored=True)
kp_c, e_pc, rp_c, _, _ = syn_rate(fk, pl, censored=True)
say(f"per-synodic first-event rates: truth {rt_s:.4f}/syn ({kt_s} events, exposure {e_t:.0f} syn)  plane {rp_s:.4f}/syn ({kp_s})  ratio {rp_s/rt_s:.3f}")
say(f"  at-risk (censored at first event) exposure: truth {rt_c:.4f}/syn ({e_tc:.0f} syn)  plane {rp_c:.4f}/syn ({e_pc:.0f} syn)  ratio {rp_c/rt_c:.3f}")
kt, _, rt, = rate(fe, h)
kp, _, rp, = rate(fk, h)
say(f"first events at h={h:.0f} P: truth {kt}/{n}  plane {kp}/{n}  parity ratio (per-P) {kp/kt:.3f}")
grid = [x for x in (8 * i for i in range(1, 65)) if x <= h] or [h]
st, sp = survival(fe, grid), survival(fk, grid)
bt = boot(fe, grid)
worst = max(range(len(grid)), key=lambda i: abs(st[i] - sp[i]))
inside = all(lo - 0.02 <= p <= hi + 0.02 for (lo, hi), p in zip(bt, sp))
pts = [p for p in (16, 64, 128, 256, int(h)) if p <= h] or [h]
idx = {p: min(range(len(grid)), key=lambda i: abs(grid[i] - p)) for p in pts}
say("S(t) — t: " + "  ".join(f"{p}" for p in pts) + "   (last point = parity horizon)")
say("      truth: " + "  ".join(f"{st[idx[p]]:.3f}" for p in pts) + "   plane: " + "  ".join(f"{sp[idx[p]]:.3f}" for p in pts))
say(f"max |dS| = {max(abs(a-b) for a,b in zip(st,sp)):.3f} at t={grid[worst]} P; plane inside truth's 95% band (+0.02 slack) everywhere: {inside}")
h1, k1, r1 = hazard(fe, 0, 128)
h2, k2, r2 = hazard(fe, 128, 512)
say(f"truth hazard 0-128 P: {h1:.3e}/P ({k1} of {r1} at risk)   128-512 P: {h2:.3e}/P ({k2} of {r2})   ratio {(h1/h2 if h2 else float('inf')):.2f}")
ent = [len(v["entries"]) for v in ev.values() if v.get("entries")]
say(f"truth entries total (full 512 P) {sum(ent)} on {len(ent)} crossing ICs; recrossers (>1 entry): {sum(1 for x in ent if x>1)}, max {max(ent)}")
say(f"plane: kills {sum(1 for v in pl.values() if v.get('dead'))} (of {len(pl)} completed ICs), refused>0: {sum(1 for v in pl.values() if v.get('refused',0)>0)}")
say("")

# ------------------------------------------------- mu=1e-2 truth, FULL horizon (folded in)
ev2 = load("ev-mu2")
fe2 = first_entries(ev2)
say("=== mu=1e-2, truth side only, FULL 512 P horizon (plane side is burst-only behind the cost wall) ===")
kt2, e2, r2s, _, _ = syn_rate(fe2, ev2, censored=False)
kt2c, e2c, r2c, _, _ = syn_rate(fe2, ev2, censored=True)
say(f"first-entries {kt2}/{len(fe2)}; per-synodic rate {r2s:.4f}/syn (exposure {e2:.0f} syn; at-risk censored {r2c:.4f}/syn, exposure {e2c:.0f} syn)")
hh1, kk1, rr1 = hazard(fe2, 0, 128)
hh2, kk2, rr2 = hazard(fe2, 128, 512)
say(f"hazard 0-128 P: {hh1:.3e}/P ({kk1} of {rr1} at risk)   128-512 P: {hh2:.3e}/P ({kk2} of {rr2})   ratio {(hh1/hh2 if hh2 else float('inf')):.1f}")
med = sorted(f for f in fe2.values() if f is not None)
say(f"median first epoch {med[len(med)//2]:.0f} P, earliest {med[0]:.2f} P; entries total {sum(len(v.get('entries',[])) for v in ev2.values())}, recrossers {sum(1 for v in ev2.values() if len(v.get('entries',[]))>1)}")
say(f"portable rate fall mu=1e-3 -> 1e-2: {rt_s:.4f} -> {r2s:.4f}/syn = {rt_s/r2s:.1f}x (full-horizon exposure), {rt_c:.4f} -> {r2c:.4f}/syn = {rt_c/r2c:.1f}x (at-risk)")
say(f"events-arm gave-ups: {sum(1 for v in ev2.values() if v.get('_gaveup'))}; min closest approach {min(v['closest_Rp'] for v in ev2.values()):.2f} Rp")
say("")

# ------------------------------------------------- the negative control (mu=1e-3, 512 P)
say("=== NEGATIVE CONTROL: coarser kick cadence (fewer surface checks per conjunction) must FAIL parity ===")
truth_first = {k: v for k, v in fe.items()}
truth_cross = {k for k, f in truth_first.items() if f is not None}
steps = [("pl-mu3", 7, "shipped"), ("pl-mu3-s5", 5, "4x coarser"), ("pl-mu3-s3", 3, "16x coarser")]
verdicts = []
for fname, s, label in steps:
    try:
        p = load(fname)
    except FileNotFoundError:
        say(f"step {s} ({label}): arm file {fname} missing")
        continue
    common2 = [k for k in p if k in truth_first]
    f2 = {k: (v["epoch_P"] if v.get("dead") and v["epoch_P"] <= h else None) for k, v in p.items()}
    f2 = {k: f2[k] for k in common2}
    kills = sum(1 for f in f2.values() if f is not None)
    kicks = [v["kicks"] / h for v in p.values() if "kicks" in v]
    import statistics as stx
    mk = stx.median(kicks) if kicks else float("nan")
    recall = sum(1 for k, f in f2.items() if f is not None and k in truth_cross)
    ratio = kills / kt if kt else float("nan")
    grid2 = [x for x in (8 * i for i in range(1, 65)) if x <= h]
    s2 = survival(f2, grid2)
    bt2 = boot(truth_first, grid2)
    ins = all(lo - 0.02 <= q <= hi + 0.02 for (lo, hi), q in zip(bt2, s2))
    dmax = max(abs(a - b) for a, b in zip(survival(truth_first, grid2), s2))
    chn = {}
    for v in p.values():
        if v.get("dead"):
            chn[v["channel"]] = chn.get(v["channel"], 0) + 1
    count_ok = 0.8 <= ratio <= 1.4
    curve_ok = ins
    verdicts.append((s, count_ok and curve_ok))
    say(f"step {s} ({label}): kills {kills}/{len(common2)}  ratio {ratio:.3f}  in [0.8,1.4]: {count_ok}  |  max|dS| {dmax:.3f}  curve in 95% band: {curve_ok}  |  on truth-crossers {recall}/{kt}  channels {chn}  median kicks/P {mk:.0f}  refused>0 {sum(1 for v in p.values() if v.get('refused',0)>0)}")
ok7 = verdicts and verdicts[0][1]
failcoarse = all(not v for _, v in verdicts[1:]) if len(verdicts) > 1 else None
say(f"CERTIFICATE VERDICT: step 7 (control) {'PASSES' if ok7 else 'FAILS (VOID: control must pass)'}; coarser arms {'FAIL' if failcoarse else 'do not both fail'} => the statistic {'discriminates' if ok7 and failcoarse else 'does NOT yet discriminate'} a skipping law")
say("")

# ------------------------------------------------- the knob record (4 P arms, kicks/P)
say("=== knob liveness (mu=1e-3, 4 P, 144 ICs): median kicks/P per step (deaths 0 on both sides) ===")

import statistics as stx
for s in (9, 7, 5, 3):
    try:
        p = load(f"pl-mu3-4P-s{s}")
        kicks = [v["kicks"] / 4.0 for v in p.values() if "kicks" in v]
        say(f"step {s}: median kicks/P {stx.median(kicks):.0f}  deaths {sum(1 for v in p.values() if v.get('dead'))}  refused>0 {sum(1 for v in p.values() if v.get('refused',0)>0)}")
    except FileNotFoundError:
        pass
say("")

# ------------------------------------------------- the mu=1e-2 cost walls (row counts ARE the datum)
say("=== the mu=1e-2 cost walls (regen reproduces them: unfinished rows at the 120 s budgets) ===")
for f, lbl in (("pl-mu2-16P-partial", "16 P, step 7, 2 workers, 120 s budget"), ("pl-mu2-64P", "64 P, step 7, 4 workers, 120 s budget"), ("pl-mu2-16P-s5", "16 P, step 5, 2 workers, 120 s budget (N5)")):
    try:
        m = sum(1 for _ in open(f"{R}/{f}.jsonl"))
        say(f"{lbl}: {m} of 144 ICs finished" + ("  (the 80fe runaway tail)" if m < 144 and "s5" not in f else ""))
    except FileNotFoundError:
        say(f"{lbl}: file missing")
try:
    m3 = sum(1 for _ in open(f"{R}/pl-mu2-4P-s3.jsonl"))
    if m3 < 144:
        dus3 = [s * u for u in (0.35, 0.6, 0.85, 1.05, 1.25, 1.45) for s in (1, -1)]
        grid3 = {(round(u, 3), round(15.0 + 30.0 * k, 1)) for u in dus3 for k in range(12)}
        have = set()
        for line in open(f"{R}/pl-mu2-4P-s3.jsonl"):
            v = json.loads(line.replace(":inf", ":0").replace(":NaN", ":0"))
            have.add((round(v["du"], 3), round(v["phi_deg"], 1)))
        miss = sorted(grid3 - have)
        say(f"4 P, step 3: {m3} of 144 ICs finished within its 400 s run — the coarse end grinds too: {miss}")
        for f5 in ("pl-mu2-4P-s9", "pl-mu2-4P-s7", "pl-mu2-4P-s5"):
            r = {(round(v["du"], 3), round(v["phi_deg"], 1)): v for v in (json.loads(x.replace(":inf", ":0").replace(":NaN", ":0")) for x in open(f"{R}/{f5}.jsonl"))}
            for k2 in miss:
                q = r.get(k2)
                say(f"  same IC at {f5}: dead={q.get('dead') if q else 'ABSENT'} kicks={q.get('kicks') if q else '-'} (alive, completes)")
except FileNotFoundError:
    pass
say("")


# ------------------------------------------------- the burst at mu=1e-2, per step
say("=== the mu=1e-2 burst (<=4 P), per cadence: same-IC set and epoch match vs the truth's 8 ===")
ev2f = first_entries(ev2)
t4 = {k: f for k, f in ev2f.items() if f is not None and f <= 4.01}
for s in (9, 7, 5, 3):
    try:
        p = load(f"pl-mu2-4P-s{s}")
    except FileNotFoundError:
        continue
    p4 = {k: (v["epoch_P"], v["channel"]) for k, v in p.items() if v.get("dead") and v["epoch_P"] <= 4.01}
    inter = set(t4) & set(p4)
    late = [k for k in t4 if k not in p4 and any(k == k2 and v.get("dead") and v["epoch_P"] > 4.01 for k2, v in p.items())]
    dmax = max((abs(t4[k] - p4[k][0]) for k in inter), default=float("nan"))
    say(f"step {s}: truth<=4P {len(t4)}  plane<=4P kills {len(p4)}  same ICs {len(inter)}/{len(t4)}  max|d_epoch| {dmax:.3f} P  (grid P/64 = 0.016 P)  kills moved past 4 P: {len(late)}  channels {sorted({c for _, c in p4.values()})}")
say(f"burst exactness (step 7) must reproduce 80fe: 8/8 with max|d_epoch| <= 0.016 P; N4 (step 9, finer) must also hold if the clause is skip-sized, not cadence-sized")
say("")

# ------------------------------------------------- P5: rtol pair at mu=1e-3
ev12, ev13 = load("ev-mu3"), load("ev-mu3fine")
f12, f13 = first_entries(ev12), first_entries(ev13)
k12 = sum(1 for f in f12.values() if f is not None)
k13 = sum(1 for f in f13.values() if f is not None)
agree = sum(1 for k in f12 if (f12[k] is None) == (f13[k] is None))
say(f"=== instrument: rtol 1e-12 vs 1e-13 (mu=1e-3) ===")
say(f"first-entry counts: {k12} vs {k13} (|d| = {abs(k12-k13)}); crossing-membership agrees on {agree}/144 ICs")
grid3 = [16 * i for i in range(1, 33)]
s12, s13 = survival(f12, grid3), survival(f13, grid3)
say(f"max |dS| between rtols: {max(abs(a-b) for a,b in zip(s12,s13)):.3f}")
scram = [k for k in f12 if f12[k] is not None and f13[k] is not None]
if scram:
    d = [abs(f12[k] - f13[k]) for k in scram]
    say(f"per-IC epoch scramble on the {len(scram)} both-crossing ICs: median {sorted(d)[len(d)//2]:.1f} P, max {max(d):.1f} P")
say("")

# ------------------------------------------------- the recrossing join (e846's kept-crossers)
try:
    orc = {}
    for line in open(f"{R}/e846/oracle.jsonl"):
        v = json.loads(line)
        orc[(round(v["du"], 3), round(v["phi_deg"], 1))] = v
    wins = set()
    for line in open(f"{R}/e846/wins.jsonl"):
        v = json.loads(line)
        wins.add((round(v["du"], 3), round(v["phi_deg"], 1)))
    kept = [k for k in orc if k not in wins]
    crossers = [k for k in kept if orc[k]["closest_Rp"] < 1.0]
    say("=== the recrossing join: is the miss channel concentrated in recrossers? ===")
    say(f"e846 (reproduced from its own data): kills {len(wins)}/144, kept {len(kept)}, kept-crossers {len(crossers)}")
    myent = {k: len(v.get("entries", [])) for k, v in ev12.items()}
    for name, grp in (("kept-crossers", crossers), ("kept-non-crossers", [k for k in kept if orc[k]["closest_Rp"] >= 1.0])):
        wmine = [k for k in grp if myent.get(k, 0) > 0]
        rec = sum(1 for k in wmine if myent[k] > 1)
        say(f"{name}: {len(grp)} ICs, with first-entries in this truth run {len(wmine)}, of which recrossers {rec}")
    allmissed = [k for k in kept if myent.get(k, 0) > 0]
    say(f"miss channel (kept ICs whose truth enters the disk here): {len(allmissed)} first-entries, recrossers among them {sum(1 for k in allmissed if myent[k]>1)} ({100*sum(1 for k in allmissed if myent[k]>1)/max(1,len(allmissed)):.0f}%) vs {sum(1 for k,v in myent.items() if v>1)}/{sum(1 for v in myent.values() if v>0)} recrossers among all crossing ICs")
except FileNotFoundError as e:
    say(f"(e846 join data not available: {e})")
say("")

# ------------------------------------------------- driver check
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
