#!/usr/bin/env python3
"""Falsifier: the additive doll-chain simultaneity key at depth >= 2 with relativistic links.

Premise under attack (representation.md par.1 'Time'; the adoptable key form of ae29/4e9c):
    key(event in doll B) = doll tick + sum over the doll chain of sinh(eta_i) * (axis_i . offset_i)
A *sum of per-link shears*. Exact at depth 1 (P6: worst miss 0.500 tick at beta 0.5) and at
depth 2 moon speed (+/-0.49 tick). The exact map for a chain is a product of Lorentz boosts,
and products of boosts are not sums of shears: the missed cross terms are O(beta1^2 * beta2)
* offset. Units: c = 1; one unit of offset = one light-tick.

Oracle: exact 2+1 Lorentz matrices (numpy float64), no shared code with any engine harness.
Two additive variants are probed (whichever way the chain is read):
  V1  each link's shear evaluated at that link's own offset (the chain-tracking form),
  V2  all shears frozen per entity and evaluated at the grandchild offset (ae29's frozen form).
"""
import json
import numpy as np


def boost(beta: float, theta: float) -> np.ndarray:
    """Boost mapping doll-frame coords to the parent frame, doll moving at +beta along theta."""
    g = 1.0 / np.sqrt(1.0 - beta * beta)
    n = np.array([np.cos(theta), np.sin(theta)])
    M = np.zeros((3, 3))
    M[0, 0] = g
    M[0, 1:] = g * beta * n
    M[1:, 0] = g * beta * n
    M[1:, 1:] = np.eye(2) + (g - 1.0) * np.outer(n, n)
    return M


def wigner_angle(L: np.ndarray) -> float:
    """Rotation part of a composed Lorentz map's spatial block (polar decomposition)."""
    S = L[1:, 1:]
    w, V = np.linalg.eigh(S.T @ S)
    Rm = S @ (V @ np.diag(w ** -0.5) @ V.T)
    return float(np.arctan2(Rm[1, 0], Rm[0, 0]))


def depth2(beta1, th1, beta2, th2, d, phi, tB=0.0):
    """Exact oracle vs the two additive key variants. Offset X_B = d units at angle phi
    from link 2's velocity direction v2, in doll 2's frame. tB = 0 isolates the shear sum."""
    g1, g2 = 1 / np.sqrt(1 - beta1**2), 1 / np.sqrt(1 - beta2**2)
    s1, s2 = beta1 * g1, beta2 * g2  # sinh(eta)
    v2 = np.array([np.cos(th2), np.sin(th2)])
    x1 = np.array([np.cos(th1), np.sin(th1)])
    XB = d * np.array([np.cos(th2 + phi), np.sin(th2 + phi)])
    E = np.array([tB, XB[0], XB[1]])
    t_exact = float((boost(beta1, th1) @ boost(beta2, th2) @ E)[0])
    # V1: chain-tracking (the event's position in doll 1 was known when it passed through)
    XA = XB + (g2 - 1.0) * (v2 @ XB) * v2 + g2 * beta2 * v2 * tB
    key1 = s2 * (v2 @ XB) + s1 * (x1 @ XA)
    # V2: frozen per entity, both shears at the grandchild offset
    key2 = s2 * (v2 @ XB) + s1 * (x1 @ XB)
    ana1 = (g1 - 1.0) * s2 * (v2 @ XB) if tB == 0 else float("nan")
    ana2 = ((g1 - 1.0) * s2 + s1 * (g2 - 1.0) * np.cos(th1 - th2)) * (v2 @ XB) if tB == 0 else float("nan")
    return dict(t_exact=t_exact, key1=float(key1), key2=float(key2),
                err1=t_exact - key1, err2=t_exact - key2, ana1=float(ana1), ana2=float(ana2),
                wigner_deg=float(np.degrees(wigner_angle(boost(beta1, th1) @ boost(beta2, th2)))))


def depthN(betas, thetas, d, phi):
    """Chain of N dolls; V1/V2 generalized, vs the exact product of boosts."""
    N = len(betas)
    v = [np.array([np.cos(t), np.sin(t)]) for t in thetas]
    g = [1 / np.sqrt(1 - b**2) for b in betas]
    s = [b * gg for b, gg in zip(betas, g)]
    XB = d * np.array([np.cos(thetas[-1] + phi), np.sin(thetas[-1] + phi)])
    E = np.array([0.0, XB[0], XB[1]])
    L = np.eye(3)
    for b, t in zip(betas, thetas):
        L = L @ boost(b, t)
    t_exact = float((L @ E)[0])
    # V1: walk positions up the chain, each link shears its own local offset
    X = XB
    key1 = 0.0
    for i in range(N - 1, -1, -1):
        key1 += s[i] * (v[i] @ X)
        if i > 0:
            X = X + (g[i] - 1.0) * (v[i] @ X) * v[i]
    # V2: every link's shear at the terminal offset
    key2 = sum(s[i] * (v[i] @ XB) for i in range(N))
    return t_exact, key1, key2


