#!/usr/bin/env python3
"""Encounter-e feedback: regulate or avalanche? (lab run 20261008-0148-dynamics-0a3d)

Population closure: dE/dt = lambda(E) * <de^2 per encounter>(E), E = sigma_e^2.
lambda(E) measured from the exact truth sweep (events per body per orbit).
<de^2> from the small-angle impulse with Coulomb log: dv = 2m/(b v_rel),
b areal-uniform in [rho^2 ln(rho/b90)], v_rel ~ sqrt(e^2 + (1.5*sigma_a)^2)*v_K, v_K=1 at a=1.
Question: does the loop e^up -> lambda^up -> pumping^up run away, self-regulate, or grow
sub-linearly? Compare fitted growth exponent with planetesimal viscous stirring (e ~ t^0.2).
"""
import json

import numpy as np

TAU = 2 * np.pi
# measured: sigma_e -> events (N=500, 400 orbits, rho=3e-3, a in [0.96,1.04], seed 20261002)
SWEEP = {1e-3: 10325, 3e-3: 16682, 1e-2: 43522, 3e-2: 82536, 8e-2: 94176, 1.5e-1: 95842}
N_BODIES = 500
ORBITS = 400.0
RHO = 3e-3

lam = {s: n / (N_BODIES * ORBITS) for s, n in SWEEP.items()}


def lam_of(sig, cap=None):
    """Interpolate log-log in sigma_e; saturate/fall beyond the peak at sigma_e*a ~ W."""
    ss = np.array(sorted(lam))
    yy = np.array([lam[s] for s in ss])
    v = np.exp(np.interp(np.log(sig), np.log(ss), np.log(yy)))
    if cap is not None and sig > cap:
        # falling branch beyond the peak: partners capped at belt width W
        v *= (cap / sig)
    return float(v)


def de2(sig, m, rho=RHO):
    """Mean squared eccentricity kick per encounter (both impulse + Coulomb log)."""
    v_rel = np.sqrt(sig**2 + (1.5 * 3e-3) ** 2)  # e-velocity + shear of nearest spacing
    b90 = m / v_rel**2
    lnL = np.log(1.0 + rho / max(b90, 1e-30))
    dv2 = (2.0 * m / v_rel) ** 2 / rho**2 * lnL
    return dv2  # delta-e squared ~ (dv/v_K)^2, v_K = 1


def integrate(sig0, m, orbits=400.0, dt=0.05, cap=None):
    E = sig0**2
    ts, sigs, lams = [0.0], [sig0], [lam_of(sig0, cap)]
    for k in range(int(orbits / dt)):
        sig = np.sqrt(E)
        l = lam_of(sig, cap)
        E = E + l * de2(sig, m) * dt
        ts.append((k + 1) * dt)
        sigs.append(np.sqrt(E))
        lams.append(lam_of(np.sqrt(E), cap))
    return np.array(ts), np.array(sigs), np.array(lams)


def fit_slope(ts, ys, frac=(0.3, 1.0)):
    m_ = (ts >= frac[0] * ts[-1]) & (ts <= frac[1] * ts[-1])
    return float(np.polyfit(np.log(ts[m_]), np.log(ys[m_]), 1)[0])


def main():
    out = {"lambda_measured": {f"{s:.0e}": lam[s] for s in lam}, "slopes": {}}
    ss = np.array(sorted(lam))
    yy = np.array([lam[s] for s in ss])
    for k in range(1, len(ss)):
        out["slopes"][f"{ss[k-1]:.0e}->{ss[k]:.0e}"] = float(
            np.polyfit(np.log(ss[k - 1:k + 1]), np.log(yy[k - 1:k + 1]), 1)[0])

    print("measured lambda per body/orbit:", {f"{s:.0e}": round(lam[s], 5) for s in lam})
    print("local slopes dln lambda/dln sigma_e:", {k: round(v, 3) for k, v in out["slopes"].items()})

    print("\ngrowth from cold belt sigma_e=1e-3, 400 orbits (m = mass ratio to primary):")
    out["growth"] = {}
    for m in (1e-12, 1e-10, 1e-8, 1e-6):
        ts, sigs, lams = integrate(1e-3, m)
        es = fit_slope(ts, sigs)
        ls = fit_slope(ts, lams)
        out["growth"][f"{m:.0e}"] = {
            "sigma_final": float(sigs[-1]), "sigma_exponent": es,
            "lambda_final": float(lams[-1]), "lambda_exponent": ls,
            "finite_time_blowup": bool(not np.isfinite(sigs[-1]) or sigs[-1] > 10)}
        print(f"  m={m:.0e}: sigma_e 1e-3 -> {sigs[-1]:.3e} (e ~ t^{es:.2f}); "
              f"lambda -> {lams[-1]:.4f} (lambda ~ t^{ls:.2f})")

    print("\nrunaway scan: exponent of dE/dt = lambda*de2 ~ E^{-alpha/2}... "
          "(alpha>0 => sub-linear, self-regulating)")
    for m in (1e-12, 1e-8, 1e-6):
        E = np.logspace(-7, -1.2, 60)
        g = np.array([lam_of(np.sqrt(e)) * de2(np.sqrt(e), m) for e in E])
        sl = float(np.polyfit(np.log(E), np.log(g), 1)[0])
        print(f"  m={m:.0e}: d(ln pumping)/d(ln E) = {sl:.2f} "
              f"{'RUNAWAY if >= +1 (finite-time)' if sl >= 1 else 'sub-linear growth, no blowup'}")
        out.setdefault("pumping_slopes", {})[f"{m:.0e}"] = sl
    json.dump(out, open("cascade.json", "w"), indent=1)


if __name__ == "__main__":
    main()
