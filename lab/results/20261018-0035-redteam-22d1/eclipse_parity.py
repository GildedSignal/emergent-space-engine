#!/usr/bin/env python3
"""Eclipse parity at game velocities: the occlusion wiring law (representation.md SS2).

Exact 2-D flat-geometry float64, c = 1. Emitters static on a far circle (N = 10^4, as
e59e). Observer at O. Occluder: disk radius R at distance d, velocity v (transverse or
oblique), crossing the observer--emitter axis at t = 0. No approximation inside any
wiring: each is a closed-form segment test.

Wirings (candidate laws for the missing occluder test):
  W1  snapshot: occluder at the frame time t_O (the "static" test as written).
  W2  retarded: occluder at one retarded time t_O - d (its sprite position as drawn).
  W2' per-ray : occluder at the row's own retarded grazing time t_O - d cos(psi).
  W3  worldtube: exact segment-vs-worldtube intersection (the correct law here).

Arm A: occluder motion, no mass. Arm O: observer motion (aberration). Arm B: differential
Shapiro delay across a strong-field transit. Writes eclipse_parity-out.json.
Deterministic; runs in seconds.
"""
import json
import math
import time as wall

import numpy as np

N = 10_000
WIRINGS = ("W1", "W2", "W2p", "W3")
OUT = {}


def min_dist(L, psi, t_O, occ_t, v, wiring):
    """Min distance from each emitter's retarded null segment to the occluder, exact.
    Segment: u*E (u=1 at the observer), light time t = t_O - u L."""
    d0 = math.hypot(*occ_t)
    E = L * np.stack([np.cos(psi), np.sin(psi)], axis=-1)           # (n,2)
    if wiring == "W3":
        anchor, vv = np.asarray(occ_t).reshape(1, 2), v
    elif wiring == "W1":
        anchor, vv = np.asarray(occ_t).reshape(1, 2), np.zeros(2)
    elif wiring == "W2":
        # exact sprite: retarded time solves |X(t_ret)| = t_O - t_ret (uniform v)
        b2 = float(v @ v)
        ox, oy = float(occ_t[0]), float(occ_t[1])
        t_ret = (t_O - math.sqrt(b2 * t_O * t_O + (1 - b2) * (ox * ox + oy * oy))) / (1 - b2)
        anchor = np.asarray(occ_t) - v * (t_O - t_ret)
        anchor, vv = anchor.reshape(1, 2), np.zeros(2)
    elif wiring == "W2p":
        anchor = np.asarray(occ_t) - np.outer(d0 * np.cos(psi), v)  # naive per-row offset
        vv = np.zeros(2)
    else:
        raise ValueError(wiring)
    A = E + L * vv                                                   # (n,2)
    B = np.broadcast_to(anchor, (len(psi), 2))
    aa = np.einsum("ij,ij->i", A, A)
    ab = np.einsum("ij,ij->i", A, B)
    u = np.clip(ab / aa, 0.0, 1.0)
    diff = u[:, None] * A - B
    return np.sqrt(np.einsum("ij,ij->i", diff, diff))


def min_dist_vs_t(L, psi, t_grid, occ_path, v, wiring):
    """min_dist over a time grid for a small psi set, vectorised over t."""
    M, P = len(t_grid), len(psi)
    occ = np.array([occ_path(t) for t in t_grid])                   # (M,2)
    d0 = np.hypot(occ[:, 0], occ[:, 1])                             # (M,) current distance
    E = L * np.stack([np.cos(psi), np.sin(psi)], axis=-1)           # (P,2)
    if wiring == "W3":
        anchor, vv = occ[:, None, :], v
    elif wiring == "W1":
        anchor, vv = occ[:, None, :], np.zeros(2)
    elif wiring == "W2":
        b2 = float(v @ v)
        tO2 = t_grid * t_grid
        r2 = occ[:, 0] ** 2 + occ[:, 1] ** 2
        t_ret = (t_grid - np.sqrt(b2 * tO2 + (1 - b2) * r2)) / (1 - b2)
        anchor = (occ - (t_grid - t_ret)[:, None] * v)[:, None, :]  # exact sprite
        vv = np.zeros(2)
    elif wiring == "W2p":
        dt = d0[:, None] * np.cos(psi)[None, :]                     # (M,P) naive per-row
        anchor = occ[:, None, :] - dt[:, :, None] * v[None, None, :]
        vv = np.zeros(2)
    else:
        raise ValueError(wiring)
    A = E + L * vv                                                  # (P,2)
    aa = np.einsum("pj,pj->p", A, A)
    ab = np.einsum("mpj,pj->mp", anchor, A)
    u = np.clip(ab / aa[None, :], 0.0, 1.0)
    diff = u[:, :, None] * A[None, :, :] - anchor
    return np.sqrt(np.einsum("mpj,mpj->mp", diff, diff))


