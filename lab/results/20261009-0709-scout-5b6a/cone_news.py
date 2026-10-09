#!/usr/bin/env python3
"""News events per probe orbit from the far field (d > r_doll), with retardation.

Restricted approximation (Toomre-Toomre style): the probe stays on its smoothed
circular orbit; the far field's tidal work W(t) = int v.F_far dt is the energy
the far field pumps into the probe. News events = crossings of W over kick
quanta (eps * E_scale, E_scale = v0^2). R-invariance: same rate at r_max = 32
and 8192 => the far-field news cost does not grow with universe age.
"""
import json
import sys
import numpy as np
from cone import build_scene, probe_motion, G, C


def news_events(kind, r_max, eps, r_doll=2.0, t_end=360.0, n_t=1200, chunk=40):
    src = build_scene(kind, r_max)
    rp, omp = probe_motion(src)
    xi0 = src["r"] * np.exp(1j * src["th"])
    far = np.abs(xi0 - rp) > r_doll
    src = {k2: v[far] for k2, v in src.items() if isinstance(v, np.ndarray) and np.size(v) == far.size}
    ts = np.linspace(0.0, t_end, n_t)
    W = np.zeros(n_t)
    for a in range(0, n_t, chunk):
        t = ts[a:a + chunk]
        xp = rp * np.exp(1j * omp * t)[:, None]
        xnow = src["r"][None, :] * np.exp(1j * (src["th"][None, :] + src["om"][None, :] * t[:, None]))
        tret = t[:, None] - np.abs(xnow - xp) / C
        for _ in range(3):
            xi = src["r"][None, :] * np.exp(1j * (src["th"][None, :] + src["om"][None, :] * tret))
            tret = t[:, None] - np.abs(xi - xp) / C
        dz = xi - xp
        d = np.abs(dz)
        F = -G * src["m"][None, :] * dz / d ** 3  # pull of far sources
        F = F - F.mean(axis=1, keepdims=True)  # the doll's free fall absorbs the dipole
        v = 1j * omp * xp  # probe velocity
        W[a:a + chunk] = np.cumsum(np.real(v * np.conj(F)).sum(axis=1)) * (ts[1] - ts[0])
    e_scale = (omp * rp) ** 2
    q = eps * e_scale
    j = np.floor(W / q)
    events = int(np.abs(np.diff(j)).sum())
    orbits = t_end * omp / (2 * np.pi)
    return dict(n_far=int(far.sum()), events=events, orbits=orbits,
                per_orbit=events / orbits, w_over_q=float(np.abs(W).max() / q))


def main():
    out = {}
    for kind, rmax in [("exp", 8192.0), ("exp", 32.0), ("unif", 8192.0), ("unif", 32.0)]:
        for eps in [1e-4, 1e-6]:
            r = news_events(kind, rmax, eps)
            out[f"{kind}{int(rmax)}_{eps:g}"] = r
            print(f"[{kind} rmax={rmax:.0f} eps={eps:g}] far={r['n_far']} "
                  f"events/orbit={r['per_orbit']:.3f} maxW/q={r['w_over_q']:.1f}", flush=True)
    with open(sys.argv[1] if len(sys.argv) > 1 else "news_results.json", "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
