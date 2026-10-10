#!/usr/bin/env python3
"""Post-processing v2 (v1 read zeros left by dropped pairs as encounters).

Kick spectrum from the measured encounter MC, the quantum-crossing rate
(H_live), closed-form checks, and the design table.

Units: a=1, v_K=1, star mass 1; rate per body per orbit; orbit at 1 AU =
3.156e7 s. Scar = one body's difference from its program: 128 bits payload +
~40 bits Elias-Fano index = 168 bits; an encounter scars 2 bodies = 336 bits.
Budget: 8 GB / 1e9 bodies = 64 bits/body (also the approved 4 GiB -> 32).
"""
import json
import numpy as np

YEAR = 3.156e7
SCAR_BITS = 336.0
BUDGET_BITS = 64.0
N0 = 1e4
W = 0.02
SIG = 0.01
RHO = 1e-4


def load_clean(raw, tag, rho):
    """b_min, v_rel for kept pairs only (dropped pairs sit at exactly 0)."""
    b = np.array(raw[tag]["bmin_flat"]).ravel()
    v = np.array(raw[tag]["vrel_flat"]).ravel()
    ok = b > 0
    return b[ok], v[ok]


def main():
    raw = json.load(open("hlive_raw.json"))
    Lam = {t: {r: raw[t]["Lambda"][str(r)] for r in (1e-4, 1e-3)}
           for t in ("cold", "hot")}

    print("== measured (reference belt W=0.02, N=1e4) ==")
    for tag in ("cold", "hot"):
        b, v = load_clean(raw, tag, RHO)
        enc = b < RHO
        p_half = np.mean(b[enc] < RHO / 2)
        v_enc = np.mean(v[enc])
        v_enc_med = np.median(v[enc])
        print(f"  [{tag}] Lambda(1e-4)={Lam[tag][1e-4]:.3f} "
              f"Lambda(1e-3)={Lam[tag][1e-3]:.3f}/orbit | encounters: "
              f"P(b<rho/2)={p_half:.3f} <v_rel>={v_enc:.4f} "
              f"median={v_enc_med:.4f} n_enc={enc.sum()}")
    b_raw = np.array(raw["cold"]["bmin_flat"]).ravel()
    v_raw = np.array(raw["cold"]["vrel_flat"]).ravel()
    v_enc = float(np.mean(v_raw[(b_raw > 0) & (b_raw < RHO)]))

    # ---- P5: crossing rate from the measured joint (b, v) vs product formula
    print("\n== P5: R(q) integrated over measured (b, v) vs product ==")
    edges = np.array(raw["cold"]["edges"])
    weight = np.array(raw["cold"]["weight"])
    centers = np.sqrt(edges[:-1] * edges[1:])
    widths = np.diff(edges)
    n1D = N0 / W
    nb, ppb = len(centers), b_raw.size // len(centers)
    bb = b_raw.reshape(nb, ppb)
    vv = v_raw.reshape(nb, ppb)
    for M_belt in (1e-7, 1e-5):
        m = M_belt / N0
        for q in (1e-6, 1e-5, 1e-4):
            # exact: per-bin P(b<rho AND 2m/(b v) > q)
            contrib = []
            for i in range(len(centers)):
                if weight[i] == 0:
                    contrib.append(0.0)
                    continue
                kept = bb[i] > 0
                dv = 2 * m / (np.maximum(bb[i][kept], 1e-12) * vv[i][kept])
                p = np.mean((bb[i][kept] < RHO) & (dv > q))
                contrib.append(p * weight[i] * 1.5 * centers[i] * widths[i])
            R_exact = 2 * n1D * np.sum(contrib)
            dv_typ = 2 * m / (RHO * v_enc)
            R_prod = Lam["cold"][1e-4] * min(1.0, dv_typ / q)
            print(f"  M={M_belt:.0e} q={q:.0e}: R_exact={R_exact:.4g} "
                  f"R_product={R_prod:.4g} ratio={R_exact/R_prod:.3f}")

    # ---- closed forms
    print("\n== closed forms ==")
    for tag, s in (("cold", SIG), ("hot", 0.1)):
        cf = 0.85 * N0 * RHO * min(s, W) ** 2 / (s * W)
        print(f"  Lambda(1e-4) {tag}: cform {cf:.3f} vs measured "
              f"{Lam[tag][1e-4]:.3f} (ratio {cf/Lam[tag][1e-4]:.3f})")
    print(f"  <v_rel|enc>={v_enc:.4f}; tail cform R=1.7 M sigma_e/(W <v> q_v)")
    # ---- design table: R computed EXACTLY from the measured (b, v) per bin,
    # scaling the kick threshold with m = M/N (b, v are N-independent).
    print("\n== design table: bits per body per hour (scar 336 bits/enc) ==")
    CORR = 2.2  # measured tail correlation: exact/product at the one
    # supported point (M=1e-7, q=1e-4: 36 events, sigma ~ 0.4)

    def R_exact_at(N, q, M_belt):
        m = M_belt / N
        tot = 0.0
        for i in range(nb):
            if weight[i] == 0:
                continue
            kept = bb[i] > 0
            dv = 2 * m / (np.maximum(bb[i][kept], 1e-12) * vv[i][kept])
            p = np.mean((bb[i][kept] < RHO) & (dv > q))
            tot += p * weight[i] * 1.5 * centers[i] * widths[i]
        return 2 * (N / W) * tot

    def R_est(N, q, M_belt):
        """Exact where the MC has support; closed form x CORR in the deep
        tail; never above Lambda(N) (all-encounters cap)."""
        lam = Lam["cold"][1e-4] * N / N0
        cf = CORR * 1.7 * M_belt * SIG / (W * v_enc * q)
        return min(lam, max(R_exact_at(N, q, M_belt), cf))

    hdr = "  %-10s %-10s | %-12s %-12s %-12s | %s" % (
        "M_belt", "q_v", "2^20", "2^23", "1e9", "verdict@1e9")
    print(hdr)
    for M_belt in (1e-7, 1e-5):
        for q in (2.0 ** -32, 1e-6, 1e-5, 1e-4):
            bits = {}
            for N in (2 ** 20, 2 ** 23, 1e9):
                bits[N] = R_est(N, q, M_belt) * (3600 * 100 / YEAR) * SCAR_BITS
            verdict = "FITS" if bits[1e9] < BUDGET_BITS else "BREAKS"
            print("  %-10s %-10.2e | %-12.3g %-12.3g %-12.3g | %s" % (
                f"{M_belt:.0e}", q, bits[2 ** 20], bits[2 ** 23],
                bits[1e9], verdict))

    # quantum boundary: q at which 1e9 belt fits exactly (rtf 100, 1 hr)
    print("\n  minimum live quantum q_v* for the 1e9 belt (rtf 100, 1 hr):")
    for M_belt in (1e-7, 1e-5):
        from scipy.optimize import brentq
        f = lambda q: R_est(1e9, q, M_belt) * (3600 * 100 / YEAR) * SCAR_BITS - BUDGET_BITS
        try:
            qs = brentq(f, 1e-12, 1e-2, xtol=1e-14)
        except Exception:
            # manual bisection (scipy may be absent)
            lo, hi = 1e-12, 1e-2
            for _ in range(200):
                mid = np.sqrt(lo * hi)
                if f(mid) > 0:
                    lo = mid
                else:
                    hi = mid
            qs = np.sqrt(lo * hi)
        print(f"  M={M_belt:.0e}: q_v* = {qs:.3g} v_K  "
              f"({qs*29.8e3:.4g} m/s at 1 AU)")
    print("\n== re-fit cadence (scars die when the program is re-fit) ==")
    print("  scarred fraction = R*T_refit < 64/168 = 0.38:")
    for M_belt in (1e-7, 1e-5):
        for q in (2.0 ** -32, 1e-6, 1e-5):
            R = R_est(1e9, q, M_belt)
            T = 0.38 / R if R > 0 else float("inf")
            print(f"  M={M_belt:.0e} q={q:.0e}: R(1e9)={R:.3g}/orbit "
                  f"T_refit<{T:.3g} orbits ({T*YEAR/86400:.3g} sim-days)")

    print("\n== player-floor check (does q_v erase anything visible?) ==")
    print("  belt at 1 AU: v_K = 29.8 km/s; kicks above q_v are the")
    print("  distinctions kept. Strongest 1-in-400 encounter kick at N=1e4:")
    for M_belt in (1e-7, 1e-5):
        m = M_belt / N0
        dv997 = 2 * m / (RHO / 20 * v_enc)
        print(f"  M={M_belt:.0e}: ~{dv997:.3g} v_K = {dv997*29.8:.3g} km/s")

    json.dump({"v_rel_enc": v_enc,
               "Lambda": {t: Lam[t] for t in Lam}},
              open("hlive_post.json", "w"), indent=1)


if __name__ == "__main__":
    main()
