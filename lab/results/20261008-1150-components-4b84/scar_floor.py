#!/usr/bin/env python3
"""Scar-ledger floor of a self-stirred belt (components lens, run 20261008-1150).

Question: what is the information floor of the live ledger a belt's own stirring
creates (bits/body, growth in time), and which store design tracks it:
A naive (touched body -> 16-byte tube, kept), B integer scar ledger, C ledger+refold.

Model: impulse-approximation encounters, miss distance uniform in b^2 between 2R and the
mutual Hill radius; v_rel sampled from Kepler pairs; per-band Poisson counts over the
horizon (increments are iid, so the state at t is a compound Poisson draw).
Axes: dE/E, dL/L, dvarpi (random walks), dt_p/P (phase drift = 0.75*1.5*(dE/E)*t,
the 0.75 averaging jumps' age over the horizon).
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

# v_rel from sampled Kepler velocity offsets (radial/tangential/vertical epicyclic terms)
def sample_vrel(n):
    e = rng.rayleigh(sig_e, (n, 2)); inc = rng.rayleigh(sig_i, (n, 2))
    f = rng.uniform(0, 2*np.pi, (n, 2)); g = rng.uniform(0, 2*np.pi, (n, 2))
    u1 = np.stack([e[:,0]*np.sin(f[:,0]), e[:,0]*np.cos(f[:,0]), inc[:,0]*np.sin(g[:,0])], 1)
    u2 = np.stack([e[:,1]*np.sin(f[:,1]), e[:,1]*np.cos(f[:,1]), inc[:,1]*np.sin(g[:,1])], 1)
    return vk * np.linalg.norm(u1 - u2, axis=1)

vrel_s = sample_vrel(200000)
v_rel = float(np.median(vrel_s))

# number density: slab volume V = (2 pi a)(2 W)(1.6 sigma_z), sigma_z = a sig_i sqrt(2)
V = (2*np.pi*a0) * (2*W) * (1.6 * a0 * sig_i * np.sqrt(2))
n_dens = N / V

def entropy_bits(x_int):
    _, c = np.unique(x_int, return_counts=True)
    p = c / c.sum()
    return float(-(p * np.log2(p)).sum())

def run(M_belt, t_orbits, nb=200000, jbits=(16, 24, 32), qtp=(2.0**-32, 2.0**-20)):
    m = M_belt / N
    R = (3*m/(4*np.pi*RHO))**(1/3.)
    b_min = 2*R
    b_max = a0 * ((2*m)/(3*MSUN))**(1/3.)   # mutual Hill
    nbands = 40
    edges = np.geomspace(b_min, b_max, nbands+1)
    bc = np.sqrt(edges[:-1]*edges[1:]); db = np.diff(edges)
    lam = n_dens * 2*np.pi*bc*v_rel*Torb*db         # encounters per body per orbit per band
    dv = 2*G*m/(bc*v_rel)                            # impulse per encounter at band centre
    wE = (2*dv/vk)/np.sqrt(3)                        # per-event sd of dE/E
    wL = (dv/vk)*np.sqrt(2/3)                        # per-event sd of dL/L
    wpi = (2*G*m/(bc*v_rel**2))/np.sqrt(3)           # per-event sd of deflection (rad)
    lam_tot = float(lam.sum())
    # per-band compound draws over the whole horizon (iid increments -> state at t)
    cE = rng.poisson(lam*t_orbits, (nb, nbands)); sE = rng.binomial(cE, 0.5)
    dEE = ((2*sE - cE) * wE).sum(1)
    cL = rng.poisson(lam*t_orbits, (nb, nbands)); sL = rng.binomial(cL, 0.5)
    dLL = ((2*sL - cL) * wL).sum(1)
    cP = rng.poisson(lam*t_orbits, (nb, nbands)); sP = rng.binomial(cP, 0.5)
    dpi = ((2*sP - cP) * wpi).sum(1)
    dtp = 0.75*1.5*np.abs(dEE)*t_orbits              # phase drift in units of P
    sigE, sigL, sigPi, sigTp = float(dEE.std()), float(dLL.std()), float(dpi.std()), float(dtp.std())
    closed_E = np.sqrt(t_orbits * (lam*wE**2).sum())
    out = {"M_belt_kg": M_belt, "t_orbits": t_orbits, "m_per_body_kg": m, "R_m": R,
           "b_min_m": b_min, "b_max_m": b_max, "lam_per_orbit": lam_tot,
           "sig_dE/E": sigE, "sig_dL/L": sigL, "sig_dvarpi_rad": sigPi, "sig_dtp_over_P": sigTp,
           "closed_form_sigE": float(closed_E), "kappa": sigE/closed_E,
           "birth_sigma_E_relative": W/(2*a0)}
    grids = {}
    for j in jbits:
        q = 0.18 * 2.0**-j          # E and L grids: band range over 2^j levels
        qp = 2*np.pi * 2.0**-j      # varpi grid
        axes = {"dE": np.rint(dEE/q).astype(np.int64),
                "dL": np.rint(dLL/q).astype(np.int64),
                "dvarpi": np.rint(dpi/qp).astype(np.int64)}
        # naive: any nonzero integer on any axis -> full 16-byte tube forever
        touched = np.zeros(nb, bool)
        for v in axes.values(): touched |= (v != 0)
        # phase axis at two clock quanta
        for qt in qtp:
            axes[f"dtp@2^-{int(round(-np.log2(qt)))}"] = np.rint(dtp/qt).astype(np.int64)
        bits = {}; Htot = 0.0
        for k, v in axes.items():
            nz = int((v != 0).sum())
            if nz:
                Htot += entropy_bits(v[v != 0]) * nz/nb + (nz/nb)*(np.log2(nb/nz) + 2)
            bits[k] = {"nonzero_frac": nz/nb, "bits_per_body": (entropy_bits(v[v != 0]) * nz/nb + (nz/nb)*(np.log2(nb/nz)+2)) if nz else 0.0}
        grids[f"j{j}"] = {
            "q_E_rel": q, "ledger_bits_per_body": Htot,
            "naive_bits_per_body": float(touched.mean()*128 + (touched.mean())*np.log2(1/max(touched.mean(),1e-12))*0),
            "axes": bits}
        grids[f"j{j}"]["naive_bits_per_body"] = float(touched.mean())*128
    out["grids"] = grids
    return out

t0 = time.time()
res = {"machine": platform.node(), "numpy": np.__version__,
       "params": {"a_AU": 2.5, "W_AU": 0.5, "N": N, "sig_e": sig_e, "sig_i": sig_i,
                  "v_rel_median_mps": v_rel, "n_density_per_m3": n_dens, "Torb_s": Torb},
       "runs": []}
cases = [(3e21, [1e2, 1e3, 1e4, 1e5]), (3e22, [1e1, 1e2, 1e3, 1e4])]
for M, ts in cases:
    for t in ts:
        r = run(M, t)
        res["runs"].append(r)
        g32 = r["grids"]["j32"]
        print(f"M={M:.0e} t={t:>8.0e} orb  sigE={r['sig_dE/E']:.2e} kappa={r['kappa']:.2f} "
              f"ledger(j32)={g32['ledger_bits_per_body']:.3f}b/b naive={g32['naive_bits_per_body']:.1f}b/b "
              f"sigTp={r['sig_dtp_over_P']:.2e}")
res["wall_s"] = time.time() - t0
with open(__file__.replace(".py", "_out.json"), "w") as f:
    json.dump(res, f, indent=1)
print("wall", res["wall_s"])
