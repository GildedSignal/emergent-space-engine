#!/usr/bin/env python3
"""Per-kick certificate churn at 1e9-scale cell occupancy (scout run fbf9).

Question (encounters od 1, cd3b): after one belt-quantum kick, how many pair
certificates must the encounter tier re-check, vs cell occupancy n at fixed
1e9-belt density? fe6b's structure pays 0.0346*n pairs per kicked body; the
kinetic/Verlet-skin treatment pays only what the slack geometry forces.

Model: planar 2-body Kepler on the shipped scenario's constants (belt a in
[2,3) AU, e Rayleigh 0.07 = the ladder belt's scale, reach B = 5e5 m from
cd3b, interval = P(2.5 AU)/4.43 = 28141.5 game-s, horizon = 8 intervals).
Arming = the shipped tier's Phase-A shape: armed iff a mean-longitude meeting
lands in the window at a crossing longitude where the radial curves are within
B. r(lambda) = a(1 - e cos(lambda - w)) (mean-longitude radial model; the
brute-force control uses the same model, so it validates the synodic/arc
arithmetic, not the radial model). Units: SI Kepler seconds throughout; the
doll's clock factor cancels in every ratio reported.

Kicks are applied at a random anomaly; pre and post element sets are taken at
that same anomaly, so pre/post armed sets differ by the kick only.

Arms: A dilute cells n = 1e2/1e3/1e4 at fixed density (+ the wide-band live
anchor), B brute-force soundness control (amplified reach), C no-margin
negative control, D concentration (fleet-class) control. Prints a table,
writes out.json.
"""
import json
import numpy as np

AU = 1.495978707e11
GM = 1.32712440018e20
B = 5e5                     # conjunction reach [m] (cd3b)
A_C = 2.5 * AU
P0 = 2 * np.pi * np.sqrt(A_C**3 / GM)
INTERVAL = P0 / 4.43        # the belt's game interval
H_INT = 8.0
H = H_INT * INTERVAL
RHO_AU = 1e9 / (np.pi * (3**2 - 2**2))   # bodies per AU^2 of annulus
TWO_PI = 2 * np.pi

rng = np.random.default_rng(20261018)


def wrap(x):
    return (x + np.pi) % TWO_PI - np.pi


def make_cell(n, seed, width=None, e_scale=0.07, shared_a=False, lam_sigma=None):
    r = np.random.default_rng(seed)
    if width is None:
        width = n / (RHO_AU * 2 * np.pi * 2.5)          # AU, at fixed density
    a = np.full(n, A_C) if shared_a else A_C + (r.random(n) - 0.5) * width * AU
    e = np.minimum(r.rayleigh(e_scale, n), 0.4)
    w = r.random(n) * TWO_PI
    lam = wrap(r.normal(0.0, lam_sigma, n)) if lam_sigma is not None else r.random(n) * TWO_PI
    nn = np.sqrt(GM / a**3)
    return dict(a=a, e=e, w=w, lam=lam, nn=nn)


def at_anomaly(bd, i, f):
    """Elements of body i with its mean longitude advanced to true anomaly f."""
    a, e, w = float(bd["a"][i]), float(bd["e"][i]), float(bd["w"][i])
    E = 2 * np.arctan2(np.sqrt(1 - e) * np.sin(f / 2), np.sqrt(1 + e) * np.cos(f / 2))
    M = E - e * np.sin(E)
    return dict(a=a, e=e, w=w, lam=float(wrap(w + M)), nn=float(np.sqrt(GM / a**3)))


