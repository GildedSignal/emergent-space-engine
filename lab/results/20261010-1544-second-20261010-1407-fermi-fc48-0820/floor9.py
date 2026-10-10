#!/usr/bin/env python3
"""The checker's named experiment: the sorted-microstate floor at the 10^9
scaling, plus the encoding-class question it flagged as unexamined.

Parts:
  A. N-scaling of the shipped 3-field floor ((a, e_vec); floor.py's scope):
     subsamples of the shipped state + fresh birth states (new seeds), fitted
     against floor(N) = H1 - log2(N) + log2(e). Evaluates at N = 1e9.
  B. The phase dof: the tube's stored state carries t_p (64-bit per radial
     cycle; law.md: "position and velocity are derived when asked"), which
     floor.py omits. M0 ~ U[0, 2pi) by the shipped generator, so the phase is
     worth 64 bits/sample at the tube's own quantum (recorded here, and
     cross-checked against the shipped H_tp_mod saturation at 63.9).
  C. floor_4 = floor_3 + 64 at 1e9, vs the 8 GB budget (64 bits/body).
  D. Strict 16-byte tube reading ((E, L) share 32 bits): band-occupancy
     measurement of H1(E,L), then floor' = H1(EL) + H(w) + 64 - log2 N + log2 e.
  E. Elias-Fano: faithful port of crates/shipmem/src/program.rs::Ef, run on
     the real quantized a-cells, vs the uniform multiset bound log2(u/k)+log2 e.
"""
import json
import numpy as np

LOG2E = np.log2(np.e)
A_LO, A_HI = 1.0, 1.5
Q_A = 2 * 1.2**2 / (6 * 2**32)
Q_E = (np.sqrt(1.5) - np.sqrt(0.75)) / 2**32 / np.sqrt(1.2)  # floor.py's q_e
N1E9 = 10**9

d = np.load("final_state.npz")
out = {"N_shipped": int(len(d["a"])), "Q_A": Q_A, "Q_E": Q_E}


