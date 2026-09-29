#!/usr/bin/env python3
"""Rung r4: does the design's event layer (exact Kepler cycles + analytic
multipole tidal kick at each conjunction) reproduce mean-motion resonance?

Configs:
  conj-quad : kick = quadrupole tidal impulse integrated along the unperturbed
              Kepler arcs over one synodic window centred on the conjunction
              (24-node Gauss-Legendre quadrature of the analytic field; no ODE
              is stepped anywhere in a candidate).
  conj-oct  : same + octupole term.
  averaged  : orbit-averaged kick (H0190 K2). The vector average of the tidal
              impulse over both mean anomalies is identically zero, so the
              surviving orbit-averaged effect is the secular apsidal
              precession pi_dot = (3/4) n1 (m2/M) (a1/a2)^3 (1-e1^2)^-2,
              applied at each conjunction. Phase coherence erased by design.
  none      : no perturbation at all.

Cases: R1 2:1 (mu = 3e-3), R2 2:1 phase-shifted (lam2(0) = 4.0 = "w2"),
controls with period ratios 5.0, 2.55, 2.15. 200 synodic periods each.
Truth: dense float64 3-body velocity Verlet (truth.c), 600/1200/2400 steps
per inner orbit. Floats throughout; the rung's thresholds are frozen.
"""
import json, math, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
TWO_PI = 2.0 * math.pi
M2 = 3.0e-3
A1, E1_0, W1, LAM1 = 1.0, 0.01, 0.0, 0.0

def case_def(ratio, lam2, e2=0.0, w2=0.0):
    a2 = ratio ** (2.0 / 3.0)
    n2 = a2 ** -1.5
    tsyn = TWO_PI / (1.0 - n2)          # n1 = 1 (a1 = 1, M* = 1)
    return dict(a2=a2, e2=e2, w2=w2, lam2=lam2, n2=n2, tsyn0=tsyn,
                T=200.0 * tsyn, ratio=ratio)

CASES = {
    "R1": case_def(2.0, 0.0),
    "R2": case_def(2.0, 0.0, e2=0.05, w2=4.0),  # phase-shifted case, w2 = 4.0
    "C1": case_def(5.0, 0.0),
    "C2": case_def(2.55, 0.0),
    "C3": case_def(2.15, 0.0),
}
RESONANT = ["R1", "R2"]
CONTROLS = ["C1", "C2", "C3"]
CONFIGS = ["conj-quad", "conj-oct", "averaged", "none"]

# ---------- Kepler machinery (mu = G M* = 1) ----------
def kepler_E(M, e):
    M = M % TWO_PI
    E = M + e * math.sin(M)
    for _ in range(60):
        d = (E - e * math.sin(E) - M) / (1.0 - e * math.cos(E))
        E -= d
        if abs(d) < 1e-14:
            break
    return E

def state_at(el, t):
    """el = (a, e, w, M0, t0); osculating state of the Kepler cycle."""
    a, e, w, M0, t0 = el
    n = a ** -1.5
    M = M0 + n * (t - t0)
    E = kepler_E(M, e)
    cE, sE = math.cos(E), math.sin(E)
    r = a * (1.0 - e * cE)
    nu = 2.0 * math.atan2(math.sqrt(1 + e) * math.sin(E / 2.0),
                          math.sqrt(1 - e) * math.cos(E / 2.0))
    lam = w + nu
    xo, yo = a * (cE - e), a * math.sqrt(1 - e * e) * sE
    vf = n * a * a / r
    vxo, vyo = -vf * sE, vf * math.sqrt(1 - e * e) * cE
    cw, sw = math.cos(w), math.sin(w)
    return dict(lam=lam, nu=nu, r=r,
                x=xo * cw - yo * sw, y=xo * sw + yo * cw,
                vx=vxo * cw - vyo * sw, vy=vxo * sw + vyo * cw,
                dl_dt=math.sqrt(a * (1 - e * e)) / (r * r))

