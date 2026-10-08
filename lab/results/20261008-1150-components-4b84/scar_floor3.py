#!/usr/bin/env python3
"""Scar-ledger floor v3 (decisive). v1 bug: plug-in histogram entropy saturates at
log2(n_samples). v2 bug: the phase axis quantized X to the E-grid before scaling to
clock quanta (double quantization). v3 computes every axis by exact FFT of the
compound-Poisson characteristic function on ITS OWN quantum grid, Gaussian branch
only when CLT conditions hold (sigma/q >= 64 and neff >= 50, or FFT grid > 2^18).
"""
import json, time, platform
import numpy as np

rng = np.random.default_rng(20261008)
AU = 1.496e11; MSUN = 1.989e30; G = 6.674e-11; RHO = 2500.0
a0 = 2.5 * AU; W = 0.25 * AU
N = 10**9
sig_e = 0.07; sig_i = 0.035
mu = G * MSUN
vk = np.sqrt(mu / a0)
Torb = 2 * np.pi * np.sqrt(a0**3 / mu)
Vslab = (2*np.pi*a0) * (2*W) * (1.6 * a0 * sig_i * np.sqrt(2))

# v_rel from sampled Kepler velocity offsets (same seed/logic as v1/v2)
e = rng.rayleigh(sig_e, (200000, 2)); inc = rng.rayleigh(sig_i, (200000, 2))
f = rng.uniform(0, 2*np.pi, (200000, 2)); g = rng.uniform(0, 2*np.pi, (200000, 2))
u1 = np.stack([e[:,0]*np.sin(f[:,0]), e[:,0]*np.cos(f[:,0]), inc[:,0]*np.sin(g[:,0])], 1)
u2 = np.stack([e[:,1]*np.sin(f[:,1]), e[:,1]*np.cos(f[:,1]), inc[:,1]*np.sin(g[:,1])], 1)
VREL = float(np.median(vk*np.linalg.norm(u1-u2, axis=1)))

def dist_entropy(lam, w, t, mcap=18):
    """(H bits, sigma, neff, p_zero, method) of round(X/q) for X = compound Poisson of
    +/- w_b steps, counts Poisson(lam_b t); w already in quanta of the storage grid."""
    lam_t = lam * t
    neff = float(lam_t.sum())
    sig = float(np.sqrt((lam_t * w**2).sum()))
    maxw = float(w.max())
    span = 6*sig + 3*maxw + 4
    Mbits = max(4, int(np.ceil(np.log2(2*span))))
    if (sig >= 64 and neff >= 50) or Mbits > mcap:
        return 0.5*np.log2(2*np.pi*np.e*sig**2), sig, neff, "gauss", 0.0
    M = 1 << Mbits
    k = np.arange(M); th = 2*np.pi*k/M
    phi = np.exp((lam_t[:, None] * (np.cos(np.outer(w, th)) - 1)).sum(0))
    p = np.fft.irfft(phi, n=M)
    p = np.clip(p, 0, None); p /= p.sum()
    pn = p[p > 1e-14]
    return float(-(pn*np.log2(pn)).sum()), sig, neff, ("fft%d" % Mbits), float(p[0])

def folded_dist_entropy(lam, w, t, mcap=18):
    """Entropy of |round(X/q)| (phase axis): full grid, then fold +-."""
    H, sig, neff, meth, _p0 = dist_entropy(lam, w, t, mcap)
    if meth == "gauss":
        return np.log2(sig) + 1.046, sig, neff, meth, 0.0  # entropy of quantized |N(0,sig)|
    M = 1 << int(meth[3:])
    lam_t = lam * t
    k = np.arange(M); th = 2*np.pi*k/M
    phi = np.exp((lam_t[:, None] * (np.cos(np.outer(w, th)) - 1)).sum(0))
    p = np.fft.irfft(phi, n=M)
    p = np.clip(p, 0, None); p /= p.sum()
    sabs = np.abs(np.fft.fftfreq(M)) * M          # |s| of each grid index
    sabs = np.rint(sabs).astype(np.int64)
    q = np.bincount(sabs, weights=p, minlength=int(sabs.max())+1)
    q = np.clip(q, 0, None); q /= q.sum()
    qn = q[q > 1e-14]
    return float(-(qn*np.log2(qn)).sum()), sig, neff, meth, float(q[0])

def bits_with_presence(H, pnz):
    return 0.0 if pnz <= 0 else H*pnz + pnz*(np.log2(1/pnz) + 2)

