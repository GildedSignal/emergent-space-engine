"""Probe 3: capture at E=1, r0=100, L = 4(1 +/- delta); kill: threshold > 1% from L=4.
Truth (exact Schwarzschild): absorbed iff L < 4."""
import math, time
from gv1 import s2_mass, s4_mass, ic_e1_infall, energy_mass, angmom, PI

def classify(L, eta, order, r0=100.0, maxsteps=500000):
    x, y, wx, wy = ic_e1_infall(L, r0)
    E = energy_mass(x, y, wx, wy)
    Lc = angmom(x, y, wx, wy)
    rmin = math.sqrt(x*x + y*y)
    rmax = rmin
    sqrt = math.sqrt
    for i in range(maxsteps):
        r = sqrt(x*x + y*y)
        dt = eta*r*sqrt(r)
        if order == 2:
            x, y, wx, wy, ab = s2_mass(x, y, wx, wy, dt)
        else:
            x, y, wx, wy, ab = s4_mass(x, y, wx, wy, dt)
        if ab:
            return ("absorbed", rmin, rmax, i, abs(E-1.0), abs(Lc-L))
        r = sqrt(x*x + y*y)
        if r < rmin:
            rmin = r
        if r > rmax:
            rmax = r
        if r > 350.0:
            return ("escaped", rmin, rmax, i, abs(E-1.0), abs(Lc-L))
    return ("timeout", rmin, rmax, maxsteps, abs(E-1.0), abs(Lc-L))

if __name__ == "__main__":
    t0 = time.perf_counter()
    eta = 1/64
    print("== probe 3: E=1 capture from r0=100, eta=1/64 ==")
    print(f"{'L':>9} {'expect':>9} {'ord':>3} {'result':>9} {'r_min':>9} {'steps':>7} {'dE':>8} {'dL':>8}")
    for d in (0.02, 0.01, 0.005):
        for sgn in (-1, 1):
            L = 4.0*(1.0 + sgn*d)
            expect = "absorbed" if L < 4.0 else "escaped"
            for order in (2, 4):
                res, rmin, rmax, st, dE, dL = classify(L, eta, order)
                ok = "OK" if res == expect else "WRONG"
                print(f"{L:9.4f} {expect:>9} {order:3d} {res:>9} {rmin:9.3f} {st:7d} "
                      f"{dE:8.1e} {dL:8.1e}  {ok}")
    print("== bisection of the capture threshold L* (eta=1/64) ==")
    for order in (2, 4):
        lo, hi = 4.0*0.98, 4.0*1.02          # lo captured, hi escaped
        rlo = classify(lo, eta, order)[0]
        rhi = classify(hi, eta, order)[0]
        if rlo != "absorbed" or rhi != "escaped":
            print(f"order={order}: bracket failed: {rlo}/{rhi}")
            continue
        for _ in range(20):
            mid = 0.5*(lo + hi)
            if classify(mid, eta, order)[0] == "absorbed":
                lo = mid
            else:
                hi = mid
        Lstar = 0.5*(lo + hi)
        print(f"order={order}: L* = {Lstar:.6f}  |L*-4|/4 = {abs(Lstar-4.0)/4.0:.2e} "
              f"(kill if > 0.01)")
    print(f"wall: {time.perf_counter()-t0:.1f} s")