def el_from_rv(x, y, vx, vy):
    r = math.hypot(x, y); v2 = vx * vx + vy * vy; rv = x * vx + y * vy
    a = 1.0 / (2.0 / r - v2)
    ex = (v2 - 1.0 / r) * x - rv * vx
    ey = (v2 - 1.0 / r) * y - rv * vy
    e = math.hypot(ex, ey)
    w = math.atan2(ey, ex)
    nu = math.atan2(y * ex - x * ey, x * ex + y * ey)
    E = 2.0 * math.atan2(math.sqrt(1 - e) * math.sin(nu / 2.0),
                         math.sqrt(1 + e) * math.cos(nu / 2.0))
    return (a, e, w, E - e * math.sin(E), 0.0)  # (a, e, w, M0, t0)

def gauss_legendre(n):
    xs, ws = [], []
    for i in range(1, n + 1):
        z = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, z
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * z * p1 - (k - 1) * p0) / k
            dp = n * (z * p1 - p0) / (z * z - 1.0)
            dz = -p1 / dp
            z += dz
            if abs(dz) < 1e-15:
                break
        xs.append(z); ws.append(2.0 / ((1.0 - z * z) * dp * dp))
    return xs, ws

GL24 = gauss_legendre(24)

def tidal_acc(x, y, Rx, Ry, order):
    """Tidal acceleration of the outer perturber on the inner body, star
    frame, truncated at multipole order l = order (2 = quadrupole, 3 = oct)."""
    R2m = Rx * Rx + Ry * Ry; R = math.sqrt(R2m)
    hx, hy = Rx / R, Ry / R
    dot = x * hx + y * hy
    c = M2 / (R2m * R)
    ax = c * (x - 3.0 * dot * hx); ay = c * (y - 3.0 * dot * hy)
    if order >= 3:
        d = M2 / (R2m * R2m * R)
        ax -= d * (7.5 * dot * dot * hx - 3.0 * dot * x - 1.5 * (x * x + y * y) * hx)
        ay -= d * (7.5 * dot * dot * hy - 3.0 * dot * y - 1.5 * (x * x + y * y) * hy)
    return ax, ay

def oc_el(oc):
    """outer perturber element tuple for state_at (e2 may be nonzero)."""
    return (oc["a2"], oc["e2"], oc["w2"],
            kepler_E(oc["lam2"] - oc["w2"], oc["e2"]), 0.0)

def next_conjunction(el, oel, t_from):
    """smallest t > t_from with (lam1 - lam2) == 2*pi*K (n1 > n2).
    Newton on the wrap-to-pi residual of lam1-lam2-2*pi*K: continuous near
    the root, whose mod-2pi discontinuity sits at +-pi, far from it."""
    n1m = el[0] ** -1.5
    n2m = oel[0] ** -1.5
    D0 = state_at(el, t_from)["lam"] - state_at(oel, t_from)["lam"]
    K = math.floor(D0 / TWO_PI) + 1
    while True:
        t = t_from + max((TWO_PI * K - D0) / max(n1m - n2m, 1e-9), 1e-9)
        for _ in range(50):
            s = state_at(el, t); s2 = state_at(oel, t)
            F = (s["lam"] - s2["lam"] - TWO_PI * K + math.pi) % TWO_PI - math.pi
            if abs(F) < 1e-12:
                break
            t -= F / (s["dl_dt"] - s2["dl_dt"])
        if t > t_from + 1e-9:
            return t
        K += 1   # the targeted crossing is at/behind t_from; take the next one

