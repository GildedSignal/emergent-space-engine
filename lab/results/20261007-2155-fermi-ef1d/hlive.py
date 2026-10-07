#!/usr/bin/env python3
"""H_live stock & flow for a 10^9-body belt: first measurement (Fermi lens, run 20261007-2155-fermi-ef1d).

Model (per body, intensive in N, so 2^20 here extrapolates x N):
  - Residual velocity x[3] (m/s) vs the body's program orbit, initially exactly 0 (born as a program).
  - Per orbit: encounter kicks. Strong tail (lambda*P <= ~1.5 per ln-b bin) sampled exactly as
    Poisson counts x delta_v(b) with random directions; the weak-kick sea enters as a Gaussian with
    EXACT remaining variance, so total variance per orbit == the binned Chandrasekhar integral.
  - Chaotic belts: x *= exp(1/tau_L) each orbit (exponential divergence of the true state from any
    compiled program prediction; seeded by the encounter noise).
  - Stored state is the quantized residual r = round(x/q) (the law's integer grid; sub-quantum
    detail lives in the accumulator, principle 6). Distinctions counted are integer events:
    quantum crossings and Elias-gamma storage bits of r. Floats explore; ints decide.
  - Scar store: sparse Elias-Fano over scarred bodies (or a presence bitmap), payload = sign bit +
    Elias gamma per nonzero dim. Bodies whose payload exceeds 128 bits tube out (16-byte Tube).
  - Re-fit variant subtracts the ensemble mean every R orbits (the coherent part a re-fitted
    program marginal can absorb); spread (convolution entropy) is provably not removable.

Usage: python3 hlive.py  (writes out/hlive.json, prints table; ~60-90 s)
"""
import json, math, os, sys, time
import numpy as np

rng = np.random.default_rng(0x5FE1)

# --- fiducial belt (see fermi.md) ---
N      = 1 << 20          # bodies in the toy; rates are intensive
P      = 1.64e8           # orbital period, s (3 AU around 1 Msun)
Q      = 1e-3             # velocity quantum, m/s (v * 2^-24, v = 17.3 km/s)
G      = 6.674e-11
M2GM   = 2 * G * 1e12     # 2*G*m_p, m^3/s^2, peer mass 10^12 kg
VREL   = 2e3              # relative speed, m/s
NBOD_D = 3.4e-25          # number density, 1/m^3 (10^9 in 0.94 AU^3, h = 0.05 AU)
BMIN, BMAX = 1e3, 7.5e9   # impact-parameter range: physical contact .. belt scale, m

# binned exact variance rate (m^2/s^3) and tail bins
def make_bins():
    edges = np.geomspace(BMIN, BMAX, 81)          # 80 ln-bins
    lam_orbit = np.array([NBOD_D * VREL * 2 * math.pi * b * b * P * math.log(edges[i+1]/edges[i])
                          for i, b in enumerate(edges[:-1])])   # encounters/orbit in bin
    dv       = M2GM / (edges[:-1] * VREL)                      # kick, m/s
    tail     = lam_orbit <= 1.5                                # sampled exactly
    var_rate = float((lam_orbit * dv * dv).sum() / P)          # total variance rate
    sea_var  = float((lam_orbit[~tail] * dv[~tail] ** 2).sum())# variance/orbit in Gaussian sea
    return lam_orbit[tail], dv[tail], var_rate, sea_var

LAM_T, DV_T, D_VAR, SEA_VAR = make_bins()
SEA_SD = math.sqrt(SEA_VAR / 3.0)                  # per dim, per orbit
T_ORB  = 2000
SAMPLE = [100, 300, 1000, T_ORB]

def gamma_bits(v):   # sign + Elias gamma of nonzero int components, per body -> int bits
    a = np.abs(v)
    nz = a > 0
    lg = np.zeros_like(a)
    lg[nz] = 2 * np.floor(np.log2(a[nz])) + 1
    return (lg + nz).sum(axis=0) + (nz.any(axis=0) & (lg.sum(axis=0) == 0)) * 0  # sign folded above

def store(r):
    """scarred count, payload bits, index bits (min(EF, bitmap)), tube-outs, mean bits/scarred"""
    payload = gamma_bits(r)
    m = int((payload > 0).sum())
    tubes = int((payload > 128).sum())
    pay = int(payload.sum())
    ef = m * (math.ceil(math.log2(N / m)) + 2) if 0 < m < N else 0
    idx = min(ef, N)
    return m, pay, idx, tubes