def main():
    out = {"controls": {}, "kill_grid": [], "named": [], "tb_channel": {}, "depth": [], "oracle_check": None}

    # --- controls ---
    r = depth2(0.5, 0.0, 0.0, 0.0, 2000.0, 0.0)
    out["controls"]["depth1_beta2_0"] = {k: r[k] for k in ("err1", "err2")}
    r = depth2(0.5, 0.0, 1e-5, 0.0, 2000.0, 0.0)
    out["controls"]["depth2_moon_speed"] = {k: r[k] for k in ("err1", "err2")}
    # kill grid + oracle self-check (numeric error vs the analytic law)
    worst = 0.0
    for b1 in (0.1, 0.3, 0.5, 0.9):
        for b2 in (0.01, 0.1, 0.3):
            for thr in (0.0, np.pi / 2, np.pi):
                for d in (100.0, 1000.0, 10000.0):
                    r = depth2(b1, 0.0, b2, thr, d, 0.0)
                    worst = max(worst, abs(r["err1"] - r["ana1"]), abs(r["err2"] - r["ana2"]))
                    out["kill_grid"].append(dict(b1=b1, b2=b2, th2_rel=thr, d=d,
                                                 err1=r["err1"], err2=r["err2"],
                                                 wigner_deg=r["wigner_deg"]))
    out["oracle_check"] = worst

    # --- named held-out rows (predictions.md) ---
    for name, args in {
        "player_group_b.3_.3_90deg_d1e3": (0.3, 0.0, 0.3, np.pi / 2, 1000.0, 0.0),
        "inspiral_b.5_.5_0deg_d2e3": (0.5, 0.0, 0.5, 0.0, 2000.0, 0.0),
        "high_gamma_b.9_.1_d1e3": (0.9, 0.0, 0.1, 0.0, 1000.0, 0.0),
        "perp_offset_null_b.5_.5_90deg": (0.5, 0.0, 0.5, np.pi / 2, 2000.0, np.pi / 2),
    }.items():
        r = depth2(*args)
        out["named"].append(dict(name=name, err1=r["err1"], err2=r["err2"],
                                 wigner_deg=r["wigner_deg"], args=list(args)))

    # --- t_B channel: the doll tick itself (double time dilation) ---
    g1 = g2 = 1 / np.sqrt(1 - 0.25)
    tB = 1e4
    t_exact = (boost(0.5, 0.0) @ boost(0.5, 0.0) @ np.array([tB, 0.0, 0.0]))[0]
    out["tb_channel"] = dict(tB=tB, exact=float(t_exact), gamma1gamma2=float(g1 * g2),
                             unscaled_error=float(t_exact - tB),
                             inner_scaled_error=float(t_exact - g2 * tB))

    # --- depth scaling (collinear, beta 0.3 each, terminal offset 1000) ---
    for n in (2, 3, 4):
        t, k1, k2 = depthN([0.3] * n, [0.0] * n, 1000.0, 0.0)
        out["depth"].append(dict(n=n, err1=float(t - k1), err2=float(t - k2)))

    n1 = sum(1 for r in out["kill_grid"] if max(abs(r["err1"]), abs(r["err2"])) >= 1.0)
    n10 = sum(1 for r in out["kill_grid"] if max(abs(r["err1"]), abs(r["err2"])) >= 10.0)
    print(f"kill grid census: {n1}/{len(out['kill_grid'])} cells >= 1 tick, {n10} >= 10 ticks")

    # --- report ---
    print("== controls ==")
    c = out["controls"]
    print(f"depth-1 (beta2=0):    err V1 {c['depth1_beta2_0']['err1']:.3e}  V2 {c['depth1_beta2_0']['err2']:.3e} ticks")
    print(f"depth-2 moon speed:   err V1 {c['depth2_moon_speed']['err1']:.3e}  V2 {c['depth2_moon_speed']['err2']:.3e} ticks")
    print(f"oracle vs analytic:   max |diff| = {out['oracle_check']:.3e} over the 108-cell grid")
    print("== named held-out rows (offsets in light-ticks) ==")
    for row in out["named"]:
        print(f"{row['name']:34s} err V1 {row['err1']:9.2f}  V2 {row['err2']:9.2f}  wigner {row['wigner_deg']:6.2f} deg")
    tb = out["tb_channel"]
    print("== doll-tick channel (beta1=beta2=0.5, tB=1e4) ==")
    print(f"exact gamma1*gamma2 = {tb['gamma1gamma2']:.4f}; unscaled-tick error {tb['unscaled_error']:.1f}; inner-gamma-only {tb['inner_scaled_error']:.1f} ticks")
    print("== depth scaling (beta 0.3 per link, d = 1000) ==")
    for row in out["depth"]:
        print(f"depth {row['n']}:  err V1 {row['err1']:8.2f}  V2 {row['err2']:8.2f}")
    w = max(out["kill_grid"], key=lambda r: max(abs(r["err1"]), abs(r["err2"])))
    print(f"worst kill cell: b1={w['b1']} b2={w['b2']} th={w['th2_rel']:.2f} d={w['d']:.0f}: V1 {w['err1']:.1f} V2 {w['err2']:.1f} ticks")

    with open("results.json", "w") as f:
        json.dump(out, f, indent=1, default=float)
    print("wrote results.json")


if __name__ == "__main__":
    main()
