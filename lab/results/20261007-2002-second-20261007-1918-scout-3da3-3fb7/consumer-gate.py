#!/usr/bin/env python3
"""Does one far-field news update per source orbit keep a real consumer's behaviour?

The scout run (20261007-1918-scout-3da3) claimed OC#50's growing light cone is a
representation artifact: hierarchical quantum-gated news bounds causal traffic at
the granularity cap. Its checker showed the quantum gate is 100% saturated at
eps=1e-6 (uncapped requirement 1.4e12/unit ~= naive pairwise), so the whole bound
rests on the CAP: one update per source orbit per consumer is behaviourally
enough. That cap was asserted, never measured. This run measures it.

Scene (a B12-class gate scene outside the crates; the plane cannot be wired
without editing them). The falsifier's own model: a Mestel galaxy with a
dominant smooth background M_enc(r)=r (v_c=1 everywhere, Phi=ln r; the derived
map, free to every consumer, principle 3) and a star component (MSTAR=0.5,
Sigma ~ 1/r on [0.2,1.0], 256 stars) whose mutual softened gravity deviates each
star from its background geodesic — that deviation is exactly the candidate's
"news". This is also the engine's architecture: analytic generators in the
dominant field with residual kicks (H0190).

Consumers are test particles at r=1.3 and r=1.8, OUTSIDE the star disk: the
star field they feel is far field (no near encounters, no encounters-tier
chaos), which is exactly the regime the news tier owns. Stars are integrated
with full news (the truth): background + softened mutual gravity. Riders:

  REF   full news: exact instantaneous star states every step (reference).
  FLOOR full news, initial angle +1e-6 rad: the scene's own chaos floor.
  G1    far news every source orbit (the code's cap, nu=1); the rider
        propagates each published source state along its background geodesic
        (the map) and re-bases it at each news event.
  G8    far news every T/8 (the dossier's stated nu=8), same map.
  K16   far news every 16 orbits (kill control: must break, else VOID).
  DR1   far news every orbit, LINEAR extrapolation x_pub + v_pub*dt (DIS
        first-order dead reckoning on the raw state; the naive reading).

Gates (pre-registered in predictions.md; behaviours and statistics, never
trajectory identity):
  Separation S_cfg(t) = |x_cfg - x_REF| against the floor S_FLOOR(t).
  PASS(cfg) iff, median over seeds at BOTH radii:
    (a) S_cfg(T)/S_FLOOR(T) <= 3,
    (b) log-log slope of S_cfg over t>2 <= floor slope + 0.2,
    (c) radial drift |mean_{last quarter} r - r_c|/r_c <= max(0.3, 3x REF's).
  K16 must FAIL at least one of (a)-(c); DR1 is expected to fail catastrophically.

Also measured each sample: force error at the REF position |a_cfg-a_REF|/|a_REF|
(the equivalent eps the news scheme commits, independent of rider divergence),
the far-field share of the force, and the stars' residual-velocity diffusion
sigma_dv (to scale to engine populations: sigma_dv^2 ~ Sigma*m; at fixed total
mass sigma_dv ~ N^-1/2; staleness position error delta ~ sigma_dv*dt^{3/2} so
nu_req ~ sigma_dv^{2/3} ~ N^{-1/3}).
"""
import json
import numpy as np

# ---------------- configuration ----------------
NSTAR, MSTAR = 256, 0.5
R0, R1 = 0.2, 1.0
EPS2 = 0.02 ** 2
DT = 1.0 / 64.0
N_ORBIT = 10.0                   # consumer orbits at r=1.3
RADII = (1.3, 1.8)               # consumers outside [R0,R1]: far-field regime
D_NEAR = 0.25                    # encounters-tier skin (guards outward-scattered stars)
SEEDS = (11, 22, 33, 44, 55)
WARM = 0.15                      # star dispersion fraction of v_c=1
NU_CFGS = {"G1": 1.0, "G8": 8.0, "K16": 1.0 / 16.0}
DR_TAG = "DR1"                   # linear dead reckoning, nu=1 schedule
RECORD_EVERY = 4                 # steps between samples
GATE_TAGS = ("G1", "G8", "K16", DR_TAG, "NN")


class Background:
    """Mestel galaxy: M_enc(r)=r, |a|=1/r inward, Phi=ln r, v_c=1."""

    def acc(self, x):
        r = np.maximum(np.hypot(x[:, 0], x[:, 1]), 1e-6)
        return -x / (r * r)[:, None]

    def acc1(self, x):
        r = max(np.hypot(x[0], x[1]), 1e-6)
        return -x / (r * r)

    def pot(self, r):
        return np.log(np.maximum(r, 1e-6))


