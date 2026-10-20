#!/usr/bin/env python3
"""r12-seen-flux: the aggregate's seen flux (dispersion channel). Run: python3 seen_flux.py.

Fleet model (frozen): N=400 members, bulk beta0=(beta,0), internal velocities v' drawn in
the fleet frame (seed 20261019), composed with the bulk by exact SR velocity addition
(perpendicular divided by gamma0) -- physical, never superluminal. Seen flux of a member
with observer-frame velocity u at photon direction n: k = 1/(gamma_u (1 - u.n)), F_i = k^4.
Path sweep: theta in [0.02,179.98] deg, 2001 samples. Truth = per-ship sum (path A);
path B is the same k re-arranged (gamma via (1-b)(1+b), dot split) to catch typos.
Diagnostics (not frozen configs): the bulk readout; the single-Gaussian moment readout on
rings; an observer-frame-dispersion case (1885's convention); a 10^6-member truth on a
subsampled path isolating readout error from the finite-N sampling floor.
"""
import json, math, random
import numpy as np
from numpy.polynomial.hermite import hermgauss

N = 400
SEED = 20261019
THETA = np.deg2rad(np.linspace(0.02, 179.98, 2001))
NX, NY = np.cos(THETA), np.sin(THETA)
OP_K = 16  # counted ops per k evaluation (gamma, dot, k, k^4), conservative

CASES = [
    ("c1-gauss-b0.5-s0.03",  "gauss", 0.5,  {"sigma": 0.03}),
    ("c2-gauss-b0.9-s0.03",  "gauss", 0.9,  {"sigma": 0.03}),
    ("c3-gauss-b0.99-s0.03", "gauss", 0.99, {"sigma": 0.03}),
    ("c4-ring-b0.9-w0.05",   "ring",  0.9,  {"brot": 0.05}),
    ("c5-ring-b0.9-w0.15",   "ring",  0.9,  {"brot": 0.15}),
    ("c6-bimodal-b0.9",      "squad", 0.9,  {"squads": [(-0.05, 0.01), (0.05, 0.01)]}),
    ("c7-gauss-b0.5-s0.10",  "gauss", 0.5,  {"sigma": 0.10}),
]

def compose(vx, vy, beta, g0):
    den = 1.0 + beta * vx
    return (vx + beta) / den, vy / (g0 * den)

def kof(ux, uy, nx, ny, path="A"):
    if path == "A":
        g = 1.0 / np.sqrt(1.0 - (ux * ux + uy * uy))
        d = 1.0 - (ux * nx + uy * ny)
    else:
        b = np.sqrt(ux * ux + uy * uy)
        g = 1.0 / np.sqrt((1.0 - b) * (1.0 + b))
        d = (1.0 - ux * nx) - uy * ny
    return 1.0 / (g * d)

def ksafe(ux, uy, nx, ny):
    """k with subluminality enforced (diagnostic Gaussian tail nodes past c)."""
    r2 = ux * ux + uy * uy
    ok = r2 < 1.0
    k = np.zeros(np.shape(ux))
    k[ok] = kof(ux[ok], uy[ok], nx, ny)
    return k, ok

