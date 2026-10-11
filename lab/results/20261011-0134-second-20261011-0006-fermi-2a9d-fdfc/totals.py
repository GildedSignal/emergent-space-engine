#!/usr/bin/env python3
"""Totals comparison under realistic encounter tails — the checker's named gold run.

Question: re-fit + canonical relabelling of unobserved bodies (label cost 0) versus
entropy-coded frozen program, BOTH under 1/b^2 encounter tails at belt rate. What
actually bounds H_live, and does the relabelled floor hold at 10^9 with m sized from
the spread?

Three jump laws, same median |jump| = 100 cells, same physical cap 1e4 cells:
  G   author's Gaussian J=100                (reproduction control, bit-exact)
  T1  areal 1/b impulse: P(|D|>x)=(Dmin/x)^2, Dmin=100/sqrt(2); E[D^2]=5.45e4
  T2  checker's |D|=K/U^2, U~U(0,1): K=25, clipped at 1e4 (5% pile at cap);
      E[D^2]=6.67e6 (the checker's 6.6e6, reconstructed with the clip pile)

Dynamics (author's, unchanged): N=2^20, s=1 cell/orbit, r=2.135e-3/body/orbit,
T=8192 orbits, checkpoints at powers of two.

Run: python3 totals.py     (~8 min, < 1 GB)
"""
import json
import numpy as np

N = 1 << 20
T = 1 << 13
S = 1.0
R_ENC = 427.0 / (1e4 * 20.0)          # 2.135e-3, r8 v2 belt 0
CAP = 1e4
M_LIST = (256, 1024, 4096, 16384, 65536, 262144)
LAWS = {
    "G":  dict(kind="gauss", J=100.0),
    "T1": dict(kind="pareto", a=100.0 / np.sqrt(2.0), alpha=2.0),
    "T2": dict(kind="pareto", a=25.0, alpha=0.5),
}

def H(c):
    c = c[c > 0].astype(np.float64)
    n = c.sum()
    return float(np.log2(n) - (c * np.log2(c)).sum() / n)

def ent_of(v):
    v = np.asarray(v, dtype=np.int64)
    return H(np.bincount(v - v.min()))

def knots_program(xs, m):
    idx = (np.arange(m + 1) * (len(xs) - 1)) // m
    ranks = np.arange(len(xs), dtype=np.float64)
    return np.rint(np.interp(ranks, idx.astype(np.float64),
                             xs[idx].astype(np.float64))).astype(np.int64)

def jump_mag(rng, k, law):
    if law["kind"] == "gauss":
        return np.rint(rng.standard_normal(k, dtype=np.float32) * law["J"])
    u = rng.random(k)
    mag = np.minimum(law["a"] * u ** (-1.0 / law["alpha"]), CAP)
    sign = np.where(rng.random(k) < 0.5, -1.0, 1.0)
    return np.rint(mag * sign)

def evolve(law, rng):
    """Author's evolve, verbatim draw order for G; snapshots at powers of two."""
    x0 = ((np.arange(N, dtype=np.float64) + 0.5)).astype(np.int32)
    x = x0.copy()
    ever_hit = np.zeros(N, dtype=bool)
    snaps = {}
    B, t = 32, 1
    while t <= T:
        nb = min(B, T - t + 1)
        d = np.rint(rng.standard_normal((nb, N), dtype=np.float32) * S)
        hit = rng.random((nb, N)) < R_ENC
        ever_hit |= hit.any(axis=0)
        fi = np.nonzero(hit.ravel())[0]
        if fi.size:
            d.ravel()[fi] += jump_mag(rng, fi.size, law).astype(np.float32)
        for i in range(nb):
            x += d[i].astype(np.int32)
            if (t + i) & -(t + i) == t + i:
                snaps[t + i] = x.copy()
        t += nb
    return x0, snaps, float(ever_hit.mean())

def measure(x0, x):
    out = {"frozen_scar_bits": ent_of(x.astype(np.int64) - x0.astype(np.int64))}
    order = np.argsort(x, kind="stable")
    xs = x[order].astype(np.int64)
    ranks = np.empty(N, dtype=np.int64)
    ranks[order] = np.arange(N, dtype=np.int64)
    out["label_perm_bits"] = ent_of(ranks - np.arange(N, dtype=np.int64))
    resid = {}
    for m in M_LIST:
        resid[str(m)] = ent_of(xs - knots_program(xs, m))
    prog = {str(m): 32.0 * m / N for m in M_LIST}
    tot = {k: resid[k] + prog[k] for k in resid}
    m_star = min(tot, key=tot.get)
    out["resid_bits"] = resid
    out["prog_bits"] = prog
    out["floor_total_bits"] = tot[m_star]
    out["m_star"] = int(m_star)
    out["resid_star_bits"] = resid[m_star]
    out["resid_262144_bits"] = resid["262144"]
    out["spread_cells"] = float(np.std(x.astype(np.int64) - x0.astype(np.int64)))
    return out

