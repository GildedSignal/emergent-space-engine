#!/usr/bin/env python3
"""One renewal quantum for the binding layer (system-lens probe, float replica).

The plane (crates/universe/src/step.rs) kicks at 1/64 of the radial period in
phase and REBINDS a new tube on every kick. Replica scene: restricted circular
three-body (Sun mu=1 + Jupiter mu_j=1e-3 on a_j=5.2 + ship), Wisdom-Holman
split, exact Kepler drift, kick = Jupiter's difference acceleration (indirect
term included), evaluated at the interval midpoint.

Configurations (identical step grid and force law otherwise):
  immediate : apply every kick at once, rebind every kick (the plane today).
  deferred  : accumulate dv exactly; apply (rebind) only when |acc| >= q_v.
  discard   : re-round the state to the q_v grid every kick, residue dropped
              (the rejected "quantized memo": random walk by construction).
Truth: immediate at 1024 kicks/orbit (512 for the resonance scene).
"""
import json
import math
import sys

MU = 1.0
MU_J = 1e-3
A_J = 5.2
N_J = math.sqrt(MU / A_J**3)


def kepler_drift(rx, ry, vx, vy, h):
    """Exact Kepler drift (mu=1) of duration h; returns new (rx,ry,vx,vy)."""
    r = math.hypot(rx, ry)
    v2 = vx * vx + vy * vy
    a = 1.0 / (2.0 / r - v2)
    rv = rx * vx + ry * vy
    k = v2 - 1.0 / r
    ex = k * rx - rv * vx
    ey = k * ry - rv * vy
    e = math.hypot(ex, ey)
    sa = math.sqrt(a)
    b = a * math.sqrt(max(0.0, 1.0 - e * e))
    M1 = h / (a * sa)
    if e >= 1e-12:
        sinE = rv / (e * sa)
        cosE = (1.0 - r / a) / e
        E0 = math.atan2(sinE, cosE)
        M1 += E0 - e * sinE
        E = M1 + e * math.sin(M1)
        for _ in range(8):
            E -= (E - e * math.sin(E) - M1) / (1.0 - e * math.cos(E))
        cE, sE = math.cos(E), math.sin(E)
        den = 1.0 - e * cE
        xpf = a * (cE - e)
        ypf = b * sE
        vxpf = -sE / (sa * den)
        vypf = b * cE / (a * sa * den)
        px, py = ex / e, ey / e
    else:
        # circular: rotate the whole state by n*h
        ang = M1
        ca, sa2 = math.cos(ang), math.sin(ang)
        return (rx * ca - ry * sa2, rx * sa2 + ry * ca,
                vx * ca - vy * sa2, vx * sa2 + vy * ca)
    qx, qy = -py, px
    return (px * xpf + qx * ypf, py * xpf + qy * ypf,
            px * vxpf + qx * vypf, py * vxpf + qy * vypf)


def kick_acc(rx, ry, t):
    """Jupiter difference acceleration (heliocentric, indirect term removed)."""
    lx = A_J * math.cos(N_J * t)
    ly = A_J * math.sin(N_J * t)
    dx = lx - rx
    dy = ly - ry
    d3 = (dx * dx + dy * dy) ** 1.5
    lj3 = A_J * A_J * A_J
    return MU_J * (dx / d3 - lx / lj3), MU_J * (dy / d3 - ly / lj3)


def energy(rx, ry, vx, vy):
    return 0.5 * (vx * vx + vy * vy) - MU / math.hypot(rx, ry)


def elems(rx, ry, vx, vy):
    r = math.hypot(rx, ry)
    v2 = vx * vx + vy * vy
    k = v2 - 1.0 / r
    rv = rx * vx + ry * vy
    ex = k * rx - rv * vx
    ey = k * ry - rv * vy
    return math.hypot(ex, ey), math.atan2(ey, ex)


