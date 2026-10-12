#!/usr/bin/env python3
"""H_live falsifier: per-body bit production in a resonance-structured belt.

Universal local form per body (driven pendulum, the normal form of a
mean-motion resonance with the e_J-forced secondary term):
    H = P^2/2 - cos(psi) + A cos(psi - tau)
Birth elements -> dimensionless detuning D = |n - n_res|/W -> birth energy
E0 = -1 + 2D in the unit pendulum (bottom -1, separatrix +1, circulate beyond).
The program stores quantized birth constants; the twin offset d0 = 1e-12 models
that birth quantum, so the free twin's spread is the body's departure from its
program.  lambda_ren: renormalized twin (shear-biased for regular rotators).
Chaotic/regular classified from the FREE twin's bits(t) shape (exponential vs
log growth); lambda_bit from its slope.  Known distortions, disclosed in the
dossier: libration period == drive period (real belts ~10^2 slower; fattens the
chaotic layer, biasing TOWARD the fat-tail claim on amounts, not on
concentration), and no secular/three-body chaos off resonance (underestimates
the baseline; lens limit).
"""
import json, os, sys, time
import numpy as np
from concurrent.futures import ProcessPoolExecutor

D0 = 1e-12
CAP = np.log2(2 * np.pi / D0)          # macrostate saturation bits (~42.5)
HERE = os.path.dirname(os.path.abspath(__file__))

def belt(rng, n=4096, amin=2.1, amax=3.3, esc=0.05):
    return rng.uniform(amin, amax, n), rng.rayleigh(esc, n)

def resonances(aJ=5.2):
    """(p, q, a_res) reduced, interior to Jupiter; n_res = (p/q) n_J."""
    from math import gcd
    out = []
    for q in range(1, 8):
        for p in range(q + 1, 13):
            if gcd(p, q) != 1:
                continue
            ares = aJ * (q / p) ** (2.0 / 3.0)
            if 1.6 < ares < 3.6:
                out.append((p, q, ares))
    return out

def assign(a, e, eJ=0.048, mu=9.55e-4, cw=None):
    """Nearest resonance in units of its own width. Returns D, Chirikov C."""
    if cw is None:
        cw = np.sqrt(16.0 / 3.0)        # UNVERIFIED prefactor; +-2x control
    n = a ** -1.5
    nJ = 5.2 ** -1.5
    eeff = np.maximum(e, eJ)
    res = resonances()
    nres = np.array([p / q * nJ for (p, q, _) in res])
    ii = np.arange(len(a))
    Dall = np.empty((len(res), len(a)))
    Wall = np.empty_like(Dall)
    for k, (p, q, _) in enumerate(res):
        d = p - q                        # resonance order
        W = cw * np.sqrt(mu) * eeff ** (d / 2.0)   # relative half-width
        Wall[k] = W
        Dall[k] = np.abs(n - nres[k]) / nres[k] / W
    jbest = np.argmin(Dall, axis=0)
    D = Dall[jbest, ii]
    order = np.argsort(Dall, axis=0)
    k1, k2 = order[0], order[1]
    dn = np.abs(nres[k1] - nres[k2])
    C = (Wall[k1, ii] * nres[k1] + Wall[k2, ii] * nres[k2]) / np.maximum(dn, 1e-12)
    pres = np.array([res[j][0] for j in jbest])
    return D, C, pres

def run_chunk(arg):
    """Integrate bodies + twins for one chunk. Deterministic per body."""
    (psi0, P0, A, periods, dtfrac, cps) = arg
    n = len(psi0)
    dt = 2 * np.pi / dtfrac
    steps = int(periods * dtfrac)
    rng = np.random.default_rng(12345)  # phase signs drawn in parent, not here
    psi = np.concatenate([psi0, psi0, psi0])
    P = np.concatenate([P0, P0 + D0, P0 + D0])
    lam_acc = np.zeros(n)
    bits = np.zeros((cps, n))
    cp_every = steps // cps
    ren_every = dtfrac
    tau = 0.0
    for step in range(steps):
        psi += dt * P
        P += dt * (-np.sin(psi) + A * np.sin(psi - tau))
        tau += dt
        if (step + 1) % 4 == 0:
            psi = np.mod(psi + np.pi, 2 * np.pi) - np.pi
        if (step + 1) % ren_every == 0:
            b, r, pb, pr = psi[:n], psi[n:2*n], P[:n], P[n:2*n]
            dd = np.hypot(np.mod(r - b + np.pi, 2*np.pi) - np.pi, pr - pb)
            lam_acc += np.log(np.maximum(dd, 1e-14) / D0)
            sc = D0 / np.maximum(dd, 1e-14)
            psi[n:2*n] = np.mod(b + sc * (np.mod(r - b + np.pi, 2*np.pi) - np.pi) + np.pi,
                                2 * np.pi) - np.pi
            P[n:2*n] = pb + sc * (pr - pb)
        if (step + 1) % cp_every == 0:
            b, f, pb, pf = psi[:n], psi[2*n:], P[:n], P[2*n:]
            df = np.hypot(np.mod(f - b + np.pi, 2*np.pi) - np.pi, pf - pb)
            bits[(step + 1) // cp_every - 1] = np.minimum(
                np.log2(np.maximum(df, 1e-300) / D0), CAP)
    return lam_acc / (periods * 2 * np.pi), bits

