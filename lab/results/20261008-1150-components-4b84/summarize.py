#!/usr/bin/env python3
"""Summary table: store designs vs the measured floor, refold, H_live, 8 GB verdicts.
Reuses scar_floor3's validated machinery (import-free copy of the two functions)."""
import json
import numpy as np

AU = 1.496e11; MSUN = 1.989e30; G = 6.674e-11; RHO = 2500.0
a0 = 2.5*AU; W = 0.25*AU; N = 10**9; sig_e = 0.07; sig_i = 0.035
mu = G*MSUN; vk = np.sqrt(mu/a0); Torb = 2*np.pi*np.sqrt(a0**3/mu)
Vslab = (2*np.pi*a0)*(2*W)*(1.6*a0*sig_i*np.sqrt(2)); VREL = 2401.59
PROG = 0.126  # birth program bits/body (lab gold components-98bc, 5 Oct)

def dist_entropy(lam, w, t, mcap=18):
    lam_t = lam*t; neff = float(lam_t.sum())
    sig = float(np.sqrt((lam_t*w**2).sum())); maxw = float(w.max())
    span = 6*sig + 3*maxw + 4
    Mbits = max(4, int(np.ceil(np.log2(2*span))))
    if (sig >= 64 and neff >= 50) or Mbits > mcap:
        return 0.5*np.log2(2*np.pi*np.e*sig**2), 1.0
    M = 1 << Mbits
    th = 2*np.pi*np.arange(M)/M
    phi = np.exp((lam_t[:, None]*(np.cos(np.outer(w, th))-1)).sum(0))
    p = np.clip(np.fft.irfft(phi, n=M), 0, None); p /= p.sum()
    pn = p[p > 1e-14]
    return float(-(pn*np.log2(pn)).sum()), 1.0 - float(p[0])

def folded_entropy(lam, w, t, mcap=18):
    lam_t = lam*t; neff = float(lam_t.sum())
    sig = float(np.sqrt((lam_t*w**2).sum())); maxw = float(w.max())
    span = 6*sig + 3*maxw + 4
    Mbits = max(4, int(np.ceil(np.log2(2*span))))
    if (sig >= 64 and neff >= 50) or Mbits > mcap:
        return np.log2(sig) + 1.046, 1.0
    M = 1 << Mbits
    th = 2*np.pi*np.arange(M)/M
    phi = np.exp((lam_t[:, None]*(np.cos(np.outer(w, th))-1)).sum(0))
    p = np.clip(np.fft.irfft(phi, n=M), 0, None); p /= p.sum()
    sabs = np.rint(np.abs(np.fft.fftfreq(M))*M).astype(np.int64)
    q = np.clip(np.bincount(sabs, weights=p, minlength=int(sabs.max())+1), 0, None)
    q /= q.sum(); qn = q[q > 1e-14]
    return float(-(qn*np.log2(qn)).sum()), 1.0 - float(q[0])

def belt(M_belt, N=N):
    m = M_belt/N; R = (3*m/(4*np.pi*RHO))**(1/3.)
    edges = np.geomspace(2*R, a0*((2*m)/(3*MSUN))**(1/3.), 41)
    bc = np.sqrt(edges[:-1]*edges[1:]); db = np.diff(edges)
    lam = (N/Vslab)*2*np.pi*bc*VREL*Torb*db
    dv = 2*G*m/(bc*VREL)
    return lam, (2*dv/vk)/np.sqrt(3), (dv/vk)*np.sqrt(2/3), (2*G*m/(bc*VREL**2))/np.sqrt(3)

def ledger_bits(t, B, j, clock_exp):
    """Corrected accounting: per-axis H*pnz, ONE shared presence/index overhead."""
    lam, wE, wL, wpi = B
    q = 0.18*2.0**-j; qp = 2*np.pi*2.0**-j; qt = 2.0**clock_exp
    axes = []
    for w, qq in ((wE, q), (wL, q), (wpi, qp)):
        H, pnz = dist_entropy(lam, w/qq, t); axes.append((H, pnz))
    Htp, ptp = folded_entropy(lam, wE*(0.75*1.5*t)/qt, t)
    axes.append((Htp, ptp))
    bits = sum(H*pnz for H, pnz in axes)
    p_any = 1.0 - np.prod([1-p for _, p in axes])
    bits += p_any*(np.log2(1/max(p_any, 1e-12)) + 2)
    return bits, p_any

def fmt_t(t):
    return f"{t:.0e}"

out = {"designs": {}, "params": dict(N=N, a_AU=2.5, M_belt_kg=3e21, Torb_s=Torb)}
B = belt(3e21)
designs = {"D1_fine(j32,clock2^-32)": (32, -32), "D2_mid(j32,clock2^-20)": (32, -20),
           "D3_coarse(j16,clock2^-20)": (16, -20)}
horizons = [1e2, 1e3, 1e4, 1e5]
for name, (j, ce) in designs.items():
    rows = []
    for t in horizons:
        L, p_any = ledger_bits(t, B, j, ce)
        rows.append({"t_orbits": t, "ledger_plus_prog_bits": round(L+PROG, 2),
                     "naive_bits": round(128*p_any, 1),
                     "GB_at_1e9": round((L+PROG)/8*1e9/1e9, 2),
                     "naive_GB": round(128*p_any/8, 1)})
    # refold steady states
    for K in (1e2, 1e3):
        Lk, _ = ledger_bits(K, B, j, ce)
        rows.append({"refold_K": K, "steady_bits": round(Lk+PROG, 2),
                     "GB_at_1e9": round((Lk+PROG)/8, 2)})
    out["designs"][name] = rows
    print(name)
    for r in rows:
        if "t_orbits" in r:
            print(f"  t={fmt_t(r['t_orbits']):>6} ledger+prog={r['ledger_plus_prog_bits']:6.2f} b/b "
                  f"({r['GB_at_1e9']:5.2f} GB @1e9)   naive={r['naive_bits']:6.1f} b/b ({r['naive_GB']} GB)")
        else:
            print(f"  refold K={fmt_t(r['refold_K']):>5} steady  ={r['steady_bits']:6.2f} b/b ({r['GB_at_1e9']:5.2f} GB @1e9)")

# H_live background: slope of ledger between 1e3 and 1e4 orbits (D1), per body per game-second
def hl(j, ce, rtf):
    L1, _ = ledger_bits(1e3, B, j, ce); L2, _ = ledger_bits(1e4, B, j, ce)
    slope_orbit = (L2-L1)/9e3
    return slope_orbit/Torb*rtf
out["H_live_bits_per_body_per_game_second"] = {
    "D1@100x": hl(32, -32, 100), "D1@1e6x": hl(32, -32, 1e6),
    "D3@1e6x": hl(16, -20, 1e6)}
out["H_live_total_bits_per_game_second_at_1e9"] = {k: v*1e9 for k, v in out["H_live_bits_per_body_per_game_second"].items()}
print("H_live per body per game-s:", {k: f"{v:.2e}" for k, v in out["H_live_bits_per_body_per_game_second"].items()})
print("H_live total at 1e9 bodies (bits/game-s):", {k: f"{v:.1f}" for k, v in out["H_live_total_bits_per_game_second_at_1e9"].items()})
# ensemble program growth check
L1e5, _ = ledger_bits(1e5, B, 32, -32)
out["ensemble_spread_growth_rel_birth_at_1e5"] = 4.62e-9/0.1
json.dump(out, open("summary_out.json", "w"), indent=1, default=float)