def kick_at(bd, i, dv_rel, r):
    """Kick body i by dv = dv_rel*|v| at a random anomaly. Returns (pre, post)
    element dicts at that same anomaly, so pre/post differ by the kick only."""
    f = r.random() * TWO_PI
    pre = at_anomaly(bd, i, f)
    a, e, w = pre["a"], pre["e"], pre["w"]
    p = a * (1 - e * e)
    rr = p / (1 + e * np.cos(f))
    th = w + f
    h = np.sqrt(GM * p)
    vr = GM / h * e * np.sin(f)
    vt = GM / h * (1 + e * np.cos(f))
    pos = np.array([rr * np.cos(th), rr * np.sin(th)])
    vel = np.array([vr * np.cos(th) - vt * np.sin(th), vr * np.sin(th) + vt * np.cos(th)])
    dv = dv_rel * np.linalg.norm(vel)
    ang = r.random() * TWO_PI
    vel = vel + dv * np.array([np.cos(ang), np.sin(ang)])
    rn = np.linalg.norm(pos)
    v2 = float(vel @ vel)
    a2 = 1.0 / (2.0 / rn - v2 / GM)
    rv = float(pos @ vel)
    ev = ((v2 - GM / rn) * pos - rv * vel) / GM
    e2 = float(np.linalg.norm(ev))
    w2 = float(np.arctan2(ev[1], ev[0]))
    f2 = th - w2
    E2 = 2 * np.arctan2(np.sqrt(max(1 - e2, 0.0)) * np.sin(f2 / 2),
                        np.sqrt(1 + e2) * np.cos(f2 / 2))
    M2 = E2 - e2 * np.sin(E2)
    return pre, dict(a=a2, e=e2, w=w2, lam=float(wrap(w2 + M2)),
                     nn=float(np.sqrt(GM / a2**3)))


def arm(i_el, j_el, t0, t1, reach=B, kmax=64):
    """Phase-A arming of scalar body i vs arrays j. Returns (armed, due_first_meeting);
    due = first meeting at/after t0 (nan beyond 1e7 intervals, or exact co-orbitals)."""
    dlam = wrap(i_el["lam"] - j_el["lam"])
    dn = i_el["nn"] - j_el["nn"]
    nj = len(dlam)
    armed = np.zeros(nj, bool)
    due = np.full(nj, np.nan)
    live = dn != 0.0
    if live.any():
        idx = np.where(live)[0]
        d_l, n_l = dlam[live], dn[live]
        lo = (n_l * t0 + d_l) / TWO_PI
        hi = (n_l * t1 + d_l) / TWO_PI
        klo = np.ceil(np.minimum(lo, hi)).astype(int)
        khi = np.floor(np.maximum(lo, hi)).astype(int)
        khi = np.minimum(khi, klo + kmax - 1)
        for k in range(int(klo.min()), int(khi.max()) + 1):
            m = (k >= klo) & (k <= khi)
            if not m.any():
                continue
            t = (-d_l[m] + TWO_PI * k) / n_l[m]
            th = wrap(i_el["lam"] + i_el["nn"] * t)
            bmiss = np.abs(
                i_el["a"] * (1 - i_el["e"] * np.cos(th - i_el["w"]))
                - j_el["a"][idx[m]] * (1 - j_el["e"][idx[m]] * np.cos(th - j_el["w"][idx[m]])))
            sel = idx[m][bmiss <= reach]
            armed[sel] = True
        # first meeting at/after t0 (for due-moves):
        k0 = np.where(n_l > 0, np.ceil((n_l * t0 + d_l) / TWO_PI),
                      np.floor((n_l * t0 + d_l) / TWO_PI))
        tf = (-d_l + TWO_PI * k0) / n_l
        tf = np.where(tf < t0, tf + TWO_PI / np.abs(n_l), tf)
        ok = (tf >= t0) & ((tf - t0) < 1e7 * INTERVAL)
        due[idx[ok]] = tf[ok]
    if (~live).any():
        # standing (shared a): reachable iff |da| <= C + B and phases inside the 2B/a band
        da = i_el["a"] - j_el["a"][~live]
        Ci = i_el["a"] * i_el["e"] * np.exp(1j * i_el["w"])
        Cj = j_el["a"][~live] * j_el["e"][~live] * np.exp(1j * j_el["w"][~live])
        C = np.abs(Ci - Cj)
        armed[~live] = (np.abs(da) <= C + reach) & (np.abs(dlam[~live]) <= 2 * reach / i_el["a"])
    return armed, due


def _clean_self(armed, due, i):
    armed[i] = False
    due[i] = np.nan


