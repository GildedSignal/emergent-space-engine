"""Is the resonance gate one certificate?  (lens: whole system; run 20261011-0736-system-785d)

Certificate candidate (one line):  excursion(delta) = 2 * pdot_coh / |theta_dot(delta)|
  theta = (j+1) lam2 - j lam1 - varpi1 ;  theta_dot = (j+1) n2 - j n1 - varpidot_sec
  pdot_coh = amplitude of the resonant (slow-phase) part of de/dt, from a lambda1-quadrature
  at fixed theta along the unperturbed orbits  (the engine's own compiled numbers).
The orbit-averaged cheap law (resonant angle averaged away) keeps e = e0.  It is valid
while excursion < quantum q_e; T_agree = min(pi/|theta_dot|, q_e/pdot_coh) when it fails.

Stages (each <= ~60 s):
  selftest   mu=0 must hold e exactly; element extraction check
  quad       certificate inputs for all (j, mu, delta) -> quad.json
  calib      far controls (band -> q_e) + negative control at exact resonance -> calib.json
  scan j mu  decisive grid -> scan-<j>-<mu>.npz
  analyze    metrics.json + tables
"""
import json, sys, time
import numpy as np


def nrm(x, keepdims=False):
    n = np.sqrt(np.einsum('...i,...i->...', x, x))
    return n[..., None] if keepdims else n


OUT = "/home/glmlab/actions-runner/_work/emergent-space-engine/lab-2/lab/results/20261011-0736-system-785d"
E0 = 0.02
NSEED = 8
DT_PER_P2 = 600.0          # dt = P2/300
SYN_HORIZON = 200          # run length in synodic periods (exact-resonance value)

def a_of_ratio(pratio):    # inner/outer period ratio -> inner semimajor axis (a2=1)
    return pratio ** (-2.0 / 3.0)

def res_params(j):
    """j=1 -> 2:1 interior resonance (n1/n2=2); j=2 -> 3:2."""
    pr = (j + 1) / j
    a1 = a_of_ratio(pr)
    T = SYN_HORIZON * 2 * np.pi / abs(a1 ** (-1.5) - 1.0)   # synodic period at exact resonance
    return pr, a1, T