def jaccard(a, b):
    union = np.logical_or(a, b).sum()
    return 1.0 if union == 0 else np.logical_and(a, b).sum() / union


def onset(tgrid, mind, R):
    idx = np.nonzero(mind < R)[0]
    return float(tgrid[idx[0]]) if len(idx) else None


def arm_a():
    print("=== Arm A: moving occluder, no mass (transverse) ===")
    L_E = 1e4
    psi = np.arange(N) * (2 * math.pi / N)
    rows = []
    for d_over_R in (2.0, 10.0, 100.0):
        R, d = 1.0, d_over_R
        for beta in (1e-4, 0.1, 0.5, 0.9):
            v = np.array([0.0, beta])
            occ = lambda t: (d, beta * t)
            ver = {w: min_dist(L_E, psi, 0.0, occ(0.0), v, w) < R for w in WIRINGS}
            n3 = int(ver["W3"].sum())
            row = dict(d_over_R=d_over_R, beta=beta, n_occ_W3=n3, frac_W3=n3 / N,
                       jac_W1=jaccard(ver["W1"], ver["W3"]),
                       jac_W2=jaccard(ver["W2"], ver["W3"]),
                       jac_W2p=jaccard(ver["W2p"], ver["W3"]),
                       n_flip_W1=int((ver["W1"] != ver["W3"]).sum()))
            span = max(8.0 * R / max(beta, 1e-6) + 4.0 * d + 50.0, 20.0)
            tgrid = np.linspace(-span, span, 200_001)
            on = {}
            for w in WIRINGS:
                mdt = min_dist_vs_t(L_E, np.array([0.0]), tgrid, occ, v, w)[:, 0]
                on[w] = onset(tgrid, mdt, R)
            row.update({f"on_{w}": on[w] for w in WIRINGS},
                       dt_on_W1=None if None in on.values() else on["W1"] - on["W3"],
                       dt_on_W2=None if None in on.values() else on["W2"] - on["W3"],
                       dt_on_W2p=None if None in on.values() else on["W2p"] - on["W3"])
            rows.append(row)
            f1 = row['dt_on_W1']; f2 = row['dt_on_W2']; f3 = row['dt_on_W2p']
            fmt = lambda x: "     None" if x is None else f"{x:+10.4f}s"
            print(f"d={d_over_R:6.0f}R beta={beta:7.4f}  nOcc(W3)={n3:5d} ({n3/N:6.2%})  "
                  f"Jac W1={row['jac_W1']:.3f} W2={row['jac_W2']:.3f} "
                  f"W2p={row['jac_W2p']:.4f}  dOnset W1={fmt(f1)} "
                  f"W2={fmt(f2)} W2p={fmt(f3)}  (d/c={d:.0f}s)")
    rim = {}
    for d_over_R in (2.0, 10.0):
        R, d, beta = 1.0, d_over_R, 0.5
        v = np.array([0.0, beta])
        psi_r = math.asin(R / d)
        span = 6.0 * R / beta + 2.0 * d + 10.0
        tgrid = np.linspace(-span, span, 200_001)
        ons = {}
        for w in WIRINGS:
            mdt = min_dist_vs_t(L_E, np.array([psi_r]), tgrid,
                                lambda t: (d, beta * t), v, w)[:, 0]
            ons[w] = onset(tgrid, mdt, R)
        rim[f"{d_over_R:.0f}R"] = {w: ons[w] - ons["W3"] for w in WIRINGS}
        pred = d * (1.0 - math.cos(psi_r))
        print(f"  d={d_over_R:3.0f}R psi_rim={math.degrees(psi_r):5.2f}deg  rim onset err: "
              f"W1={ons['W1']-ons['W3']:+9.4f}s W2={ons['W2']-ons['W3']:+8.4f}s "
              f"W2p={ons['W2p']-ons['W3']:+.2e}s   predicted W2 = d(1-cos psi) = {pred:.4f}s")
    print("-- oblique arm (45 deg, held out), d=10R --")
    obl = []
    for beta in (0.1, 0.5):
        R, d = 1.0, 10.0
        v = beta * np.array([math.cos(math.pi / 4), math.sin(math.pi / 4)])
        occ = lambda t: (d + v[0] * t, v[1] * t)  # centre crosses (d, 0) at t = 0
        ver = {w: min_dist(L_E, psi, 0.0, occ(0.0), v, w) < R for w in WIRINGS}
        obl.append(dict(beta=beta, n_occ=int(ver["W3"].sum()),
                        jac_W1=jaccard(ver["W1"], ver["W3"]),
                        jac_W2p=jaccard(ver["W2p"], ver["W3"])))
        print(f"  beta={beta}: nOcc(W3)={int(ver['W3'].sum())}  Jac W1="
              f"{jaccard(ver['W1'], ver['W3']):.3f}  W2p={jaccard(ver['W2p'], ver['W3']):.4f}")
    return dict(L_E=L_E, rows=rows, rim=rim, oblique=obl)


