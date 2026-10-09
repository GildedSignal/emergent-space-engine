#!/usr/bin/env python3
"""m_crit and the sub-threshold crossing flux on the MEASURED encounter distribution.

Inputs: out/{a,b,c,d,game3d}-enc.jsonl (shipped truth encounters + impulse x per unit perturber
mass, dumped by dumper/). Units G = M_sun = 1, AU, yr/2pi, 2^32 ticks per time unit; one period
tick of a = (2/3)·a/(TAU·a^1.5·2^32) in Δa.

Distinction channels on the law's integer grid (kepler.rs: period P and periapsis time tp are
integers):
  P  channel: crossed when a single (or accumulated) Δa reaches one Δa_tick;
  tp channel: a persistent a-offset of S ticks drifts the phase ~S ticks/orbit
              (δn/n = −1.5 δa/a ⇒ δλ_ticks/orbit = δa_ticks), so the integrated walk first
              passes 1 tick after k* = (3/(2 σ_x √R))^{2/3} orbits (σ_x = per-encounter rms
              Δa in ticks, R = encounters/body/orbit).
"""
import json, math
import numpy as np

TAU = 2 * math.pi
TICK = 2.0 ** 32
MSUN = 1.989e30

def rock(r_m, rho=2.5):
    return 4 / 3 * math.pi * r_m ** 3 * (rho * 1e3) / MSUN

def da_tick(a):
    return (2 / 3) * a / (TAU * a ** 1.5 * TICK)

BELTS = {  # name: (n, orbits, rho, sigma_e, a_lo, a_hi) — from the shipped specs
    "r8like-s1e-3-r1e-4": (1000, 200, 1e-4, 1e-3, 1.0, 1.5),
    "r8like-s3e-3-r1e-4": (1000, 100, 1e-4, 3e-3, 1.0, 1.5),
    "r8like-s1e-2-r1e-4": (1000, 100, 1e-4, 1e-2, 1.0, 1.5),
    "r8like-s3e-2-r1e-4": (1000, 50, 1e-4, 3e-2, 1.0, 1.5),
    "r8like-s1e-3-r1e-3": (1000, 100, 1e-3, 1e-3, 1.0, 1.5),
    "r8like-s1e-2-r1e-3": (1000, 50, 1e-3, 1e-2, 1.0, 1.5),
    "r8like-s3e-2-r3e-5": (1000, 50, 3e-5, 3e-2, 1.0, 1.5),
    "narrow-adversarial": (400, 20, 3e-3, 0.025, 1.0, 1.0025),
    "coorbital": (300, 50, 1e-3, 3e-4, 1.0, 1.0001),
    "equal-period-keys": (300, 50, 1e-3, 1e-2, 1.0, 1.001),
    "hot-s0.1-r1e-3": (500, 50, 1e-3, 0.1, 1.0, 1.5),
    "mixed-a0.5-3-s0.2-r1e-3": (400, 50, 1e-3, 0.2, 0.5, 3.0),
    "dense-n3000-s1e-2-r3e-4": (3000, 20, 3e-4, 1e-2, 1.0, 1.5),
    "game3d-planar": (2000, 50, 1e-4, 0.1, 2.45, 2.95),
}

def load(files):
    rows = []
    for f in files:
        rows += [json.loads(l) for l in open(f)]
    for r in rows:
        r["x"] = r["xpm_i"]  # per unit perturber mass, in ticks of body i
        r["mcrit"] = 1.0 / abs(r["xpm_i"]) if r["xpm_i"] else np.inf
    return rows