def pairwise(xs, ms, xt, eps2, self_force=False):
    dx = xs[None, :, :] - xt[:, None, :]
    d2 = (dx * dx).sum(-1) + eps2
    if self_force:
        np.fill_diagonal(d2, np.inf)
    inv3 = 1.0 / (d2 * np.sqrt(d2))
    return (dx * inv3[:, :, None] * ms[None, :, None]).sum(1)


def run_seed(seed, bg, nstar=NSTAR, mstar=MSTAR, n_orbit=None, rec=None):
    rng = np.random.default_rng(seed)
    n_orbit = n_orbit if n_orbit is not None else N_ORBIT
    rec = rec or RECORD_EVERY
    u = rng.random(nstar)
    rs = R0 * (R1 / R0) ** u
    th = rng.random(nstar) * 2 * np.pi
    xs = np.stack([rs * np.cos(th), rs * np.sin(th)], 1)
    tang = np.stack([-np.sin(th), np.cos(th)], 1)
    vs = tang + WARM * rng.standard_normal((nstar, 2))   # v_c = 1
    ms = np.full(nstar, mstar / nstar)
    per = 2 * np.pi * rs                                 # source orbit (v_c=1)

    tags = ["REF", "FLOOR"] + list(NU_CFGS) + [DR_TAG, "NN"]
    meta, xr, vr = [], [], []
    for rc in RADII:
        for tag in tags:
            ang = 1e-6 if tag == "FLOOR" else 0.0
            xr.append(rc * np.array([np.cos(ang), np.sin(ang)]))
            vr.append(np.array([-np.sin(ang), np.cos(ang)]))
            meta.append(tag)
    xr, vr = np.array(xr), np.array(vr)
    NR = len(xr)

    gpos = {k: xs.copy() for k in NU_CFGS}
    gvel = {k: vs.copy() for k in NU_CFGS}
    nxt = {k: per / nu for k, nu in NU_CFGS.items()}
    dpos, dvel = xs.copy(), vs.copy()
    dnxt = per.copy()
    dt_pub = np.zeros(nstar)

    t_end = n_orbit * 2 * np.pi * RADII[0]
    nsteps = int(t_end / DT)
    t = 0.0
    ast = pairwise(xs, ms, xs, EPS2, self_force=True) + bg.acc(xs)

    def rider_acc(t_now):
        out = np.zeros((NR, 2))
        dr1_far = dpos + dvel * (t_now - dt_pub)[:, None]
        for i in range(NR):
            tag = meta[i]
            if tag in ("REF", "FLOOR"):
                out[i] = pairwise(xs, ms, xr[i][None, :], EPS2)[0]
                continue
            if tag == "NN":
                d = np.hypot(xs[:, 0] - xr[i, 0], xs[:, 1] - xr[i, 1])
                near = d < D_NEAR
                out[i] = pairwise(xs[near], ms[near], xr[i][None, :], EPS2)[0]
                continue
            d = np.hypot(xs[:, 0] - xr[i, 0], xs[:, 1] - xr[i, 1])
            near = d < D_NEAR
            far_src = dr1_far if tag == DR_TAG else gpos[tag]
            src = np.where(near[:, None], xs, far_src)
            out[i] = pairwise(src, ms, xr[i][None, :], EPS2)[0]
        return out

    samp = {k: [] for k in ("t", "x", "E", "L", "r")}
    samp_fg, far_share, vs_hist = [], [], []

    nsteps_loop = nsteps  # (loop begins below)
    for n in range(nsteps):
        for k in NU_CFGS:
            hit = t >= nxt[k] - 0.5 * DT
            if hit.any():
                gpos[k][hit] = xs[hit]
                gvel[k][hit] = vs[hit]
                nxt[k] = np.where(hit, nxt[k] + per / NU_CFGS[k], nxt[k])
        hit = t >= dnxt - 0.5 * DT
        if hit.any():
            dpos[hit] = xs[hit]
            dvel[hit] = vs[hit]
            dt_pub[hit] = t
            dnxt = np.where(hit, dnxt + per, dnxt)

        # stars: truth = background geodesic + softened mutual gravity
        xs = xs + vs * DT + 0.5 * ast * DT * DT
        ast_new = pairwise(xs, ms, xs, EPS2, self_force=True) + bg.acc(xs)
        vs += 0.5 * (ast + ast_new) * DT
        ast = ast_new

        # geodesic ghosts: published states propagated on the background map
        for k in NU_CFGS:
            g = gpos[k]
            ga = bg.acc(g)
            gpos[k] = g + gvel[k] * DT + 0.5 * ga * DT * DT
            ga2 = bg.acc(gpos[k])
            gvel[k] = gvel[k] + 0.5 * (ga + ga2) * DT

        aall = rider_acc(t) + bg.acc(xr)
        xr = xr + vr * DT + 0.5 * aall * DT * DT
        aall2 = rider_acc(t + DT) + bg.acc(xr)
        vr += 0.5 * (aall + aall2) * DT

        t += DT
        if n % rec == 0:
            r = np.hypot(xr[:, 0], xr[:, 1])
            samp["t"].append(t)
            samp["x"].append(xr.copy())
            samp["r"].append(r)
            samp["E"].append(0.5 * (vr * vr).sum(1) + bg.pot(r))
            samp["L"].append(xr[:, 0] * vr[:, 1] - xr[:, 1] * vr[:, 0])
            fg = {}
            for rc_i, rc in enumerate(RADII):
                i_ref = rc_i * len(tags)
                xref = xr[i_ref]
                a_ref = pairwise(xs, ms, xref[None, :], EPS2)[0] + bg.acc1(xref)
                g0 = float(np.hypot(*a_ref))
                for tag in GATE_TAGS:
                    if tag == "NN":
                        d2 = np.hypot(xs[:, 0] - xref[0], xs[:, 1] - xref[1])
                        near2 = d2 < D_NEAR
                        a_nn = pairwise(xs[near2], ms[near2], xref[None, :], EPS2)[0]
                        a_cfg = a_nn + bg.acc1(xref)
                    else:
                        d = np.hypot(xs[:, 0] - xref[0], xs[:, 1] - xref[1])
                        near = d < D_NEAR
                        if tag == DR_TAG:
                            far_src = dpos + dvel * (t - dt_pub)[:, None]
                        else:
                            far_src = gpos[tag]
                        src = np.where(near[:, None], xs, far_src)
                        a_cfg = pairwise(src, ms, xref[None, :], EPS2)[0] + bg.acc1(xref)
                    fg[f"{tag}@{rc}"] = float(np.hypot(*(a_cfg - a_ref))) / max(g0, 1e-12)
            samp_fg.append(fg)
            fs = []
            for rc_i in range(len(RADII)):
                i_ref = rc_i * len(tags)
                d = np.hypot(xs[:, 0] - xr[i_ref, 0], xs[:, 1] - xr[i_ref, 1])
                af = pairwise(xs[d >= D_NEAR], ms[d >= D_NEAR],
                              xr[i_ref][None, :], EPS2)[0]
                g0 = float(np.hypot(aall[i_ref, 0], aall[i_ref, 1]))
                fs.append(float(np.hypot(*af)) / max(g0, 1e-12))
            far_share.append(fs)
        if n % 32 == 0:
            rr = np.maximum(np.hypot(xs[:, 0], xs[:, 1]), 1e-9)
            vs_hist.append(vs - np.stack([-xs[:, 1], xs[:, 0]], 1) / rr[:, None])

    return dict(tags=tags, meta=meta, radii=list(RADII),
                t=np.array(samp["t"]), x=np.array(samp["x"]),
                E=np.array(samp["E"]), L=np.array(samp["L"]), r=np.array(samp["r"]),
                fg=samp_fg, far_share=np.array(far_share), vs_hist=vs_hist)


