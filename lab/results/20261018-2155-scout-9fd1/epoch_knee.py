#!/usr/bin/env python3
"""epoch_knee.py — the epoch rule's knee, pooled (run 20261018-2155-scout-9fd1).

Toy of the encounters epoch rule (08d0's named follow-up). A pair is a due-distance
D (ticks x 2^16) closed by a drift dd (ticks x 2^16 per kick); a hit lands when
D <= w/2. Every kick applies a quantum +/- sigma to dd (the belt's quantum kick,
e87d's delta-d). Every E kicks the tier re-arms EXACTLY from the current (D, dd):
j_cert = (D - w/2)/dd; a hit is CAUGHT iff the last re-arm certified j_cert <= E
(the due was scheduled); otherwise it is MISSED until the next re-arm (a leak).

Integer-valued float64 throughout (all magnitudes < 2^53, add/sub exact). Floats
explore; the design rule is stated in integers at the end.

Wiki-sourced constants: w = 23 ticks; d in [1.5,6]e5; 08d0's quantum p95-relative
size kappa ~ 0.08 of dd (e87d: delta-d p50 2.4e4 ticks at d ~ 3e5, i.e. ~8% of a
3.75e5-tick mean due at j0 ~ 1e6). j0 drawn log-uniform, geometric mean 1e5 (a 10x
time acceleration vs 08d0's 1e6, disclosed; the knee law is in kicks and needs
knee << j0, which holds: 150 << 1e5 as 150 << 1e6 to within the log).
"""
import numpy as np, sys, time

SCALE = 2 ** 16
W2 = 11.5 * SCALE                 # w/2 in toy units (w = 23 ticks)
DMIN, DMAX = 1.5e5 * SCALE, 6e5 * SCALE
J0_LO, J0_HI = 2.5e4, 4e5         # log-uniform, geo-mean 1e5
NPAIRS = 800

def run(seed, E, kappa_med, horizon, never_arm=False):
    rng = np.random.default_rng(seed)
    j0 = np.exp(rng.uniform(np.log(J0_LO), np.log(J0_HI), NPAIRS))
    dd = (rng.uniform(DMIN, DMAX, NPAIRS)) / j0
    D = W2 + j0 * rng.uniform(0, 1, NPAIRS) * dd   # stationary residual (size-biased)
    sigma = kappa_med * np.median(dd)   # one fixed quantum size per arm
    armed = np.zeros(NPAIRS, bool)
    hits = leaks = 0
    pph = np.zeros(NPAIRS); ppl = np.zeros(NPAIRS)
    for t in range(horizon):
        if not never_arm and t % E == 0:              # exact re-arm every E kicks
            armed = ((D - W2) / dd) <= E
        D = D - dd
        dd = dd + sigma * rng.integers(0, 2, NPAIRS) * 2 - sigma
        np.maximum(dd, sigma, out=dd)      # keep drift positive (disclosed)
        h = D <= W2
        if h.any():
            nh = int(h.sum())
            hits += nh
            lk = int((~armed[h]).sum())
            leaks += lk
            pph += h; ppl += h & ~armed
            D[h] = rng.uniform(DMIN, DMAX, nh)   # re-deal the next conjunction
    return dict(hits=hits, leaks=leaks, horizon=horizon, pph=pph, ppl=ppl)

def main():
    t0 = time.time()
    kappas = [0.04, 0.08, 0.16]
    Es = [8, 16, 32, 64, 96, 128, 192, 256, 384, 512, 1024, 2048, 4096]
    seeds = [1, 2, 777]
    out = sys.argv[1] if len(sys.argv) > 1 else "epoch_knee.csv"
    rows = []
    for kap in kappas:                       # controls (P1, P2)
        r = run(1, 10 ** 9, kap, 4096, never_arm=True)
        assert r["leaks"] == r["hits"] and r["hits"] > 0, "P2 control failed"
        rows.append(("noarm", kap, None, 1, r["leaks"], r["hits"], 4096))
        r = run(1, 1, kap, 4096)
        assert r["leaks"] == 0, "P1 control failed"
        rows.append(("E1", kap, 1, 1, 0, r["hits"], 4096))
    for kap in kappas:                       # decisive grid (run once)
        for E in Es:
            L = H = 0; HZ = 0
            for s in seeds:
                r = run(s, E, kap, horizon=min(12288, max(6144, 3 * E)))
                L += r["leaks"]; H += r["hits"]; HZ = r["horizon"]
            rows.append(("grid", kap, E, len(seeds), L, H, HZ))
    with open(out, "w") as f:
        f.write("arm,kappa,E,seeds,leaks,hits,pair_kicks,leak_per_pair_kick\n")
        for a, kap, E, ns, L, H, hz in rows:
            pk = ns * hz * NPAIRS
            f.write(f"{a},{kap},{E},{ns},{L},{H},{pk},{(L/pk if E else float('nan')):.3e}\n")
    # knee readout
    print("== pooled-zero knee ==")
    for kap in kappas:
        knee = max([E for E in Es if next(r for r in rows if r[0] == "grid"
                    and r[1] == kap and r[2] == E)[4] == 0] or [0])
        print(f"kappa={kap}: E_knee = {knee}")
    # P6 grazer clustering, above-knee cells at base kappa (fresh seed 5)
    print("== P6 top-decile(by hits) leak share ==")
    for E in [512, 1024]:
        r = run(5, E, 0.08, 12288)
        if r["leaks"] == 0:
            print(f"E={E}: 0 leaks"); continue
        idx = np.argsort(r["pph"])[::-1]
        top = idx[: NPAIRS // 10]
        print(f"E={E}: leaks={r['leaks']} top-decile share="
              f"{r['ppl'][top].sum() / max(r['ppl'].sum(), 1):.2f}")
    print(f"wrote {out}; {time.time()-t0:.1f}s")

if __name__ == "__main__":
    main()
