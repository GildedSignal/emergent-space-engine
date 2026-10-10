#!/usr/bin/env python3
"""Analysis: sufficient cadence K*, predictor zeta, held-out transfer, FTLE,
cost ratio. Reads out_{A,B,C}.npz, out_{A,C}_ftle.npz, out_*_birth.npz."""
import json
import numpy as np

MUJ = 9.545937e-4
A_J = 5.204
MU_S = 4 * np.pi ** 2
NJ = np.sqrt(MU_S * (1 + MUJ) / A_J ** 3)

FLOORS = dict(rel=(0.10, 0.15, 0.10), abs=(2e-3, 1.5e-3, 3e-3))


def scalars(e):
    return e.mean(axis=0), e.std(axis=0), e.max(axis=0)


def sufficient(es_dict, truth_key):
    """min cadence whose 3 behaviour scalars match truth within tolerance."""
    ks = sorted(int(k[1:]) for k in es_dict if k.startswith("e"))
    mt, st, xt = scalars(es_dict[truth_key])
    kstar = np.full(len(mt), -1, dtype=int)
    for k in ks:
        m, s, x = scalars(es_dict[f"e{k}"])
        dm = np.abs(m - mt) / np.maximum(FLOORS["rel"][0] * mt, FLOORS["abs"][0])
        ds = np.abs(s - st) / np.maximum(FLOORS["rel"][1] * st, FLOORS["abs"][1])
        dx = np.abs(x - xt) / np.maximum(FLOORS["rel"][2] * xt, FLOORS["abs"][2])
        ok = (dm <= 1) & (ds <= 1) & (dx <= 1)
        kstar = np.where((kstar < 0) & ok, k, kstar)
    return kstar, ks


def zeta(a0, e0, muj=MUJ, C=1.0):
    n = np.sqrt(MU_S / a0 ** 3)
    z = np.full_like(a0, np.inf)
    for p in range(1, 9):
        for q in (1, 2):
            nres = (p + q) / p * NJ
            dn = np.abs(n - nres)
            w = nres * C * np.sqrt(muj) * np.maximum(e0, 1e-3) ** (q / 2)
            z = np.minimum(z, dn / w)
    return z


def spearman(x, y):
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    rx -= rx.mean(); ry -= ry.mean()
    return float((rx * ry).sum() / np.sqrt((rx ** 2).sum() * (ry ** 2).sum()))


def analyse(belt, ks=None):
    d = np.load(f"out_{belt}.npz")
    b = np.load(f"out_{belt}_birth.npz")
    a0, e0 = b["a"], b["e"]
    keys = [k for k in d.files if k.startswith("e")]
    truth_key = max(keys, key=lambda k: int(k[1:]))
    kstar, ks = sufficient({k: d[k] for k in keys}, truth_key)
    return kstar, ks, a0, e0, truth_key


out = {}

# --- belt A (tuning) ---
kstarA, ksA, aA, eA, tA = analyse("A")
have = kstarA > 0
print(f"A: never-sufficient {(~have).mean()*100:.1f}%, ladder {ksA}, truth {tA}")
# calibrate C so zeta=1 sits at the median of raw zeta among K*>=128 bodies
zA_raw = zeta(aA, eA)
C_cal = float(np.median(zA_raw[(kstarA >= 128) & have]))
zA = zA_raw / C_cal

med = np.median(kstarA[have]); p90 = np.percentile(kstarA[have], 90)
p99 = np.percentile(kstarA[have], 99)
spread = p90 / med
# cost ratio: uniform at p99 vs scheduled (never-bodies pay top cadence)
top = max(ksA)
uni = top * len(kstarA) if p99 >= top else int(p99) * len(kstarA)
sched = int(kstarA[have].sum()) + int(top * (~have).sum())
print(f"A: median K* {med:.0f}, p90 {p90:.0f}, spread {spread:.1f}x, "
      f"uniform(p99={p99:.0f})/scheduled = {uni/sched:.1f}x")
rhoA = spearman(np.log(kstarA[have]), np.log(zA[have]))
print(f"A: Spearman rho(logK*, log zeta) = {rhoA:.3f}  (C_cal={C_cal:.3g})")

# K*(zeta) map from A: median log K* per log-zeta bin
lz = np.log(zA[have]); lk = np.log(kstarA[have])
bins = np.quantile(lz, np.linspace(0, 1, 9))
bid = np.clip(np.digitize(lz, bins) - 1, 0, 7)
mapx, mapy = [], []
for i in range(8):
    sel = bid == i
    if sel.sum() >= 5:
        mapx.append(lz[sel].mean()); mapy.append(lk[sel].mean())
mapx, mapy = np.array(mapx), np.array(mapy)


def predict_k(lz_new):
    return np.exp(np.interp(lz_new, mapx, mapy))


out["A"] = dict(never=float((~have).mean()), median=float(med), p90=float(p90),
                spread=float(spread), cost_ratio=float(uni / sched), rho=rhoA, C=C_cal)

# --- held-out belts ---
for belt, muj in (("B", MUJ), ("C", 3 * MUJ)):
    kstar, ks, a0, e0, tkey = analyse(belt)
    hv = kstar > 0
    z = zeta(a0, e0, muj) / C_cal
    rho = spearman(np.log(kstar[hv]), np.log(z[hv]))
    pred = predict_k(np.log(z[hv]))
    within2 = (np.abs(np.log(pred) - np.log(kstar[hv])) <= np.log(2)).mean()
    print(f"{belt}: never {(~hv).mean()*100:.1f}%, rho={rho:.3f}, "
          f"within-factor-2 {within2*100:.0f}%  (truth {tkey})")
    out[belt] = dict(never=float((~hv).mean()), rho=float(rho),
                     within2=float(within2))

    if belt == "C":
        # P5: cliff concentration in zeta (A and C pooled)
        zpool = np.concatenate([zA[kstarA < 0], z[kstar < 0]])
        print(f"cliff: never-sufficient with zeta<1: {(zpool < 1).mean()*100:.0f}% "
              f"(n={len(zpool)})")

# --- FTLE ---
for belt in ("A", "C"):
    try:
        f = np.load(f"out_{belt}_ftle.npz")
        ly = f["lyap"]
        b = np.load(f"out_{belt}_birth.npz")
        z = zeta(b["a"], b["e"], MUJ if belt == "A" else 3 * MUJ) / C_cal
        chaotic = ly > 2e-3
        rho = spearman(np.log(ly[chaotic]), -np.log(z[chaotic]))
        print(f"{belt} FTLE: chaotic {chaotic.mean()*100:.0f}%, "
              f"median lambda {np.median(ly[chaotic]) if chaotic.any() else 0:.4g}/yr, "
              f"rho(log lambda, -log zeta)={rho:.3f}")
        out[f"ftle_{belt}"] = dict(chaotic=float(chaotic.mean()),
                                   med_lambda=float(np.median(ly[chaotic])) if chaotic.any() else 0.0,
                                   rho=float(rho))
    except FileNotFoundError:
        print(f"{belt} FTLE file missing")

if "ftle_A" in out and "ftle_C" in out:
    out["lambda_ratio_C_over_A"] = out["ftle_C"]["med_lambda"] / out["ftle_A"]["med_lambda"]
    print(f"median lambda ratio C/A = {out['lambda_ratio_C_over_A']:.2f}")

json.dump(out, open("analysis.json", "w"), indent=1)
print("wrote analysis.json")