def run(a0, e0, orbits, kicks_per_orbit, mode, qv, sample=None):
    """One WH run. mode: immediate|deferred|discard. Returns (renewals, out)."""
    r0 = a0 * (1.0 - e0)
    v0 = math.sqrt(MU / a0 * (1.0 + e0) / (1.0 - e0))
    rx, ry, vx, vy = r0, 0.0, 0.0, v0
    P0 = 2 * math.pi * a0 ** 1.5
    H = P0 / kicks_per_orbit
    accx = accy = 0.0
    renewals = 0
    marks = set(sample) if sample is not None else set()
    out = {"t": [], "E": [], "e": [], "w": [], "r": [], "lam": []}
    t = 0.0
    steps = int(orbits * kicks_per_orbit)
    rx, ry, vx, vy = kepler_drift(rx, ry, vx, vy, 0.5 * H)
    for i in range(steps):
        t += 0.5 * H
        ax, ay = kick_acc(rx, ry, t)
        dvx, dvy = ax * H, ay * H
        if mode == "immediate":
            vx += dvx
            vy += dvy
            renewals += 1
        elif mode == "deferred":
            accx += dvx
            accy += dvy
            if math.hypot(accx, accy) >= qv:
                vx += accx
                vy += accy
                accx = accy = 0.0
                renewals += 1
        elif mode == "discard":
            vx = round((vx + dvx) / qv) * qv
            vy = round((vy + dvy) / qv) * qv
            renewals += 1
        t += 0.5 * H
        rx, ry, vx, vy = kepler_drift(rx, ry, vx, vy, H)
        t += 0.5 * H
        if (i + 1) % kicks_per_orbit == 0 and (i + 1) // kicks_per_orbit in marks:
            e, w = elems(rx, ry, vx, vy)
            out["t"].append(t)
            out["E"].append(energy(rx, ry, vx, vy))
            out["e"].append(e)
            out["w"].append(w)
            out["r"].append((rx, ry))
            out["lam"].append(math.atan2(ry, rx))
    return renewals, out


def growth_exponent(ts, errs):
    """log-log slope of error vs time (positive samples only)."""
    pts = [(math.log(t), math.log(max(er, 1e-300)))
           for t, er in zip(ts, errs) if t > 0 and er > 0]
    if len(pts) < 3:
        return float("nan")
    n = len(pts)
    sx = sum(p[0] for p in pts)
    sy = sum(p[1] for p in pts)
    sxx = sum(p[0] * p[0] for p in pts)
    sxy = sum(p[0] * p[1] for p in pts)
    return (n * sxy - sx * sy) / (n * sxx - sx * sx)


def compare(name, a0, e0, orbits, kpo, truth, defers, discard_q=None, marks=None):
    res = {}
    ren, out = run(a0, e0, orbits, kpo, "immediate", None, sample=marks)
    res["immediate"] = (ren, out)
    for qv in defers:
        ren, out = run(a0, e0, orbits, kpo, "deferred", qv, sample=marks)
        res["deferred q=%.3e" % qv] = (ren, out)
    if discard_q:
        ren, out = run(a0, e0, orbits, kpo, "discard", discard_q, sample=marks)
        res["discard q=%.3e" % discard_q] = (ren, out)
    print("\n=== %s (a0=%g, e0=%g, %d orbits, %d kicks/orbit) ===" %
          (name, a0, e0, orbits, kpo))
    print("%-26s %11s %10s %6s %9s %11s %6s" %
          ("config", "renew/orbit", "max|dE|", "expE", "max|de|", "dW/orbit", "expW"))
    rows = []
    for cfg, (ren, out) in res.items():
        dE = [abs(a - b) for a, b in zip(out["E"], truth["E"])]
        de = [abs(a - b) for a, b in zip(out["e"], truth["e"])]
        dw = []
        for a, b in zip(out["w"], truth["w"]):
            d = a - b
            while d > math.pi:
                d -= 2 * math.pi
            while d < -math.pi:
                d += 2 * math.pi
            dw.append(d)
        expE = growth_exponent(truth["t"], dE)
        expW = growth_exponent(truth["t"], [abs(x) for x in dw])
        print("%-26s %11.2f %10.2e %6.2f %9.2e %11.3e %6.2f" %
              (cfg, ren / orbits, max(dE), expE, max(de), dw[-1] / orbits, expW))
        rows.append({"config": cfg, "renewals_per_orbit": ren / orbits,
                     "max_dE": max(dE), "expE": expE, "max_de": max(de),
                     "dW_per_orbit": dw[-1] / orbits, "expW": expW,
                     "max_dW": max(abs(x) for x in dw)})
    return rows


