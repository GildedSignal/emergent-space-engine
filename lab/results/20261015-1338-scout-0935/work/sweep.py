#!/usr/bin/env python3
"""The decisive sweep: free-fall and burn scenes, scar table, JSON out."""
import json, sys
import numpy as np
import news_strong as ns

def run_scene(v0, a_burn=0.0, jerk=0.0, r0=20.0, n_samples=60, label=""):
    src = ns.Source(np.array(v0, float), a_burn=a_burn, jerk=jerk)
    P = 2 * np.pi * np.sqrt(r0 ** 3)
    # window: keep |dv_burn| <= 0.3 and the source subluminal
    dv = lambda t: abs(a_burn) * t + 0.5 * abs(jerk) * t * t
    t_lim = 1.2 * P
    if a_burn != 0.0 or jerk != 0.0:
        # keep dv <= 0.3 and subluminal
        t_grow = 0.0
        while dv(t_grow) <= 0.3 and t_grow < 1e6:
            t_grow += 1.0
        t_lim = min(t_lim, max(t_grow - 1.0, 1.0), (0.85 - np.linalg.norm(src.v0)) / (abs(a_burn) + 1e-12) if a_burn else 1e9)
    t_max = t_lim
    n_orbits = t_max / P
    events = ns.orbit_events(src, r0, n_samples=n_samples, steps_per_orbit=200,
                             n_orbits=max(n_orbits, 0.05))
    rows = []
    for (t, x, v) in events:
        if t > t_max:
            break
        R_now = np.linalg.norm(x - src.at(t)[0])
        if not (0.5 * r0 <= R_now <= 2.5 * r0):
            continue
        G = ns.gamma_fd(src, t, x)
        a_ex = -G[1:4, 0, 0]
        A = ns.arms(src, t, x)
        row = {"t": t, "R": R_now, "beta_c": np.linalg.norm(v - src.at(t)[1])}
        ax = a_ex / np.linalg.norm(a_ex)
        for k, av in A.items():
            err = av - a_ex
            row[k] = float(np.linalg.norm(err) / np.linalg.norm(a_ex))
            row[k + "_perp"] = float(np.linalg.norm(err - np.dot(err, ax) * ax) / np.linalg.norm(a_ex))
        rows.append(row)
    s = {"label": label, "n": len(rows), "v0": list(v0), "a_burn": a_burn, "jerk": jerk,
         "r0": r0,
         "R_med": float(np.median([r["R"] for r in rows])),
         "beta_c_med": float(np.median([r["beta_c"] for r in rows]))}
    for k in ("R1", "R0", "R2", "R2b"):
        s[k] = float(np.median([r[k] for r in rows]))
        s[k + "_max"] = max(r[k] for r in rows)
        s[k + "_perp"] = float(np.median([r[k + "_perp"] for r in rows]))
    return s

scenes = []
# free-fall grid
for r0 in (200.0, 50.0, 20.0, 12.0):
    for b in (0.003, 0.03, 0.1, 0.3):
        scenes.append(((b, 0), dict(r0=r0), f"ff b={b} r0={r0}"))
# burns: gentle 0.10 vc / 0.25 P, hard 0.82 vc / P  (7ab4's programme)
for r0 in (50.0, 20.0, 12.0):
    vc = np.sqrt(1.0 / r0); P = 2 * np.pi * np.sqrt(r0 ** 3)
    for name, dv, frac in (("gentle", 0.10 * vc, 0.25), ("hard", 0.82 * vc, 1.0)):
        ab = dv / (frac * P)
        scenes.append(((0.1, 0), dict(a_burn=ab, r0=r0), f"{name} r0={r0} a={ab:.2e}"))
# held-out rows run only if argv says so
if len(sys.argv) > 1 and sys.argv[1] == "heldout":
    scenes = [((0.2, 0), dict(r0=16.0), "held ff b=0.2 r0=16"),
              ((0.2, 0), dict(a_burn=0.10 * np.sqrt(1/16) / (0.25 * 2 * np.pi * 64), r0=16.0), "held gentle r0=16"),
              ((0.1, 0), dict(a_burn=0.82 * np.sqrt(1/30) / (2 * np.pi * 30 ** 1.5), r0=30.0), "held hard r0=30"),
              ((0.1, 0), dict(a_burn=0.10 * np.sqrt(1/20) / (0.25 * 2 * np.pi * 20 ** 1.5), jerk=0.10 * np.sqrt(1/20) / (0.25 * 2 * np.pi * 20 ** 1.5) / 40, r0=20.0), "held jerk r0=20 (a doubles per 40 t)"),
              ((0.1, 0), dict(a_burn=-0.10 * np.sqrt(1/20) / (0.25 * 2 * np.pi * 20 ** 1.5), r0=20.0), "held retro r0=20")]

out = []
for (v0, kw, label) in scenes:
    s = run_scene(v0, **kw, label=label)
    out.append(s)
    print(json.dumps({k: (f"{v:.3e}" if isinstance(v, float) else v) for k, v in s.items()}))
    sys.stdout.flush()

with open("sweep.json" if len(sys.argv) == 1 else "sweep_heldout.json", "w") as f:
    json.dump(out, f, indent=1)