def arm_observer():
    """Observer at beta_O = 0.5: aberrated arcs and coordinate-arc parity error."""
    print("=== Arm O: observer beta_O = 0.5, d = 2R, occluder static ===")
    L_E = 1e4
    R, d = 1.0, 2.0
    psi = np.arange(N) * (2 * math.pi / N)
    out = {}
    for label, bO in (("approach(+x toward occluder)", +0.5), ("recede", -0.5)):
        E = L_E * np.stack([np.cos(psi), np.sin(psi)], axis=-1)
        Rdist = np.linalg.norm(E, axis=-1)
        look = E / Rdist[:, None]                    # look direction, root frame
        occ_xy = np.array([d, 0.0])
        aa = np.einsum("ij,ij->i", E, E)
        ab = np.einsum("ij,ij->i", E, np.broadcast_to(occ_xy, (N, 2)))
        u = np.clip(ab / aa, 0.0, 1.0)
        diff = u[:, None] * E - occ_xy
        occ_true = np.linalg.norm(diff, axis=-1) < R
        ang_coord = np.degrees(np.arctan2(look[:, 1], look[:, 0])) % 360.0
        g = 1.0 / math.sqrt(1 - bO * bO)
        nx, ny = look[:, 0], look[:, 1]
        npx = (nx + bO) / (1.0 + bO * nx)            # look dir into the +bO x frame
        npy = ny / (g * (1.0 + bO * nx))
        ang_obs = np.degrees(np.arctan2(npy, npx)) % 360.0

        def halfarc(ang, mask):
            a = ang[mask]
            z = np.exp(1j * np.radians(a)).mean()
            centre = math.degrees(math.atan2(z.imag, z.real)) % 360.0
            dev = (a - centre + 180.0) % 360.0 - 180.0
            return 0.5 * (dev.max() - dev.min()), centre
        h_obs, _ = halfarc(ang_obs, occ_true)
        h_coord, c_coord = halfarc(ang_coord, occ_true)
        occ_wrong = np.abs((ang_coord - c_coord + 180.0) % 360.0 - 180.0) < h_coord
        mis = int((occ_wrong != occ_true).sum())
        arc_err = abs(h_obs - 30.0) / 30.0
        out[label] = dict(half_arc_obs_deg=h_obs, half_arc_coord_deg=h_coord,
                          arc_size_error=arc_err, misclassified=mis, frac=mis / N,
                          n_occ=int(occ_true.sum()))
        print(f"  {label}: half-arc observer-frame {h_obs:.2f} deg, coordinate-frame "
              f"{h_coord:.2f} deg (static 30.00; arc-size error {arc_err:.1%}); "
              f"coordinate-arc row parity misclassifies {mis} rows ({mis/N:.3%})")
    return out


