#!/usr/bin/env python3
"""Red-team probe: does phase-neighbour rank certificate hold on co-orbital
swarms with orientation/eccentricity dispersion (collision debris), or only on
aligned formations?

Truth: exact Kepler (sigma_a = 0 -> common period; one period of dense time
sampling is a complete truth). Encounter = min pair distance over one period
< R_enc. Events are distinct by construction: one min-distance per pair.

Certificates:
  phase  : circular rank in mean anomaly M at epoch (frozen for sigma_a=0).
           k* = max circular M-rank over real encounter pairs.
           miss(k) = fraction of encounter pairs with rank > k.
  shell  : pairwise tier proxy (miss-free necessary condition): radial shells
           [a(1-e)-R, a(1+e)+R] overlap. setup = #candidate pairs (cost).

Usage: python3 coorb_probe.py scenes.json out.json
"""
import json, sys, time, zlib
import numpy as np

TWO_PI = 2.0 * np.pi
D2R = np.pi / 180.0


def rng_of(seed):
    return np.random.default_rng(seed)


def draw(spec_v, r, n):
    """{"v": const} | {"dist":"uniform","lo","hi"} | {"dist":"normal","mu","sigma"}
    | {"dist":"absnorm","sigma","clip"}"""
    if "v" in spec_v:
        return np.full(n, spec_v["v"])
    d = spec_v.get("dist")
    if d == "uniform":
        return r.uniform(spec_v.get("lo", 0.0), spec_v.get("hi", TWO_PI), n)
    if d == "normal":
        return r.normal(spec_v.get("mu", 0.0), spec_v["sigma"], n)
    if d == "absnorm":
        return np.clip(np.abs(r.normal(0.0, spec_v["sigma"], n)), 0.0, spec_v.get("clip", 0.9))
    raise ValueError(str(spec_v))


def make_scene(spec, n, seed):
    r = rng_of(seed)
    Mlo, Mhi = spec.get("Marc", [0.0, TWO_PI])
    return dict(a=np.full(n, 1.0), e=draw(spec["e"], r, n),
                om=np.mod(draw(spec["omega"], r, n), TWO_PI),
                Om=np.mod(draw(spec["Omega"], r, n), TWO_PI),
                inc=draw(spec["inc"], r, n),
                M0=r.uniform(Mlo, Mhi, n))


def positions(bod, T):
    """(n, T, 3) positions over one common period, M uniform in time."""
    n = bod["a"].size
    a, e = bod["a"][:, None], bod["e"][:, None]
    om, Om, inc = bod["om"][:, None], bod["Om"][:, None], bod["inc"][:, None]
    t = np.linspace(0.0, TWO_PI, T, endpoint=False)
    M = bod["M0"][:, None] + t[None, :]
    E = M.copy()
    for _ in range(10):  # Newton; e<=0.9 converges
        f = E - e * np.sin(E) - M
        E = E - f / (1.0 - e * np.cos(E))
    b_ = a * np.sqrt(1.0 - e * e)
    xo = a * (np.cos(E) - e)
    yo = b_ * np.sin(E)
    co, so = np.cos(om), np.sin(om)
    cO, sO = np.cos(Om), np.sin(Om)
    ci, si = np.cos(inc), np.sin(inc)
    x = xo * (co * cO - so * sO * ci) - yo * (cO * so + sO * co * ci)
    y = xo * (sO * co + cO * so * ci) - yo * (sO * so - cO * co * ci)
    z = xo * (so * si) + yo * (co * si)
    return np.stack([x, y, z], axis=-1)


def truth_min_dist(P):
    """(n, n) min pairwise distance over the sampled period."""
    n = P.shape[0]
    out = np.zeros((n, n))
    for i in range(n - 1):
        d = P[i + 1:, :, :] - P[i, :, :]
        out[i, i + 1:] = np.sqrt((d * d).sum(-1).min(axis=1))
    out += out.T
    return out


def cert_phase(bod):
    """circular rank in M at epoch, as (n,n) matrix."""
    M0 = np.mod(bod["M0"], TWO_PI)
    order = np.argsort(M0)
    idx = np.empty_like(order)
    idx[order] = np.arange(M0.size)
    d = np.abs(idx[:, None] - idx[None, :])
    return np.minimum(d, M0.size - d)

