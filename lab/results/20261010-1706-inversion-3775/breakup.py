#!/usr/bin/env python3
"""Inversion run 20261010-1706-inversion-3775: the breakup cloud vs the co-orbital certificate.

Scenes (coplanar Kepler, mu=1, breakup at P=(1,0), circular v0=1):
  cloud     N fragments, velocity dispersion sigma (Gaussian, radial+tangential)
  formation N bodies on ONE orbit (a=1,e=0.05,varsigma=0), passage-time lattice train
  belt      a~U[0.95,1.05], e~Rayleigh(0.02), angles uniform  (design's diffuse regime)

Truth: a pair's crossings are the two roots of (dV)cos th + (dW) sin th = dU (== the Binet cone);
conjunction epochs at a crossing are tau_i + m T_i; near a co-passage through a shared point the
relative motion is d(s) = |dv*s + v_j*dt| with s within the window (clamped: near-twin pairs'
catch-up conjunctions belong to other epochs, not this window). Validated vs Kepler (P7).
Phase rank is CIRCULAR (rank along the orbit, as the certificate defines its neighbours).
"""
import json, os, time
import numpy as np

MU = 1.0
R0 = 1.0
B = 1e-4            # encounter radius (r0 units)
SIGMA = 1e-3        # breakup dispersion / v0
TAUC = 3 * B        # certificate window 3 b / v0
TWO_PI = 2 * np.pi


def kepler_E(M, e):
    E = M.copy()
    for _ in range(10):
        E -= (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E


def nu_of_E(E, e):
    return 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))


def elements_from_state(x, y, vx, vy):
    r = np.hypot(x, y); v2 = vx**2 + vy**2
    eps = v2 / 2 - MU / r
    a = -MU / (2 * eps)
    h = x * vy - y * vx
    rv = x * vx + y * vy
    ex = ((v2 - MU / r) * x - rv * vx) / MU
    ey = ((v2 - MU / r) * y - rv * vy) / MU
    e = np.hypot(ex, ey); varpi = np.arctan2(ey, ex)
    p = h * h / MU
    cosn = np.clip((p / r - 1) / np.maximum(e, 1e-15), -1, 1)
    nu = np.sign(rv + 1e-300) * np.arccos(cosn)
    E = 2 * np.arctan2(np.sqrt(1 - e) * np.sin(nu / 2), np.sqrt(1 + e) * np.cos(nu / 2))
    M0 = (E - e * np.sin(E)) % TWO_PI
    n = a ** -1.5
    return dict(a=a, e=e, varpi=varpi, M0=M0, n=n, T=TWO_PI / n, tau_P=np.zeros_like(a),
                vx=vx, vy=vy, scene="cloud")


def make_cloud(N, sigma, seed):
    rng = np.random.default_rng(seed)
    vx = rng.normal(0, sigma, N)
    vy = 1.0 + rng.normal(0, sigma, N)
    return elements_from_state(np.full(N, R0), np.zeros(N), vx, vy)


def make_formation(N, d_tau=0.4e-4):
    a = np.full(N, 1.0); e = np.full(N, 0.05); varpi = np.zeros(N)
    n = a ** -1.5; T = TWO_PI / n
    tau = (np.arange(N) - N / 2) * d_tau
    nu_P = np.arccos(((1 - e**2) / R0 - 1) / e)
    E_P = 2 * np.arctan2(np.sqrt(1 - e) * np.sin(nu_P / 2), np.sqrt(1 + e) * np.cos(nu_P / 2))
    M_P = E_P - e * np.sin(E_P)
    M0 = (M_P - n * tau) % TWO_PI
    return dict(a=a, e=e, varpi=varpi, M0=M0, n=n, T=T, tau_P=tau % T[0],
                vx=None, vy=None, scene="formation")


def make_belt(N, seed, awidth=0.2, esig=0.02):
    rng = np.random.default_rng(seed)
    a = rng.uniform(1 - awidth, 1 + awidth, N)
    e = rng.rayleigh(esig, N)
    varpi = rng.uniform(0, TWO_PI, N)
    M0 = rng.uniform(0, TWO_PI, N)
    n = a ** -1.5
    return dict(a=a, e=e, varpi=varpi, M0=M0, n=n, T=TWO_PI / n,
                tau_P=None, vx=None, vy=None, scene="belt")


