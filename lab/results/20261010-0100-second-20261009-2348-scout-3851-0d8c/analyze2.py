#!/usr/bin/env python3
"""Analyse the coupled-certificate sweeps: every dossier number prints here."""
import glob
import json
import numpy as np

results = []
for f in sorted(glob.glob("results2-*.json")):
    results.extend(json.load(open(f)))
laws = ("truth", "chart", "avg", "avgkin", "chartQ16", "chartQ12",
        "frozen", "chan2")
THRESH = 0.02


def grid_step(Om_ratio, x):
    lg = np.log(np.asarray(Om_ratio))
    d = np.diff(lg)
    return float(np.interp(np.log(max(x, 1e-9)), lg[:-1], d, right=d[-1],
                           left=d[0]))


def compare(Om, bs_ref, bs_law, tol=1.0):
    """Matches law bands to truth bands within tol grid steps.
    Returns (missed_truth, extra_law, shifts, peak_errs)."""
    shifts, pks = [], []
    used = np.zeros(len(bs_law), bool)
    miss = 0
    for b in bs_ref:
        s = grid_step(Om, b["center"])
        cand = [i for i, c in enumerate(bs_law)
                if not used[i] and abs(c["center"] - b["center"]) <= tol * s]
        if cand:
            i = min(cand, key=lambda i: abs(bs_law[i]["center"] - b["center"]))
            used[i] = True
            shifts.append(abs(bs_law[i]["center"] - b["center"]) / s)
            if b["peak"] > 5 * THRESH:
                pks.append(abs(bs_law[i]["peak"] - b["peak"]) / b["peak"])
        else:
            miss += 1
    extra = int((~used).sum())
    return miss, extra, np.array(shifts), np.array(pks) if pks else np.zeros(1)


print("=== validation (closed forms vs exact transport) ===")
mx = dict(dL11=0, dL33=0, dL13=0, dL22=0, dom=0, dpsi_int=0)
for line in open("val.json"):
    v = json.loads(line)
    for k in mx:
        mx[k] = max(mx[k], v[k])
    if v["e"] == 0.0:
        u = 1.0 / v["rp"]
        print(f"  circular rp={v['rp']:.0f}: Delta psi = {v['dpsi']:.6f} vs "
              f"-2pi sqrt(1-3u) = {-2*np.pi*np.sqrt(1-3*u):.6f}")
print("  worst:", {k: f"{x:.1e}" for k, x in mx.items()})

print("\n=== circular analytic cross-check (autonomous monodromy) ===")
import marck
for r in results:
    if r["e"] != 0.0:
        continue
    o = marck.orbit_tables(r["rp"], 0.0, n_tau=4001)
    cc = marck.closed_tables(o)
    a, b, c, om = cc['L11'][0], cc['L33'][0], cc['L13'][0], cc['om'][0]
    OmR = o['Om_r']
    worst = 0.0
    for ratio in (0.5, 0.834, 1.2, 2.0, 3.0):
        Om = ratio * OmR
        A = np.array([[0, 0, 1, 0], [0, 0, 0, 1],
                      [om**2 + a - Om**2, c, 0, 2*om],
                      [c, om**2 + b - Om**2, -2*om, 0]])
        M = marck.__dict__ and np.array(
            [[0, 0, 1, 0], [0, 0, 0, 1],
             [om**2+a-Om**2, c, 0, 2*om], [c, om**2+b-Om**2, -2*om, 0]])
        from scipy.linalg import expm
        MF = expm(A * o['T_r'])
        # orbital-frame monodromy: conjugate by R(Delta psi)
        dpsi = om * o['T_r']
        c_, s_ = np.cos(dpsi), np.sin(dpsi)
        R = np.array([[c_, s_, 0, 0], [-s_, c_, 0, 0], [0, 0, c_, s_],
                      [0, 0, -s_, c_]])
        ev = np.linalg.eigvals(R @ MF)
        rho = max(abs(ev).max(), 1.0)
        Om_grid = np.array([ratio]) * OmR
        mine = marck.floquet2x2(np.full(4001, a), np.full(4001, b),
                                np.full(4001, c), np.full(4001, om),
                                np.zeros(4001), o['T_r'], Om_grid, sub=2)[0]
        worst = max(worst, abs(np.log(rho) - mine))
    print(f"  rp={r['rp']:.0f}: |analytic expm - sweep| worst {worst:.2e}")