# ---- tail moments control (P0) -------------------------------------------------
moments = {}
for name in ("T1", "T2"):
    rng = np.random.default_rng(99)
    mag = np.abs(jump_mag(rng, 10_000_000, LAWS[name]))
    moments[name] = {"E_D2": float((mag.astype(np.float64) ** 2).mean()),
                     "median": float(np.median(mag))}
print("tail moments:", json.dumps(moments))

# ---- the three runs ------------------------------------------------------------
AUTHOR_RUN1 = [  # results.json run 1 of 20261011-0006-fermi-2a9d, for the G assertion
    (1, 2.1395, 2.2532, 1.7555), (2, 2.6673, 2.6322, 2.4617), (4, 3.2179, 2.9843, 3.1231),
    (8, 3.8028, 3.2734, 3.7706), (16, 4.4405, 3.5994, 4.4472), (32, 5.1603, 4.0712, 5.1896),
    (64, 5.9745, 4.4318, 6.0097), (128, 6.8787, 4.801, 6.9062), (256, 7.8021, 5.0828, 7.8167),
    (512, 8.6144, 5.374, 8.6161), (1024, 9.2496, 5.5922, 9.2472), (2048, 9.7798, 5.8724, 9.7775),
    (4096, 10.2865, 6.0729, 10.2846), (8192, 10.7868, 6.3162, 10.7853)]

out = {"N": N, "T": T, "s": S, "r_enc": R_ENC, "cap": CAP, "m_list": list(M_LIST),
       "moments": moments, "runs": []}
for name in ("G", "T1", "T2"):
    rng = np.random.default_rng(20261011)
    print(f"evolving law {name} ...", flush=True)
    x0, snaps, ever_hit = evolve(LAWS[name], rng)
    run = {"law": name, "ever_hit_frac": ever_hit, "points": []}
    for tt in sorted(snaps):
        m = measure(x0, snaps[tt])
        m["t"] = tt
        run["points"].append(m)
    if name == "G":  # author's H_delta block, same draw order, for the bit-match check
        d1 = np.rint(rng.normal(0.0, S, N))
        dj = d1.copy()
        hit = rng.random(N) < R_ENC
        dj[hit] += np.rint(rng.normal(0.0, LAWS["G"]["J"], int(hit.sum())))
        run["H_delta_bits"] = ent_of(d1)
        run["H_delta_with_jumps_bits"] = ent_of(dj)
        run["H_jump_bits"] = ent_of(np.rint(rng.normal(0.0, LAWS["G"]["J"], N)))
    out["runs"].append(run)

# G bit-match assertion against the author's record (P1)
g = out["runs"][0]
ok = len(g["points"]) == 14 and abs(g["H_delta_bits"] - 2.1047938061630695) < 1e-9
for p, (tt, f, r256, lab) in zip(g["points"], AUTHOR_RUN1):
    ok &= p["t"] == tt and abs(p["frozen_scar_bits"] - f) < 1e-4 \
          and abs(p["resid_bits"]["256"] - r256) < 1e-4 \
          and abs(p["label_perm_bits"] - lab) < 1e-4
print("G bit-match vs author run 1:", "PASS" if ok else "FAIL")
out["G_reproduction_pass"] = bool(ok)

with open("totals.json", "w") as f:
    json.dump(out, f, indent=1)

for run in out["runs"]:
    print(f"\n== law {run['law']}  ever_hit={run['ever_hit_frac']:.3f}")
    print("   t  frozen  label  floor  m*   resid*  prog*  resid@262144  spread"
          "  noRelabel")
    for p in run["points"]:
        nr = p["resid_star_bits"] + p["label_perm_bits"] + p["prog_bits"][str(p["m_star"])]
        print(f"{p['t']:6d} {p['frozen_scar_bits']:6.2f} {p['label_perm_bits']:6.2f} "
              f"{p['floor_total_bits']:6.2f} {p['m_star']:6d} {p['resid_star_bits']:6.2f} "
              f"{p['prog_bits'][str(p['m_star'])]:6.3f} {p['resid_262144_bits']:6.2f} "
              f"{p['spread_cells']:9.0f} {nr:6.2f}")