def run_dilute(n, seed, dv_list, n_kicks=None):
    bd = make_cell(n, seed)
    out = {"n": n, "width_AU": n / (RHO_AU * 2 * np.pi * 2.5)}
    n_kicks = n_kicks or min(n, 200)
    targets = rng.choice(n, n_kicks, replace=False)
    for dv in dv_list:
        r = np.random.default_rng(seed + int(-np.log2(dv) * 100))
        f_on = f_off = band = armed_per = 0.0
        dmed, dinh = [], []
        for i in targets:
            pre, post = kick_at(bd, i, dv, r)
            a0, d0 = arm(pre, bd, 0.0, H)
            a1, d1 = arm(post, bd, 0.0, H)
            _clean_self(a0, d0, i)
            _clean_self(a1, d1, i)
            f_on += int(np.sum(a1 & ~a0))
            f_off += int(np.sum(~a1 & a0))
            armed_per += int(a0.sum())
            band += int(np.sum(np.isfinite(d0) & (d0 < (H_INT + 2) * INTERVAL)))
            mm = np.isfinite(d0) & np.isfinite(d1)
            if mm.any():
                dmed.append(float(np.median(np.abs(d1[mm] - d0[mm]))) / INTERVAL)
                inh = mm & (d0 < 2 * H)
                if inh.any():
                    dinh.append(float(np.median(np.abs(d1[inh] - d0[inh]))) / INTERVAL)
        out[f"dv_2e{int(round(-np.log2(dv)))}"] = dict(
            kicks=n_kicks, candidates_per_kick=n - 1,
            armed_per_body=armed_per / n_kicks,
            flips_on_per_kick=f_on / n_kicks, flips_off_per_kick=f_off / n_kicks,
            near_band_per_body=band / n_kicks,
            due_move_median_intervals=np.median(dmed) if dmed else None,
            due_move_inhorizon_intervals=np.median(dinh) if dinh else None)
    return out


def run_live_anchor(seed, n_bodies=40, n_part=100000, dv_list=(2**-23, 2**-20, 2**-17)):
    """Wide-band partners at true belt density: the real armed set and its kick churn."""
    r = np.random.default_rng(seed + 7)
    span = 0.35 * AU
    scale = 1e9 * (2 * span / AU) / n_part       # sampled -> true partner count
    res = {}
    for dv in dv_list:
        armed_tot = f_on = f_off = 0.0
        d_inh, d_all = [], []
        for _ in range(n_bodies):
            i_arr = dict(a=np.array([A_C]), e=np.array([min(r.rayleigh(0.07), 0.4)]),
                         w=np.array([r.random() * TWO_PI]), lam=np.array([r.random() * TWO_PI]))
            i_arr["nn"] = np.sqrt(GM / i_arr["a"]**3)
            aj = float(i_arr["a"][0]) + (r.random(n_part) - 0.5) * 2 * span
            j_el = dict(a=aj, e=np.minimum(r.rayleigh(0.07, n_part), 0.4),
                        w=r.random(n_part) * TWO_PI, lam=r.random(n_part) * TWO_PI)
            j_el["nn"] = np.sqrt(GM / aj**3)
            pre, post = kick_at(i_arr, 0, dv, r)
            a0, d0 = arm(pre, j_el, 0.0, H)
            a1, d1 = arm(post, j_el, 0.0, H)
            armed_tot += a0.sum() * scale
            f_on += int(np.sum(a1 & ~a0)) * scale
            f_off += int(np.sum(~a1 & a0)) * scale
            mm = np.isfinite(d0) & np.isfinite(d1) & (d0 < 2 * H)
            if mm.any():
                d_inh.append(float(np.median(np.abs(d1[mm] - d0[mm]))) / INTERVAL)
            m2 = np.isfinite(d0) & np.isfinite(d1)
            if m2.any():
                d_all.append(float(np.median(np.abs(d1[m2] - d0[m2]))) / INTERVAL)
        res[f"dv_2e{int(round(-np.log2(dv)))}"] = dict(
            armed_per_body=armed_tot / n_bodies,
            flips_on_per_kick=f_on / n_bodies, flips_off_per_kick=f_off / n_bodies,
            due_move_inhorizon_intervals=np.median(d_inh) if d_inh else None,
            due_move_median_intervals=np.median(d_all) if d_all else None)
    return dict(seed=seed, bodies=n_bodies, partners_each=n_part, arms=res)


