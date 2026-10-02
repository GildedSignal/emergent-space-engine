import numpy as np, sys, json
sys.path.insert(0, ".")
from replica import *

GM_S = 1.0
a1 = 1.0
Norb = 300
fams = [("2:1", 2.0, 2, 1), ("3:2", 1.5, 3, 2)]
mus = [3e-4, 3e-3]
dets = [-1.0, 0.0, 1.0]
phases = [0.1, np.pi / 2 + 0.1]

cases = []
for (nm, ratio, p, q), mu, j, ph in [(f, m, j, ph) for f in fams for m in mus for j in dets for ph in phases]:
    W = 2.5 * mu ** (2.0 / 3.0)
    pr = ratio + j * W / 3.0
    cases.append(dict(name=nm, p=p, q=q, mu=mu, det=j, phase=ph,
                      a2=a1 * pr ** (2.0 / 3.0)))

NC = len(cases)
gm = np.ones(2 * NC)                                # drift around star
e0 = 0.02
st0 = np.zeros((2 * NC, 4))
for c, case in enumerate(cases):
    st0[2 * c] = state_from_elements(GM_S, a1, e0, 0.5, case["phase"])
    st0[2 * c + 1] = state_from_elements(GM_S, case["a2"], e0, 1.7, case["phase"] + 0.3)

def accel(st, t):
    d = st[0::2, :2] - st[1::2, :2]
    r = np.linalg.norm(d, axis=1)
    mu = np.array([c["mu"] for c in cases])
    a0 = -mu[:, None] * d / r[:, None] ** 3
    a1_ = mu[:, None] * d / r[:, None] ** 3
    out = np.empty((2 * NC, 2))
    out[0::2] = a0; out[1::2] = a1_
    return out

def mean_longitude(st):
    a, e, vp, nu = elements(st[..., 0], st[..., 1], st[..., 2], st[..., 3], GM_S)
    E = 2.0 * np.arctan2(np.sqrt(np.abs((1 - e) / (1 + e))) * np.sin(0.5 * nu), np.cos(0.5 * nu))
    M = E - e * np.sin(E)
    return a, e, vp, M + vp

def analyse(tr):
    """tr: (S, 2NC, 4) -> per case emax, theta wrap range, libration amplitude."""
    S = tr.shape[0]
    a, e, vp, lam = mean_longitude(tr.reshape(-1, 4))
    a = a.reshape(S, -1); e = e.reshape(S, -1); vp = vp.reshape(S, -1); lam = lam.reshape(S, -1)
    out = []
    for c, case in enumerate(cases):
        p, q = case["p"], case["q"]
        th = (p * lam[:, 2 * c + 1] - q * lam[:, 2 * c] - vp[:, 2 * c]) % TWOPI
        dth = np.abs(np.diff(np.unwrap(th))).max() if S > 1 else 0.0
        circ = np.ptp(np.unwrap(th)) > TWOPI           # circulating
        # libration amplitude: half the peak-to-peak of the unwrapped angle minus drift
        uu = np.unwrap(th)
        if not circ:
            amp = 0.5 * (np.max(uu) - np.min(uu))
        else:
            amp = TWOPI
        out.append(dict(emax1=float(np.max(e[10:, 2 * c])), emax2=float(np.max(e[10:, 2 * c + 1])),
                        amax1=float(np.max(a[10:, 2 * c])), circ=bool(circ), amp=float(amp)))
    return out

P1 = TWOPI * np.sqrt(a1 ** 3 / GM_S)
sample_every = 2 * 2 ** 3                            # fixed in steps: sample every 2^4 steps

def run(scheme, k):
    it = Integrator(scheme, gm, accel)
    tr = it.run(st0.copy(), Norb * 2 ** k, P1 / 2 ** k, 2 * 2 ** 3)
    return analyse(tr), it.nkick / (2 * NC) / Norb    # kicks per body-orbit (inner period)

res = {"cases": [{k: (v if not isinstance(v, (np.floating, float)) else float(v)) for k, v in c.items()} for c in cases],
       "Norb": Norb, "runs": {}}
for kref in (9,):
    an, _ = run("dkd", kref)
    res[f"ref{kref}"] = an
    print("ref", kref, "emax1", ["%.3e" % r["emax1"] for r in an], flush=True)

for scheme in ("dkd", "saba2", "whc3"):
    for k in (2, 3, 4, 5, 6):
        an, kpo = run(scheme, k)
        res["runs"][f"{scheme}_k{k}"] = an
        res["runs"][f"{scheme}_k{k}_kicks"] = KICKS_PER_STEP[scheme] * 2 ** k
        print(scheme, k, "emax1", ["%.2e" % r["emax1"] for r in an[:6]], flush=True)
json.dump(res, open("../s2.json", "w"), indent=1)
print("saved")