def main():
    data = {}
    # ---------- Scene A: off resonance ----------
    a0, e0, orbits = 2.0, 0.05, 1000
    marks = list(range(1, orbits + 1, 5))
    ren, tout = run(a0, e0, orbits, 1024, "immediate", None, sample=marks)
    print("truth: %d kicks, %d marks" % (ren, len(marks)))
    H = a0 ** 1.5 / 64
    dv_est = MU_J * H / (A_J - a0) ** 2
    defers = [dv_est * f for f in (2, 8, 32, 128)]
    data["A"] = compare("A off-resonance", a0, e0, orbits, 64, tout, defers,
                        discard_q=dv_est * 8, marks=marks)
    for kpo in (8, 16):
        ren, out = run(a0, e0, orbits, kpo, "immediate", None, sample=marks)
        dE = [abs(a - b) for a, b in zip(out["E"], tout["E"])]
        de = [abs(a - b) for a, b in zip(out["e"], tout["e"])]
        expE = growth_exponent(tout["t"], dE)
        print("%-26s %11.2f %10.2e %6.2f %9.2e" %
              ("immediate@%d" % kpo, ren / orbits, max(dE), expE, max(de)))
        data.setdefault("A_coarse", []).append(
            {"config": "immediate@%d" % kpo, "renewals_per_orbit": ren / orbits,
             "max_dE": max(dE), "expE": expE, "max_de": max(de)})

    # ---------- Scene B: 2:1 resonance ----------
    a0r = A_J * 2 ** (-2.0 / 3.0)
    e0r, orbitsr = 0.02, 1000
    marks = list(range(1, orbitsr + 1, 5))
    ren, trout = run(a0r, e0r, orbitsr, 512, "immediate", None, sample=marks)
    dvr = MU_J * (a0r ** 1.5 / 64) / (A_J - a0r) ** 2
    print("\n=== B 2:1 resonance (a0=%.4f, e0=%g, truth 512/orbit) ===" % (a0r, e0r))
    print("%-26s %11s %9s %6s %9s" %
          ("config", "renew/orbit", "e_max", "pump", "psi_wind"))

    def psi_windings(out):
        tot, prev = 0.0, None
        for t, lam, w in zip(out["t"], out["lam"], out["w"]):
            psi = 2 * N_J * t - lam - w
            psi = math.atan2(math.sin(psi), math.cos(psi))
            if prev is not None:
                d = psi - prev
                while d > math.pi:
                    d -= 2 * math.pi
                while d < -math.pi:
                    d += 2 * math.pi
                tot += d
            prev = psi
        return tot / (2 * math.pi)

    rows = []
    ren_i, iout = run(a0r, e0r, orbitsr, 64, "immediate", None, sample=marks)
    emax_i = max(iout["e"])
    print("%-26s %11.2f %9.4f %6.3f %9.1f" %
          ("immediate", ren_i / orbitsr, emax_i, 1.0, psi_windings(iout)))
    rows.append({"config": "immediate", "renewals_per_orbit": ren_i / orbitsr,
                 "e_max": emax_i, "pump": 1.0, "psi_windings": psi_windings(iout)})
    for f in (2, 8, 32, 128):
        qv = dvr * f
        ren, out = run(a0r, e0r, orbitsr, 64, "deferred", qv, sample=marks)
        emax = max(out["e"])
        pump = emax / emax_i if emax_i > 0 else float("nan")
        print("%-26s %11.2f %9.4f %6.3f %9.1f" %
              ("deferred q=%.3e" % qv, ren / orbitsr, emax, pump, psi_windings(out)))
        rows.append({"config": "deferred q=%.3e" % qv,
                     "renewals_per_orbit": ren / orbitsr, "e_max": emax,
                     "pump": pump, "psi_windings": psi_windings(out)})
    data["B"] = rows

    with open(sys.argv[1] if len(sys.argv) > 1 else "deferral.json", "w") as f:
        json.dump(data, f, indent=1)


if __name__ == "__main__":
    main()