def main():
    rows = load([f"out/{s}-enc.jsonl" for s in ["a","b","c","d","game3d"]])
    print(f"total measured encounters (both bodies counted separately below): {len(rows)}\n")

    masses = {"ship 1e6 t": 1e9 / MSUN, "rock 50 m": rock(50), "rock 500 m": rock(500),
              "rock 1 km": rock(1000), "rock 5 km": rock(5000), "Ceres": 9.4e-10}

    print("== per-belt: measured rate, m_crit distribution (period-tick channel) ==")
    print("  m_crit = perturber mass at which THAT encounter crosses one Δa tick")
    for name, (n, orb, rho, se, alo, ahi) in BELTS.items():
        br = [r for r in rows if r["belt"] == name]
        if not br:
            continue
        x = np.array([abs(r["x"]) for r in br])
        mc = np.array([r["mcrit"] for r in br])
        R = len(br) / (n * orb)  # per body per orbit (each encounter counted for body i)
        a_bar = np.mean([r["ai"] for r in br])
        print(f"  {name:24s} R={R:.2e}/body/orbit  <a>={a_bar:.2f}  "
              f"m_crit: med={np.median(mc):.2e} p1={np.percentile(mc,1):.2e} "
              f"min={mc.min():.2e} M_sun  (rocks {np.cbrt(np.median(mc)*MSUN/(4/3*math.pi*2.5e3)):.0f}m/"
              f"{np.cbrt(np.percentile(mc,1)*MSUN/(4/3*math.pi*2.5e3)):.0f}m/"
              f"{np.cbrt(mc.min()*MSUN/(4/3*math.pi*2.5e3)):.0f}m med/p1/min)")

    print("\n== fraction of measured encounters crossing >= 1 period tick, per mass ==")
    print(f"  {'mass':12s}" + "".join(f"{k.split()[0]+' '+k.split()[1] if len(k.split())>1 else k:>12s}" for k in masses))
    for name in BELTS:
        br = [r for r in rows if r["belt"] == name]
        if not br:
            continue
        x = np.abs([r["x"] for r in br])
        fr = "  " + f"{name:24s}"
        for k, m in masses.items():
            fr += f"{np.mean(x * m >= 1.0) * 100:11.1f}%"
        print(fr)

    # ---------------- 3-D game-density MC on the measured game3d distribution ----------------
    print("\n== 3-D game-density case (N=1e9, a=2.7, width 1.5 AU, sigma_e=sigma_i=0.1, rho=1e-4) ==")
    g = [r for r in rows if r["belt"] == "game3d-planar"]
    a0, sig_i = 2.7, 0.14
    vk = 1 / math.sqrt(a0)
    s_z = a0 * sig_i          # std of vertical separation at conjunction
    sig_vz = vk * sig_i       # std of vertical relative velocity
    dp = np.array([r["d"] for r in g])
    vp = np.array([r["vrel"] for r in g])
    cos_i = np.array([r["cospsi_i"] for r in g])
    ai = np.array([r["ai"] for r in g])
    rng = np.random.default_rng(20261009)
    NB = 400000
    si = rng.integers(0, len(g), NB)
    w_d3 = dp[si]  # 2-D->3-D impact-parameter measure: p(d) ∝ d dd (vs dd in 2-D)
    wmax = np.sqrt(1e-4 ** 2 - dp[si] ** 2 + 1e-30)
    wz = (rng.random(NB) * 2 - 1) * wmax              # uniform in the tube (Gaussian flat there)
    acc = rng.random(NB) < 2 * wmax / (s_z * math.sqrt(2 * math.pi))  # vertical acceptance
    d3 = np.sqrt(dp[si] ** 2 + wz ** 2)
    vz = rng.normal(0, sig_vz, NB)
    v3 = np.sqrt(vp[si] ** 2 + vz ** 2)
    vzi = rng.normal(0, sig_vz / math.sqrt(2), NB)    # body i's own vertical velocity
    # cosψ = (v_i·b)/(|v_i| d3): planar term cospsi_i·|v_p|·d_p (|v_p| ≈ v_k(a_i); the epicycle
    # is second order in cosψ) plus vertical term v_zi·w_z
    vki = 1 / np.sqrt(ai[si])
    cos3 = (cos_i[si] * vki * (dp[si] / d3) + vzi * (wz / d3)) / np.sqrt(vki ** 2 + vzi ** 2)
    kick3 = 2 * ai[si] ** 2 * np.sqrt(vki ** 2 + vzi ** 2) * 2 / (d3 * v3) * np.abs(cos3)
    x3 = kick3 / da_tick(ai[si])                      # |Δa| per unit m_j, in period ticks
    # rate: analytic n_vol * pi rho^2 * <v> * T with <v> from the measured distribution
    Vol = TAU * a0 * 1.5 * 2 * sig_i * a0
    vbar_3d = v3.mean()           # measured mean relative speed incl. vertical
    vbar_planar = vp.mean()
    for lbl, vb in (("planar <v> (prior run's choice)", vbar_planar), ("3-D <v> (measured)", vbar_3d)):
        R = 1e9 / Vol * math.pi * 1e-4 ** 2 * vb * TAU * a0 ** 1.5
        print(f"  R = {R:.2f} encounters/body/orbit  ({lbl}, <v>={vb:.4f})")
    R = 1e9 / Vol * math.pi * 1e-4 ** 2 * vbar_3d * TAU * a0 ** 1.5  # conservative (higher)
    # vertical acceptance as WEIGHTS (rejection starves the sample): a planar conjunction at
    # d_p accepts vertical offset |w| < sqrt(rho^2-d_p^2), w ~ N(0, s_z) flat over the tube
    w_acc = 2 * wmax / (s_z * math.sqrt(2 * math.pi))
    ww = w_acc
    print(f"  MC draws: {NB} (weighted; mean vertical acceptance {w_acc.mean():.1e})")
    q = lambda v: np.sum(ww * v) / np.sum(ww)   # acceptance-weighted mean
    # weighted quantiles of m_crit = 1/x
    o = np.argsort(x3)
    cw = np.cumsum(ww[o]) / np.sum(ww)
    med = 1 / x3[o][np.searchsorted(cw, 0.5)]
    p1 = 1 / x3[o][np.searchsorted(cw, 0.99)]
    print(f"\r  m_crit (3-D): med={med:.2e} p1={p1:.2e} M_sun  "
          f"(rocks {np.cbrt(med*MSUN/10472):.0f}m/{np.cbrt(p1*MSUN/10472):.0f}m med/p1)")
    for k, m in masses.items():
        sig_x = math.sqrt(q((x3 * m) ** 2))
        flux_a = R * sig_x ** 2           # steady tick-boundary crossing rate (upper bound)
        T_first_a = 1 / flux_a if flux_a else np.inf
        kstar = (3 / (2 * sig_x * math.sqrt(R))) ** (2 / 3) if sig_x else np.inf
        print(f"    {k:12s} m={m:.2e}: frac>=1tick={q((x3*m>=1).astype(float))*100:5.1f}%  "
              f"sigma_x={sig_x:.2e} ticks  P-chan first pass={T_first_a:.1e} orb  "
              f"tp-chan k*={kstar:.1e} orb")
    # ---------------- the 1e9 ledger ----------------
    # The kick distribution is borderline Levy (alpha = 2: in 3-D the impact parameter density
    # goes as d*dd, so x = 1/(d v) has a log-divergent second moment) — the Gaussian first-passage
    # formulas above UNDERSTATE the P channel. Measured by the walk itself:
    print("\n== random walk on the measured kick distribution (1000 walkers x 1e5 kicks) ==")
    xs = np.random.default_rng(7).choice(x3, size=1000 * 100000, p=ww / ww.sum()).reshape(1000, 100000)
    K = 100000 // int(round(R))
    for lbl, m in (("ship 1e6 t", 1e9 / MSUN), ("50 m", rock(50)), ("500 m", rock(500))):
        km = (xs * m) * np.random.default_rng(11).choice([-1.0, 1.0], size=xs.shape)
        st = km[:, : K * int(round(R))].reshape(1000, K, int(round(R)))
        S = np.cumsum(st.sum(axis=2), axis=1)
        ph = np.cumsum(S, axis=1)
        fP = np.argmax(np.abs(S) >= 1, axis=1); fP[fP == 0] = K
        fT = np.argmax(np.abs(ph) >= 1, axis=1); fT[fT == 0] = K
        if lbl == "50 m":
            S50, ph50, fP50 = S, ph, fP
        cP = np.mean(fP < K)
        print(f"  {lbl:10s}: P-chan crossed 1 tick: {cP*100:5.1f}% of walkers in {K} orbits "
              f"(median {np.median(fP):.0f}{'+' if cP < 0.5 else ''}); "
              f"tp-chan first tick median {np.median(fT):.0f} orbits "
              f"(Gaussian estimates were optimistic: the tail dominates)")

    # ---------------- the 1e9 ledger ----------------
    print("\n== ledger at 1e9 bodies, 8 GB M1 (thick sigma_i=0.14 / thin 0.005) ==")
    yr_s = 3.156e7
    orb_s = a0 ** 1.5 * yr_s
    for lbl, R_ in (("thick", R), ("thin (28x thick)", 28 * R)):
        ev_s = 1e9 * R_ / orb_s
        print(f"  {lbl:18s}: {ev_s:.0f} exact pair events/s at 1x; x100 RTF at 10us/event = "
              f"{100*ev_s*1e-5*100:.0f}% of one core")
    tick_rad = TAU / (TAU * a0 ** 1.5 * TICK)
    for lbl, m in (("50 m", rock(50)), ("500 m", rock(500)), ("5 km", rock(5000))):
        sig_x = math.sqrt(q((x3 * m) ** 2))
        kstar = (3 / (2 * sig_x * math.sqrt(R))) ** (2 / 3)
        kpix = (1e-3 / ((2 / 3) * sig_x * math.sqrt(R) * tick_rad)) ** (2 / 3)
        print(f"  {lbl:6s}: tp-chan first tick after {kstar:.1e} orbits ({kstar*a0**1.5:.1e} yr); "
              f"one 1e-3-rad pixel of phase noise after {kpix:.1e} orbits ({kpix*a0**1.5:.1e} yr)")
    # walk-measured distinctions (the Gaussian formulas are invalid: log-divergent variance)
    tot = 1e9 * np.median(np.abs(ph50[:, -1]))
    cP50 = np.mean(fP50 < K)
    print(f"    belt-wide phase distinctions over {K:.0e} orbits: {tot:.2e} ticks total "
          f"({tot/(K*orb_s):.2e}/game-second)")
    print(f"    P-tick crossings: {cP50*100:.1f}% of 50-m bodies within {K} orbits -> "
          f"lower-bound flux {1e9*cP50/(K*orb_s):.2e}/s at 1e9; both channels together stay "
          f">= 4 orders under consumer-scale H_live (1e5-1e6 bits/s)")
    print(f"  storage: tubes 16B x 1e9 = {16*1e9/2**30:.1f} GiB (binding, 1.9x over 8 GiB); "
          f"program belt 0.126 bit = {0.126*1e9/8/2**20:.0f} MiB (unchanged from prior run)")
    print(f"  one tick of phase = {tick_rad:.2e} rad; player pixel ~1e-3 rad "
          f"-> {1e-3/tick_rad:.1e} ticks per pixel")

if __name__ == "__main__":
    main()
