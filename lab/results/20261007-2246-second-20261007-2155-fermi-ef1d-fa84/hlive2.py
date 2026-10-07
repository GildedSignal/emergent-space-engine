#!/usr/bin/env python3
"""H_live flow recomputed on MEASURED inputs (run ...-fa84, second author on 20261007-2155-fermi-ef1d).

The checker's named experiment: replace the toy's ASSUMED tau_L = 300 orbits (all bodies)
and the assumed perturber set with what `measure_taul.py` measured on the plane's shipped
configuration (PLANETS of crates/universe + B18b's belt SPEC at 2.0-2.5 AU).

Two outputs, both from measured inputs only:
  A. the STOCK at 1e4 yr: bits implied by each measured body's actual a-residual
     (windowed rms, linear drift removed, converted to the law's velocity quantum
     q_v = v(a) * 2^-24 — the per-region quantum of bottleneck 5, not the toy's single Q);
  B. the FLOW beyond 1e4 yr: the original toy (verbatim store() and kick machinery, same
     encounter layer) with per-body amplification exp(CHUNK/tau_i): fraction f_chaos of
     bodies carry a measured tau, the rest never amplify (the measured regular belt).
     Upper bound: no resonance saturation modelled, exactly like the original hot case.

Controls: `assumed300` reproduces the original 6.57 bits/body row (must, or the port is
wrong); `measured-refit` subtracts the ensemble mean every 500 orbits; `negative` (D = 0)
must be zero everywhere. Writes out/hlive2.json.
"""
import json, math, os, sys, time
import numpy as np

# ---- the original toy, verbatim where it matters (base/hlive.py of run -ef1d) ----
N      = 1 << 20
P      = 1.64e8           # toy orbit, s (3 AU, 5.19 yr) — the toy clock, kept for comparability
Q      = 1e-3             # m/s
G      = 6.674e-11
M2GM   = 2 * G * 1e12
VREL   = 2e3
NBOD_D = 3.4e-25
BMIN, BMAX = 1e3, 7.5e9

def make_bins():
    edges = np.geomspace(BMIN, BMAX, 81)
    lam_orbit = np.array([NBOD_D * VREL * 2 * math.pi * b * b * P * math.log(edges[i+1]/edges[i])
                          for i, b in enumerate(edges[:-1])])
    dv = M2GM / (edges[:-1] * VREL)
    tail = lam_orbit <= 1.5
    var_rate = float((lam_orbit * dv * dv).sum() / P)
    sea_var = float((lam_orbit[~tail] * dv[~tail] ** 2).sum())
    return lam_orbit[tail], dv[tail], var_rate, sea_var

LAM_T, DV_T, D_VAR, SEA_VAR = make_bins()
SEA_SD = math.sqrt(SEA_VAR / 3.0)
T_ORB = 2000
SAMPLE = [100, 300, 1000, T_ORB]
CHUNK = 10

def gamma_bits(v):
    a = np.abs(v)
    nz = a > 0
    lg = np.zeros_like(a)
    lg[nz] = 2 * np.floor(np.log2(a[nz])) + 1
    return (lg + nz).sum(axis=0)

def store(r):
    payload = gamma_bits(r)
    m = int((payload > 0).sum())
    tubes = int((payload > 128).sum())
    pay = int(payload.sum())
    ef = m * (math.ceil(math.log2(N / m)) + 2) if 0 < m < N else 0
    return m, pay, min(ef, N), tubes

def tail_kicks(g, x):
    lam_tot = float(LAM_T.sum())
    cnt = g.poisson(lam_tot, N)
    hit = np.nonzero(cnt)[0]
    if hit.size == 0:
        return
    body_idx = np.repeat(hit, cnt[hit])
    bins = g.choice(len(LAM_T), size=body_idx.size, p=LAM_T / lam_tot)
    u = g.normal(size=(3, body_idx.size))
    u /= np.linalg.norm(u, axis=0)
    x[:, body_idx] += DV_T[bins] * u

def run(name, tau=None, refit=None, dmul=1.0, seed=None):
    """tau: scalar (all bodies) or per-body array (inf = never amplify)."""
    g = np.random.default_rng(seed) if seed is not None else np.random.default_rng(0x5FE1)
    x = np.zeros((3, N)); r_prev = np.zeros((3, N), dtype=np.int64)
    crossings = 0; rows = []
    sd = math.sqrt(D_VAR * dmul * P / 3.0)
    amp = (np.full(N, math.exp(CHUNK / tau)) if np.isscalar(tau) or tau is None
           else np.exp(CHUNK / np.asarray(tau, dtype=float)))
    amp[~np.isfinite(amp) | (amp < 1.0)] = 1.0
    for orb in range(CHUNK, T_ORB + 1, CHUNK):
        if dmul > 0:
            x += g.normal(0.0, sd * math.sqrt(CHUNK), (3, N))
        x *= amp[None, :]
        if refit and orb % refit == 0:
            x -= x.mean(axis=1, keepdims=True)
        r = np.rint(x / Q).astype(np.int64)
        crossings += int(np.abs(r - r_prev).sum())
        r_prev = r
        if orb in SAMPLE:
            m, pay, idx, tubes = store(r)
            rows.append(dict(cfg=name, orbits=orb, scarred_frac=m / N,
                             bits_per_scarred=pay / max(m, 1),
                             total_bits_per_body=(pay + idx) / N, tubes=tubes,
                             crossings_per_body=crossings / N,
                             sigma_quanta=float(np.sqrt((x * x).sum(axis=0)).mean() / Q)))
    return rows

