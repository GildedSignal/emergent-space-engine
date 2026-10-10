#!/usr/bin/env python3
"""H_live probe: bits of live distinguishing information per body per game-second,
for a 10^9-body belt, against the player's velocity floor q_v.

Kernel: shearing-sheet encounter flux, per-body kick from the exact hyperbolic
deflection (gravitational focusing included), impulse form where t = 2Gm/(b v^2) << 1.
Flux (2-D thin disk): encounters with |impact parameter| in [b, b+db] cross two strips
of width db per unit time at relative speed v:  dlambda = 2 (Sigma/m) v db  [1/s].
Store model (shipmem form P): program (launch orbit) + residual scar; sub-floor kicks
accumulate as a random walk (influences below one quantum accumulate) and mutate the
scar when the residual crosses a quantum of the floor.

Outputs metrics.json. Controls: exact hyperbolic kernel vs direct leapfrog integration
(canonical and cold case), Richardson convergence, and the impulse-only kernel on the
cold case, which must deviate strongly (negative control).
"""
import json
import math
import os
import numpy as np

G = 6.674e-11
MSUN = 1.989e30
AU = 1.496e11

# ---------------- scene ----------------
a = 2.2 * AU
GM = G * MSUN
Porb = 2 * math.pi * math.sqrt(a**3 / GM)
OMEGA = 2 * math.pi / Porb
WIDTH = 0.5 * AU
AREA = 2 * math.pi * a * WIDTH
NBODIES = 1e9
MBELT = 2e21                    # real-belt mass
MBODY = MBELT / NBODIES         # 2e12 kg each
RBODY = 6e3                     # ~ radius at 2.5 g/cc
BMIN = 2 * RBODY                # contact; below it is the collision channel (excluded)
BMAX = WIDTH / 2.0              # belt half-width decoherence cutoff
RNG = np.random.default_rng(20261010)
WARP = 100.0                    # the plane's measured real-time rate

def vrel(b, sig):
    return np.sqrt((1.5 * OMEGA * b) ** 2 + sig ** 2)

def kick_each(b, sig, focusing=True):
    """Per-body |dv| of an equal-mass pair, impact parameter b, v_inf from the sheet."""
    v = vrel(b, sig)
    t = 2 * G * MBODY / (b * v * v)
    if focusing:
        return v * t / np.sqrt(1 + t * t)   # v*sin(theta/2), theta = relative deflection
    return v * t                            # impulse, no focusing

# ---------------- controls ----------------
def integrate_passage(b, vinf, Lfac=30.0, nsteps=200000):
    """Direct leapfrog integration of the relative two-body passage; returns |dv_each|."""
    mu = G * 2 * MBODY
    L = Lfac * b
    v0 = math.sqrt(vinf**2 + 2 * mu / L)     # exact energy at finite start distance
    x, y = -L, b
    vx, vy = v0, 0.0
    dt = (2 * L / v0) / nsteps
    def acc(x, y):
        r3 = (x * x + y * y) ** 1.5
        return -mu * x / r3, -mu * y / r3
    ax, ay = acc(x, y)
    for _ in range(nsteps):
        x += vx * dt + 0.5 * ax * dt * dt
        y += vy * dt + 0.5 * ay * dt * dt
        ax2, ay2 = acc(x, y)
        vx += 0.5 * (ax + ax2) * dt
        vy += 0.5 * (ay + ay2) * dt
        ax, ay = ax2, ay2
    vend = math.hypot(vx, vy)
    s = vinf / vend                           # rescale to |v_inf| magnitude
    dv = math.hypot(vx * s - vinf, vy * s)
    return dv / 2.0