def belt(M_belt, N=N):
    m = M_belt / N
    R = (3*m/(4*np.pi*RHO))**(1/3.)
    b_min = 2*R
    b_max = a0 * ((2*m)/(3*MSUN))**(1/3.)
    edges = np.geomspace(b_min, b_max, 41)
    bc = np.sqrt(edges[:-1]*edges[1:]); db = np.diff(edges)
    n_dens = N / Vslab
    lam = n_dens * 2*np.pi*bc*VREL*Torb*db
    dv = 2*G*m/(bc*VREL)
    wE = (2*dv/vk)/np.sqrt(3)          # per-event sd, relative |E| units
    wL = (dv/vk)*np.sqrt(2/3)          # relative L units
    wpi = (2*G*m/(bc*VREL**2))/np.sqrt(3)  # radians
    return dict(m=m, R=R, b_min=b_min, b_max=b_max, lam=lam, wE=wE, wL=wL, wpi=wpi,
                lam_tot=float(lam.sum()), n_dens=n_dens)

def scenario(M_belt, t, B, clocks=(("2^-32", 2.0**-32), ("2^-20", 2.0**-20)), jbits=(16,24,32)):
    out = {"M_belt_kg": M_belt, "t_orbits": t, "grids": {}}
    for j in jbits:
        q = 0.18 * 2.0**-j
        qp = 2*np.pi * 2.0**-j
        shape = {}; shape_tot = 0.0; pnz_shape = 0.0
        for name, w, qq in (("dE", B["wE"], q), ("dL", B["wL"], q), ("dvarpi", B["wpi"], qp)):
            H, sig, neff, meth, p0 = dist_entropy(B["lam"], w/qq, t)
            pnz = 1.0 - p0   # exact: no stored integer differs from the program's
            b = bits_with_presence(H, pnz)
            shape[name] = {"bits": round(b, 2), "sig_over_q": round(sig, 1), "method": meth}
            shape_tot += b
            pnz_shape = max(pnz_shape, pnz)
        phase = {}
        for cname, qt in clocks:
            wclock = B["wE"] * (0.75*1.5*t) / qt   # E-steps scaled to clock quanta
            H, sig, neff, meth, p0 = folded_dist_entropy(B["lam"], wclock, t)
            pnz = 1.0 - p0
            phase[cname] = {"bits": round(bits_with_presence(H, pnz), 2),
                            "sig_over_q": round(sig, 1), "method": meth}
        out["grids"][f"j{j}"] = {"shape": shape, "shape_total": round(shape_tot, 2),
                                 "phase": phase, "pnz_shape": round(pnz_shape, 4)}
        out["sig_dE/E"] = float(np.sqrt(t*(B["lam"]*B["wE"]**2).sum()))
    return out

t0 = time.time()
R = {"machine": platform.node(), "v_rel_mps": VREL, "n_at_N1e9": N/Vslab,
     "Torb_s": Torb, "runs": []}
B1 = belt(3e21); B2 = belt(3e22); B3 = belt(3e21, N=10**8)
R["lam_tot_base"] = B1["lam_tot"]; R["lam_tot_N1e8"] = B3["lam_tot"]
for M, B, ts in ((3e21, B1, [1e2, 1e3, 1e4, 1e5]), (3e22, B2, [1e1, 1e2, 1e3, 1e4])):
    for t in ts:
        r = scenario(M, t, B)
        R["runs"].append(r)
        for j, cname in (("j32", "2^-32"), ("j32", "2^-20"), ("j16", "2^-20")):
            pass
        g32 = r["grids"]["j32"]
        print(f"M={M:.0e} t={t:>7.0e} sigE={r['sig_dE/E']:.2e} shape32={g32['shape_total']:5.1f} "
              f"ph32={g32['phase']['2^-32']['bits']:5.1f}({g32['phase']['2^-32']['method']}) "
              f"ph20={g32['phase']['2^-20']['bits']:5.1f}")
s9 = scenario(3e21, 1e3, B1)["sig_dE/E"]; s8 = scenario(3e21, 1e3, B3)["sig_dE/E"]
R["N_scaling"] = {"sigma_N1e9": s9, "sigma_N1e8": s8, "ratio": s8/s9, "predicted": np.sqrt(10)}
print("N-scaling ratio (predicted 3.162):", round(s8/s9, 3))
R["wall_s"] = time.time() - t0
json.dump(R, open("scar_floor3_out.json", "w"), indent=1, default=float)
print("wall", round(R["wall_s"], 1))
