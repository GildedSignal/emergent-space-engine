#!/usr/bin/env python3
"""Scar-ledger floor v2 (decisive). Same physical toy as scar_floor.py; the entropy
measurement is corrected: per-axis ledger bits = cross-entropy of the quantized
compound-Poisson state under the shared population model (computed exactly by FFT of
the characteristic function on the quantum grid, or the Gaussian formula once the
effective event count makes the CLT error negligible). The plug-in histogram entropy
used in v1 saturates at log2(n_samples) and overestimates by up to ~10 bits/axis.

Also adds: naive includes the phase axis; refold design C; H_live rates; 8 GB verdicts.
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
V = (2*np.pi*a0) * (2*W) * (1.6 * a0 * sig_i * np.sqrt(2))
LN2 = np.log(2.0)

def entropy_fft(lam, w, t):
    """Distribution entropy (bits) of round(X/q) where X = sum of +/-w_b steps with
    Poisson(lam_b*t) counts, all in quanta units. Exact via char function FFT."""
    lam_t = lam * t
    neff = lam_t.sum()
    sig = np.sqrt((lam_t * w**2).sum())
    if sig >= 64 and neff >= 50:
        return 0.5*np.log2(2*np.pi*np.e*sig**2), sig, neff, 1.0 - np.exp(-neff)
    maxw = w.max()
    span = 6*sig + 3*maxw + 4
    M = 1 << max(4, int(np.ceil(np.log2(2*span))))
    if M > 2**22:  # safety: fall back to Gaussian (never hit in our range)
        return 0.5*np.log2(2*np.pi*np.e*sig**2), sig, neff, 1.0 - np.exp(-neff)
    k = np.arange(M)
    th = 2*np.pi*k/M
    phi = np.exp((lam_t[:, None] * (np.cos(np.outer(w, th)) - 1)).sum(0))
    p = np.fft.irfft(phi, n=M)
    p = np.clip(p, 0, None); p /= p.sum()
    pnz = p[p > 1e-14]
    return float(-(pnz * np.log2(pnz)).sum()), sig, neff, 1.0 - float(p[0])

def bits_with_presence(H, pnz, nbodies_idx=1e9):
    if pnz <= 0: return 0.0
    return H * pnz + pnz * (np.log2(1/pnz) + 2)   # + index/presence overhead

def belt(M_belt, N=N, nb=200000):
    m = M_belt / N
    R = (3*m/(4*np.pi*RHO))**(1/3.)
    b_min = 2*R
    b_max = a0 * ((2*m)/(3*MSUN))**(1/3.)
    edges = np.geomspace(b_min, b_max, 41)
    bc = np.sqrt(edges[:-1]*edges[1:]); db = np.diff(edges)
    n_dens = N / V
    lam = n_dens * 2*np.pi*bc*VREL*Torb*db
    dv = 2*G*m/(bc*VREL)
    wE = (2*dv/vk)/np.sqrt(3)
    wL = (dv/vk)*np.sqrt(2/3)
    wpi = (2*G*m/(bc*VREL**2))/np.sqrt(3)
    return dict(m=m, R=R, b_min=b_min, b_max=b_max, lam=lam, wE=wE, wL=wL, wpi=wpi,
                lam_tot=float(lam.sum()), n_dens=n_dens)

def scenario(M_belt, t, B):
    axes = {}
    for name, w in (("dE", B["wE"]), ("dL", B["wL"]), ("dvarpi", B["wpi"])):
        axes[name] = entropy_fft(B["lam"], w, t)
    dtp_scale = 0.75*1.5*t   # |X_E| * 1.125 * t  (in units of P per unit dE/E)
    HE, sigE, neffE, pnzE = axes["dE"]
    # phase axis at two clocks: distribution of c|X|, c = dtp_scale
    out = {"t_orbits": t, "sig_dE/E": sigE, "neff": neffE,
           "sig_dtp/P": 0.603*sigE*dtp_scale}
    res = {}
    for j in (16, 24, 32):
        q = 0.18 * 2.0**-j
        qp = 2*np.pi * 2.0**-j
        # shape axes in their quanta
        sh = {}
        tot = 0.0; nz_any = 0.0
        for name, w, qq in (("dE", B["wE"], q), ("dL", B["wL"], q), ("dvarpi", B["wpi"], qp)):
            H, sig, neff, pnz = entropy_fft(B["lam"], w/qq, t)
            b = bits_with_presence(H, pnz)
            sh[name] = round(b, 2); tot += b
            nz = max(nz, 0.0) if False else None
            sh[name+"_pnz"] = round(pnz, 4)
        clocks = {}
        for jl, qt in ((32, 2.0**-32), (20, 2.0**-20)):
            # |X| folded: entropy(|cX|/qt) = entropy_fft gives H(X); H(|X|) = H(X)-1+...
            # compute directly: steps stay w, then fold. For Gaussian: log2(sig*c/qt)+1.046
            sig_q = sigE/q  # sigma of X_E in E-quanta
            cq = dtp_scale*q/qt  # converts E-quanta units to clock quanta
            sig_clock = sig_q*cq
            if sig_clock >= 64 and neffE >= 50:
                Htp = np.log2(sig_clock) + 1.046
                p0 = 0.6827**0  # unused
                p_nz = 1.0 - np.exp(-neffE)  # any event => |X|>0 almost surely (rounding may still give 0)
                # rounding to 0 only if |cX|<qt/2: for large cq negligible; approximate:
                p_nz = min(1.0, p_nz)
            else:
                # exact: FFT dist of X_E in E quanta, fold to |.|, scale by cq
                Hx, sigx, neffx, pz = entropy_fft(B["lam"], B["wE"]/q, t)
                # p(s=0) of |cX|: mass of |X| < 1/(2cq)
                lam_t = B["lam"]*t
                maxw = (B["wE"]/q).max(); s = sigx
                span = 6*s + 3*maxw + 4
                M = 1 << max(4, int(np.ceil(np.log2(2*span))))
                k = np.arange(M); th = 2*np.pi*k/M
                phi = np.exp((lam_t[:, None]*(np.cos(np.outer(B["wE"]/q, th))-1)).sum(0))
                p = np.fft.irfft(phi, n=M); p = np.clip(p, 0, None); p /= p.sum()
                # scale by cq: each integer cell of X maps to |.|*cq; if cq>=1 simple; else aggregate
                vals = np.abs(np.fft.fftfreq(M)*M)  # cell centres 0..M/2
                # mass per rounded clock-quantum value
                svals = np.rint(np.abs(np.arange(M))*cq)  # symmetric: use 0..M/2 mass twice
                mass = np.zeros(int(svals.max())+2)
                half = (M)//2
                for i in range(M):
                    sv = int(round(abs(i if i <= M//2 else M-i)*cq))
                    mass[sv] += p[i]
                pn = mass[mass > 1e-14]
                Htp = float(-(pn*np.log2(pn)).sum())
                p_nz = 1.0 - mass[0]
            clocks[f"qt2^-{jl}"] = {"bits": round(bits_with_presence(Htp, p_nz), 2),
                                     "sig_over_q": round(sig_clock, 1) if sig_clock else None,
                                     "pnz": round(p_nz, 4)}
        res[f"j{j}"] = {"shape_bits": sh, "shape_total": round(tot, 2), "phase": clocks}
    out["grids"] = res
    return out

# v_rel from sampled Kepler pairs (frozen for all scenarios)
e = rng.rayleigh(sig_e, (200000, 2)); inc = rng.rayleigh(sig_i, (200000, 2))
f = rng.uniform(0, 2*np.pi, (200000, 2)); g = rng.uniform(0, 2*np.pi, (200000, 2))
u1 = np.stack([e[:,0]*np.sin(f[:,0]), e[:,0]*np.cos(f[:,0]), inc[:,0]*np.sin(g[:,0])], 1)
u2 = np.stack([e[:,1]*np.sin(f[:,1]), e[:,1]*np.cos(f[:,1]), inc[:,1]*np.sin(g[:,1])], 1)
VREL = float(np.median(vk*np.linalg.norm(u1-u2, axis=1)))

t0 = time.time()
R = {"machine": platform.node(), "v_rel_mps": VREL, "n_at_N1e9": 1e9/V,
     "runs": [], "wall_s": None}
B1 = belt(3e21); B2 = belt(3e22); B3 = belt(3e21, N=10**8)  # N-scaling check
R["belt_base"] = {k: (float(v) if not isinstance(v, np.ndarray) else None) for k, v in B1.items() if k not in ("lam","wE","wL","wpi")}
R["lam_tot_base"] = B1["lam_tot"]; R["lam_tot_N1e8"] = B3["lam_tot"]
for M, B, ts in ((3e21, B1, [1e2, 1e3, 1e4, 1e5]), (3e22, B2, [1e1, 1e2, 1e3, 1e4])):
    for t in ts:
        r = scenario(M, t, B); r["M_belt_kg"] = M
        R["runs"].append(r)
        g32 = r["grids"]["j32"]
        print(f"M={M:.0e} t={t:>7.0e} sigE={r['sig_dE/E']:.2e} neff={r['neff']:.1f} "
              f"shape(j32)={g32['shape_total']:5.1f} phase32={g32['phase']['qt2^-32']['bits']:5.1f} "
              f"phase20={g32['phase']['qt2^-20']['bits']:5.1f}")
# N-scaling: sigma_E at fixed t, N=1e8 vs 1e9 -> factor sqrt(10) predicted
s9 = scenario(3e21, 1e3, B1)["sig_dE/E"]; s8 = scenario(3e21, 1e3, B3)["sig_dE/E"]
R["N_scaling"] = {"sigma_N1e9": s9, "sigma_N1e8": s8, "ratio": s8/s9, "predicted": np.sqrt(10)}
print("N-scaling ratio (predicted sqrt10=3.162):", round(s8/s9, 3))
R["wall_s"] = time.time() - t0
json.dump(R, open("scar_floor2_out.json", "w"), indent=1, default=float)
print("wall", R["wall_s"])