def controls():
    out = {}
    b, sig = 1e5, 20.0                        # canonical belt: t ~ 6.7e-6 (impulse regime)
    num = integrate_passage(b, vrel(b, sig))
    ker = float(kick_each(np.array([b]), sig)[0])
    out["canonical_exact_kernel_relerr"] = abs(num - ker) / ker
    num2 = integrate_passage(b, vrel(b, sig), nsteps=400000)
    out["canonical_richardson_relerr"] = abs(num - num2) / num
    b2, sig2 = 1e5, 0.01                      # cold swarm: t ~ 15 (strong focusing)
    num3 = integrate_passage(b2, vrel(b2, sig2))
    ker3 = float(kick_each(np.array([b2]), sig2)[0])
    imp3 = float(kick_each(np.array([b2]), sig2, focusing=False)[0])
    out["cold_exact_kernel_relerr"] = abs(num3 - ker3) / ker3
    out["cold_impulse_vs_exact_ratio"] = imp3 / ker3
    return out

# ---------------- analytic encounter structure ----------------
BGRID = np.geomspace(BMIN, BMAX, 4000)

def encounter(sig, Sigma, q, focusing=True):
    """lam_plus [1/s], size sampler, h_size [bits], D_weak [m^2/s^3], <s^2> [m^2/s^2]."""
    b = BGRID
    v = vrel(b, sig)
    dv = kick_each(b, sig, focusing=focusing)
    dlnb = np.diff(np.log(b))
    db_ = b[:-1] * dlnb
    dlam = (Sigma / MBODY) * 2 * v[:-1] * db_       # 1/s, per log-grid bin
    dvb = dv[:-1]
    mask = dvb > q
    lam_plus = float(dlam[mask].sum())
    D_weak = float((dlam[~mask] * dvb[~mask] ** 2).sum())
    w = dlam[mask]
    if w.size:
        h_size = float(-(w / w.sum() * np.log2(w / w.sum())).sum())
        pw = w / w.sum()
    else:
        h_size, pw = 0.0, np.array([1.0])
    def sample(n):
        idx = RNG.choice(w.size, size=n, p=pw)
        return dvb[idx]
    w2 = float((w * dvb[mask] ** 2).sum())               # <s^2> weighted, for variance
    ms2 = w2 / w.sum() if w.sum() > 0 else 0.0
    return lam_plus, sample, h_size, D_weak, ms2

def lam_plus_of_q(sig, Sigma, qs, focusing=True):
    return np.array([encounter(sig, Sigma, q, focusing)[0] for q in qs])

# ---------------- growth MC (program + residual scar) ----------------
def growth_mc(Sigma, sig0, q, epochs=14, nb=10000):
    """Per-body 2-D residual (u,w). Epoch k covers (2^(k-1), 2^k] orbits; each epoch
    adds its own dt, so cumulative time is exact. Sub-floor kicks: Gaussian with the
    exact weak diffusion D_weak (the below-one-quantum accumulation). Above-floor kicks:
    explicit Poisson jumps while affordable (<= EXP_CAP per epoch, exact sizes), else
    compounded as a Gaussian with the exact above-floor variance lam*<s^2> (CLT; the
    residual is measured Gaussian, kurtosis ~3, by the time it matters)."""
    EXP_CAP = 2000.0
    u = np.zeros(nb); w = np.zeros(nb)
    sig_rel = sig0
    hist = []
    t_prev = 0.0
    for k in range(epochs + 1):
        orbits = 2.0 ** k
        dt = orbits * Porb - t_prev
        t_prev = orbits * Porb
        lam, sample, h_size, Dw, ms2 = encounter(sig_rel, Sigma, q)
        mean = lam * dt
        var_above = 0.5 * lam * ms2 * dt                  # per-dof above-floor variance
        if 1e-9 < mean <= EXP_CAP:                       # explicit jumps, exact sizes
            var_above -= 0.5 * mean * ms2                 # their variance comes from the draws
            counts = RNG.poisson(mean, nb)
            total = counts.sum()
            if total > 0:
                sizes = sample(total)
                angs = RNG.uniform(0, 2 * np.pi, total)
                idx = np.repeat(np.arange(nb), counts)
                np.add.at(u, idx, sizes * np.cos(angs))
                np.add.at(w, idx, sizes * np.sin(angs))
        u += RNG.normal(0, np.sqrt(0.5 * Dw * dt + max(var_above, 0.0)), nb)
        w += RNG.normal(0, np.sqrt(0.5 * Dw * dt + max(var_above, 0.0)), nb)
        sd = float(np.sqrt((u * u + w * w).mean() / 2))
        sig_rel = math.sqrt(sig0**2 + sd**2)
        # measured shape entropy at bin sd/32, shifted analytically to bin q
        bins = np.linspace(-4 * sd, 4 * sd, 257)
        Hh, _, _ = np.histogram2d(u, w, bins=[bins, bins])
        p = Hh.ravel() / Hh.sum()
        p = p[p > 0]
        Hshape = float(-(p * np.log2(p)).sum())
        Hq = Hshape + 2 * math.log2((sd / 32.0) / q) if sd > 0 else 0.0
        hist.append(dict(orbits=int(orbits), sigma_resid_m_per_s=sd, H_bits=float(Hq),
                         mutation_per_orbit=lam * Porb + 2 * np.sqrt(0.5 * Dw * Porb * 2 / np.pi) / q))
    return hist

