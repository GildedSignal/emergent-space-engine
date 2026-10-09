#!/usr/bin/env python3
"""Does a body's billable gravity-news cone saturate as the universe's causal radius grows?

Scene: 2D disk of sources on circular orbits (3D-falloff tides through the plane, the game's
plane). Probe at r_p on a circular orbit in the smoothed field. The doll's free fall absorbs
l=0/l=1; the compiled geometry absorbs the smooth axisymmetric background; what bills as NEWS
is the traceless l=2 tide of discrete sources, evaluated on the probe's past light cone,
gated by the kick quantum eps_q (relative to tau_loc = Omega_p^2).

Units: G = M_d = R_d = c = 1.

Outputs:
  M1  N_naive(R), N_sig(R, eps), billing-annulus count, tail remainder vs R
  GEN far-field generator size: kept lines per level, quantum-gated; N and mass-function sweeps

Scenes: exp (exponential disk), unif (uniform to R_max), clump (exp + 0.1 M_d at ~30 R_d).
"""
import json
import sys
import numpy as np

RNG = np.random.default_rng(20261009)
G, C = 1.0, 1.0


def build_scene(kind, r_max, n_total=40000, half_octaves=True, mass="equal"):
    """Dyadic annuli of sources, mass per annulus from the surface density model."""
    step = 2.0 ** 0.5 if half_octaves else 2.0
    edges = [0.25]
    while edges[-1] < r_max:
        edges.append(edges[-1] * step)
    edges[-1] = r_max
    rk_in = np.array(edges[:-1]); rk_out = np.array(edges[1:])

    def sigma(r):
        if kind in ("exp", "clump"):
            s = np.exp(-r)
        else:  # uniform: constant column to r_max
            s = np.ones_like(r)
        if kind == "clump":
            # companion: lognormal bump of width 1.5 centred at 30, total 0.1 M_d-scale
            w = np.exp(-0.5 * ((np.log(r / 30.0) / 0.35) ** 2)) / r
            s = s + 0.14 * w / w.max()
        return s

    m_ann = np.pi * (rk_out ** 2 - rk_in ** 2) * 0.5 * (sigma(rk_in) + sigma(rk_out))
    share = m_ann / m_ann.sum()
    n_ann = np.maximum(8, np.ceil(share * n_total).astype(int))
    # circular orbits in the smoothed potential of the same model
    m_enc = np.pi * rk_in ** 2 * sigma(rk_in)
    r_mid = np.sqrt(rk_in * rk_out)

    src_r, src_th, src_m, src_ann, src_om = [], [], [], [], []
    for k in range(len(rk_in)):
        n = n_ann[k]
        r = np.sqrt(rk_in[k] ** 2 + RNG.random(n) * (rk_out[k] ** 2 - rk_in[k] ** 2))
        th = RNG.random(n) * 2 * np.pi
        v2 = G * (np.pi * r ** 2 * sigma(r)) / np.maximum(r, 1e-9)
        om = np.sqrt(np.maximum(v2, 1e-12)) / np.maximum(r, 1e-9)
        src_r.append(r); src_th.append(th)
        if mass == "pareto":  # dN/dm ~ m^-2: the heavy tail bills, the crumbs aggregate
            w = 1.0 / RNG.random(n)
            mi = m_ann[k] * w / w.sum()
        else:
            mi = np.full(n, m_ann[k] / n)
        src_m.append(mi); src_ann.append(np.full(n, k))
        src_om.append(om)
    src = dict(r=np.concatenate(src_r), th=np.concatenate(src_th),
               m=np.concatenate(src_m), k=np.concatenate(src_ann),
               om=np.concatenate(src_om), ann_m=m_ann, r_mid=r_mid, m_enc=m_enc)
    return src


def positions(src, tau):
    return src["r"][None, :] * np.exp(1j * (src["th"][None, :] + src["om"][None, :] * tau[:, None]))


def tide_l2(xi, xp):
    """Traceless in-plane l=2 tidal amplitude (complex) of sources at xi seen at xp."""
    dz = xi - xp
    d = np.abs(dz)
    return G * (np.conj(dz) / d) ** 2 / d ** 3  # m/d^3 * e^{-2i phi}; |.| is the norm


def probe_motion(src):
    rp = 1.0
    v2 = G * (np.pi * rp ** 2 * np.exp(-rp)) / rp
    omp = np.sqrt(v2) / rp
    return rp, omp