def members(case):
    kind, beta, p = case[1], case[2], case[3]
    rng = random.Random(SEED)
    if kind == "gauss":
        vp = np.array([[rng.gauss(0.0, p["sigma"]), rng.gauss(0.0, p["sigma"])] for _ in range(N)])
        desc = {"squads": [((0.0, 0.0), p["sigma"], 1.0)]}
    elif kind == "ring":
        phi = 2 * math.pi * np.arange(N) / N
        vp = p["brot"] * np.stack([-np.sin(phi), np.cos(phi)], axis=1)
        desc = {"formation": "ring", "brot": p["brot"]}
    else:  # squad
        vp = np.array([[rng.gauss(mu, sg), rng.gauss(0.0, sg)]
                       for mu, sg in [p["squads"][0]] * (N // 2) + [p["squads"][1]] * (N // 2)])
        desc = {"squads": [((mu, 0.0), sg, 0.5) for mu, sg in p["squads"]]}
    g0 = 1.0 / math.sqrt(1.0 - beta * beta)
    ux, uy = compose(vp[:, 0], vp[:, 1], beta, g0)
    return ux, uy, desc

def squad_rate(mu, beta, g0):
    """d(4 ln k)/dv'_par at the squad mean, head-on (sizes the quadrature)."""
    d = 1e-4
    u_ = compose(np.array([mu[0] - d]), np.array([mu[1]]), beta, g0)
    u0 = compose(np.array([mu[0]]), np.array([mu[1]]), beta, g0)
    kk = float(kof(u_[0], u_[1], 1.0, 0.0)); k0 = float(kof(u0[0], u0[1], 1.0, 0.0))
    return 4.0 * abs(math.log(kk) - math.log(k0)) / d

def build_quads(desc, beta, g0):
    quads, nodes = [], 0
    for mu, sg, w in desc["squads"]:
        npar = int(min(32, max(12, (squad_rate(mu, beta, g0) * sg) ** 2 // 2 + 12)))
        xs, ws = hermgauss(npar); xt, wt = hermgauss(10)
        quads.append((np.array(mu), sg, w, xs, ws, xt, wt)); nodes += npar * 10
    return quads, nodes

def run_case(case):
    kind, beta = case[1], case[2]
    ux, uy, desc = members(case)
    g0 = 1.0 / math.sqrt(1.0 - beta * beta)
    S = len(THETA)
    truth = np.empty(S); truthB = np.empty(S); onesmp = np.empty(S)
    bulk = np.empty(S); mixq = np.empty(S)
    m1g = np.empty(S) if kind == "ring" else None
    twopath = 0.0
    quads, mixq_nodes = (build_quads(desc, beta, g0) if "squads" in desc else ([], 0))
    if desc.get("formation") == "ring":
        br = desc["brot"]; phin = 2 * math.pi * (np.arange(64) + 0.5) / 64
        xs, ws = hermgauss(24); xt, wt = hermgauss(10); sg1 = br / math.sqrt(2.0)
        mixq_nodes = 64
    for i in range(S):
        nx, ny = NX[i], NY[i]
        kA = kof(ux, uy, nx, ny); kB = kof(ux, uy, nx, ny, path="B")
        twopath = max(twopath, float(np.max(np.abs(kA - kB) / kA)))
        truth[i] = np.sum(kA ** 4); truthB[i] = np.sum(kB ** 4)
        onesmp[i] = N * kA[0] ** 4
        bulk[i] = N * kof(np.array(beta), np.array(0.0), nx, ny) ** 4
        if quads:
            F = 0.0
            for mu, sg, w, xs, ws, xt, wt in quads:
                vx = mu[0] + sg * math.sqrt(2.0) * xs[:, None] * np.ones_like(xt)[None, :]
                vy = mu[1] + sg * math.sqrt(2.0) * np.ones_like(xs)[:, None] * xt[None, :]
                ww = (ws[:, None] * wt[None, :]) / math.pi
                qx, qy = compose(vx, vy, beta, g0)
                kq, _ = ksafe(qx, qy, nx, ny)
                F += w * float(np.sum(ww * kq ** 4))
            mixq[i] = N * F
        else:  # ring: the formation's own geometry, periodic trapezoid (spectral)
            vx = -br * np.sin(phin); vy = br * np.cos(phin)
            qx, qy = compose(vx, vy, beta, g0)
            mixq[i] = N * float(np.mean(kof(qx, qy, nx, ny) ** 4))
            vx = sg1 * math.sqrt(2.0) * xs[:, None] * np.ones_like(xt)[None, :]
            vy = sg1 * math.sqrt(2.0) * np.ones_like(xs)[:, None] * xt[None, :]
            ww = (ws[:, None] * wt[None, :]) / math.pi
            qx, qy = compose(vx, vy, beta, g0)
            km, _ = ksafe(qx, qy, nx, ny)
            m1g[i] = N * float(np.sum(ww * km ** 4))
    err = lambda F: np.abs(F / truth - 1.0)
    arms = {"per-ship": truthB, "one-sample": onesmp, "mix-quad": mixq, "bulk": bulk}
    if m1g is not None: arms["moment-1gauss"] = m1g
    kh = kof(ux, uy, 1.0, 0.0); kT = kof(ux, uy, 0.0, 1.0)
    return {"p99": {a: float(np.percentile(err(F), 99)) for a, F in arms.items()},
            "median": {a: float(np.median(err(F))) for a, F in arms.items()},
            "two_path": twopath, "nodes": mixq_nodes,
            "cv_k4_head": float(np.std(kh ** 4) / np.mean(kh ** 4)),
            "cv_k4_trans": float(np.std(kT ** 4) / np.mean(kT ** 4))}

def obs_frame_case(beta, sigma, n=400, seed=SEED + 1):
    """1885's convention: dispersion given directly in the observer frame."""
    rng = random.Random(seed)
    u = np.array([[beta + rng.gauss(0.0, sigma), rng.gauss(0.0, sigma)] for _ in range(n)])
    u = u[np.hypot(u[:, 0], u[:, 1]) < 1.0][:n]
    while len(u) < n:  # redraw rejects (rare at these sigmas)
        v = np.array([beta + rng.gauss(0.0, sigma), rng.gauss(0.0, sigma)])
        if np.hypot(*v) < 1.0: u = np.vstack([u, v])
    p99 = []
    for i in range(0, len(THETA), 20):
        kA = kof(u[:, 0], u[:, 1], NX[i], NY[i])
        p99.append(abs(float(np.sum(kA ** 4)) / (n * float(kof(np.array(beta), np.array(0.0), NX[i], NY[i])) ** 4) - 1.0))
    cv_head = float(np.std(kof(u[:, 0], u[:, 1], 1.0, 0.0) ** 4) / np.mean(kof(u[:, 0], u[:, 1], 1.0, 0.0) ** 4))
    return {"p99_bulkrel_sub": float(np.percentile(p99, 99)), "cv_k4_head": cv_head}

def big_truth_error(case, n=10**6, stride=20):
    """mix-quad vs a 10^6-member truth on a subsampled path: isolates readout error."""
    name, kind, beta = case[0], case[1], case[2]
    rng = random.Random(SEED + 2)
    p = case[3]; g0 = 1.0 / math.sqrt(1.0 - beta * beta)
    if kind == "gauss":
        vp = np.array([[rng.gauss(0.0, p["sigma"]), rng.gauss(0.0, p["sigma"])] for _ in range(n)])
        desc = {"squads": [((0.0, 0.0), p["sigma"], 1.0)]}
    elif kind == "ring":
        phi = 2 * math.pi * np.arange(n) / n
        vp = p["brot"] * np.stack([-np.sin(phi), np.cos(phi)], axis=1)
        desc = {"formation": "ring", "brot": p["brot"]}
    else:
        vp = np.array([[rng.gauss(mu, sg), rng.gauss(0.0, sg)]
                       for mu, sg in [p["squads"][0]] * (n // 2) + [p["squads"][1]] * (n // 2)])
        desc = {"squads": [((mu, 0.0), sg, 0.5) for mu, sg in p["squads"]]}
    ux, uy = compose(vp[:, 0], vp[:, 1], beta, g0)
    quads, nodes = (build_quads(desc, beta, g0) if "squads" in desc else ([], 0))
    errs = []
    for i in range(0, len(THETA), stride):
        nx, ny = NX[i], NY[i]
        T = float(np.sum(kof(ux, uy, nx, ny) ** 4))
        if quads:
            F = 0.0
            for mu, sg, w, xs, ws, xt, wt in quads:
                vx = mu[0] + sg * math.sqrt(2.0) * xs[:, None] * np.ones_like(xt)[None, :]
                vy = mu[1] + sg * math.sqrt(2.0) * np.ones_like(xs)[:, None] * xt[None, :]
                ww = (ws[:, None] * wt[None, :]) / math.pi
                qx, qy = compose(vx, vy, beta, g0)
                kq, _ = ksafe(qx, qy, nx, ny)
                F += w * float(np.sum(ww * kq ** 4))
            errs.append(abs(n * F / T - 1.0))
        else:
            vx = -p["brot"] * np.sin(2 * math.pi * (np.arange(64) + 0.5) / 64)
            vy = p["brot"] * np.cos(2 * math.pi * (np.arange(64) + 0.5) / 64)
            qx, qy = compose(vx, vy, beta, g0)
            errs.append(abs(n * float(np.mean(kof(qx, qy, nx, ny) ** 4)) / T - 1.0))
    return {"p99_readout_err_1e6": float(np.percentile(errs, 99)), "max_readout_err_1e6": float(np.max(errs))}

results = {}
for case in CASES:
    r = run_case(case)
    g2 = 1.0 / (1.0 - case[2] ** 2)
    sig = case[3].get("sigma", case[3].get("brot", 0.0) / math.sqrt(2.0))
    r["cv1885_head"] = math.sqrt(math.expm1(16 * (g2 * sig) ** 2))
    results[case[0]] = r
    print(f"{case[0]:22s} " + "  ".join(f"{a} {v:.4g}" for a, v in sorted(r["p99"].items())))

results["d-obs-frame-b0.9-s0.03"] = obs_frame_case(0.9, 0.03)
for c in [CASES[0], CASES[4], CASES[6]]:
    results[f"d-1e6-truth-{c[0]}"] = big_truth_error(c)

twopath = max(r["two_path"] for r in results.values() if "two_path" in r)
metrics = {
    "per-ship":   {"p99_flux_error": max(results[c[0]]["p99"]["per-ship"] for c in CASES),
                   "two_path_max_rel_diff": twopath, "ops_per_fleet_frame": N * (OP_K + 1)},
    "one-sample": {"p99_flux_error": max(results[c[0]]["p99"]["one-sample"] for c in CASES),
                   "two_path_max_rel_diff": twopath, "ops_per_fleet_frame": OP_K + 3},
    "mix-quad":   {"p99_flux_error": max(results[c[0]]["p99"]["mix-quad"] for c in CASES),
                   "two_path_max_rel_diff": twopath,
                   "ops_per_fleet_frame": int(max(results[c[0]]["nodes"] for c in CASES) * (OP_K + 2))},
}
json.dump(metrics, open("metrics.json", "w"), indent=1)
json.dump(results, open("diagnostics.json", "w"), indent=1, default=float)
print(json.dumps(metrics, indent=1))
for c in CASES:
    r = results[c[0]]
    print(f"{c[0]:22s} cv_head {r['cv_k4_head']:.3f} (1885-law {r['cv1885_head']:.3f})  cv_trans {r['cv_k4_trans']:.3f}  median one-sample {r['median']['one-sample']:.3f}")
print("d-obs-frame:", results["d-obs-frame-b0.9-s0.03"])
for k in [f"d-1e6-truth-{c[0]}" for c in [CASES[0], CASES[4], CASES[6]]]:
    print(k, results[k])