def shell_setup_count(e, a, R):
    q = a * (1.0 - e)
    Q = a * (1.0 + e)
    ok = (q[:, None] <= Q[None, :] + R) & (q[None, :] <= Q[:, None] + R)
    n = a.size
    return int((np.triu(ok, 1)).sum())


def circ_diff(x):
    d = np.abs(x[:, None] - x[None, :])
    return np.minimum(d, TWO_PI - d)


def run_scene(name, spec, n, T, R, seed):
    t0 = time.time()
    bod = make_scene(spec, n, seed)
    P = positions(bod, T)
    mind = truth_min_dist(P)
    enc = np.triu(mind < R, 1)
    n_enc = int(enc.sum())
    rank = cert_phase(bod)
    res = dict(scene=name, n=n, T=T, R=R, seed=seed,
               e_mean=float(bod["e"].mean()), e_max=float(bod["e"].max()),
               n_enc=n_enc, setup_shell=shell_setup_count(bod["e"], bod["a"], R))
    if n_enc == 0:
        res.update(k_star=None, miss_at={})
        return res
    rr = rank[enc]
    k_star = int(rr.max())
    res["k_star"] = k_star
    res["miss_at"] = {str(k): float((rr > k).mean()) for k in (2, 4, 8, 16, 32, 64)}
    # geometry of missed pairs at k=4 (the gold's rank)
    ii, jj = np.nonzero(enc)
    miss = rank[ii, jj] > 4
    res["n_miss4"] = int(miss.sum())
    if miss.sum() > 0:
        dom = circ_diff(bod["om"])[ii, jj]
        res["missed_dw_median"] = float(np.median(dom[miss]) / D2R)
        res["kept_dw_median"] = float(np.median(dom[~miss]) / D2R)
        res["missed_de_median"] = float(np.median(np.abs(bod["e"][ii] - bod["e"][jj])[miss]))
    # group shape numbers (candidate trigger)
    res["e_rms"] = float(np.sqrt((bod["e"] ** 2).mean()))
    om_c = np.mod(bod["om"], TWO_PI)
    # circular dispersion of omega (K statistic, in degrees)
    C, S = np.cos(om_c).mean(), np.sin(om_c).mean()
    res["omega_disp_deg"] = float(np.sqrt(-2.0 * np.log(np.hypot(C, S))) / D2R if np.hypot(C, S) > 0 else 180.0)
    # Phi: geometric spread of the group over the encounter scale
    dw = circ_diff(om_c)
    de = np.abs(bod["e"][:, None] - bod["e"][None, :])
    phi_pairs = (de + res["e_rms"] * dw)  # ~ radial excursion difference scale, in units of a
    res["Phi_pair_rms_over_R"] = float(np.sqrt((phi_pairs[np.triu_indices(n, 1)] ** 2).mean()) / R)
    res["seconds"] = round(time.time() - t0, 1)
    print(f"{name:22s} n_enc={n_enc:6d} k*={k_star:4d} miss4={res['miss_at']['4']:6.1%} "
          f"setup={res['setup_shell']:8d} Phi/R={res['Phi_pair_rms_over_R']:8.1f} ({res['seconds']}s)",
          flush=True)
    return res