def run_layer(config, case):
    oc = CASES[case]
    oel = oc_el(oc)
    el = (A1, E1_0, W1, kepler_E(LAM1 - W1, E1_0), 0.0)
    T = oc["T"]
    t = 0.0
    kicks = []
    epochs = [dict(t0=0.0, el=el)]
    t0w = time.time()
    while True:
        tc = next_conjunction(el, oel, t)
        if tc >= T:
            break
        a, e, w, M0, tel = el
        n1 = a ** -1.5
        tsyn = TWO_PI / (n1 - oc["a2"] ** -1.5)
        if config == "none":
            pass
        elif config == "averaged":
            pidot = 0.75 * n1 * M2 * (a / oc["a2"]) ** 3 / (1 - e * e) ** 2 \
                    / (1 - oc["e2"] ** 2) ** 1.5
            prev = epochs[-1]
            M0_at_tc = prev["el"][3] + n1 * (tc - prev["t0"])
            el = (a, e, w + pidot * tsyn, M0_at_tc, tc)
        else:
            order = 2 if config == "conj-quad" else 3
            half = 0.5 * tsyn
            dvx = dvy = 0.0
            for xg, wg in zip(*GL24):
                ti = tc + half * xg
                s = state_at(el, ti)
                s2 = state_at(oel, ti)
                ax, ay = tidal_acc(s["x"], s["y"], s2["x"], s2["y"], order)
                dvx += wg * ax; dvy += wg * ay
            dvx *= half; dvy *= half
            s = state_at(el, tc)
            el = el_from_rv(s["x"], s["y"], s["vx"] + dvx, s["vy"] + dvy)
            el = (el[0], el[1], el[2], el[3], tc)
        if not (0 < el[1] < 0.95 and 0 < el[0] < 3.0):
            raise RuntimeError(f"elements out of range {el} at {tc}")
        epochs.append(dict(t0=tc, el=el))
        lam2c = state_at(oel, tc)["lam"]
        kicks.append(dict(t=tc, e=el[1], psi=lam2c - el[2]))
        t = tc
    wall = time.time() - t0w
    # uniform-in-time sampling: e1 staircase, resonant angle psi
    NS = 4096
    sr = si = 0.0
    maxe = 0.0
    samples = []
    for j in range(NS):
        ts = j * T / NS
        k = _epoch_index(epochs, ts)
        el = epochs[k]["el"]
        if el[1] > maxe:
            maxe = el[1]
        s = state_at(el, ts)
        lam2 = state_at(oel, ts)["lam"]
        psi = (2.0 * lam2 - s["lam"] - el[2]) % TWO_PI
        sr += math.cos(psi); si += math.sin(psi)
        samples.append((ts, el[1], psi))
    conc = math.hypot(sr, si) / NS
    return dict(case=case, config=config, maxe1=maxe, conc=conc,
                nkicks=len(kicks), norb=T / TWO_PI, wall=wall,
                epochs=[(e["t0"], e["el"][0], e["el"][1], e["el"][2]) for e in epochs],
                kicks=kicks, samples=samples)

def _epoch_index(epochs, t):
    lo, hi = 0, len(epochs) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if epochs[mid]["t0"] <= t:
            lo = mid
        else:
            hi = mid - 1
    return lo

# ---------- drivers ----------
def run_truth():
    os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
    sump = os.path.join(HERE, "data", "truth_summary.txt")
    open(sump, "w").close()
    for name, oc in CASES.items():
        for res, mode in (("600", "summary"), ("1200", "summary"), ("2400", "full")):
            out = os.path.join(HERE, "data", f"truth_{name}_{res}.txt") \
                  if mode == "full" else "/dev/null"
            cmd = [os.path.join(HERE, "truth"), repr(A1), repr(E1_0), repr(W1),
                   repr(LAM1), repr(oc["a2"]), repr(oc["e2"]), repr(oc["w2"]),
                   repr(oc["lam2"]), repr(M2), repr(oc["T"]), res, mode, out]
            r = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"{name}/{res}", r.stdout.strip())
            with open(sump, "a") as f:
                f.write(f"{name} {res} {r.stdout.strip()}\n")

def truth_series(name):
    """(t, e1, lam1, varpi1) from the 2400-step full truth samples."""
    rows = []
    with open(os.path.join(HERE, "data", f"truth_{name}_2400.txt")) as f:
        for line in f:
            p = line.split()
            rows.append((float(p[0]), float(p[2]), float(p[3]), float(p[4])))
    return rows

def truth_stats(name):
    e1 = []
    sr = si = 0.0
    with open(os.path.join(HERE, "data", f"truth_{name}_2400.txt")) as f:
        for line in f:
            p = line.split()
            t, a1, e, lam1, w1, a2, e2, lam2, w2 = map(float, p)
            e1.append(e)
            psi = (2.0 * lam2 - lam1 - w1) % TWO_PI
            sr += math.cos(psi); si += math.sin(psi)
    return max(e1), math.hypot(sr, si) / len(e1)