def classify(bits, cp_t):
    """chaotic | saturated | regular; lambda_bit from free-twin slope."""
    n = bits.shape[1]
    lam_bit = np.zeros(n)
    r2 = np.zeros(n)
    sat = bits[-1] >= CAP - 0.5
    chaotic = sat.copy()
    for i in range(n):
        y = bits[:, i]
        ok = y < CAP - 1.0
        if ok.sum() >= 4:
            t = cp_t[ok]; yy = y[ok]
            slope = np.polyfit(t, yy, 1)[0]
            pred = np.polyval((slope, np.polyfit(t, yy, 1)[1]), t)
            r2[i] = 1.0 - np.sum((yy - pred)**2) / max(np.sum((yy - yy.mean())**2), 1e-12)
            if slope >= 1e-3 and y[-1] >= 20.0:
                chaotic[i] = True
                if not sat[i]:
                    lam_bit[i] = slope / np.log2(np.e)
            elif sat[i]:
                lam_bit[i] = slope / np.log2(np.e)
    # saturated: lower bound from time to reach cap
    for i in np.where(sat & (lam_bit == 0))[0]:
        y = bits[:, i]
        k = np.argmax(y >= CAP - 0.5)
        t0 = cp_t[0] if k == 0 else cp_t[k - 1]
        y0 = y[0] if k == 0 else y[k - 1]
        lam_bit[i] = max(0.0, (CAP - y0)) / max(cp_t[k] - t0, 1.0) / np.log2(np.e)
    return chaotic, sat, lam_bit, r2

def gini(x):
    x = np.sort(np.maximum(x, 0.0)); n = len(x); s = x.sum()
    if s <= 0: return 0.0
    i = np.arange(1, n + 1)
    return float((2*np.sum(i*x)/(n*s)) - (n + 1)/n)

def top_share(x, frac):
    x = np.maximum(x, 0.0); s = x.sum()
    if s <= 0: return 0.0
    k = max(1, int(round(frac*len(x))))
    return float(np.sort(x)[-k:].sum()/s)

def spearman(x, y):
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    return float(np.corrcoef(rx, ry)[0, 1])