def brute_validation(seed=4242, N=80, reach_val=0.02 * AU, steps=9000):
    r = np.random.default_rng(seed)
    a = (2.3 + 0.4 * r.random(N)) * AU
    e = np.minimum(r.rayleigh(0.07, N), 0.4)
    w = r.random(N) * TWO_PI
    lam0 = r.random(N) * TWO_PI
    nn = np.sqrt(GM / a**3)
    T = 2 * P0
    tgrid = np.linspace(0, T, steps)
    lam = lam0[:, None] + nn[:, None] * tgrid[None, :]
    rad = a[:, None] * (1 - e[:, None] * np.cos(lam - w[:, None]))
    events = 0
    missed = 0
    bd = dict(a=a, e=e, w=w, lam=lam0, nn=nn)
    armed_mat = np.zeros((N, N), bool)
    for i in range(N):
        i_el = {k: bd[k][i] for k in bd}
        ar, _ = arm(i_el, bd, 0.0, T, reach=reach_val)
        ar[i] = False
        armed_mat[i] = ar
    for i in range(N):
        du = np.unwrap(lam[i] - lam, axis=1)
        cross = np.zeros_like(du, bool)
        cross[:, :-1] = np.sign(du[:, :-1]) != np.sign(du[:, 1:])
        js, ks = np.where(cross)
        for j, k in zip(js, ks):
            if j <= i:
                continue
            f1, f2 = du[j, k], du[j, k + 1]
            al = abs(f1) / (abs(f1) + abs(f2))
            lams = lam[i, k] + (lam[i, k + 1] - lam[i, k]) * al
            bmiss = abs(a[i] * (1 - e[i] * np.cos(lams - w[i]))
                        - a[j] * (1 - e[j] * np.cos(lams - w[j])))
            if bmiss <= reach_val:
                events += 1
                if not armed_mat[i, j]:
                    missed += 1
    return dict(events=events, closed_form_armed_pairs=int(armed_mat.sum()),
                missed_by_closed_form=missed,
                note="reach amplified to 0.02 AU so events exist at N=80")


def negative_control(seed=4242, N=300, reach_val=0.02 * AU, kicks=100):
    """No-margin schedule: horizon == rebuild window [0,T]; kicks at T/2 are not
    re-armed; events newly in-window after the kick are lost."""
    r = np.random.default_rng(seed + 1)
    bd = make_cell(N, seed + 99, width=0.4)
    T = 2 * P0
    lost = {}
    for dv in (2**-17, 2**-14):
        L = 0
        for i in rng.choice(N, kicks, replace=False):
            pre, post = kick_at(bd, i, dv, r)
            a_pre, _ = arm(pre, bd, T / 2, T, reach=reach_val)
            a_post, _ = arm(post, bd, T / 2, T, reach=reach_val)
            a_pre[i] = a_post[i] = False
            L += int(np.sum(a_post & ~a_pre))
        lost[f"dv_2e{int(round(-np.log2(dv)))}"] = L
    return dict(kicks=kicks, events_lost_no_margin=lost)