def binet(f):
    p = f["a"] * (1 - f["e"]**2)
    return 1 / p, f["e"] * np.cos(f["varpi"]) / p, f["e"] * np.sin(f["varpi"]) / p


def cone_retention(f, step=512):
    U, V, W = binet(f); n = len(U); keep = 0
    for s in range(0, n, step):
        e_ = min(s + step, n)
        dU = U[s:e_, None] - U[None, :n]
        dV = V[s:e_, None] - V[None, :n]
        dW = W[s:e_, None] - W[None, :n]
        m = (dU**2 <= dV**2 + dW**2)
        m &= (np.arange(s, e_)[:, None] < np.arange(n)[None, :])
        keep += int(m.sum())
    return keep, n * (n - 1) // 2


def plane_residual(f):
    U, V, _ = binet(f)
    return float(np.max(np.abs(U + V - 1.0)))


def vel_at_theta(f, theta):
    e = f["e"]; varpi = f["varpi"]; p = f["a"] * (1 - e**2); h = np.sqrt(MU * p)
    nu = theta - varpi
    vr = MU / h * e * np.sin(nu); vt = MU / h * (1 + e * np.cos(nu))
    return vr * np.cos(theta) - vt * np.sin(theta), vr * np.sin(theta) + vt * np.cos(theta)


def vel_at_theta_id(f, ids, theta):
    e = f["e"][ids]; varpi = f["varpi"][ids]; p = f["a"][ids] * (1 - e**2); h = np.sqrt(MU * p)
    nu = theta - varpi
    vr = MU / h * e * np.sin(nu); vt = MU / h * (1 + e * np.cos(nu))
    return vr * np.cos(theta) - vt * np.sin(theta), vr * np.sin(theta) + vt * np.cos(theta)


def epochs_vec(f, ids, thetas):
    e_ = f["e"][ids]; varpi = f["varpi"][ids]; nn = f["n"][ids]; TT = f["T"][ids]; M0 = f["M0"][ids]
    nu = thetas - varpi
    E = 2 * np.arctan2(np.sqrt(1 - e_) * np.sin(nu / 2), np.sqrt(1 + e_) * np.cos(nu / 2))
    Mth = E - e_ * np.sin(E)
    return ((Mth - M0) % TWO_PI) / nn, TT


def miss_dist(vxi, vyi, vxj, vyj, dt, tauc):
    """min |dv*s + v_j*dt| over s in [-tauc, tauc] (arrays; dt array too)."""
    dvx = vxj - vxi; dvy = vyj - vyi
    dv2 = dvx**2 + dvy**2
    Cx = vxj * dt; Cy = vyj * dt
    s = np.where(dv2 > 1e-28, -(Cx * dvx + Cy * dvy) / np.maximum(dv2, 1e-28), 0.0)
    s = np.clip(s, -tauc, tauc)
    return np.hypot(dvx * s + Cx, dvy * s + Cy)


def at_P_truth(f, t0, tH, b=B, tauc=TAUC):
    """exact at-P conjunctions via the global epoch stream (cloud: epochs = m T_i)."""
    Ts = f["T"]; N = len(Ts)
    m0 = np.ceil(t0 / Ts).astype(int)
    m1 = np.ceil(tH / Ts).astype(int)
    counts = np.maximum(m1 - m0, 0)
    ev_t = (np.concatenate([np.arange(m0[i], m1[i]) * Ts[i] for i in range(N)])
            if counts.sum() else np.empty(0))
    if ev_t.size == 0:
        return [], 0
    ev_i = np.repeat(np.arange(N), counts)
    o = np.argsort(ev_t); ev_t = ev_t[o]; ev_i = ev_i[o]
    hi = np.searchsorted(ev_t, ev_t + tauc, side="right")
    vx = f["vx"]; vy = f["vy"]
    out = []
    for p in range(len(ev_t) - 1):
        for q in range(p + 1, hi[p]):
            i, j = int(ev_i[p]), int(ev_i[q])
            dt = ev_t[q] - ev_t[p]
            d = float(miss_dist(vx[i], vy[i], vx[j], vy[j], dt, tauc))
            if d < b:
                out.append((i, j, float(ev_t[q]), d))
    return out, len(ev_t)