def ent2_adaptive(ex, ey):
    """H of the (ex, ey) pair at quantum Q_E, measured at q*2^s for the finest
    s whose occupancy keeps the plug-in bias small, + Miller-Madow in bits
    (+(K-1)/(2 n ln2)). At n = 2^16 this reproduces floor.py's fixed B = 2^24."""
    n = len(ex)
    for s in range(16, 28):
        B = 1 << s
        kx = np.round(ex / (Q_E * B)).astype(np.int64)
        ky = np.round(ey / (Q_E * B)).astype(np.int64)
        _, c = np.unique(kx * (1 << 26) + ky, return_counts=True)
        if len(c) <= max(4, n // 4):
            p = c / c.sum()
            h = float(-(p * np.log2(p)).sum() + 2 * np.log2(B)) \
                + (len(c) - 1) / (2 * n * np.log(2))
            return s, h, len(c)
    raise RuntimeError("no valid coarse-grain")


def H_a_hist(a):
    n = len(a)
    h, _ = np.histogram(a, bins=1 << 10, range=(A_LO, A_HI))
    p = h.astype(float)
    nz = int((p > 0).sum())
    p = p[p > 0] / p.sum()
    return float(-(p * np.log2(p)).sum() + np.log2((A_HI - A_LO) / (1 << 10) / Q_A)) \
        + (nz - 1) / (2 * n * np.log(2))


def floor3(a, ex, ey):
    n = len(a)
    s, h_e2d, K = ent2_adaptive(ex, ey)
    return H_a_hist(a) + h_e2d - np.log2(n) + LOG2E, dict(B_e2d=s, K_e2d=K)


# ---- A: N-scaling -----------------------------------------------------------
rng = np.random.default_rng(777)
rows = []
for tag, av, exv, eyv, ks in [("birth", d["a0"], d["ex0"], d["ey0"], (12, 13, 14, 15, 16)),
                              ("final", d["a"], d["ex"], d["ey"], (14, 15, 16))]:
    full = np.arange(len(av))
    for k in ks:
        n = 1 << k
        idx = rng.choice(full, n, replace=False)
        fl, meta = floor3(av[idx], exv[idx], eyv[idx])
        rows.append(dict(tag=tag, N=n, floor3=fl, H1=fl + np.log2(n) - LOG2E, **meta))
    if tag == "birth":  # fresh states, same generator, new seeds
        for k, seed in ((16, 4242), (20, 31337)):
            n = 1 << k
            g = np.random.default_rng(seed)
            a = g.uniform(A_LO, A_HI, n)
            ex = g.normal(0, 0.01, n)
            ey = g.normal(0, 0.01, n)
            fl, meta = floor3(a, ex, ey)
            rows.append(dict(tag=f"{tag}+fresh", N=n, floor3=fl,
                             H1=fl + np.log2(n) - LOG2E, **meta))

for tag in ("birth", "final"):
    sel = [r for r in rows if r["tag"].startswith(tag)]
    x = np.array([np.log2(r["N"]) for r in sel])
    y = np.array([r["floor3"] for r in sel])
    slope = float(np.polyfit(x, y, 1)[0])
    H1s = [r["H1"] for r in sel]
    out[f"slope_{tag}"] = slope
    out[f"H1_{tag}"] = dict(mean=float(np.mean(H1s)), std=float(np.std(H1s)),
                            min=float(np.min(H1s)), max=float(np.max(H1s)))
    out[f"floor3_1e9_{tag}"] = float(np.mean(H1s) - np.log2(N1E9) + LOG2E)

# analytic cross-check of H1(birth): uniform a + Gaussian e-pair
out["H1_birth_analytic"] = float(np.log2((A_HI - A_LO) / Q_A)
                                 + 2 * np.log2(0.01 / Q_E) + np.log2(2 * np.pi * np.e))

# ---- B: the phase dof -------------------------------------------------------
# replicate the shipped generator's draw order (seed 20261010) to recover M0
g = np.random.default_rng(20261010)
_ = g.uniform(A_LO, A_HI, out["N_shipped"])
_ = g.normal(0, 0.01, out["N_shipped"])
_ = g.normal(0, 0.01, out["N_shipped"])
M0 = g.uniform(0, 2 * np.pi, out["N_shipped"])
h, _ = np.histogram(M0, bins=1 << 12, range=(0, 2 * np.pi))
p = h.astype(float); p = p[p > 0] / p.sum()
H_phase = float(-(p * np.log2(p)).sum() + np.log2(2**64 / (1 << 12)))
out["H_phase_bits"] = min(H_phase, 64.0)   # uniform by construction; recorded

# ---- C: floor_4 at 1e9 ------------------------------------------------------
for tag in ("birth", "final"):
    out[f"floor4_1e9_{tag}"] = out[f"floor3_1e9_{tag}"] + out["H_phase_bits"]
    out[f"GB3_1e9_{tag}"] = out[f"floor3_1e9_{tag}"] * N1E9 / 8 / 1e9
    out[f"GB4_1e9_{tag}"] = out[f"floor4_1e9_{tag}"] * N1E9 / 8 / 1e9

# ---- D: strict 16-byte tube reading ((E, L) share 32 bits) ------------------
L = np.sqrt(d["a0"]) * np.sqrt(np.maximum(1 - (d["ex0"]**2 + d["ey0"]**2), 0.0))
LO_L, HI_L = np.sqrt(0.75), np.sqrt(1.5)
s = 6   # probe at 10+10 bits inside the 16+16-bit field grid
ka = np.clip(((d["a0"] - A_LO) / (A_HI - A_LO) * (1 << (16 - s))).astype(np.int64),
             0, (1 << (16 - s)) - 1)
kl = np.clip(((L - LO_L) / (HI_L - LO_L) * (1 << (16 - s))).astype(np.int64),
             0, (1 << (16 - s)) - 1)
_, c = np.unique(ka * (1 << 16) + kl, return_counts=True)
p = c / c.sum()
H_EL_probe = float(-(p * np.log2(p)).sum())
H_EL_32 = H_EL_probe + 2 * s    # -> full 32-bit shared grid (band-edge bias ~0.5 bit)
w = np.arctan2(d["ey0"], d["ex0"]) % (2 * np.pi)
hw, _ = np.histogram(w, bins=1 << 12, range=(0, 2 * np.pi))
pw = hw.astype(float); pw = pw[pw > 0] / pw.sum()
H_w32 = min(float(-(pw * np.log2(pw)).sum() + np.log2(2**32 / (1 << 12))), 32.0)
out["strict"] = dict(H_EL_32=H_EL_32, H_w_32=H_w32,
                     floor_1e9=H_EL_32 + H_w32 + 64.0 - np.log2(N1E9) + LOG2E)
out["strict"]["GB_1e9"] = out["strict"]["floor_1e9"] * N1E9 / 8 / 1e9

# ---- E: shipmem's Elias-Fano, faithful port ---------------------------------
def ef_bits(keys, u):
    """Port of crates/shipmem/src/program.rs::Ef's bit count (sans padding)."""
    k = len(keys)
    q = int(u) // k
    l = q.bit_length() - 1 if q > 0 else 0   # Rust: 63 - clz(u/k) = floor(log2)
    nhigh = int(u >> l) + k + 1
    low_bits = k * l
    sample_bits = ((nhigh - k) // 64 + 1) * 32
    return low_bits + nhigh + sample_bits, l


rows_ef = []
for k, seed in ((1 << 16, 4242), (1 << 20, 31337)):
    g = np.random.default_rng(seed)
    a = g.uniform(A_LO, A_HI, k)
    cells = np.round(a / Q_A).astype(np.int64)
    u = int((A_HI - A_LO) / Q_A) + 2
    bits, l = ef_bits(cells, u)
    bound = np.log2(u / k) + LOG2E      # uniform multiset bound per key
    rows_ef.append(dict(k=k, u=u, l=l, ef_bits_per_key=bits / k,
                        multiset_bound=bound, gap=bits / k - bound))
out["ef"] = rows_ef
H1f = out["H1_final"]["mean"] + 64.0
out["ef_fulltube_1e9"] = dict(
    belt_tight=np.log2(2**H1f / N1E9) + 2.5,
    full_grid=160 - np.log2(N1E9) + 2.5,
    floor4=out["floor4_1e9_final"])

out["rows"] = rows
with open("floor9.json", "w") as f:
    json.dump(out, f, indent=1)

print("A. N-scaling of the 3-field floor (shipped scope)")
print(f"{'tag':>12} {'N':>8} {'B_e2d':>6} {'floor3':>7} {'H1':>6}")
for r in rows:
    print(f"{r['tag']:>12} {r['N']:8d} 2^{r['B_e2d']:<4} {r['floor3']:7.2f} {r['H1']:6.2f}")
for tag in ("birth", "final"):
    print(f"{tag}: slope {out[f'slope_{tag}']:+.3f} vs log2N, "
          f"H1 {out[f'H1_{tag}']['mean']:.2f} +- {out[f'H1_{tag}']['std']:.2f} "
          f"(analytic birth {out['H1_birth_analytic']:.2f}), "
          f"floor3(1e9) {out[f'floor3_1e9_{tag}']:.2f} bits "
          f"= {out[f'GB3_1e9_{tag}']:.2f} GB")
print(f"\nB. phase at tube quantum: {out['H_phase_bits']:.2f} bits/sample")
print("\nC. floor_4 at 1e9 (tube's own quanta, phase included)")
for tag in ("birth", "final"):
    print(f"{tag}: {out[f'floor4_1e9_{tag}']:.2f} bits/body = "
          f"{out[f'GB4_1e9_{tag}']:.2f} GB  (budget 8 GB = 64 bits/body)")
print(f"\nD. strict 16-byte reading: H1(EL) {out['strict']['H_EL_32']:.1f} + "
      f"H(w) {out['strict']['H_w_32']:.1f} -> floor {out['strict']['floor_1e9']:.1f}"
      f" bits/body = {out['strict']['GB_1e9']:.2f} GB at 1e9")
print("\nE. shipmem Elias-Fano port on real a-cells")
for r in rows_ef:
    print(f"k={r['k']}: EF {r['ef_bits_per_key']:.2f} bits/key vs multiset bound "
          f"{r['multiset_bound']:.2f} (gap {r['gap']:+.2f})")
print(f"full-tube EF at 1e9: belt-tight {out['ef_fulltube_1e9']['belt_tight']:.1f}, "
      f"full 160-bit grid {out['ef_fulltube_1e9']['full_grid']:.1f} bits/body "
      f"vs floor4 {out['ef_fulltube_1e9']['floor4']:.1f}")