# ---------------- Kepler (GM=1) ----------------
def kepler_rv(a, e, M):
    """position/velocity on a Kepler orbit, varpi=0, from mean anomaly M (vectorized)."""
    E = M.copy()
    for _ in range(12):
        E -= (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    cE, sE = np.cos(E), np.sin(E)
    n = a ** -1.5
    r = np.stack([a * (cE - e), a * np.sqrt(1 - e * e) * sE], axis=-1)
    Edot = n / (1.0 - e * cE)
    v = np.stack([-a * sE * Edot, a * np.sqrt(1 - e * e) * cE * Edot], axis=-1)
    return r, v

def osc_elems(rrel, vrel):
    """osculating (a, e, varpi, lam) from heliocentric state, GM=1."""
    vv = np.sum(vrel * vrel, -1); rr = nrm(rrel)
    evec = ((vv - 1.0 / rr)[..., None] * rrel - np.sum(rrel * vrel, -1)[..., None] * vrel)
    e = nrm(evec)
    a = 1.0 / (2.0 / rr - vv)
    varpi = np.arctan2(evec[..., 1], evec[..., 0])
    # true longitude-ish: angle of r
    lam = np.arctan2(rrel[..., 1], rrel[..., 0])
    return a, e, varpi, lam, evec

# ---------------- truth integrator ----------------
def leapfrog_scan(j, mu, a1_list, T, seeds=None, want_series=()):
    """Run all (a1 x seed) systems; barycentric leapfrog, star M=1, planet mu, test 0.
    Returns dict of per-system scalars + a few e(t) series."""
    if seeds is None:
        seeds = np.arange(NSEED) * 2 * np.pi / NSEED
    A1, S = np.meshgrid(np.asarray(a1_list), seeds, indexing="ij")
    A1, S = A1.ravel(), S.ravel()
    N = A1.size
    dt = 2 * np.pi / DT_PER_P2
    nsteps = int(np.ceil(T / dt))
    ck = 16

    # barycentric init
    q = np.zeros((N, 3, 2)); p = np.zeros((N, 3, 2)); m = np.zeros(3); m[0] = 1.0; m[1] = mu
    q[:, 1, 0] = 1.0 / (1.0 + mu); p[:, 1, 1] = np.sqrt(1.0 + mu) / (1.0 + mu)
    q[:, 0, 0] = -mu / (1.0 + mu); p[:, 0, 1] = -mu * np.sqrt(1.0 + mu) / (1.0 + mu)
    rp, vp = kepler_rv(A1, np.full(N, E0), S)
    q[:, 2] = q[:, 0, :] + rp; p[:, 2] = p[:, 0, :] + vp

    def acc(qq):
        d01 = qq[:, 1] - qq[:, 0]; r01 = nrm(d01, keepdims=True)
        a_ = np.zeros_like(qq)
        a_[:, 0] += mu * d01 / r01 ** 3
        a_[:, 1] -= 1.0 * d01 / r01 ** 3
        d12 = qq[:, 1] - qq[:, 2]; r12 = nrm(d12, keepdims=True)
        a_[:, 2] += mu * d12 / r12 ** 3
        d02 = qq[:, 0] - qq[:, 2]; r02 = nrm(d02, keepdims=True)
        a_[:, 2] += 1.0 * d02 / r02 ** 3
        return a_

    def energy(qq, pp):
        ke = 0.5 * (m[0] * np.sum(pp[:, 0] ** 2, -1) + m[1] * np.sum(pp[:, 1] ** 2, -1))
        d01 = nrm(qq[:, 1] - qq[:, 0])
        return ke - m[1] / d01

    E_init = energy(q, p)
    a_ = acc(q); p += 0.5 * dt * a_
    nck = nsteps // ck
    eser = np.zeros((nck, N))
    thser = np.zeros((nck, N))
    tser = np.zeros(nck)
    for i in range(nsteps):
        q += dt * p
        a_ = acc(q)
        if i == nsteps - 1:
            p += dt * a_
        else:
            p += dt * a_
        if (i + 1) % ck == 0:
            k = (i + 1) // ck - 1
            vfull = p - 0.5 * dt * a_
            rrel = q[:, 2] - q[:, 0]; vrel = vfull[:, 2] - vfull[:, 0]
            aa, ee, vp_, lam, _ = osc_elems(rrel, vrel)
            # planet true longitude (circular): angle of q2 - q0
            lam2 = np.arctan2(q[:, 1, 1] - q[:, 0, 1], q[:, 1, 0] - q[:, 0, 0])
            thser[k] = (j + 1) * lam2 - j * lam - vp_
            eser[k] = ee; tser[k] = (i + 1) * dt
    p_fin = p - 0.5 * dt * acc(q)
    E_fin = energy(q, p_fin)
    res = {"N": N, "nsteps": nsteps, "dt": dt, "Edrift": float(np.max(np.abs(E_fin - E_init))),
           "a1": A1, "seed": S, "emax": eser.max(0), "emin": eser.min(0), "efin": eser[-1]}
    # theta unwrap + regime
    dth = np.diff(np.unwrap(thser, axis=0), axis=0)
    res["theta_net"] = dth.sum(0)
    res["theta_amp"] = np.unwrap(thser, axis=0).max(0) - np.unwrap(thser, axis=0).min(0)
    series = {}
    for idx in want_series:
        series[str(idx)] = (tser, eser[:, idx].copy(), np.unwrap(thser[:, idx]))
    res["series"] = series
    res["_eser"] = eser
    return res

def agree_times(res, q_e, a1_list=None, j=1, e0=E0):
    """T_agree on the synodic running mean of e (the averaged law predicts the mean).
    Window = one synodic period of that system."""
    eser = res["_eser"]; N = res["N"]
    T = np.zeros(N)
    for i in range(N):
        if a1_list is None:
            w = 1
        else:
            k = i // NSEED
            n1 = a1_list[k] ** -1.5
            w = max(1, int(round(2 * np.pi / abs(n1 - 1.0) / (res["dt"] * 16))))
        em = np.convolve(eser[:, i], np.ones(w) / w, mode="valid")
        bad = np.nonzero(np.abs(em - e0) > q_e)[0]
        T[i] = (bad[0] + w) * res["dt"] * 16 if bad.size else -1.0
    return T

# ---------------- cheap-path quadrature (certificate inputs) ----------------
def quad_cert(j, mu, a1, e0=E0, nL=512, nTh=64):
    """pdot_coh = max over theta of |<de/dt>_{lambda1 at fixed theta}| ; varpidot_sec ;
    computed along unperturbed orbits (heliocentric, direct+indirect)."""
    lam1 = (np.arange(nL) + 0.5) / nL * 2 * np.pi
    ths = (np.arange(nTh) + 0.5) / nTh * 2 * np.pi
    LAM1 = np.tile(lam1, nTh); TH = np.repeat(ths, nL)
    LAM2 = (TH + j * LAM1) / (j + 1.0)          # varpi1 = 0
    r, v = kepler_rv(np.full(LAM1.size, a1), np.full(LAM1.size, e0), LAM1)
    r2 = np.stack([np.cos(LAM2), np.sin(LAM2)], -1)          # a2 = 1
    d = r2 - r; dn = nrm(d, keepdims=True)
    ap = mu * (d / dn ** 3 - r2)                              # direct + indirect
    vv = np.sum(v * v, -1); rr = nrm(r)
    rv = np.sum(r * v, -1)
    aosc = 1.0 / (2.0 / rr - vv)
    evec = ((vv - 1.0 / rr)[:, None] * r - rv[:, None] * v)
    eosc = nrm(evec)
    Lz = r[..., 0] * v[..., 1] - r[..., 1] * v[..., 0]
    Ldot = r[..., 0] * ap[..., 1] - r[..., 1] * ap[..., 0]
    Edot = np.sum(v * ap, -1)
    adot = 2 * aosc ** 2 * Edot
    edot = (adot * (1 - eosc ** 2) - 2 * Lz * Ldot) / (2 * aosc * eosc)
    pd = edot.reshape(nTh, nL).mean(1)
    pdot_coh = float(np.max(np.abs(pd)))
    # secular varpi precession: devec/dt = d(evec)/dv . ap  (Kepler part cancels)
    def evec_of(rq, vq):
        vvv = np.sum(vq * vq, -1); rrr = np.linalg.norm(rq, -1)
        return ((vvv - 1.0 / rrr)[:, None] * rq - np.sum(rq * vq, -1)[:, None] * vq)
    # secular precession: uniform independent average over (lam1, lam2), not theta
    nS = 200
    l1 = (np.arange(nS) + 0.5) / nS * 2 * np.pi
    L1g, L2g = np.meshgrid(l1, l1, indexing="ij")
    rs, vs = kepler_rv(np.full(L1g.size, a1), np.full(L1g.size, e0), L1g.ravel())
    r2s = np.stack([np.cos(L2g.ravel()), np.sin(L2g.ravel())], -1)
    ds = r2s - rs; dns = nrm(ds, keepdims=True)
    aps = mu * (ds / dns ** 3 - r2s)
    h = 1e-6
    devs = (evec_of(rs, vs + h * aps) - evec_of(rs, vs - h * aps)) / (2 * h)
    evs = evec_of(rs, vs); es = nrm(evs)
    cross = evs[..., 0] * devs[..., 1] - evs[..., 1] * devs[..., 0]
    varpidot = float((cross / es ** 2).mean())
    n1 = a1 ** -1.5
    thdot = (j + 1) * 1.0 - j * n1 - varpidot
    return {"pdot_coh": pdot_coh, "varpidot_sec": varpidot, "thdot": float(thdot),
            "pd_res_amp": pdot_coh, "n1": float(n1)}

# ---------------- stages ----------------
def st_selftest():
    pr, a1, T = res_params(1)
    r = leapfrog_scan(1, 0.0, [a1], min(T, 400.0))
    e = r["_eser"]
    amp1 = e[: len(e) // 2].max() - e[: len(e) // 2].min()
    amp2 = e[len(e) // 2 :].max() - e[len(e) // 2 :].min()
    pred = 2 * (2 * 2 * np.pi / 600.0) ** 2 / 2  # peak-to-peak of (n1*dt)^2/2 ringing
    print("mu=0: ringing amp=%.3e (pred %.3e), drift amp1=%.3e amp2=%.3e (must be equal-ish)" %
          (amp2, pred, amp1, amp2))
    assert abs(amp2 - pred) < 0.5 * pred and abs(amp1 - amp2) < 0.2 * amp1  # bounded, no drift

def st_quad():
    out = {}
    for j in (1, 2):
        pr, a1ex, _ = res_params(j)
        dgrid = np.array([0.0] + [s * v for s in (1, -1) for v in
                          (0.0005, 0.001, 0.002, 0.004, 0.008, 0.016, 0.032)])
        dgrid = np.sort(np.unique(dgrid))
        for mu in (3e-4, 1e-3, 3e-3):
            ent = {}
            for d in dgrid:
                a1 = a1ex * (1 + d)
                ent["%+.5f" % d] = quad_cert(j, mu, a1)
            ent["a1_exact"] = a1ex
            ent["mu"] = mu
            out["j%d_mu%g" % (j, mu)] = ent
    json.dump(out, open(OUT + "/quad.json", "w"), indent=1)
    pr1, a11, _ = res_params(1); pr2, a12, _ = res_params(2)
    print("quad done. examples:")
    print(" 2:1 mu=1e-3 exact:", out["j1_mu0.001"]["+0.00000"])
    print(" 3:2 mu=3e-4 exact:", out["j2_mu0.0003"]["+0.00000"])

def st_calib():
    out = {}
    for j, farpr in ((1, 2.15), (2, 1.9)):
        a1far = a_of_ratio(farpr)
        for mu in (3e-4, 1e-3, 3e-3):
            pr, a1ex, T = res_params(j)
            r = leapfrog_scan(j, mu, [a1far], T)
            Taf = agree_times(r, 1e9, [a1far], j)   # dummy: never fails; use series band
            n1f = a1far ** -1.5
            wf = max(1, int(round(2 * np.pi / abs(n1f - 1.0) / (r["dt"] * 16))))
            emb = np.convolve(r["_eser"][:, 0], np.ones(wf) / wf, mode="valid")
            for s in range(1, r["N"]):
                emb2 = np.convolve(r["_eser"][:, s], np.ones(wf) / wf, mode="valid")
                emb = np.concatenate([emb, emb2])
            band = float(emb.max() - emb.min())
            q_e = max(2.0 * band, 0.002)
            out["j%d_mu%g" % (j, mu)] = {"far_pratio": farpr, "band": band, "q_e": q_e,
                                         "Edrift": r["Edrift"]}
            print("j=%d mu=%g far band=%.5f -> q_e=%.4f  Edrift=%.2e" % (j, mu, band, q_e, r["Edrift"]))
    # negative control: exact resonance, mu=3e-3, 2:1 must fail fast
    pr, a1ex, T = res_params(1)
    r = leapfrog_scan(1, 3e-3, [a1ex], T)
    qe = out["j1_mu0.003"]["q_e"]
    Ta = agree_times(r, qe, [a1ex], 1)
    frac_fail = float(np.mean(Ta > 0))
    print("negative control 2:1 mu=3e-3 exact: fail fraction=%.2f (must be 1.0), "
          "median T_agree=%.1f" % (frac_fail, np.median(Ta[Ta > 0])))
    out["negctl"] = {"frac_fail": frac_fail, "T_agree_median": float(np.median(Ta[Ta > 0]))}
    json.dump(out, open(OUT + "/calib.json", "w"), indent=1)

def st_scan(j, mu):
    pr, a1ex, T = res_params(j)
    dgrid = np.array([0.0] + [s * v for s in (1, -1) for v in
                     (0.0005, 0.001, 0.002, 0.004, 0.008, 0.016, 0.032)])
    dgrid = np.sort(np.unique(dgrid))
    a1l = list(a1ex * (1 + dgrid))
    t0 = time.time()
    r = leapfrog_scan(j, mu, a1l, T, want_series=(0, len(dgrid) // 2))
    # running-mean (synodic window) series per system -> band + T_agree over a q_e grid
    qgrid = np.geomspace(0.002, 0.16, 15)
    N = r["N"]; nck = r["_eser"].shape[0]
    band = np.zeros(N); Tage = np.full((qgrid.size, N), -1.0)
    ems = np.zeros((nck, N))
    for i in range(N):
        k = i // NSEED
        n1 = a1l[k] ** -1.5
        w = max(1, int(round(2 * np.pi / abs(n1 - 1.0) / (r["dt"] * 16))))
        em = np.convolve(r["_eser"][:, i], np.ones(w) / w, mode="valid")
        ems[:, i] = np.concatenate([np.full(w - 1, em[0]), em])
        band[i] = em.max() - em.min()
        for qi, q in enumerate(qgrid):
            bad = np.nonzero(np.abs(em - E0) > q)[0]
            if bad.size:
                Tage[qi, i] = (bad[0] + w) * r["dt"] * 16
    res = {"j": j, "mu": mu, "dgrid": dgrid.tolist(), "T": T, "a1": a1l,
           "qgrid": qgrid.tolist(), "Tage": Tage.tolist(), "band": band.tolist(),
           "emax": r["emax"].tolist(), "emin": r["emin"].tolist(),
           "theta_net": r["theta_net"].tolist(), "theta_amp": r["theta_amp"].tolist(),
           "Edrift": r["Edrift"], "wall_s": time.time() - t0, "dt": r["dt"],
           "series": {k: [list(v[0][::8]), list(v[1]), list(v[2][::8])]
                      for k, v in r["series"].items()}}
    np.save(OUT + ("/scan-j%d-mu%g.npy" % (j, mu)), res, allow_pickle=True)
    print("scan j=%d mu=%g done in %.1fs Edrift=%.2e" % (j, mu, res["wall_s"], r["Edrift"]))
    # control-side printout ONLY: outermost detunings (calibration) + exact resonance (negative ctl)
    for lab, idx in (("outer+", len(dgrid) - 1), ("outer-", 1), ("exact", len(dgrid) // 2)):
        b = band[idx * NSEED:(idx + 1) * NSEED]
        tq = Tage[:, idx * NSEED:(idx + 1) * NSEED]
        print("  ctl %-6s d=%+.4f band_med=%.5f  failfrac(q=0.004)=%.2f" %
              (lab, dgrid[idx], np.median(b), np.mean(tq[2] > 0)))

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "selftest": st_selftest()
    elif cmd == "quad": st_quad()
    elif cmd == "calib": st_calib()
    elif cmd == "scan": st_scan(int(sys.argv[2]), float(sys.argv[3]))
    elif cmd == "analyze":
        exec(open(OUT + "/analyze.py").read())
