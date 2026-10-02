import numpy as np, sys, json
sys.path.insert(0, ".")
from replica import *

GM_S = 1.0
muA, muB = 2.0 ** -18, 2.0 ** -15
aA, eA, wA, MA = 1.0133e8, 0.02, np.pi, 0.2 * TWOPI
aB, eB = 1.15e8, 0.13
wBs = [0.0, 1.0, 2.0, 3.0]
MBs = [0.5, 3.5]
Norb = 30
PA = TWOPI * np.sqrt(aA ** 3 / GM_S)

cases = [(wB, MB) for wB in wBs for MB in MBs]      # 8 phases, nothing engineered to pass closely
NC = len(cases)
gm = np.ones(2 * NC)
mus = np.zeros(2 * NC); mus[0::2] = muA; mus[1::2] = muB

st0 = np.zeros((2 * NC, 4))
for c, (wB, MB) in enumerate(cases):
    st0[2 * c] = state_from_elements(GM_S, aA, eA, wA, MA)
    st0[2 * c + 1] = state_from_elements(GM_S, aB, eB, wB, MB)

def accel(st, t):
    d = st[0::2, :2] - st[1::2, :2]
    r = np.linalg.norm(d, axis=1)
    out = np.empty((2 * NC, 2))
    out[0::2] = -mus[1::2, None] * d / r[:, None] ** 3
    out[1::2] = mus[0::2, None] * d / r[:, None] ** 3
    return out

RH_mut = ((muA + muB) / 3.0) ** (1.0 / 3.0) * 1.05e8

def run(scheme, k):
    it = Integrator(scheme, gm, accel)
    st = st0.copy()
    ns = Norb * 2 ** k
    mind = np.full(NC, 1e30)
    for i in range(ns):
        st = it.step(st, PA / 2 ** k)
        d = np.linalg.norm(st[0::2, :2] - st[1::2, :2], axis=1)
        mind = np.minimum(mind, d)
    a, e, vp, nu = elements(st[:, 0], st[:, 1], st[:, 2], st[:, 3], GM_S)
    return dict(mind=[float(x) for x in mind],
                aA=[float(x) for x in a[0::2]], aB=[float(x) for x in a[1::2]],
                eA=[float(x) for x in e[0::2]], eB=[float(x) for x in e[1::2]])

res = {"RH_mut": RH_mut, "cases": cases, "runs": {}}
for kref in (10, 11):
    res[f"ref{kref}"] = run("dkd", kref)
    print("ref", kref, "mind/RH", ["%.1f" % (m / RH_mut) for m in res[f"ref{kref}"]["mind"]], flush=True)

for scheme in ("dkd", "saba2", "saba3", "whc3"):
    for k in (3, 4, 5, 6, 7):
        r = run(scheme, k)
        res["runs"][f"{scheme}_k{k}"] = dict(kicks_per_orbit=KICKS_PER_STEP[scheme] * 2 ** k, **r)
        ref = res["ref11"]
        ea = max(abs(x / y - 1) for x, y in zip(r["eA"], ref["eA"]))
        aB_ = max(abs(x / y - 1) for x, y in zip(r["aB"], ref["aB"]))
        print(scheme, k, "worst dE_A=%.2e dB_a=%.2e" % (ea, aB_), flush=True)
json.dump(res, open("../s4.json", "w"), indent=1)
print("saved")
