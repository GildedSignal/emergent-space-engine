"""Rung r3 ships: handoff metric (100 SOI crossings of the counter-rotating co-orbital
transfer vs a continuous N-body reference) and assist metric (64 flybys).

Transfer: ship on retrograde circular heliocentric orbit r = 1 + 3e-3 AU (70 R_p),
crosses the planet's SOI twice per year. Reference = one continuous adaptive-RK4
(half-step agreement 1e-9) 3-body integration; the doll is re-expressed in the new
doll's frame at each of the reference's crossings and propagated to the next one
(per-segment fidelity: resonant-chaotic divergence of a fully autonomous doll would
otherwise confound the handoff metric; the exponent then tests exactly whether
handoff errors compound).

handoff_energy_growth_exponent = OLS slope of ln|dE_helio| vs handoff index (1..100).
assist_pass_fraction = fraction of flybys with ||dv_doll - dv_ref|| <= 0.01 ||dv_ref||.
"""
import json
import math
import subprocess

import numpy as np

RUN = "./rung3_ships"
D_OFF = 3e-3
G = 39.478417604357434


def run_ref(t_end, tol="1e-9"):
    r = 1.0 + D_OFF
    v = math.sqrt(G/r)
    inp = f"{r:.17g} 0.0 0.0 {-v:.17g}\n"
    out = subprocess.run([RUN, "ref3", str(t_end), tol], input=inp,
                         capture_output=True, text=True, timeout=600)
    cross = []
    for line in out.stdout.split("\n"):
        f = line.split()
        if f and f[0] == "CROSS":
            cross.append(dict(i=int(f[1]), t=float(f[2]), dir=int(f[3]),
                              ship=[float(x) for x in f[4:8]],
                              planet=[float(x) for x in f[8:12]]))
        if f and f[0] == "DONE":
            done = dict(ncross=int(f[1]), t=float(f[2]), eerr=float(f[4]))
    return cross, done


def doll_segments(config, cross):
    """For each reference crossing i, re-express state in the new doll's frame and
    propagate the doll to its own next SOI crossing; record |dE_helio| vs reference
    at crossing i+1."""
    errs, kinds = [], []
    for i in range(len(cross)-1):
        c = cross[i]
        inside = c["dir"] == -1    # dir -1: reference crossed inward -> planet-doll segment next
        kind = "planet" if inside else "star"
        inp = f"{c['t']:.17g} " + " ".join(f"{x:.17g}" for x in c["ship"]) + "\n"
        out = subprocess.run([RUN, "dollseg", config, kind], input=inp,
                             capture_output=True, text=True, timeout=120)
        f = out.stdout.split()
        seg = [float(x) for x in f[1:6]]
        tc, s = seg[0], seg[1:5]
        E_d = 0.5*(s[2]**2+s[3]**2) - G/math.hypot(s[0], s[1])
        cr = cross[i+1]["ship"]
        E_r = 0.5*(cr[2]**2+cr[3]**2) - G/math.hypot(cr[0], cr[1])
        errs.append(abs(E_d - E_r))
        kinds.append(kind)
    return errs, kinds


def flybys(config):
    rng_bs = [1.5*(50.0/1.5)**(k/63.0) for k in range(64)]  # placeholder, replaced by rung sampler
    return rng_bs


def main():
    cross, done = run_ref(26.0)
    assert len(cross) >= 101, f"only {len(cross)} crossings"
    cross = cross[:101]   # 100 handoffs
    print("reference:", done, "crossings kept:", len(cross)-1)

    # numerical convergence of the reference: tol 1e-11 vs 1e-9
    cross2, _ = run_ref(26.0, "1e-11")
    dt = max(abs(a["t"]-b["t"]) for a, b in zip(cross[:101], cross2[:101]))
    dv = max(math.hypot(a["ship"][2]-b["ship"][2], a["ship"][3]-b["ship"][3])
             for a, b in zip(cross[:101], cross2[:101]))
    print(f"reference convergence (tol 1e-9 vs 1e-11): max |dt| = {dt:.3e} yr, max |dv| = {dv:.3e} AU/yr")

    results = {}
    for config in ("schw", "kepler"):
        errs, kinds = doll_segments(config, cross)
        errs = np.array(errs)
        idx = np.arange(1, len(errs)+1)
        slope = np.polyfit(idx, np.log(errs), 1)[0]
        results[config] = dict(
            exponent=float(slope),
            err_first=float(errs[:5].mean()), err_last=float(errs[-5:].mean()),
            err_max=float(errs.max()), err_median=float(np.median(errs)),
            n=len(errs))
        print(config, results[config])

    # flybys: b log-uniform [1.5, 50] R_p from the rung sampler
    import random
    rng = random.Random(20261002)
    for _ in range(256):
        rng.uniform(math.log(20.0), math.log(1000.0))
        rng.uniform(0.0, 0.6)
        rng.uniform(0.01, 0.25)
    bs = [math.exp(rng.uniform(math.log(1.5), math.log(50.0))) for _ in range(64)]
    inp = "\n".join(f"{b!r}" for b in bs) + "\n"
    fly = {}
    for config in ("schw", "kepler"):
        out = subprocess.run([RUN, "flyby", config, "1e-9"], input=inp,
                             capture_output=True, text=True, timeout=1200)
        rows = []
        for line in out.stdout.split("\n"):
            f = line.split()
            if f and f[0] == "FLY":
                b, tend = float(f[1]), float(f[2])
                dvd = np.array([float(f[3]), float(f[4])])
                dvr = np.array([float(f[5]), float(f[6])])
                rel = np.linalg.norm(dvd-dvr)/np.linalg.norm(dvr)
                ang = math.atan2(dvd[0]*dvr[1]-dvd[1]*dvr[0], dvd @ dvr)
                rows.append(dict(b=b, rel=float(rel), ang=float(ang),
                                 mag=float(np.linalg.norm(dvd)), magr=float(np.linalg.norm(dvr))))
        rel = np.array([r["rel"] for r in rows])
        fly[config] = dict(pass_fraction=float((rel <= 0.01).mean()),
                           worst=float(rel.max()), rows=rows, n=len(rows))
        print("flyby", config, fly[config]["pass_fraction"], "worst", fly[config]["worst"], "n", len(rows))

    out = dict(transfer=results, flyby={k: {kk: vv for kk, vv in v.items() if kk != "rows"} for k, v in fly.items()},
               fly_rows=fly["schw"]["rows"], ref_conv=[dt, dv], ref_done=done)
    with open("ships_out.json", "w") as f:
        json.dump(out, f, indent=1)
    # keep full flyby rows for the picture
    with open("fly_rows.json", "w") as f:
        json.dump({k: v["rows"] for k, v in fly.items()}, f)


if __name__ == "__main__":
    main()