def shapiro(b, r_E, r_O, M):
    return 2.0 * M * math.log(4.0 * r_E * r_O / (b * b))


def arm_b():
    print("=== Arm B: differential Shapiro delay across a strong-field transit ===")
    M = 1.0
    r_O, R_p = 20.0 * M, 1.0 * M
    E = 100.0 * M * np.array([math.cos(2.5), math.sin(2.5)])
    Opos = np.array([r_O, 0.0])
    seg = Opos - E
    Lseg = float(np.linalg.norm(seg))
    udir = seg / Lseg
    b_ray = abs(float(np.cross(E, udir)))
    r_E = float(np.linalg.norm(E))
    s = np.linspace(0.0, Lseg, 2_000_001)
    pts = E[None, :] + s[:, None] * udir[None, :]
    r = np.linalg.norm(pts, axis=1)
    quad = 2.0 * M * float(np.sum(1.0 / r)) * (Lseg / (len(s) - 1))
    logf = shapiro(b_ray, r_E, r_O, M)
    exact = 2.0 * M * math.log(((r_E + math.sqrt(r_E ** 2 - b_ray ** 2))
                                * (r_O + math.sqrt(r_O ** 2 - b_ray ** 2))) / b_ray ** 2)
    print(f"  b_ray={b_ray:.2f}M: delay quad={quad:.4f}s  log={logf:.4f}s  "
          f"exact={exact:.4f}s  (log vs quad {abs(logf-quad)/quad:.2%})")
    diff_limb = (shapiro(b_ray + R_p, r_E, r_O, M) - shapiro(b_ray - R_p, r_E, r_O, M))
    rows = {}
    for beta in (1e-4, 0.5):
        dur = 2.0 * R_p / beta
        rows[f"beta{beta}"] = dict(duration=dur, diff_limb=abs(diff_limb),
                                   rel=abs(diff_limb) / dur, w1_error=2.0 * R_p,
                                   naive=logf)
        print(f"  beta={beta:7.4f}: transit {dur:10.2f}s | sprite-consistent differential "
              f"{abs(diff_limb):.4f}s ({abs(diff_limb)/dur:.3%}) | W1 error d/c = "
              f"{2.0*R_p:.1f}s | naive no-cancel delay {logf:.2f}s (not the observable)")
    return dict(M=M, r_O=r_O, R_p=R_p, b_ray=b_ray, shapiro_quad=quad, shapiro_log=logf,
                shapiro_exact=exact, rel_err_log_vs_quad=abs(logf - quad) / quad,
                diff_limb=abs(diff_limb), rows=rows)


def price():
    print("=== Price: exact W3 per row (vectorised; order of magnitude, shared x86) ===")
    L_E = 1e4
    psi = np.arange(100_000) * (2 * math.pi / 100_000)
    v = np.array([0.0, 0.5])
    reps = 20
    t0 = wall.perf_counter()
    for _ in range(reps):
        min_dist(L_E, psi, 0.0, (10.0, 0.0), v, "W3")
    dt = (wall.perf_counter() - t0) / reps
    print(f"  100k rows: {dt*1e3:.2f} ms/pass -> {dt*1e9/100_000:.0f} ns/row "
          f"(numpy one-off overhead included)")
    return dict(ms_per_100k=dt * 1e3, ns_per_row=dt * 1e9 / 100_000)


def main():
    OUT["arm_a"] = arm_a()
    OUT["observer"] = arm_observer()
    OUT["arm_b"] = arm_b()
    OUT["price"] = price()
    with open(__file__.replace(".py", "-out.json"), "w") as f:
        json.dump(OUT, f, indent=1)
    print("wrote", __file__.replace(".py", "-out.json"))


if __name__ == "__main__":
    main()
