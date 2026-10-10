#!/usr/bin/env python3
"""One renewal quantum for the binding layer — CORRECTED RECORD (second-author run).

Derived from 20261010-1816-system-67f2/deferral.py (verbatim copy kept as
deferral-orig.py) with three changes, each fixing a defect the second checker
named (check2.md, "The one experiment to gold"):

 1. CLOCK FIX. The original advanced the force clock by 1.5*H per kick (three
    0.5*H increments) while the body advanced H, so the perturber phase used in
    the force led the ship by ~119 revolutions per 1000 orbits (effective
    perturber rate 1.5*N_J). Now the kick is evaluated at the body's own time:
    kick j at (j-0.5)*H, the midpoint of the interval [(j-1)H, jH] it
    represents. Scene B's a0 = A_J*2^(-2/3) is therefore a TRUE 2:1 resonance
    again (n = 2*N_J), and psi = 2*N_J*t - lam - w is the actual resonant angle.
 2. QUANTCARRY CONTROL. New mode isolating magnitude error from timing error:
    every kick applied on time, but rounded to the same q_v grid with the
    residue carried exactly. Same quantum as deferred, exact timing. This is
    the instrument the split rule needs (the original 'discard' control drops
    the residue and, under the mistimed force, spuriously looked bounded).
 3. EJECTION GUARD. If a kick leaves E > 0 (hyperbolic), the orbit and time are
    recorded and the run stops instead of corrupting the Kepler drift.

Everything else (force law, WH split, exact Kepler drift, q ladder factors,
mark cadence, growth-exponent definition) is the author's, unchanged, so this
table maps 1:1 onto the original record. Modes:
  immediate : apply every kick at once (the plane today).
  deferred  : accumulate dv exactly; apply (rebind) only when |acc| >= q_v.
  discard   : re-round the state to the q_v grid every kick, residue dropped.
  quantcarry: round each kick to the q_v grid, carry residue, apply ON TIME.
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
    """One WH run, force at the BODY's time (corrected clock).

    mode: immediate|deferred|discard|quantcarry. Returns (renewals, out);
    out["ejected_at_orbit"] is set (else None) if a kick left E > 0.
    """
    r0 = a0 * (1.0 - e0)
    v0 = math.sqrt(MU / a0 * (1.0 + e0) / (1.0 - e0))
    rx, ry, vx, vy = r0, 0.0, 0.0, v0
    P0 = 2 * math.pi * a0 ** 1.5
    H = P0 / kicks_per_orbit
    accx = accy = 0.0
    resx = resy = 0.0
    renewals = 0
    ejected_at = None
    marks = set(sample) if sample is not None else set()
    out = {"t": [], "E": [], "e": [], "w": [], "r": [], "lam": [],
           "ejected_at_orbit": None}
    t = 0.5 * H                 # body time of the first kick (its midpoint)
    steps = int(orbits * kicks_per_orbit)
    rx, ry, vx, vy = kepler_drift(rx, ry, vx, vy, 0.5 * H)
    for i in range(steps):
        ax, ay = kick_acc(rx, ry, t)          # FORCE AT BODY TIME (fix #1)
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
        elif mode == "quantcarry":
            tx, ty = dvx + resx, dvy + resy    # fix #2: exact timing,
            apx = qv * round(tx / qv)          # magnitude rounded to q_v,
            apy = qv * round(ty / qv)          # residue carried exactly.
            resx, resy = tx - apx, ty - apy
            vx += apx
            vy += apy
            renewals += 1
        else:
            raise ValueError(mode)
        if energy(rx, ry, vx, vy) > 0.0:       # fix #3: hyperbolic guard
            ejected_at = (i + 1) / kicks_per_orbit
            out["ejected_at_orbit"] = ejected_at
            e, w = elems(rx, ry, vx, vy)
            out["t"].append(t)
            out["E"].append(energy(rx, ry, vx, vy))
            out["e"].append(e)
            out["w"].append(w)
            out["r"].append((rx, ry))
            out["lam"].append(math.atan2(ry, rx))
            break
        rx, ry, vx, vy = kepler_drift(rx, ry, vx, vy, H)
        t += H                                 # one kick per H of BODY time
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


def compare(name, a0, e0, orbits, kpo, truth, configs, marks=None):
    """configs: list of (label, mode, qv)."""
    res = []
    for label, mode, qv in configs:
        ren, out = run(a0, e0, orbits, kpo, mode, qv, sample=marks)
        res.append((label, ren, out))
    print("\n=== %s (a0=%g, e0=%g, %d orbits, %d kicks/orbit) ===" %
          (name, a0, e0, orbits, kpo))
    print("%-26s %11s %10s %6s %9s %11s %6s %7s" %
          ("config", "renew/orbit", "max|dE|", "expE", "max|de|", "dW/orbit",
           "expW", "eject@"))
    rows = []
    for label, ren, out in res:
        m = min(len(out["E"]), len(truth["E"]))
        dE = [abs(a - b) for a, b in zip(out["E"][:m], truth["E"][:m])]
        de = [abs(a - b) for a, b in zip(out["e"][:m], truth["e"][:m])]
        dw = []
        for a, b in zip(out["w"][:m], truth["w"][:m]):
            d = a - b
            while d > math.pi:
                d -= 2 * math.pi
            while d < -math.pi:
                d += 2 * math.pi
            dw.append(d)
        expE = growth_exponent(truth["t"][:m], dE)
        expW = growth_exponent(truth["t"][:m], [abs(x) for x in dw])
        ej = out["ejected_at_orbit"]
        print("%-26s %11.2f %10.2e %6.2f %9.2e %11.3e %6.2f %7s" %
              (label, ren / orbits, max(dE), expE, max(de),
               (dw[-1] / orbits) if dw else float("nan"), expW,
               ("%.0f" % ej) if ej is not None else "-"))
        rows.append({"config": label, "renewals_per_orbit": ren / orbits,
                     "max_dE": max(dE), "expE": expE, "max_de": max(de),
                     "dW_per_orbit": (dw[-1] / orbits) if dw else None,
                     "expW": expW,
                     "max_dW": max(abs(x) for x in dw) if dw else None,
                     "ejected_at_orbit": ej,
                     "marks": m})
    return rows


def psi_windings(out):
    """Winding total of psi = 2*N_J*t - lam - w (the TRUE 2:1 resonant angle
    under the corrected clock)."""
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


def main():
    data = {}
    # ---------- Scene A: off resonance (the author's scene, corrected clock) ----------
    a0, e0, orbits = 2.0, 0.05, 1000
    marks = list(range(1, orbits + 1, 5))
    ren, tout = run(a0, e0, orbits, 1024, "immediate", None, sample=marks)
    print("scene A truth: %d kicks, %d marks" % (ren, len(marks)))
    dv_est = MU_J * (a0 ** 1.5 / 64) / (A_J - a0) ** 2
    configs = [("immediate", "immediate", None)]
    configs += [("deferred q=%.3e" % (dv_est * f), "deferred", dv_est * f)
                for f in (2, 8, 32, 128)]
    configs += [("discard q=%.3e" % (dv_est * 8), "discard", dv_est * 8),
                ("quantcarry q=%.3e" % (dv_est * 8), "quantcarry", dv_est * 8)]
    data["A"] = compare("A off-resonance", a0, e0, orbits, 64, tout,
                        configs, marks=marks)
    for kpo in (8, 16):
        ren, out = run(a0, e0, orbits, kpo, "immediate", None, sample=marks)
        m = min(len(out["E"]), len(tout["E"]))
        dE = [abs(a - b) for a, b in zip(out["E"][:m], tout["E"][:m])]
        de = [abs(a - b) for a, b in zip(out["e"][:m], tout["e"][:m])]
        expE = growth_exponent(tout["t"][:m], dE)
        print("%-26s %11.2f %10.2e %6.2f %9.2e" %
              ("immediate@%d" % kpo, ren / orbits, max(dE), expE, max(de)))
        data.setdefault("A_coarse", []).append(
            {"config": "immediate@%d" % kpo, "renewals_per_orbit": ren / orbits,
             "max_dE": max(dE), "expE": expE, "max_de": max(de)})

    # ---------- Scene A2: high eccentricity, off resonance ----------
    e0h = 0.3
    ren, thout = run(a0, e0h, orbits, 1024, "immediate", None, sample=marks)
    dvh = MU_J * (a0 ** 1.5 / 64) / (A_J - a0) ** 2
    data["A2"] = compare("A2 off-resonance e=0.3", a0, e0h, orbits, 64, thout,
                         [("immediate", "immediate", None),
                          ("deferred q=%.3e" % (dvh * 8), "deferred", dvh * 8),
                          ("quantcarry q=%.3e" % (dvh * 8), "quantcarry", dvh * 8),
                          ("discard q=%.3e" % (dvh * 8), "discard", dvh * 8)],
                         marks=marks)

    # ---------- Scene B: TRUE 2:1 resonance (a0 = A_J*2^(-2/3), n = 2 N_J) ----------
    a0r = A_J * 2 ** (-2.0 / 3.0)
    e0r, orbitsr = 0.02, 1000
    marksr = list(range(1, orbitsr + 1, 5))
    ren, trout = run(a0r, e0r, orbitsr, 512, "immediate", None, sample=marksr)
    dvr = MU_J * (a0r ** 1.5 / 64) / (A_J - a0r) ** 2
    print("\n=== B TRUE 2:1 resonance (a0=%.4f, e0=%g, truth 512/orbit) ===" %
          (a0r, e0r))
    print("%-26s %11s %9s %6s %9s %7s" %
          ("config", "renew/orbit", "e_max", "pump", "psi_wind", "eject@"))
    rows = []
    bconfigs = [("immediate", "immediate", None)]
    bconfigs += [("deferred q=%.3e" % (dvr * f), "deferred", dvr * f)
                 for f in (2, 8, 32, 128)]
    bconfigs += [("quantcarry q=%.3e" % (dvr * 8), "quantcarry", dvr * 8),
                 ("discard q=%.3e" % (dvr * 8), "discard", dvr * 8)]
    emax_i = None
    for label, mode, qv in bconfigs:
        ren, out = run(a0r, e0r, orbitsr, 64, mode, qv, sample=marksr)
        emax = max(out["e"])
        if label == "immediate":
            emax_i = emax
        pump = emax / emax_i if emax_i > 0 else float("nan")
        ej = out["ejected_at_orbit"]
        print("%-26s %11.2f %9.4f %6.3f %9.1f %7s" %
              (label, ren / orbitsr, emax, pump, psi_windings(out),
               ("%.0f" % ej) if ej is not None else "-"))
        rows.append({"config": label, "renewals_per_orbit": ren / orbitsr,
                     "e_max": emax, "pump": pump,
                     "psi_windings": psi_windings(out),
                     "ejected_at_orbit": ej})
    data["B"] = rows
    data["B_truth"] = {"config": "truth immediate@512", "e_max": max(trout["e"]),
                       "psi_windings": psi_windings(trout)}

    # ---------- Convergence probes (no bug: q -> 0 recovers immediate) ----------
    print("\n=== probes (scene A, 1000 orbits, truth 1024/orbit) ===")
    probes = []
    for mode, qv in [("deferred", 1e-9), ("deferred", 1e-7),
                     ("discard", 1e-7), ("discard", 1e-6),
                     ("quantcarry", 1e-7)]:
        ren, out = run(a0, e0, orbits, 64, mode, qv, sample=marks)
        dE = [abs(a - b) for a, b in zip(out["E"], tout["E"])]
        exp = growth_exponent(tout["t"], dE)
        print("%-12s %-10s renew/orbit=%6.2f max|dE|=%10.2e exp=%5.2f" %
              (mode, qv, ren / orbits, max(dE), exp))
        probes.append({"mode": mode, "q": qv, "renewals_per_orbit": ren / orbits,
                       "max_dE": max(dE), "expE": exp})
    data["probes"] = probes

    with open(sys.argv[1] if len(sys.argv) > 1 else "deferral.json", "w") as f:
        json.dump(data, f, indent=1)


if __name__ == "__main__":
    main()