def run_concentration(seed=31, n=2000, dv=2**-23):
    """Fleet-class control: shared (a, e, w) keys ring, phases concentrated
    (sigma_lambda = 5e-6 rad). The kick epoch is shared: partners' longitudes are
    advanced by the same n*dt, so relative phases (the standing structure) are
    preserved exactly. Standing pairs here are the dwell class: the binary armed
    model has no dwell, so dissolution flips are an upper bound (caveat in the
    dossier)."""
    bd = make_cell(n, seed, shared_a=True)
    bd["e"][:] = 0.01
    bd["w"][:] = 0.7
    bd["lam"][:] = wrap(0.3 + np.random.default_rng(seed + 5).normal(0.0, 5e-6, n))
    r = np.random.default_rng(seed + 2)
    targets = rng.choice(n, 50, replace=False)
    a_tot = f_on = f_off = 0.0
    for i in targets:
        f = r.random() * TWO_PI
        # epoch shift from epoch 0 (M0 = lam - w by construction) to anomaly f,
        # applied to everyone (shared n, so relative phases are preserved):
        M0 = float(wrap(bd["lam"][i] - bd["w"][i]))
        Ef = 2 * np.arctan2(np.sqrt(1 - bd["e"][i]) * np.sin(f / 2),
                            np.sqrt(1 + bd["e"][i]) * np.cos(f / 2))
        Mf = Ef - bd["e"][i] * np.sin(Ef)
        dt = (Mf - M0) / bd["nn"][i]
        jd = dict(a=bd["a"], e=bd["e"], w=bd["w"], lam=wrap(bd["lam"] + bd["nn"] * dt),
                  nn=bd["nn"])
        pre = dict(a=float(bd["a"][i]), e=float(bd["e"][i]), w=float(bd["w"][i]),
                   lam=float(wrap(bd["w"][i] + Mf)), nn=float(bd["nn"][i]))
        p = pre["a"] * (1 - pre["e"] ** 2)
        rr = p / (1 + pre["e"] * np.cos(f))
        th = pre["w"] + f
        h = np.sqrt(GM * p)
        vr = GM / h * pre["e"] * np.sin(f)
        vt = GM / h * (1 + pre["e"] * np.cos(f))
        pos = np.array([rr * np.cos(th), rr * np.sin(th)])
        vel = np.array([vr * np.cos(th) - vt * np.sin(th), vr * np.sin(th) + vt * np.cos(th)])
        dvv = dv * np.linalg.norm(vel)
        ang = r.random() * TWO_PI
        vel = vel + dvv * np.array([np.cos(ang), np.sin(ang)])
        rn = np.linalg.norm(pos)
        v2 = float(vel @ vel)
        a2 = 1.0 / (2.0 / rn - v2 / GM)
        rv = float(pos @ vel)
        ev = ((v2 - GM / rn) * pos - rv * vel) / GM
        e2 = float(np.linalg.norm(ev))
        w2 = float(np.arctan2(ev[1], ev[0]))
        f2 = th - w2
        E2 = 2 * np.arctan2(np.sqrt(max(1 - e2, 0.0)) * np.sin(f2 / 2),
                            np.sqrt(1 + e2) * np.cos(f2 / 2))
        M2 = E2 - e2 * np.sin(E2)
        post = dict(a=a2, e=e2, w=w2, lam=float(wrap(w2 + M2)), nn=float(np.sqrt(GM / a2**3)))
        a0, _ = arm(pre, jd, 0.0, H)
        a1, _ = arm(post, jd, 0.0, H)
        a0[i] = a1[i] = False
        a_tot += int(a0.sum())
        f_on += int(np.sum(a1 & ~a0))
        f_off += int(np.sum(~a1 & a0))
    return dict(n=n, dv=dv, kicks=50, standing_per_body=a_tot / 50,
                flips_on_per_kick=f_on / 50, flips_off_per_kick=f_off / 50,
                caveat="binary armed model, no dwell: dissolution flips are an upper bound")


def main():
    res = {}

    def g(x):
        return "none" if x is None else f"{x:.3g}"
    print("== A: dilute cells at 1e9 density (wholesale vs slack-aware) ==")
    res["dilute"] = []
    for n in (100, 1000, 10000):
        o = run_dilute(n, seed=20261018 + n, dv_list=[2**-23, 2**-20])
        res["dilute"].append(o)
        for key, v in o.items():
            if isinstance(v, dict):
                print(f"n={o['n']:>6} W={o['width_AU']:.1e}AU {key}: cand/kick={v['candidates_per_kick']:.0f} "
                      f"armed/body={v['armed_per_body']:.4g} flips/kick={v['flips_on_per_kick'] + v['flips_off_per_kick']:.4g} "
                      f"nearband/body={v['near_band_per_body']:.4g} "
                      f"dmed={g(v['due_move_median_intervals'])} dinh={g(v['due_move_inhorizon_intervals'])}")
    print("== A2: live anchor (wide-band partners at true density) ==")
    res["live_anchor"] = run_live_anchor(5150)
    print(json.dumps(res["live_anchor"], indent=1))
    print("== B: brute-force soundness control ==")
    res["validation"] = brute_validation()
    print(json.dumps(res["validation"], indent=1))
    print("== C: no-margin negative control ==")
    res["negative"] = negative_control()
    print(json.dumps(res["negative"], indent=1))
    print("== D: concentration (fleet-class) control ==")
    res["concentration"] = run_concentration()
    print(json.dumps(res["concentration"], indent=1))
    with open("out.json", "w") as f:
        json.dump(res, f, indent=1)
    print("wrote out.json")


if __name__ == "__main__":
    main()