# ---- measured inputs ----
YEAR_S = 3.156e7
TOY_P_YR = P / YEAR_S                     # 5.19 yr per toy orbit

def load_measured():
    d = json.load(open("out/taul.json"))
    m = next(r for r in d if r["cfg"] == "measured")
    return m, next(r for r in d if r["cfg"] == "dt_half")

def stock_bits(m):
    """A: bits implied by the measured residuals at the last window (<= 1e4 yr)."""
    rms = np.array(m["rms_windows"][-1])            # AU, per body (window 3162-10000 yr)
    a0 = np.array(m["a0"])
    v = 29784.0 / np.sqrt(a0)                       # m/s heliocentric at a0
    qv = v * 2.0 ** -24                             # the law's velocity quantum at that a
    dv = (v / 2.0) * (rms / a0)                     # a-residual -> velocity residual
    quanta = dv / qv
    scarred = quanta > 0.5
    r = np.rint(np.stack([quanta[scarred], np.zeros(scarred.sum()), np.zeros(scarred.sum())]))
    m_s, pay, idx, tubes = (None, None, None, None)
    payload = gamma_bits(r)
    ms = int((payload > 0).sum())
    pay = int(payload.sum())
    ef = ms * (math.ceil(math.log2(N / max(ms, 1))) + 2) if 0 < ms < N else 0
    return dict(scarred_frac_measured=float(scarred.mean()),
                rms_quanta_median=float(np.median(quanta)),
                rms_quanta_p99=float(np.percentile(quanta, 99)),
                bits_per_scarred=pay / max(ms, 1),
                total_bits_per_body=(pay + min(ef, N)) / N if ms else 0.0,
                tubes=int((payload > 128).sum()), n=len(a0))

def main():
    t0 = time.time()
    m, half = load_measured()
    ch = np.array(m["chaotic"])
    tau_orb_meas = np.array(m["tau_orb"])[ch] * TOY_P_YR   # measured tau in TOY orbits
    f = float(ch.mean())
    print(f"measured: n={m['n']} f_chaos={f:.5f} tau_orb(toy) median={np.median(tau_orb_meas):.0f} "
          f"p10={np.percentile(tau_orb_meas,10):.0f} p90={np.percentile(tau_orb_meas,90):.0f} "
          f"dt_half f={half['chaotic_frac']:.5f}")

    rng = np.random.default_rng(0x5EED)
    tau_vec = np.full(N, np.inf)
    if ch.any():
        members = rng.random(N) < f
        tau_vec[members] = rng.choice(tau_orb_meas, members.sum())
    rows = []
    rows += run("assumed300", tau=300.0, seed=0x5FE1)            # control: the original row
    rows += run("negative", tau=tau_vec, dmul=0.0, seed=0x5FE1)  # D = 0: zero everywhere
    rows += run("measured", tau=tau_vec, seed=0x5FE1)
    rows += run("measured-refit", tau=tau_vec, refit=500, seed=0x5FE1)
    rows += run("measured-dense100", tau=tau_vec, dmul=100.0, seed=0x5FE1)
    out = dict(measured_scene=dict(f_chaos=f, n=m["n"],
                                   tau_yr_median_chaotic=m["tau_yr_chaotic_median"],
                                   bounded_rms_AU_regular=m["bounded_rms_AU_regular"],
                                   e_exceed_cap=m["e_exceed_cap"], a_out_of_band=m["a_out_of_band"],
                                   massive_energy_drift=m["massive_energy_drift"],
                                   dt_half_f_chaos=half["chaotic_frac"]),
               stock_1e4yr=stock_bits(m), rows=rows)
    os.makedirs("out", exist_ok=True)
    json.dump(out, open("out/hlive2.json", "w"), indent=1)
    for r in rows:
        print(f"{r['cfg']:>16} orbits={r['orbits']:>5} scarred={r['scarred_frac']:.6f} "
              f"bits/body={r['total_bits_per_body']:.4f} tubes={r['tubes']:>6} sigma_q={r['sigma_quanta']:.3f}")
    s = out["stock_1e4yr"]
    print(f"STOCK(measured, 1e4 yr): scarred={s['scarred_frac_measured']:.6f} "
          f"bits/scarred={s['bits_per_scarred']:.2f} bits/body={s['total_bits_per_body']:.5f} "
          f"median rms={s['rms_quanta_median']:.3f} q p99={s['rms_quanta_p99']:.3f} q tubes={s['tubes']}")
    print(f"wall={time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