def window_pair_count(f, t0, tH, tauc=TAUC):
    Ts = f["T"]; N = len(Ts)
    m0 = np.ceil(t0 / Ts).astype(int); m1 = np.ceil(tH / Ts).astype(int)
    counts = np.maximum(m1 - m0, 0)
    ev_t = np.concatenate([np.arange(m0[i], m1[i]) * Ts[i] for i in range(N)])
    ev_t = np.sort(ev_t)
    hi = np.searchsorted(ev_t, ev_t + tauc, side="right")
    return int((hi - np.arange(len(ev_t)) - 1).clip(min=0).sum())


def at_P_truth_generic(f, t0, tH, b=B, tauc=TAUC):
    """formation: same orbit, epochs = tau lattice; distance = v(P) |dt| (parallel limit)."""
    vx, vy = vel_at_theta(f, 0.0)
    v = float(np.hypot(vx[0], vy[0]))
    taus = f["tau_P"]; T = float(f["T"][0]); n = len(taus)
    out = []
    m0 = int(np.ceil((t0 - taus.max()) / T)); m1 = int(np.floor((tH - taus.min()) / T))
    order = np.argsort(taus); ts = taus[order]
    for m in range(max(m0, 0), m1 + 1):
        ev = ts + m * T
        hi = np.searchsorted(ev, ev + tauc, side="right")
        for p in range(len(ev)):
            for q in range(p + 1, min(hi[p], len(ev))):
                d = v * (ev[q] - ev[p])
                if d < b:
                    out.append((int(order[p]), int(order[q]), float(ev[q]), float(d)))
    return out, n * max(m1 - m0 + 1, 0)


def at_Q_truth_sample(f, t0, tH, npairs, b=B, tauc=TAUC, seed=7, blk_size=4096):
    """second-crossing conjunctions on a random pair subsample, extrapolated."""
    rng = np.random.default_rng(seed)
    N = len(f["a"]); all_pairs = N * (N - 1) // 2
    pi_ = rng.integers(0, N, npairs * 2); pj_ = rng.integers(0, N, npairs * 2)
    m = pi_ < pj_; pi_, pj_ = pi_[m][:npairs], pj_[m][:npairs]
    U, V, W = binet(f)
    A = V[pi_] - V[pj_]; Bw = W[pi_] - W[pj_]; C = U[pj_] - U[pi_]
    G = np.hypot(A, Bw)
    ok = np.abs(C) <= G
    thQ = (2 * np.arctan2(Bw, A)) % TWO_PI
    cnt = 0; enc = []
    idx = np.where(ok)[0]
    for s in range(0, len(idx), blk_size):
        blk = idx[s:s + blk_size]
        th = thQ[blk]
        taus_i, Ts_i = epochs_vec(f, pi_[blk], th)
        taus_j, Ts_j = epochs_vec(f, pj_[blk], th)
        m_lo = max(int(np.ceil((t0 - max(taus_i.max(), taus_j.max()) - tauc)
                               / max(Ts_i.max(), Ts_j.max()))), 0)
        m_hi = int(np.ceil(tH / min(Ts_i.min(), Ts_j.min()))) + 1
        mi = np.arange(m_lo, m_hi)
        Ei = taus_i[:, None] + mi[None, :] * Ts_i[:, None]
        Ej = taus_j[:, None] + mi[None, :] * Ts_j[:, None]
        Ei = np.where((Ei >= t0) & (Ei <= tH), Ei, np.inf)
        Ej = np.where((Ej >= t0) & (Ej <= tH), Ej, -np.inf)
        D = Ej[:, None, :] - Ei[:, :, None]          # (blk, m_i, m_j)
        vxi, vyi = vel_at_theta_id(f, pi_[blk], th)
        vxj, vyj = vel_at_theta_id(f, pj_[blk], th)
        d = miss_dist(vxi[:, None, None], vyi[:, None, None],
                      vxj[:, None, None], vyj[:, None, None], D, tauc)
        hit = (D > 0) & (np.abs(D) < tauc) & (d < b)
        cnt += int(hit.sum())
        if hit.any():
            bi, mi_, mj_ = np.where(hit)
            for x in range(min(len(bi), 50)):
                enc.append((int(pi_[blk[bi[x]]]), int(pj_[blk[bi[x]]]), float(Ei[bi[x], mi_[x]])))
    return cnt, len(idx), all_pairs, enc