def run_checks():
    """(a) kick-integral quadrature convergence GL24 vs 4xGL48;
    (b) `averaged` precession vs classical quadrupole formula vs truth (C1)."""
    oc = CASES["R1"]
    oel = oc_el(oc)
    el = (A1, E1_0, W1, kepler_E(LAM1 - W1, E1_0), 0.0)
    tc = next_conjunction(el, oel, 0.0)
    n1 = el[0] ** -1.5
    tsyn = TWO_PI / (n1 - oc["a2"] ** -1.5)
    for label, panes in (("GL24", 1), ("4xGL48", 4)):
        dvx = dvy = 0.0
        if panes == 1:
            half = 0.5 * tsyn
            for xg, wg in zip(*GL24):
                ti = tc + half * xg
                s = state_at(el, ti)
                s2 = state_at(oel, ti)
                ax, ay = tidal_acc(s["x"], s["y"], s2["x"], s2["y"], 3)
                dvx += wg * ax; dvy += wg * ay
            dvx *= half; dvy *= half
        else:
            q = tsyn / (2 * panes)
            xs, ws = gauss_legendre(48)
            centres = [(i + 0.5) / panes - 0.5 for i in range(panes)]
            for cc in centres:
                for xg, wg in zip(xs, ws):
                    ti = tc + (cc + xg / (2 * panes)) * tsyn
                    s = state_at(el, ti)
                    s2 = state_at(oel, ti)
                    ax, ay = tidal_acc(s["x"], s["y"], s2["x"], s2["y"], 3)
                    dvx += wg * ax * q; dvy += wg * ay * q
        print(f"kick {label}: |dv| = {math.hypot(dvx, dvy):.8e}")
    res = run_layer("averaged", "C1")
    e = res["epochs"]
    dw = (e[-1][3] - e[0][3]) % TWO_PI
    dt = e[-1][0] - e[0][0]
    print(f"averaged C1: dvarpi/dt = {dw / dt:.6e}")
    print(f"classical quad: {0.75 * M2 / CASES['C1']['a2'] ** 3:.6e}")
    w1s, ts = [], []
    with open(os.path.join(HERE, "data", "truth_C1_2400.txt")) as f:
        for line in f:
            p = line.split()
            ts.append(float(p[0])); w1s.append(float(p[4]))
    dw_t = (w1s[-1] - w1s[0]) % TWO_PI
    print(f"truth C1: dvarpi/dt = {dw_t / (ts[-1] - ts[0]):.6e}")

def write_metrics():
    M = {}
    for cfg in CONFIGS:
        pump, lib, ctrl = [], [], 0.0
        kpo = []
        rows = {}
        for case in CASES:
            law = run_layer(cfg, case)
            tmaxe, tconc = truth_stats(case)
            if case in RESONANT:
                pump.append(law["maxe1"] / tmaxe)
                lib.append(law["conc"] / tconc)
            else:
                r = law["maxe1"] / tmaxe
                if 0.8 <= r <= 1.2:
                    ctrl += 1.0 / 3.0
            kpo.append(law["nkicks"] / law["norb"])
            rows[case] = dict(maxe1=round(law["maxe1"], 6),
                              truth_maxe1=round(tmaxe, 6),
                              conc=round(law["conc"], 4),
                              truth_conc=round(tconc, 4),
                              kicks=law["nkicks"], wall=round(law["wall"], 2))
        kpo.sort()
        M[cfg] = dict(e_pump_ratio_min=min(pump), e_pump_ratio_max=max(pump),
                      libration_ratio_min=min(lib), control_pass_fraction=ctrl,
                      dense_steps=0, kicks_per_orbit=kpo[len(kpo) // 2])
        print(cfg, json.dumps(M[cfg]))
        for c in rows:
            print("   ", c, json.dumps(rows[c]))
    with open(os.path.join(HERE, "metrics.json"), "w") as f:
        json.dump(M, f, indent=1)

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "truth":
        run_truth()
    elif cmd == "layer":
        res = run_layer(sys.argv[2], sys.argv[3])
        for k in ("samples", "epochs", "kicks"):
            res.pop(k)
        print(json.dumps(res))
    elif cmd == "check":
        run_checks()
    elif cmd == "metrics":
        write_metrics()
    elif cmd == "picture":
        import picture_util
        picture_util.main(HERE)
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