print("\n=== per-case band counts ===")
print(f"{'rp':>7} {'e':>3} " + " ".join(f"{l:>9}" for l in laws))
for r in results:
    print(f"{r['rp']:>7.0f} {r['e']:>3} "
          + " ".join(f"{len(r['bands'][l]):>9}" for l in laws))

for lawname, tag in (("chart", "P1 chart (closed forms)"),
                     ("chartQ16", "P4 chart Q=2^16"),
                     ("chartQ12", "P4 chart Q=2^12"),
                     ("frozen", "P5 scout's frozen scalar"),
                     ("avgkin", "P3 avg + exact omega")):
    print(f"\n=== {tag} vs coupled truth ===")
    tm = te = 0
    allsh, allpk = [], []
    for r in results:
        Om = r["Om_over_Om_r"]
        m, x, sh, pk = compare(Om, r["bands"]["truth"], r["bands"][lawname])
        tm += m
        te += x
        allsh.append(sh)
        allpk.append(pk)
    sh = np.concatenate(allsh) if allsh else np.zeros(1)
    pk = np.concatenate(allpk) if allpk else np.zeros(1)
    n_true = sum(len(r["bands"]["truth"]) for r in results)
    n_law = sum(len(r["bands"][lawname]) for r in results)
    print(f"  truth bands {n_true}; this law {n_law}; "
          f"truth bands MISSED {tm}/{n_true}; law bands with no truth "
          f"partner {te}/{n_law}")
    print(f"  matched center shift: max {sh.max():.3f} grid steps; "
          f"peak rel-err: max {pk.max():.3f}, median {np.median(pk):.4f}")

print("\n=== P2 avg (law.md reading) vs truth ===")
tot_param_missed = 0
tot_truth = 0
for r in results:
    Om = np.asarray(r["Om_over_Om_r"])
    bt, ba = r["bands"]["truth"], r["bands"]["avg"]
    covered = np.zeros(len(Om), bool)
    for b in ba:
        covered |= (Om >= b["lo"]) & (Om <= b["hi"])
    missed = 0
    for b in bt:
        i = int(np.searchsorted(Om, b["center"]))
        if not covered[min(i, len(Om) - 1)]:
            missed += 1
    tot_param_missed += missed
    tot_truth += len(bt)
    hi_avg = max(x["hi"] for x in ba)
    print(f"  rp={r['rp']:.0f} e={r['e']}: truth {len(bt)} bands, avg finds "
          f"{len(ba)}, missed {missed}; avg ruin peak "
          f"{max(x['peak'] for x in ba):.1f}/orbit vs truth peak "
          f"{max(x['peak'] for x in bt):.1f}/orbit")
print(f"  TOTAL truth bands {tot_truth}; missed by avg {tot_param_missed}")

print("\n=== P6 chan2 (out-of-plane compressive) ===")
for r in results:
    bs = r["bands"]["chan2"]
    pk = max((b["peak"] for b in bs), default=0.0)
    print(f"  rp={r['rp']:.0f} e={r['e']}: {len(bs)} bands, max peak "
          f"{pk:.3f}/orbit (in-plane truth peak "
          f"{max(b['peak'] for b in r['bands']['truth']):.2f})")

print("\n=== P8 stable gap below k=1 (rotation confinement) ===")
n_gap = 0
for r in results:
    bt = r["bands"]["truth"]
    if len(bt) >= 2 and bt[0]["hi"] < 0.8 * bt[1]["lo"]:
        Om = np.asarray(r["Om_over_Om_r"])
        mu = np.asarray(r["laws"]["truth"])
        sel = (Om > bt[0]["hi"] * 1.02) & (Om < bt[1]["lo"] * 0.98)
        if sel.any() and mu[sel].max() < THRESH:
            n_gap += 1
            print(f"  rp={r['rp']:.0f} e={r['e']}: stable gap "
                  f"({bt[0]['hi']:.3f}, {bt[1]['lo']:.3f}) where avg reports "
                  f"{np.asarray(r['laws']['avg'])[sel].max():.2f}/orbit ruin")
print(f"  stable-gap cases: {n_gap}/12 (P8 as worded: "
      f"{'held' if n_gap >= 6 else 'FAILED'})")