def lambda_all(f, t):
    M = (f["M0"] + f["n"] * t) % TWO_PI
    E = kepler_E(M, f["e"])
    return f["varpi"] + nu_of_E(E, f["e"])


def pos_of(f, t, N):
    lam = lambda_all(f, t)
    pos = np.empty(N, int); pos[np.argsort(lam)] = np.arange(N)
    return pos

def lambda_all(f, t):
    M = (f["M0"] + f["n"] * t) % TWO_PI
    E = kepler_E(M, f["e"])
    return (f["varpi"] + nu_of_E(E, f["e"])) % TWO_PI


def crank(i, j, pos, N):
    dr = abs(int(pos[i]) - int(pos[j]))
    return min(dr, N - dr)


def xy_of(f, i, t):
    M = (f["M0"][i] + f["n"][i] * t) % TWO_PI
    E = kepler_E(M, np.full_like(t, f["e"][i]))
    nu = nu_of_E(E, f["e"][i])
    r = f["a"][i] * (1 - f["e"][i] * np.cos(E))
    th = f["varpi"][i] + nu
    return r * np.cos(th), r * np.sin(th)


if __name__ == "__main__":
    t_start = time.time()
    res = {"machine": os.popen("grep -m1 'model name' /proc/cpuinfo").read().strip(),
           "load": os.getloadavg(), "b": B, "sigma": SIGMA, "tauc": TAUC}

    # ---------- P1/P2/P5: cone retention, null plane, spreads, cone-probe trigger
    for name, f in [("cloud", make_cloud(4000, SIGMA, 11)),
                    ("belt", make_belt(4000, 12)),
                    ("formation", make_formation(4000))]:
        keep, tot = cone_retention(f)
        res[f"cone_{name}"] = [keep, tot, keep / tot]
        res[f"spread_{name}"] = dict(
            sigma_a_over_a=float(np.std(f["a"]) / np.mean(f["a"])),
            mean_e=float(np.mean(f["e"])),
            varpi_resultant=float(np.abs(np.mean(np.exp(1j * f["varpi"])))))
        rng = np.random.default_rng(13)
        U, V, W = binet(f); Np = len(U)
        probes = rng.integers(0, Np, (Np, 16))
        inside = ((U[probes] - U[:, None])**2
                  <= (V[probes] - V[:, None])**2 + (W[probes] - W[:, None])**2)
        res[f"probek16_{name}"] = float(np.mean(inside))
    res["plane_residual_cloud"] = plane_residual(make_cloud(4000, SIGMA, 11))

    # ---------- truth + certificates on the cloud: N scaling at mixed age, plus ages
    for (N, age, H) in [(300, 256, 32), (1000, 0.25, 2), (1000, 4, 8), (1000, 256, 32),
                        (4000, 256, 32)]:
        f = make_cloud(N, SIGMA, 21 + N)
        t0, tH = age * TWO_PI, (age + H) * TWO_PI
        enc_P, nev = at_P_truth(f, t0, tH)
        wpairs = window_pair_count(f, t0, tH)
        Ts = f["T"]; Tbar = float(np.mean(Ts))
        enc_by_w = {}
        for (i, j, tc, d) in enc_P:
            enc_by_w.setdefault(int((tc - t0) // Tbar), []).append((i, j, tc))
        miss_k4 = 0; ranks_at_sort = []
        for w, lst in sorted(enc_by_w.items()):
            pos = pos_of(f, t0 + w * Tbar, N)
            for (i, j, tc) in lst:
                r = crank(i, j, pos, N)
                ranks_at_sort.append(r)
                if r > 4:
                    miss_k4 += 1
        rng = np.random.default_rng(5)
        samp = ([enc_P[x] for x in rng.choice(len(enc_P), size=min(300, len(enc_P)), replace=False)]
                if enc_P else [])
        rank_at_conj = [crank(i, j, pos_of(f, tc, N), N) for (i, j, tc, d) in samp]
        still = {dd: 0 for dd in (Tbar / 8, Tbar / 4, Tbar / 2, Tbar)}
        for (i, j, tc, d) in samp:
            for dd in still:
                if crank(i, j, pos_of(f, tc - dd, N), N) <= 4:
                    still[dd] += 1
        cntQ, nsampQ, all_pairs, _ = at_Q_truth_sample(f, t0, tH, 20000)
        estQ = cntQ * all_pairs / nsampQ
        seQ = (all_pairs / nsampQ) * np.sqrt(max(cntQ, 1) * (1 - max(cntQ, 1) / nsampQ))
        res[f"cloud_N{N}_age{age}"] = dict(
            encounters_at_P=len(enc_P), events=nev, window_pairs=wpairs,
            work_per_encounter_coarrival=(wpairs / len(enc_P) if enc_P else None),
            encounters_at_Q_est=float(estQ), at_Q_se=float(seQ),
            phase_rank4_misses=miss_k4, n_ranked=len(enc_P),
            miss_fraction=(miss_k4 / len(enc_P) if enc_P else None),
            rank_at_sort_max=(int(np.max(ranks_at_sort)) if ranks_at_sort else None),
            rank_at_conj_max=(int(np.max(rank_at_conj)) if rank_at_conj else None),
            rank_at_conj_med=(float(np.median(rank_at_conj)) if rank_at_conj else None),
            churn_still_within4={f"{k:.4f}": v / max(len(samp), 1) for k, v in still.items()})
        print(f"cloud_N{N}_age{age}", json.dumps(res[f"cloud_N{N}_age{age}"]), flush=True)

    # ---------- formation control: per-orbit cadence misses must be zero
    ff = make_formation(1000)
    enc, nev = at_P_truth_generic(ff, TWO_PI, 34 * TWO_PI)
    pos = pos_of(ff, TWO_PI, 1000)
    res["formation_ctrl"] = dict(
        encounters=len(enc),
        rank4_misses=sum(1 for (i, j, tc, d) in enc if crank(i, j, pos, 1000) > 4),
        max_rank=(max(crank(i, j, pos, 1000) for (i, j, tc, d) in enc) if enc else None))

    # ---------- P7 validation: analytic windowed d_min vs direct Kepler propagation
    f = make_cloud(1000, SIGMA, 31)
    enc, _ = at_P_truth(f, 256 * TWO_PI, 258 * TWO_PI)
    rng = np.random.default_rng(3)
    errs = []
    for (i, j, tc, d) in [enc[x] for x in rng.choice(len(enc), size=min(250, len(enc)), replace=False)]:
        tg = tc + np.linspace(-TAUC, TAUC, 121)
        xi = xy_of(f, i, tg); xj = xy_of(f, j, tg)
        dmin = float(np.min(np.hypot(xi[0] - xj[0], xi[1] - xj[1])))
        errs.append(abs(dmin - d) / max(d, 1e-12))
    res["p7_validation"] = dict(n=len(errs), max_rel_err=float(np.max(errs)),
                                p95=float(np.percentile(errs, 95)))

    pairs1e6 = 1e6 * (1e6 - 1) / 2
    res["tier1_setup_1e6"] = dict(
        pairs=pairs1e6, core_s_at_2p5us=pairs1e6 * 2.5e-6, core_s_at_24us=pairs1e6 * 24e-6,
        gib_at_80B=pairs1e6 * 80 / 2**30)
    res["runtime_s"] = time.time() - t_start
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "results.json"), "w") as fh:
        json.dump(res, fh, indent=1, default=str)
    print(json.dumps(res, indent=1, default=str))
