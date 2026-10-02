import numpy as np, sys, json
sys.path.insert(0, ".")
from replica import *

GM_S, GM_H = 1.0, 2.0 ** -18
aH, eH, varpiH, M0H = 9.93e7 / (1 - 0.02), 0.02, np.pi, 0.2 * TWOPI
nH = np.sqrt(GM_S / aH ** 3)
PH = TWOPI / nH
RH = aH * (GM_H / 3.0) ** (1.0 / 3.0)

def moon_accel(st, t):
    xp, _ = ellipse_xv(aH, eH, varpiH, np.array([M0H + nH * t]))
    xp = np.asarray(xp)[0]
    xabs = st[:, :2] + xp[None, :]
    r = np.linalg.norm(xabs, axis=1)
    return -GM_S * xabs / r[:, None] ** 3 + GM_S * xp / np.linalg.norm(xp) ** 3

heldout = "--heldout" in sys.argv
e0 = 0.3 if heldout else 0.05
fracs = [0.25, 0.4, 0.6, 0.8]
am = np.array([f * RH for f in fracs])
Pm0 = TWOPI * np.sqrt(am ** 3 / GM_H)
Norb = 50
schemes = ["dkd", "saba2", "saba3", "whc3", "whc3b"]
ks = [1, 2, 3, 4, 5, 6, 7]

def run_one(scheme, k, m):
    st0 = state_from_elements(GM_H, am[m], e0, TWOPI / 16, 0.4375 * TWOPI)[None]
    tau = Pm0[m] / 2 ** k
    it = Integrator(scheme, [GM_H], moon_accel)
    tr = it.run(st0, Norb * 2 ** k, tau, 2 ** k)     # sample each moon orbit
    a, e, vp, _ = elements(tr[:, 0, 0], tr[:, 0, 1], tr[:, 0, 2], tr[:, 0, 3], GM_H)
    S = len(a); sl = slice(S // 2, S)
    uu = np.unwrap(vp)
    rate = np.polyfit(np.arange(S)[sl], uu[sl], 1)[0] * Pm0[m] / PH  # rad per Home orbit
    return dict(rate=float(rate), emax=float(np.nanmax(e[2:])),
                esc=bool(e[-1] >= 1.0 or a[-1] > 3 * a[0])), tr

res = {"e0": e0, "fracs": fracs, "ref": {}, "runs": {}, "telescope": {}}
for kref in (10, 11):
    res["ref"][kref] = [run_one("dkd", kref, m)[0] for m in range(4)]
conv = max(abs(res["ref"][10][m]["rate"] / res["ref"][11][m]["rate"] - 1) for m in range(4))
res["ref_convergence"] = conv
print("ref rates rad/HomeOrbit:", ["%.4e" % r["rate"] for r in res["ref"][11]], "conv", conv, flush=True)

for scheme in schemes:
    for k in ks:
        rows = [run_one(scheme, k, m)[0] for m in range(4)]
        res["runs"][f"{scheme}_k{k}"] = dict(kicks_per_orbit=KICKS_PER_STEP[scheme] * 2 ** k, moons=rows)
        print(scheme, k, ["%.3e" % r["rate"] for r in rows], ["%.3f" % r["emax"] for r in rows], flush=True)

# telescoping: whc3 vs whc3b trajectory closeness at k=3
for m in (1, 2):
    _, t3 = run_one("whc3", 3, m)
    _, tb = run_one("whc3b", 3, m)
    res["telescope"][f"moon{m}_maxdiff_over_a"] = float(np.max(np.abs(t3 - tb)) / am[m])
print("telescoping diff/a:", res["telescope"], flush=True)
json.dump(res, open(f"../s1{'_heldout' if heldout else ''}.json", "w"), indent=1)
print("saved")
