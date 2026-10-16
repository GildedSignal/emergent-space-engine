"""Probe 1 + 5: precession vs oracle, and events (steps) per orbit against p."""
import math, time
from gv1 import (s2_mass, s4_mass, ic_bound_periapsis, energy_mass, angmom,
                 periapsis_advance_gr, PI)

def run_bound(p, e, eta, order, korbits, maxfact=80.0):
    x, y, wx, wy, E0, L0, sc = ic_bound_periapsis(p, e)
    T = 0.0
    phi = 0.0
    ph_prev = 0.0
    steps = 0
    absorbed = False
    periT = [0.0]
    periPhi = [0.0]
    pts = []
    maxsteps = int(maxfact*korbits/eta) + 1000
    sqrt = math.sqrt
    atan2 = math.atan2
    twopi = 2.0*PI
    s2 = s2_mass
    s4 = s4_mass
    while len(periPhi) < korbits + 1 and steps < maxsteps:
        r = sqrt(x*x + y*y)
        dt = eta*r*sqrt(r)
        if order == 2:
            x, y, wx, wy, ab = s2(x, y, wx, wy, dt)
        else:
            x, y, wx, wy, ab = s4(x, y, wx, wy, dt)
        if ab:
            absorbed = True
            break
        T += dt
        steps += 1
        ph = atan2(y, x)
        d = ph - ph_prev
        if d > PI:
            d -= twopi
        elif d < -PI:
            d += twopi
        phi += d
        ph_prev = ph
        p3 = (T, sqrt(x*x + y*y), phi)
        if len(pts) >= 2:
            (ta, ra, fa), (tb, rb, fb) = pts[-2], pts[-1]
            tc, rc, fc = p3
            if ra > rb and rb <= rc:      # local min at b
                d1 = (rb - ra)/(tb - ta)
                d2 = (rc - rb)/(tc - tb)
                cc = (d2 - d1)/(tc - ta)
                if cc > 0.0:
                    ts = 0.5*(ta + tb) - d1/(2.0*cc)
                    fs = fb + (fb - fa)/(tb - ta)*(ts - tb)
                    periT.append(ts)
                    periPhi.append(fs)
                pts = [p3]
            else:
                pts.append(p3)
                if len(pts) > 3:
                    pts = pts[-3:]
        else:
            pts.append(p3)
    n = len(periPhi) - 1
    Ef = energy_mass(x, y, wx, wy)
    Lf = angmom(x, y, wx, wy)
    return {
        "n_orbits": n, "advance": (periPhi[n] - periPhi[0])/n - twopi if n > 0 else float("nan"),
        "steps_per_orbit": steps/n if n else float("nan"),
        "T_orbit": periT[n]/n if n else float("nan"),
        "E_drift": (Ef - E0)/E0, "L_drift": (Lf - L0)/L0, "absorbed": absorbed,
        "ic_check": sc, "steps": steps,
    }

if __name__ == "__main__":
    t0 = time.perf_counter()
    print("== probe 1: periapsis advance vs oracle ==")
    print(f"{'p':>7} {'e':>4} {'eta':>7} {'ord':>3} {'orbits':>7} {'adv_law':>12} "
          f"{'adv_GR':>12} {'rel_err':>10} {'steps/orb':>9} {'E_drift':>10} {'L_drift':>10}")
    rows = []
    for (p, e, K) in [(20.0, 0.2, 24), (20.0, 0.5, 24), (100.0, 0.2, 30), (100.0, 0.5, 30),
                      (1000.0, 0.2, 120), (1000.0, 0.5, 120)]:
        agr = periapsis_advance_gr(p, e)
        for eta in (1/16, 1/32, 1/64, 1/128):
            for order in (2, 4):
                r = run_bound(p, e, eta, order, K)
                rel = abs(r["advance"] - agr)/agr
                rows.append((p, e, eta, order, r, agr, rel))
                print(f"{p:7.0f} {e:4.1f} {eta:7.4f} {order:3d} {r['n_orbits']:7d} "
                      f"{r['advance']:12.6f} {agr:12.6f} {rel:10.2e} "
                      f"{r['steps_per_orbit']:9.1f} {r['E_drift']:10.2e} {r['L_drift']:10.2e}")
    # convergence of the error in eta (slope -2 for order 2, -4 for order 4)
    print("== eta-convergence of precession error (log-log slopes) ==")
    for (p, e) in [(20.0, 0.2), (20.0, 0.5), (1000.0, 0.2), (1000.0, 0.5)]:
        for order in (2, 4):
            xs, ys = [], []
            for eta in (1/16, 1/32, 1/64, 1/128):
                rel = [rr[6] for rr in rows if rr[0] == p and rr[1] == e
                       and rr[2] == eta and rr[3] == order][0]
                xs.append(math.log(1.0/eta))
                ys.append(math.log(rel))
            n = len(xs)
            mx = sum(xs)/n; my = sum(ys)/n
            slope = sum((a-mx)*(b-my) for a, b in zip(xs, ys))/sum((a-mx)**2 for a in xs)
            print(f"p={p:6.0f} e={e:.1f} order={order}: error ~ eta^(-{slope:5.2f}) "
                  f"(expect {order})")
    print("== probe 5: events per orbit vs p (eta=1/64 and 1/128, order 2) ==")
    print(f"{'p':>7} {'e':>4} {'eta':>7} {'steps/orbit':>12} {'T_orbit':>12} {'2pi/eta':>9}")
    for (p, e, K) in [(20.0, 0.2, 24), (20.0, 0.5, 24), (100.0, 0.2, 30), (100.0, 0.5, 30),
                      (1000.0, 0.2, 120), (1000.0, 0.5, 120)]:
        for eta in (1/64, 1/128):
            r = run_bound(p, e, eta, 2, K)
            print(f"{p:7.0f} {e:4.1f} {eta:7.4f} {r['steps_per_orbit']:12.1f} "
                  f"{r['T_orbit']:12.2f} {2*PI/eta:9.1f}")
    print(f"wall: {time.perf_counter()-t0:.1f} s")