# ---------------- run ----------------
def main():
    res = {}
    res["env"] = dict(nproc=os.cpu_count(),
                      loadavg1=open("/proc/loadavg").read().split()[0],
                      memfree_kb=open("/proc/meminfo").readline().split()[1])
    res["scene"] = dict(a_AU=2.2, width_AU=0.5, N=NBODIES, belt_kg=MBELT,
                        body_kg=MBODY, Porb_s=Porb, warp=WARP)
    res["controls"] = controls()
    print("CONTROLS:", json.dumps(res["controls"], indent=1))

    Sigma0 = MBELT / AREA
    scenes = {
        "belt":        dict(Sigma=Sigma0, sig0=20.0),
        "dense_x2500": dict(Sigma=Sigma0 * 2500, sig0=20.0),
        "coldswarm":   dict(Sigma=Sigma0 * 2500, sig0=0.01),
    }
    qs = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2]

    lam = {}
    for name, sc in scenes.items():
        vals = lam_plus_of_q(sc["sig0"], sc["Sigma"], qs)     # 1/s
        lam[name] = dict(zip(map(str, qs), (vals * Porb).tolist()))   # per orbit
        nz = vals > 0
        lam[name]["beta_fit"] = float(np.polyfit(np.log(np.array(qs)[nz]),
                                                 np.log(vals[nz]), 1)[0])
        lam[name]["per_body_per_games_at_q1e-6"] = float(vals[0] * WARP)
    res["lambda_plus_per_body_per_orbit"] = lam
    res["sigma_linearity_ratio"] = lam["dense_x2500"]["1e-06"] / lam["belt"]["1e-06"] / 2500.0
    print(json.dumps(lam, indent=1))

    growth = {}
    for name, sc in scenes.items():
        hist = growth_mc(sc["Sigma"], sc["sig0"], 1e-6)
        growth[name] = hist
        print("%-12s sigma_end=%.3g m/s H_end=%.1f bits  store@1e9: dof2=%.2f GB dof3=%.2f GB"
              % (name, hist[-1]["sigma_resid_m_per_s"], hist[-1]["H_bits"],
                 NBODIES * hist[-1]["H_bits"] / 8e9,
                 NBODIES * hist[-1]["H_bits"] * 1.5 / 8e9))
    res["growth_q1e-6"] = growth

    h = growth["belt"]
    lam1, _, hsize, _, _ = encounter(scenes["belt"]["sig0"], scenes["belt"]["Sigma"], 1e-6)
    creation = lam1 * Porb * max(hsize, 1.0)                 # bits/body/orbit arriving
    growth_rate = (h[-1]["H_bits"] - h[0]["H_bits"]) / h[-1]["orbits"]
    res["reabsorption"] = dict(creation_bits_per_body_per_orbit=creation,
                               live_growth_bits_per_body_per_orbit=growth_rate,
                               reabsorbed_fraction=1 - growth_rate / creation)

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "metrics.json"), "w") as f:
        json.dump(res, f, indent=1)

if __name__ == "__main__":
    main()