def metrics(res):
    out = {}
    x, E, L, r, t = res["x"], res["E"], res["L"], res["r"], res["t"]
    nt = len(res["tags"])
    late = t > 2.0
    q = max(len(r) // 4, 1)
    for rc_i, rc in enumerate(res["radii"]):
        i_ref = rc_i * nt
        ref_x = x[:, i_ref]
        floor_i = rc_i * nt + 1
        S_floor = np.hypot(*(x[:, floor_i] - ref_x).T)
        floor_sl = np.polyfit(np.log(t[late]),
                              np.log(np.maximum(S_floor[late], 1e-300)), 1)[0]
        out[f"floor@{rc}"] = dict(S_end=float(S_floor[-1]), slope=float(floor_sl))
        for k, tag in enumerate(res["tags"]):
            i = rc_i * nt + k
            e = (E[:, i] - E[0, i]) / abs(E[0, i])
            d = dict(M_E=float(np.abs(e).max()),
                     M_L=float(np.abs((L[:, i] - L[0, i]) / abs(L[0, i])).max()),
                     r_exc=float(np.abs(r[:, i] - res["radii"][rc_i]).max()),
                     r_mean_last=float(np.mean(r[-3 * q:, i])),
                     r_rms_last=float(np.sqrt(np.mean(
                         (r[-3 * q:, i] - np.mean(r[-3 * q:, i])) ** 2))))
            if tag in GATE_TAGS:
                S = np.hypot(*(x[:, i] - ref_x).T)
                sl = np.polyfit(np.log(t[late]),
                                np.log(np.maximum(S[late], 1e-300)), 1)[0]
                d.update(S_end=float(S[-1]), slope=float(sl),
                         S_ratio_end=float(S[-1] / max(S_floor[-1], 1e-300)),
                         slope_excess=float(sl - floor_sl))
            out[f"{tag}@{rc}"] = d
        for tag in GATE_TAGS:
            v = np.array([s[f"{tag}@{rc}"] for s in res["fg"]])
            out[f"{tag}@{rc}"]["fg_med"] = float(np.median(v))
            out[f"{tag}@{rc}"]["fg_p90"] = float(np.percentile(v, 90))
        out[f"far_share@{rc}"] = float(np.median(res["far_share"][:, rc_i]))
    vh = res["vs_hist"]
    dvs = []
    for a in range(len(vh) - 16):
        dv = vh[a + 16] - vh[a]
        dvs.append((dv * dv).sum(1).mean())
    out["star_dv2_per_16units"] = float(np.median(dvs))
    return out


def main():
    import sys
    seeds = SEEDS
    nstar = NSTAR
    if len(sys.argv) > 1:
        nstar = int(sys.argv[1])
    if len(sys.argv) > 2:
        seeds = tuple(int(s) for s in sys.argv[2].split(","))
    bg = Background()
    all_res = {}
    for seed in seeds:
        all_res[seed] = metrics(run_seed(seed, bg, nstar=nstar))
        print(f"seed {seed} done", flush=True)
    agg = {}
    for key in all_res[seeds[0]]:
        if key == "star_dv2_per_16units" or key.startswith("far_share"):
            agg[key] = float(np.median([all_res[s][key] for s in seeds]))
        else:
            agg[key] = {kk: float(np.median([all_res[s][key][kk] for s in seeds]))
                        for kk in all_res[seeds[0]][key]}
    verdicts = {}
    for rc in RADII:
        fl = agg[f"floor@{rc}"]
        ref_mean = agg[f"REF@{rc}"]["r_mean_last"]
        ref_rms = agg[f"REF@{rc}"]["r_rms_last"]
        for tag in ("FLOOR",) + GATE_TAGS:
            m = agg[f"{tag}@{rc}"]
            mu_gate = abs(m["r_mean_last"] - ref_mean) / rc <= 0.05
            sg_gate = abs(m["r_rms_last"] - ref_rms) / rc <= 0.05
            extra = dict(mu_delta=abs(m["r_mean_last"] - ref_mean) / rc,
                         sg_delta=abs(m["r_rms_last"] - ref_rms) / rc)
            if tag in GATE_TAGS:
                extra.update(S_ratio_end=m.get("S_ratio_end"),
                             slope_excess=m.get("slope_excess"),
                             floor_slope=fl["slope"])
            verdicts[f"{tag}@{rc}"] = dict(
                **extra, mu_gate=bool(mu_gate), sg_gate=bool(sg_gate),
                gate_pass=bool(mu_gate and sg_gate))
    out = dict(nstar=nstar, seeds=list(seeds),
               per_seed={str(s): all_res[s] for s in seeds}, median=agg,
               verdicts=verdicts,
               kill_control_failed=verdicts[f"K16@{RADII[0]}"]["gate_pass"] is False)
    fn = f"consumer-gate-out-n{nstar}-{'x'.join(str(s) for s in seeds)}.json"
    with open(fn, "w") as f:
        json.dump(out, f, indent=1)
    slim = {"median": agg, "verdicts": verdicts,
            "kill_control_failed": out["kill_control_failed"]}
    print(json.dumps(slim, indent=1))


if __name__ == "__main__":
    main()
