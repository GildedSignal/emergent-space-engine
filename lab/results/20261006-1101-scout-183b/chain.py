#!/usr/bin/env python3
"""C7: chained scar diffusion. Each body's post-kick state feeds the next
conjunction. Measures whether the cumulative quantized delta (the scar) has a
saturating entropy (scatterings self-terminate: bodies leave the crossing band)
or grows without bound. Worst case: whole belt inside the chaotic zone (C1 scene).
"""
import json, sys
import numpy as np
import scar_floor as sf

G = 4 * np.pi ** 2

def main(cfg, out_path):
    rng = np.random.default_rng(cfg["seed"])
    N, J = cfg["n_bodies"], cfg["steps"]
    a0, a1 = cfg["a_belt"]; sig_e = cfg["sig_e"]
    mp, ap = cfg["m_planet"], cfg["a_planet"]
    mu = G; np_ = np.sqrt(mu / ap ** 3)
    rh_p = ap * (mp / 3.0) ** (1 / 3); bcut = cfg["bcut_rh"] * rh_p
    a = rng.uniform(a0, a1, N); e = rng.rayleigh(sig_e, N).clip(1e-9, 0.6)
    w = rng.uniform(0, 2 * np.pi, N); M0 = rng.uniform(0, 2 * np.pi, N)
    Mp = rng.uniform(0, 2 * np.pi)
    E0 = -mu / (2 * a); L0 = np.sqrt(mu * a * (1 - e * e))
    Espan = abs(mu / (2 * a0) - mu / (2 * a1))
    Lspan = abs(np.sqrt(mu * a1) - np.sqrt(mu * a0))
    n = np.sqrt(mu / a ** 3)
    Ts0 = 2 * np.pi / np.abs(n - np_)
    # per-body clock: last conjunction time, current state
    tk = rng.uniform(0, 1, N) * Ts0
    a_c, e_c, w_c, M_c = a.copy(), e.copy(), w.copy(), M0.copy()
    alive = np.ones(N, bool)          # still tracked (not escaped, still bound)
    escaped = np.zeros(N, bool)
    dE_cum = np.zeros(N); dL_cum = np.zeros(N)  # cumulative scar (exact state delta)
    n_enc = np.zeros(N, int)
    med_key_hist = []; ent_hist = []
    qb = 32
    qE, qL = Espan / 2 ** qb, Lspan / 2 ** qb

    for k in range(J):
        idx = np.where(alive)[0]
        if len(idx) == 0: break
        ai, ei, wi, Mi0 = a_c[idx], e_c[idx], w_c[idx], M_c[idx]
        ni = np.sqrt(mu / ai ** 3)
        Ts = 2 * np.pi / np.abs(ni - np_)
        t = tk[idx] + Ts  # next conjunction after last
        for _ in range(8):
            Mi = (Mi0 + ni * t) % (2 * np.pi)
            Mpl = (Mp + np_ * t) % (2 * np.pi)
            psi = sf.longitude(ai, ei, wi, Mi) - sf.longitude(np.full_like(Mi, ap), 1e-12, np.zeros_like(Mi), Mpl)
            psi = (psi + np.pi) % (2 * np.pi) - np.pi
            t = t - psi / (ni - np_)
        Mi = (Mi0 + ni * t) % (2 * np.pi)
        Mpl = (Mp + np_ * t) % (2 * np.pi)
        x, y, vx, vy, r, nu = sf.elements_to_state(ai, ei, wi, Mi)
        xp, yp, vxp, vyp, _, _ = sf.elements_to_state(np.full_like(Mi, ap), 1e-12, np.zeros_like(Mi), Mpl)
        d = np.hypot(x - xp, y - yp)
        vrx, vry = vx - vxp, vy - vyp
        vrel = np.hypot(vrx, vry)
        theta = 2 * np.arctan(G * mp / np.maximum(d, 1e-9) / np.maximum(vrel, 1e-9) ** 2)
        rx, ry = (xp - x) / d, (yp - y) / d
        sg = -np.sign(vrx * ry - vry * rx)
        ct, st = np.cos(theta), np.sin(theta)
        dvx = ct * vrx - sg * st * vry - vrx
        dvy = sg * st * vrx + ct * vry - vry
        En, an, en, Ln = sf.state_to_elements(x, y, vx + dvx, vy + dvy)
        # chain the state only where an encounter happened
        hit = (d < bcut) & (En < 0) & (an > 0.05) & (an < 50)
        # new mean anomaly at same position for chained state
        hit_idx = idx[hit]
        if hit.any():
            # rebuild M for the new orbit at the current position
            r_h = np.hypot(x[hit], y[hit])
            nun = np.arctan2(y[hit], x[hit])
            cosE = np.clip((1 - r_h / an[hit]) / np.maximum(en[hit], 1e-12), -1, 1)
            sinE = np.clip((x[hit] * (vy[hit] + dvy[hit]) - y[hit] * (vx[hit] + dvx[hit]))
                           / np.sqrt(mu * an[hit]) / np.maximum(en[hit], 1e-12), -1, 1)
            E_new = np.arctan2(sinE, cosE)
            M_new = (E_new - en[hit] * sinE) % (2 * np.pi)
            w_new = (nun - np.arctan2(np.sqrt(1 - en[hit] ** 2) * sinE, en[hit] + cosE)) % (2 * np.pi)
            a_c[hit_idx] = an[hit]; e_c[hit_idx] = en[hit]
            w_c[hit_idx] = w_new; M_c[hit_idx] = M_new
            n_enc[idx[hit]] += 1
            dE_cum[hit_idx] = En[hit] - E0[hit_idx]
            dL_cum[hit_idx] = Ln[hit] - L0[hit_idx]
        # advance non-hit bodies' clocks (their conjunction just passed uneventfully)
        tk[idx] = t
        escaped[idx[(En > 0) | (an >= 50) | (an <= 0.05)]] = True
        alive[idx[(En > 0) | (an >= 50) | (an <= 0.05)]] = False
        # scarred set and its coded size
        kE = np.round(dE_cum / qE).astype(np.int64); kL = np.round(dL_cum / qL).astype(np.int64)
        scarred = (kE != 0) | (kL != 0)
        if (k + 1) % max(1, J // 24) == 0:
            def ent(v):
                s = np.sign(v); m = np.floor(np.log2(np.abs(v) + 1) * 4).astype(np.int64)
                lbl = (s < 0) * 10 ** 6 + m
                _, c = np.unique(lbl, return_counts=True); p = c / c.sum()
                return float(-(p * np.log2(p)).sum())
            ent_hist.append((k + 1, float(scarred.mean()), ent(kE[scarred & (kE != 0)]) if (scarred & (kE != 0)).any() else 0.0,
                             float(np.log2(np.abs(kE[scarred & (kE != 0)]).mean())) if (scarred & (kE != 0)).any() else 0.0))
    out = dict(config=cfg, escaped_frac=float(escaped.mean()),
               med_enc_per_body=float(np.median(n_enc)), mean_enc_per_body=float(n_enc.mean()),
               enc_hist=ent_hist, final_scarred_frac=float((((np.round(dE_cum / qE)) != 0) | ((np.round(dL_cum / qL)) != 0)).mean()))
    json.dump(out, open(out_path, "w"), indent=1, default=str)
    print("escaped:", round(out["escaped_frac"], 3), "| med enc/body:", out["med_enc_per_body"],
          "| final scarred:", out["final_scarred_frac"])
    for row in ent_hist[-8:]:
        print("  step %5d  scarred %.3f  H(deltaE) %.2f bits  log2|kE| %.2f" % tuple(row))

if __name__ == "__main__":
    main(json.load(open(sys.argv[1])), sys.argv[2])