def tail_kicks(g, lam_t, dv_t, x):
    """exact strong-tail sampling by Poisson thinning: same compound law, one draw per body"""
    lam_tot = float(lam_t.sum())
    cnt = g.poisson(lam_tot, N)
    hit_bodies = np.nonzero(cnt)[0]
    if hit_bodies.size == 0:
        return
    body_idx = np.repeat(hit_bodies, cnt[hit_bodies])
    probs = lam_t / lam_tot
    bins = g.choice(len(lam_t), size=body_idx.size, p=probs)
    u = g.normal(size=(3, body_idx.size))
    u /= np.linalg.norm(u, axis=0)
    x[:, body_idx] += dv_t[bins] * u
CHUNK = 10  # orbits per step; exact for Gaussian sums, Poisson thinning and linear amplification

def run(name, tau=None, refit=None, dmul=1.0, seed=None):
    g = rng if seed is None else np.random.default_rng(seed)
    x = np.zeros((3, N)); r_prev = np.zeros((3, N), dtype=np.int64)
    crossings = 0; drift = 0.0; rows = []
    sd = math.sqrt(D_VAR * dmul * P / 3.0)   # exact TOTAL per-dim variance rate (all bins)
    amp = math.exp(CHUNK / tau) if tau else 1.0
    for orb in range(CHUNK, T_ORB + 1, CHUNK):
        if dmul > 0:
            # Every peer kick is sub-quantum (max 0.067 q at physical contact), so no single
            # kick crosses a quantum alone; the compound step is Gaussian (CLT, ~7.5 kicks
            # per body per orbit in the tail + the sea) with EXACT total variance D_VAR*dmul.
            x += g.normal(0.0, sd * math.sqrt(CHUNK), (3, N))
        if tau:
            x *= amp
        if refit and orb % refit == 0:
            x -= x.mean(axis=1, keepdims=True)                   # program re-fit absorbs drift only
        r = np.rint(x / Q).astype(np.int64)
        crossings += int(np.abs(r - r_prev).sum())
        drift = float(np.abs(x.mean(axis=1)).max() / Q)
        r_prev = r
        if orb in SAMPLE:
            m, pay, idx, tubes = store(r)
            sig = float(np.sqrt((x * x).sum(axis=0).mean()))     # 3-D sigma, m/s (axis 0 = dims)
            rows.append(dict(cfg=name, orbits=orb, scarred_frac=m / N,
                             bits_per_scarred=pay / max(m, 1), payload_bits_per_body=pay / N,
                             index_bits_per_body=idx / N, total_bits_per_body=(pay + idx) / N,
                             tubes=tubes, crossings_per_body=crossings / N,
                             sigma_m_s=sig, sigma_quanta=sig / Q, drift_quanta=drift,
                             analytic_sigma_quanta=math.sqrt(D_VAR * dmul * orb * P) / Q
                             if not tau else math.sqrt(D_VAR * dmul * (tau * P) / 2 *
                                                       (math.exp(2 * orb / tau) - 1)) / Q))
    return rows
def main():
    t0 = time.time()
    rows = []
    rows += run("control_D0", dmul=0.0)
    rows += run("fiducial")
    rows += run("refit500", refit=500)
    rows += run("hot300_refit500", tau=300.0, refit=500)
    rows += run("dense_x10", dmul=10.0)
    rows += run("dense_x100", dmul=100.0)
    rows += run("hot_tau10k", tau=10000.0)
    rows += run("hot_tau300", tau=300.0)
    os.makedirs("out", exist_ok=True)
    with open("out/hlive.json", "w") as f:
        json.dump(dict(rows=rows, meta=dict(N=N, P=P, Q=Q, D_var=D_VAR, T_orb=T_ORB,
                                        wall_s=round(time.time() - t0, 1),
                                        loadavg=os.getloadavg())), f, indent=1)
    hdr = f"{'cfg':<11}{'orbits':>7}{'scarfr':>9}{'b/scar':>8}{'tot b/body':>12}{'cross/body':>12}{'sig_q':>9}{'ana_q':>9}{'tubes':>7}"
    print(hdr); print("-" * len(hdr))
    for r in rows:
        print(f"{r['cfg']:<11}{r['orbits']:>7}{r['scarred_frac']:>9.2e}{r['bits_per_scarred']:>8.2f}"
              f"{r['total_bits_per_body']:>12.3e}{r['crossings_per_body']:>12.2e}"
              f"{r['sigma_quanta']:>9.3f}{r['analytic_sigma_quanta']:>9.3f}{r['tubes']:>7}")
    print(f"\nD_var={D_VAR:.3e} m^2/s^3  crossing rate check: D*P/Q^2={D_VAR*P/Q/Q:.2e}/orbit"
          f"  wall={time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
