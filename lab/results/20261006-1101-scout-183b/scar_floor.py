#!/usr/bin/env python3
"""Scar-floor falsifier: H_live (bits of live distinctions) of a stirred belt.

2D belt (G=4*pi^2, M*=1, AU/yr): bodies born banded-a, Rayleigh e, uniform angles.
A secondary m_p at a_p (circular) stirs the belt via synodic conjunctions.
At each conjunction (solved exactly by Newton on the longitude difference) we
apply the impulse approximation, recompute elements, and ask: is the kick a
DISTINCTION on a q-bit grid of the tube key (E, L)? A kick below one quantum is
zero information. We measure:
  rate of distinguishable encounters per body per orbit (vs distance to secondary)
  bits per scar record (empirical entropies of quantized deltas)
  repeat correlation (lag-1 autocorr + conditional entropy) of successive kicks
  -> bits/body at horizons; the 10^9-in-8GB verdict.

Floats explore only; all decisions are integer-valued (quantized deltas != 0).
Usage: scar_floor.py CONFIG.json OUT.json
"""
import json, sys
import numpy as np

G = 4 * np.pi ** 2  # AU^3 / (M_sun yr^2)

def kepler_M_to_E(M, e, it=6):
    E = M + e * np.sin(M)
    for _ in range(it):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E

def elements_to_state(a, e, w, M, mu=G):
    E = kepler_M_to_E(M, e)
    cE, sE = np.cos(E), np.sin(E)
    r = a * (1 - e * cE)
    nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E), np.sqrt(1 - e) * (1 + np.cos(E)))
    x = r * np.cos(w + nu); y = r * np.sin(w + nu)
    p = a * (1 - e * e)
    h = np.sqrt(mu * p)
    vx = (-mu / h) * (np.sin(nu))
    vy = (mu / h) * (e + np.cos(nu))
    cw, sw = np.cos(w), np.sin(w)
    px = vx * cw - vy * sw; py = vx * sw + vy * cw
    return x, y, px, py, r, nu

def state_to_elements(x, y, vx, vy, mu=G):
    r = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    E = v2 / 2 - mu / r
    a = -mu / (2 * E)
    L = x * vy - y * vx
    e = np.sqrt(np.maximum(0, 1 + 2 * E * L * L / (mu * mu)))
    return E, a, e, L

def longitude(a, e, w, M):
    E = kepler_M_to_E(M, e)
    nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E), np.sqrt(1 - e) * (1 + np.cos(E)))
    return w + nu