SCENES = {
    # controls (the cert's home turf)
    "ctl-ring-circ-aligned": dict(e={"v": 0.0}, omega={"v": 0.0}, Omega={"v": 0.0}, inc={"v": 0.0}),
    "ctl-arc-circ-aligned": dict(e={"v": 0.0}, omega={"v": 0.0}, Omega={"v": 0.0}, inc={"v": 0.0},
                                 Marc=[0.0, 30 * D2R]),
    "ctl-ring-e03-aligned": dict(e={"v": 0.3}, omega={"v": 0.0}, Omega={"v": 0.0}, inc={"v": 0.0}),
    # eccentricity dispersion, aligned
    "se002-aligned": dict(e={"dist": "absnorm", "sigma": 0.02}, omega={"v": 0.0}, Omega={"v": 0.0}, inc={"v": 0.0}),
    "se005-aligned": dict(e={"dist": "absnorm", "sigma": 0.05}, omega={"v": 0.0}, Omega={"v": 0.0}, inc={"v": 0.0}),
    "se01-aligned": dict(e={"dist": "absnorm", "sigma": 0.1}, omega={"v": 0.0}, Omega={"v": 0.0}, inc={"v": 0.0}),
    "se03-aligned": dict(e={"dist": "absnorm", "sigma": 0.3}, omega={"v": 0.0}, Omega={"v": 0.0}, inc={"v": 0.0}),
    # apsidal dispersion at fixed e
    "sw015-e03": dict(e={"v": 0.3}, omega={"dist": "normal", "sigma": 15 * D2R}, Omega={"v": 0.0}, inc={"v": 0.0}),
    "sw045-e03": dict(e={"v": 0.3}, omega={"dist": "normal", "sigma": 45 * D2R}, Omega={"v": 0.0}, inc={"v": 0.0}),
    "sw090-e03": dict(e={"v": 0.3}, omega={"dist": "normal", "sigma": 90 * D2R}, Omega={"v": 0.0}, inc={"v": 0.0}),
    "sw180-e01": dict(e={"v": 0.1}, omega={"dist": "uniform"}, Omega={"v": 0.0}, inc={"v": 0.0}),
    "sw180-e03": dict(e={"v": 0.3}, omega={"dist": "uniform"}, Omega={"v": 0.0}, inc={"v": 0.0}),
    "sw180-e06": dict(e={"v": 0.6}, omega={"dist": "uniform"}, Omega={"v": 0.0}, inc={"v": 0.0}),
    # node dispersion (planar rotation of the ellipses)
    "Om180-e03-i15": dict(e={"v": 0.3}, omega={"v": 0.0}, Omega={"dist": "uniform"}, inc={"v": 15 * D2R}),
    # bimodal apsides: two counter-aligned sub-fleets
    "bimodal-e03": None,  # handled specially
    # the physical workload: collision debris ring (tight a, wide e/omega/Omega)
    "debris-ring": dict(e={"dist": "uniform", "lo": 0.05, "hi": 0.6}, omega={"dist": "uniform"},
                        Omega={"dist": "uniform"}, inc={"dist": "normal", "sigma": 10 * D2R}),
}


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 384
    T = int(sys.argv[2]) if len(sys.argv) > 2 else 8192
    out_path = sys.argv[3] if len(sys.argv) > 3 else "results.json"
    results = []
    for name, spec in SCENES.items():
        if name == "bimodal-e03":
            r = rng_of(7)
            half = n // 2
            spec = dict(e={"v": 0.3}, omega={"v": 0.0}, Omega={"v": 0.0}, inc={"v": 0.0},
                        _bimodal=(0.0, np.pi, half))
        seed = zlib.crc32(name.encode()) % (2**31)
        if spec is None:
            continue
        if "_bimodal" in spec:
            lo, hi, half = spec.pop("_bimodal")
            bod_spec = dict(e={"v": 0.3}, omega={"v": 0.0}, Omega={"v": 0.0}, inc={"v": 0.0})
            bod = make_scene(bod_spec, n, seed)
            bod["om"][half:] = np.pi
            res = run_scene_bod(name, bod, T, R=0.005)
            results.append(res)
            continue
        results.append(run_scene(name, spec, n, T, R=0.005, seed=seed))
    with open(out_path, "w") as f:
        json.dump(results, f, indent=1)
    print("wrote", out_path)


def run_scene_bod(name, bod, T, R):
    t0 = time.time()
    P = positions(bod, T)
    mind = truth_min_dist(P)
    enc = np.triu(mind < R, 1)
    n_enc = int(enc.sum())
    rank = cert_phase(bod)
    rr = rank[enc]
    res = dict(scene=name, n=bod["a"].size, T=T, R=R, n_enc=n_enc,
               setup_shell=shell_setup_count(bod["e"], bod["a"], R),
               k_star=int(rr.max()) if n_enc else None,
               miss_at={str(k): float((rr > k).mean()) for k in (2, 4, 8, 16, 32, 64)} if n_enc else {})
    res["seconds"] = round(time.time() - t0, 1)
    print(f"{name:22s} n_enc={n_enc:6d} k*={res['k_star']:4d} miss4={res['miss_at']['4']:6.1%} "
          f"setup={res['setup_shell']:8d} ({res['seconds']}s)", flush=True)
    return res


if __name__ == "__main__":
    main()