def static_accounting(src, eps_list):
    """M1 at t=0: counts vs causal radius R."""
    rp, omp = probe_motion(src)
    tau_loc = omp ** 2
    xp = rp + 0j
    xi = src["r"] * np.exp(1j * src["th"])
    d = np.abs(xi - xp)
    amp = G * src["m"] / d ** 3
    q = G * src["m"] * np.exp(-2j * np.angle(xi - xp)) / d ** 3
    K = int(src["k"].max()) + 1
    ann_edge = 0.25 * (2.0 ** 0.5) ** np.arange(2 * K + 2)
    out = {"tau_loc": tau_loc, "rows": []}
    for R in np.unique(np.concatenate([ann_edge[ann_edge > 1], [2, 4, 8, 16, 32, 64, 1e9]])):
        if R > max(64.0, ann_edge[-1]):
            R = max(64.0, ann_edge[-1]) if ann_edge[-1] <= 64 else R
        sel = d < R
        row = dict(R=float(min(R, ann_edge[-1])), n_naive=int(sel.sum()))
        for eps in eps_list:
            row[f"n_sig_{eps:g}"] = int((amp > eps * tau_loc).sum())
            bill = 0
            for k in range(K):
                m = sel & (src["k"] == k)
                if m.any() and abs(q[m].sum()) > eps * tau_loc:
                    bill += 1
            row[f"ann_bill_{eps:g}"] = bill
            tail = abs(q[d >= R].sum()) if (d >= R).any() else 0.0
            row[f"tail_{eps:g}"] = tail / (eps * tau_loc)
        out["rows"].append(row)
    return out


def news_rate(src, eps, t_end=240.0, n_t=480, chunk=24):
    """M2: quantum crossings of each annulus's retarded l=2 tide, per unit probe time."""
    rp, omp = probe_motion(src)
    tau_loc = omp ** 2
    K = int(src["k"].max()) + 1
    ts = np.linspace(0.0, t_end, n_t)
    prev = None
    events = 0
    for a in range(0, n_t, chunk):
        t = ts[a:a + chunk]
        xp = rp * np.exp(1j * (0.7 + omp * t))[:, None]
        xnow = src["r"][None, :] * np.exp(1j * (src["th"][None, :] + src["om"][None, :] * t[:, None]))
        tret = t[:, None] - np.abs(xnow - xp) / C
        for _ in range(3):  # light-cone Newton
            xi = src["r"][None, :] * np.exp(1j * (src["th"][None, :] + src["om"][None, :] * tret))
def far_and_generator(src, eps_list, r_doll=2.0):
    """Local/far split and the compiled-generator size of the far field.

    Cost model (principle 3: derivable evolution is free; news = stored state):
    a level's multipole generator keeps member lines until the quadratic tail
    of dropped lines is below the quantum. Reads per kick = kept lines summed
    over levels. Quantum crossings of the aggregate VALUE are NOT cost: the
    value is derived from stored member tubes (t mod period)."""
    rp, omp = probe_motion(src)
    tau_loc = omp ** 2
    xi = src["r"] * np.exp(1j * src["th"])
    xp = rp + 0j
    d = np.abs(xi - xp)
    amp = G * src["m"] / d ** 3
    out = {"tau_loc": tau_loc}
    for eps in eps_list:
        q_eps = eps * tau_loc
        far = d > r_doll
        out[f"far_sig_{eps:g}"] = int((amp[far] > q_eps).sum())
        kept_total = 0
        per_level = []
        for k in range(int(src["k"].max()) + 1):
            m = (src["k"] == k) & far
            if not m.any():
                per_level.append(0)
                continue
            a = np.sort(amp[m])[::-1]
            tail = np.sqrt(np.concatenate([np.cumsum((a[::-1] ** 2))[::-1][1:], [0.0]]))
            below = tail < q_eps  # tail[j] = quadrature tail of lines dropped after top-j
            j = int(np.argmax(below)) if below.any() else a.size
            per_level.append(j)
            kept_total += j
        out[f"kept_{eps:g}"] = kept_total
        out[f"levels_kept_{eps:g}"] = sum(1 for x in per_level if x > 0)
    return out


def main():
    eps_list = [1e-4, 1e-6, 1e-8]
    res = {}
    for name, kind, rmax in [("exp", "exp", 8192.0), ("unif", "unif", 8192.0),
                             ("clump", "clump", 8192.0), ("exp32", "exp", 32.0)]:
        src = build_scene(kind, rmax)
        res[name] = dict(n_src=int(src["r"].size), r_max=rmax,
                         static=static_accounting(src, eps_list),
                         gen=far_and_generator(src, eps_list))
        print(f"[{name}] n={res[name]['n_src']} " +
              json.dumps(res[name]["gen"]), flush=True)
    sweep = {}
    for n_tot, mass in [(40000, "equal"), (400000, "equal"), (400000, "pareto"),
                        (4000000, "pareto")]:
        src = build_scene("exp", 8192.0, n_total=n_tot, mass=mass)
        sweep[f"exp_n{n_tot}_{mass}"] = dict(n_src=int(src["r"].size),
                                             gen=far_and_generator(src, eps_list))
        print(f"[sweep n={n_tot} {mass}]", json.dumps(sweep[f"exp_n{n_tot}_{mass}"]["gen"]), flush=True)
    res["sweep"] = sweep
    with open(sys.argv[1] if len(sys.argv) > 1 else "cone_results.json", "w") as f:
        json.dump(res, f, indent=1)
    print("written")


if __name__ == "__main__":
    main()