def run(cfg, out_path):
    rng = np.random.default_rng(cfg["seed"])
    N = cfg["n_bodies"]
    a0, a1 = cfg["a_belt"]
    sig_e = cfg["sig_e"]
    mp, ap = cfg["m_planet"], cfg["a_planet"]
    mu = G  # star 1 Msun
    np_ = np.sqrt(mu / ap ** 3)          # planet mean motion
    J = cfg["conjunctions_per_body"]     # successive conjunctions tracked per body
    qbits_list = cfg["qbits"]            # grid widths for the (E,L) key
    bcut_rh = cfg.get("bcut_rh", 3.0)    # encounter cutoff in mutual Hill radii
    rh_p = ap * (mp / 3.0) ** (1 / 3)    # secondary Hill radius (approx, about star)
    bcut = bcut_rh * rh_p
    T_p = 2 * np.pi / np_

    # --- birth belt ---
    a = rng.uniform(a0, a1, N)
    e = np.abs(rng.rayleigh(sig_e, N)).clip(1e-9, 0.6)
    w = rng.uniform(0, 2 * np.pi, N)
    M0 = rng.uniform(0, 2 * np.pi, N)
    n = np.sqrt(mu / a ** 3)
    T_orb = 2 * np.pi / n

    E0 = -mu / (2 * a)
    L0 = np.sqrt(mu * a * (1 - e * e))
    # 32-bit-equivalent key grid over the belt's own E,L range (the doll's band)
    Espan = abs(mu / (2 * a0) - mu / (2 * a1))
    Lspan = abs(np.sqrt(mu * a1 * (1 - 0)) - np.sqrt(mu * a0 * (1 - 0)))

    # --- conjunction tracking, chunked ---
    psi_res = []
    enc_d = []      # encounter distance / r_H
    enc_da = []     # delta a / a
    enc_de = []     # delta e
    enc_dE = []; enc_dL = []; enc_dM = []
    enc_body = []; enc_kidx = []; enc_da_sep = []
    seq_dkey = np.zeros((N, J), dtype=np.int32)  # quantized dE key per conjunction (32-bit)
    seq_enc = np.zeros((N, J), dtype=bool)
    n_conj_samples = 0

    Mp = rng.uniform(0, 2 * np.pi)  # planet mean anomaly at t=0
    CH = cfg.get("chunk", 20000)
    for lo in range(0, N, CH):
        hi = min(lo + CH, N)
        ai, ei, wi, Mi0 = a[lo:hi], e[lo:hi], w[lo:hi], M0[lo:hi]
        ni = n[lo:hi]
        m = hi - lo
        # conjunction times: relative longitude psi(t) = 0. Seed from linear mean longitudes.
        Ts = 2 * np.pi / np.abs(ni - np_)
        t0 = rng.uniform(0, 1, m) * Ts  # random phase: ergodic over conjunction index
        tk = t0[:, None] + np.arange(J)[None, :] * Ts[:, None]  # (m, J)
        for _ in range(8):  # Newton on psi with true longitudes
            Mi = (Mi0[:, None] + ni[:, None] * tk) % (2 * np.pi)
            Mpl = (Mp + np_ * tk) % (2 * np.pi)
            psi = longitude(ai[:, None], ei[:, None], wi[:, None], Mi) - \
                  longitude(np.full_like(Mi, ap), 1e-12, np.zeros_like(Mi), Mpl)
            psi = (psi + np.pi) % (2 * np.pi) - np.pi
            tk = tk - psi / (ni[:, None] - np_)
        Mi = (Mi0[:, None] + ni[:, None] * tk) % (2 * np.pi)
        Mpl = (Mp + np_ * tk) % (2 * np.pi)
        psi_end = longitude(ai[:, None], ei[:, None], wi[:, None], Mi) - \
            longitude(np.full_like(Mi, ap), 1e-12, np.zeros_like(Mi), Mpl)
        psi_end = (psi_end + np.pi) % (2 * np.pi) - np.pi
        psi_res.append(float(np.median(np.abs(psi_end))))
        xi, yi, vxi, vyi, ri, nui = elements_to_state(ai[:, None], ei[:, None], wi[:, None], Mi)
        xp, yp, vxp, vyp, rp, nup = elements_to_state(np.full_like(Mi, ap), 1e-12, np.zeros_like(Mi), Mpl)
        d = np.hypot(xi - xp, yi - yp)
        vrx, vry = vxi - vxp, vyi - vyp
        vrel = np.hypot(vrx, vry)
        # impulse deflection: rotate v_rel by theta toward the secondary
        theta = 2 * np.arctan(G * mp / np.maximum(d, 1e-9) / np.maximum(vrel, 1e-9) ** 2)
        rx, ry = (xp - xi) / d, (yp - yi) / d
        cross = vrx * ry - vry * rx
        sg = -np.sign(cross)  # rotate v_rel toward r_hat
        ct, st = np.cos(theta), np.sin(theta)
        dvx = vrel * (ct * vrx / vrel - sg * st * vry / vrel) - vrx
        dvy = vrel * (ct * vry / vrel + sg * st * vrx / vrel) - vry
        nvx, nvy = vxi + dvx, vyi + dvy
        En, an, en, Ln = state_to_elements(xi, yi, nvx, nvy)
        # timing shift of the kick is folded into the record-bits proxy (see verdict)
        hit = d < bcut
        seq_enc[lo:hi, :] = hit.reshape(m, J)
        n_conj_samples += m * J
        if hit.any():
            enc_d.append((d[hit] / rh_p))
            b_ai = np.broadcast_to(ai[:, None], (m, J))[hit]
            enc_da.append((an[hit] - b_ai) / b_ai)
            enc_de.append(en[hit] - np.broadcast_to(ei[:, None], (m, J))[hit])
            b_E0 = np.broadcast_to(E0[lo:hi, None], (m, J))[hit]
            b_L0 = np.broadcast_to(L0[lo:hi, None], (m, J))[hit]
            enc_dE.append(En[hit] - b_E0)
            enc_dL.append(Ln[hit] - b_L0)
            enc_da_sep.append(((ap - b_ai) / rh_p))
            body_idx = np.broadcast_to(np.arange(lo, hi)[:, None], (m, J))[hit]
            kidx = np.broadcast_to(np.arange(J)[None, :], (m, J))[hit]
            enc_body.append(body_idx); enc_kidx.append(kidx)
        # 32-bit reference key for repeat-correlation (finest grid)
        de = En - E0[lo:hi, None]
        seq_dkey[lo:hi, :] = np.clip(np.round(de / (Espan / 2 ** 32)), -2**31, 2**31 - 1).astype(np.int32)

    enc = {k: (np.concatenate(v) if v else np.array([])) for k, v in dict(
        d=enc_d, da=enc_da, de=enc_de, dE=enc_dE, dL=enc_dL, dsep=enc_da_sep,
        body=enc_body, kidx=enc_kidx).items()}
    n_enc = len(enc["d"])

    # conjunctions per body per orbit (rate of opportunities)
    Ts_med = 2 * np.pi / np.abs(n - np_)
    conj_per_orbit = np.median(T_orb / Ts_med)

    # --- quantized scars at each grid width ---
    q_results = {}
    for qb in qbits_list:
        qE = Espan / 2 ** qb
        qL = Lspan / 2 ** qb
        kE = np.round(enc["dE"] / qE).astype(np.int64)
        kL = np.round(enc["dL"] / qL).astype(np.int64)
        scar = (kE != 0) | (kL != 0)
        # empirical entropies of nonzero quantized deltas (log2-binned magnitudes)
        def ent(v):
            if len(v) == 0: return 0.0
            s = np.sign(v); m = np.floor(np.log2(np.abs(v) + 1) * 4).astype(np.int64)
            lbl = (s < 0) * 1000 + m
            _, c = np.unique(lbl, return_counts=True)
            p = c / c.sum()
            return float(-(p * np.log2(p)).sum())
        q_results[qb] = dict(
            n_enc=int(n_enc),
            n_scar=int(scar.sum()),
            scar_frac_of_enc=float(scar.mean()) if n_enc else 0.0,
            H_keyE=ent(kE[scar & (kE != 0)]) if n_enc else 0.0,
            H_keyL=ent(kL[scar & (kL != 0)]) if n_enc else 0.0,
            med_abs_kE=float(np.median(np.abs(kE[(kE != 0)]))) if (kE != 0).any() else 0.0,
        )
    # --- repeat correlation on the 32-bit key sequence (per body, per conjunction) ---
    valid = seq_enc.copy()
    # lag-1 autocorrelation of dkey among consecutive encounter pairs on same body
    a_enc, b_enc = seq_dkey[:, :-1][valid[:, 1:] & valid[:, :-1]], seq_dkey[:, 1:][valid[:, 1:] & valid[:, :-1]]
    if len(a_enc) > 3:
        ac = float(np.corrcoef(a_enc.astype(float), b_enc.astype(float))[0, 1])
    else:
        ac = None
    def cond_ent(xs, ys):
        if len(xs) < 10: return None
        bx = np.clip(np.floor(np.log2(np.abs(xs.astype(np.int64)) + 1) * 4).astype(int), 0, 130) + (xs < 0) * 200
        by = np.clip(np.floor(np.log2(np.abs(ys.astype(np.int64)) + 1) * 4).astype(int), 0, 130) + (ys < 0) * 200
        j = bx * 100 + by
        _, cj = np.unique(j, return_counts=True); pj = cj / len(xs)
        _, cx = np.unique(bx, return_counts=True); px = cx / len(xs)
        Hj = -(pj * np.log2(pj)).sum(); Hx = -(px * np.log2(px)).sum()
        return float(Hj - Hx)
    Hcond = cond_ent(a_enc, b_enc)

    # per-body encounter counts over the tracked window
    per_body = seq_enc.sum(axis=1)
    window_orbits = J / np.median(T_orb / Ts_med)
    frac_hit = float((per_body > 0).mean())
    mean_rate = float(per_body.sum() / N / window_orbits)
    poisson_vm = float(per_body.var() / max(per_body.mean(), 1e-12))

    # distance profile: scar rate vs separation from the secondary (r_H bins)
    dsep_body = (ap - a) / rh_p
    bins = np.array([-1e9, -6, -4, -3, -2, -1, 0, 1e9])
    prof = []
    for i in range(len(bins) - 1):
        sel = (dsep_body >= bins[i]) & (dsep_body < bins[i + 1])
        if sel.sum() > 30:
            r = float(seq_enc[sel].sum() / sel.sum() / window_orbits)
            prof.append((float(bins[i]), float(bins[i + 1]), int(sel.sum()), r))

    # --- verdict: bits/body at horizons (32-bit grid), population 1e9 ---
    qb = 32
    qr = q_results.get(qb, q_results[max(q_results)])
    rec_bits = qr["H_keyE"] + qr["H_keyL"] + 8.0  # + timing shift (proxy)
    # sparse index: Elias-Fano over 1e9 with scarred fraction s: log2(1/s)+1.6
    def bits_at(T_orb_horizon):
        lam = mean_rate * T_orb_horizon  # expected encounters per body
        s = min(1.0 - np.exp(-lam), 0.999999)
        idx = np.log2(1 / max(s, 1e-12)) + 1.6
        # repeat records: correlated; bounded by lam records (upper) / 1 (lower)
        lower = s * (idx + rec_bits)
        upper = s * idx + lam * rec_bits
        return dict(lower=lower, upper=upper, s=float(s), lam=float(lam))
    verdict = {str(T): bits_at(T) for T in cfg["horizons"]}

    out = dict(
        config=cfg, rh_p=rh_p, psi_residual_med=max(psi_res) if psi_res else None, conj_per_orbit=float(conj_per_orbit),
        window_orbits=float(window_orbits), n_encounters=int(n_enc),
        n_conj_samples=int(n_conj_samples),
        enc_per_body_per_orbit=mean_rate, frac_bodies_hit=frac_hit, poisson_var_mean=poisson_vm,
        q_results={str(k): v for k, v in q_results.items()},
        lag1_dkey_autocorr=ac, H_cond_dkey=Hcond,
        profile=prof, verdict=verdict,
        kick_stats=dict(
            med_dE_over_E=float(np.median(np.abs(enc["dE"])) / abs(np.median(E0))) if n_enc else None,
            med_dv_over_vk=None, med_d_over_rh=float(np.median(enc["d"])) if n_enc else None,
        ),
    )
    # ship-ship control: mutual impulse for aggregate masses (analytic, no MC needed)
    ctrl = []
    for ms_kg in [1e6, 1e9, 1e12]:
        ms = ms_kg / 1.989e30  # M_sun
        for b_m in [1e3, 1e4, 1e5]:
            b = b_m / 1.496e11  # AU
            vrel = 5e-3  # AU/yr (750 m/s, sigma_e=0.05 belt)
            dv = 2 * G * ms / (b * vrel)  # AU/yr
            dv_over_vk = dv / (2 * np.pi)
            dE_over_E = 2 * dv_over_vk  # tangential impulse: da/a = 2 dv/v_K
            key32 = dE_over_E * abs(np.median(E0)) / (Espan / 2 ** 32)
            ctrl.append(dict(m_kg=ms_kg, b_m=b_m, dv_over_vk=float(dv_over_vk),
                             key_units_32bit=float(key32)))
    out["ship_ship_control"] = ctrl
    with open(out_path, "w") as f:
        json.dump(out, f, indent=1, default=str)
    print("wrote", out_path, "| encounters:", n_enc, "| enc/body/orbit:",
          round(mean_rate, 5), "| frac hit:", round(frac_hit, 4))

if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1]))
    run(cfg, sys.argv[2])