def main(periods=10000, A=0.15, cw=None, tag="main", n=4096, workers=6):
    rng = np.random.default_rng(20261012)
    a, e = belt(rng, n)
    D, C, pres = assign(a, e, cw=cw)
    # birth ICs (deterministic, in parent)
    E0 = -1.0 + 2.0 * np.minimum(D, 3.0)   # local form valid within ~3 widths (VOID fix)
    psi0 = np.empty(n); P0 = np.empty(n)
    inside = E0 < 1.0
    psi0[inside] = rng.uniform(-1, 1, inside.sum()) * np.arccos(np.clip(-E0[inside], -1, 1))
    psi0[~inside] = rng.uniform(-np.pi, np.pi, (~inside).sum())
    P0 = np.sqrt(np.maximum(0.0, 2 * (E0 + np.cos(psi0)))) * np.where(rng.random(n) < 0.5, 1. - 0., -1.)
    cps = 16
    chunks = np.array_split(np.arange(n), workers)
    args = [(psi0[idx], P0[idx], A, periods, 32, cps) for idx in chunks]
    t0 = time.perf_counter()
    with ProcessPoolExecutor(max_workers=workers) as ex:
        outs = list(ex.map(run_chunk, args))
    wall = time.perf_counter() - t0
    lam_ren = np.concatenate([o[0] for o in outs])
    bits = np.concatenate([o[1] for o in outs], axis=1)
    cp_t = np.linspace(periods / cps, periods, cps)
    chaotic, sat, lam_bit, r2 = classify(bits, cp_t)
    b_end = bits[-1]
    i1 = int(np.abs(cp_t - 1000).argmin())
    i3 = int(np.abs(cp_t - 3000).argmin())
    if i3 == i1:
        i3 = min(i1 + 1, cps - 1)
    early_flow = (bits[i3] - bits[i1]) / (cp_t[i3] - cp_t[i1])
    near = D <= 1.0
    far = D > 3.0
    sep = D < 1.5
    b_reg = float(np.median(b_end[~chaotic])) if (~chaotic).any() else 0.0
    excess = np.maximum(0.0, b_end - b_reg)
    unsat_ch = chaotic & ~sat
    pesin_ratio = b_end[unsat_ch] / (lam_ren[unsat_ch] * periods * np.log2(np.e)) \
        if unsat_ch.any() else np.array([])
    out = {
        "tag": tag, "n": n, "periods": periods, "A": A, "cw": cw,
        "wall_s": round(wall, 1), "seed_belt": 20261012, "sat_cap_bits": CAP,
        "frac_near_D_le_1": float(near.mean()),
        "frac_chaotic": float(chaotic.mean()), "frac_saturated": float(sat.mean()),
        "frac_regular": float((~chaotic).mean()),
        "b_reg_bits": b_reg,
        "gini_total_stock": gini(b_end),
        "top1pct_total_stock": top_share(b_end, 0.01),
        "gini_excess": gini(excess),
        "top1pct_excess": top_share(excess, 0.01),
        "top5pct_excess": top_share(excess, 0.05),
        "gini_early_flow": gini(early_flow),
        "top1pct_early_flow": top_share(early_flow, 0.01),
        "P2_free_slope_median_R2_chaotic": float(np.median(r2[chaotic])) if chaotic.any() else None,
        "P2_free_slope_min_R2_chaotic": float(r2[chaotic].min()) if chaotic.any() else None,
        "P2_neg_control_frac_far_slow": float((early_flow[far] < 1e-3).mean()) if far.any() else None,
        "P2_neg_control_max_flow_far": float(early_flow[far].max()) if far.any() else None,
        "ctrl_chaotic_frac_sep_D_lt_1p5": float(chaotic[sep].mean()) if sep.any() else None,
        "ctrl_chaotic_frac_far_D_gt_3": float(chaotic[far].mean()) if far.any() else None,
        "ctrl_min_lam_bit_chaotic": float(lam_bit[chaotic].min()) if chaotic.any() else None,
        "P3_share_excess_D_le_2": float(excess[D <= 2].sum() / excess.sum()) if excess.sum() > 0 else None,
        "P3_frac_bodies_D_le_2": float((D <= 2).mean()),
        "P3_excess_share_D_gt_2": float(excess[D > 2].sum() / excess.sum()) if excess.sum() > 0 else None,
        "P4_n_overlap_C_ge_1": int((C >= 1).sum()),
        "P4_gini_overlap_excess": gini(excess[C >= 1]) if (C >= 1).any() else None,
        "P4_gini_nonoverlap_excess": gini(excess[C < 1]) if (C < 1).any() else None,
        "spearman_lam_vs_D": spearman(lam_bit, D),
        "median_lam_bit": float(np.median(lam_bit)),
        "mean_bits_end": float(b_end.mean()), "max_bits_end": float(b_end.max()),
        "bits_end_p99": float(np.percentile(b_end, 99)),
        "median_bits_chaotic": float(np.median(b_end[chaotic])) if chaotic.any() else None,
        "median_bits_regular": b_reg,
    }
    with open(f"{HERE}/summary-{tag}.json", "w") as f:
        json.dump(out, f, indent=1)
    np.savez_compressed(f"{HERE}/perbody-{tag}.npz", a=a, e=e, D=D, C=C, pres=pres,
                        lam_ren=lam_ren, lam_bit=lam_bit, bits_end=b_end,
                        chaotic=chaotic, sat=sat)
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    periods = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    A = float(sys.argv[2]) if len(sys.argv) > 2 else 0.15
    cw = float(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3] != "d" else None
    tag = sys.argv[4] if len(sys.argv) > 4 else "main"
    main(periods, A, cw, tag)
