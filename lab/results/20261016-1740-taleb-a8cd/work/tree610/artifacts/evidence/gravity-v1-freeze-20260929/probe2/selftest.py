"""Self-tests for gv1b: oracles, exact landing, no-crossing identity, C2 pick,
reversibility contrast (C1 vs C2), light pipeline validation, river linearity,
throughput benchmark."""
import math, time
import gv1b as G

t0 = time.perf_counter()

print("== 1. oracle spot checks (frozen numbers from the earlier probe) ==")
checks = [
    ("adv(20,0.2)", G.periapsis_advance_gr(20.0, 0.2), 1.227808, 1e-5),
    ("adv(20,0.5)", G.periapsis_advance_gr(20.0, 0.5), 1.233862, 1e-5),
    ("adv(1000,0.2)", G.periapsis_advance_gr(1000.0, 0.2), 0.018935, 1e-4),
    ("defl(10)", G.deflection_gr(10.0), 0.590396, 1e-5),
    ("defl(30)", G.deflection_gr(30.0), 0.1482, 2e-3),
    ("rturn(10)", G.null_turning_radius(10.0), 8.788851, 1e-6),
]
for name, got, want, tol in checks:
    ok = abs(got - want)/abs(want) < tol
    print(f"  {name:16s} got={got:.9f} want={want:.6f} rel={abs(got-want)/abs(want):.2e} "
          f"{'OK' if ok else 'FAIL'}")
r_ = G.null_turning_radius(10.0)
resid = r_*r_/(1.0 - 2.0/r_) - 100.0
ser = 4.0/30.0 + 15.0*math.pi/(4.0*30.0*30.0)
print(f"  rturn residual r^2/(1-2/r)-b^2 = {resid:.2e}; defl(30) vs series = "
      f"{abs(G.deflection_gr(30.0)-ser)/G.deflection_gr(30.0):.2e}")

print("== 2. C1 with no crossings == plain fixed-Delta S2 (p=20, e=0.2, eta=1/64) ==")
eta = 1.0/64.0
x1, y1, w1x, w1y, E0, L0 = G.ic_bound_periapsis(20.0, 0.2)
x2, y2, w2x, w2y = x1, y1, w1x, w1y
dt_fix = eta*G.T32[4]
maxdiff = 0.0
cr_tot = 0
for i in range(3000):
    x1, y1, w1x, w1y, k, dT, ev, cr, ab = G.c1_step(x1, y1, w1x, w1y, 4, eta, 2, False)
    cr_tot += cr
    x2, y2, w2x, w2y, ab2 = G.s2_mass(x2, y2, w2x, w2y, dt_fix)
    d = max(abs(x1-x2), abs(y1-y2), abs(w1x-w2x), abs(w1y-w2y))
    if d > maxdiff:
        maxdiff = d
print(f"  max state diff over 3000 steps: {maxdiff:.3e} (crossings seen: {cr_tot}) "
      f"{'OK' if maxdiff < 1e-9 and cr_tot == 0 else 'FAIL'}")

print("== 3. exact landing (p=20, e=0.5, eta=1/16: crossings must be exact) ==")
x, y, wx, wy, E0, L0 = G.ic_bound_periapsis(20.0, 0.5)
worst = 0.0
ncr = 0
for i in range(4000):
    x, y, wx, wy, k, dT, ev, cr, ab = G.c1_step(x, y, wx, wy, 4, 1.0/16.0, 4, False)
    if cr:
        ncr += cr
        r = math.sqrt(x*x + y*y)
        m = round(math.log2(r))
        worst = max(worst, abs(r - 2.0**m)/2.0**m)
print(f"  crossings: {ncr}, worst |r-2^m|/2^m after landing: {worst:.3e} "
      f"{'OK' if worst < 1e-14 else 'FAIL'}")

print("== 4. C2 midpoint-cell pick: distribution over one orbit (p=20, e=0.5) ==")
from collections import Counter
for eta in (1.0/16.0, 1.0/64.0):
    x, y, wx, wy, E0, L0 = G.ic_bound_periapsis(20.0, 0.5)
    k = G.shell_of(x)
    picks = Counter()
    finer = 0
    for i in range(2000):
        kshell = G.shell_of(math.sqrt(x*x + y*y))
        x, y, wx, wy, k, dT, ev, cr, ab = G.c2_step(x, y, wx, wy, kshell, eta, 2, False)
        picks[k] += 1
        if k < kshell:
            finer += 1
    print(f"  eta={eta:.4f}: chosen cells {dict(picks)}, "
          f"finer-than-position: {finer/2000:.3f}")

print("== 5. split-map consistency: S(-dt) o S(dt) = Id (palindromic S2/S4) ==")
# A pure momentum flip is NOT time reversal for the river split (the river
# keeps its direction), so trajectory retracing is not a symmetry here.  The
# testable identity is composition inversion; the Yoshida palindrome makes it
# hold for S4 as well.
x0, y0, wx0, wy0, E0, L0 = G.ic_bound_periapsis(20.0, 0.5)
for order, fn in ((2, G.s2_mass), (4, G.s4_mass)):
    x, y, wx, wy = x0, y0, wx0, wy0
    for _ in range(50):
        x, y, wx, wy, ab = fn(x, y, wx, wy, 0.37)
    for _ in range(50):
        x, y, wx, wy, ab = fn(x, y, wx, wy, -0.37)
    res = max(abs(x-x0), abs(y-y0), abs(wx-wx0), abs(wy-wy0))
    print(f"  o{order}: roundtrip residual = {res:.3e} {'OK' if res < 1e-9 else 'FAIL'}")

print("== 6. light pipeline validation: C3 fixed dt=0.5, o4, from r0=1e4 ==")
eta_val = 0.5/G.RREF32
for b in (10.0, 30.0):
    d, ev, cr, ab, bdr = G.run_photon_r0("C3", 4, eta_val, b)
    agr = G.deflection_gr(b)
    print(f"  b={b:5.1f}: delta={d:.8f} oracle={agr:.8f} rel={abs(d-agr)/agr:.2e} "
          f"steps={ev} b_drift={bdr:.1e} {'OK' if abs(d-agr)/agr < 1e-4 else 'FAIL'}")

print("== 7. river free fall under C1 cells (u=0: r^{3/2} exactly linear) ==")
x, y, wx, wy = 100.0, 0.0, 0.0, 0.0
T = 0.0
for _ in range(25):
    x, y, wx, wy, k, dT, ev, cr, ab = G.c1_step(x, y, wx, wy, 6, 1.0/64.0, 2, False)
    if ab:
        print("  ABSORBED unexpectedly")
        break
    T += dT
r = math.sqrt(x*x + y*y)
want = 100.0*math.sqrt(100.0) - G.CB2*T
print(f"  r^(3/2) = {r*math.sqrt(r):.9f} vs {want:.9f} "
      f"{'OK' if abs(r*math.sqrt(r)-want) < 1e-6 else 'FAIL'}")

print("== 8. throughput (steps/s, p=20 e=0.5) ==")
for cfg in ("C1", "C2", "C3"):
    for order in (2, 4):
        x, y, wx, wy, E0, L0 = G.ic_bound_periapsis(20.0, 0.5)
        step = G.STEPPERS[cfg]
        k = G.shell_of(x)
        t1 = time.perf_counter()
        n = 0
        while time.perf_counter() - t1 < 0.8:
            for _ in range(200):
                x, y, wx, wy, k, dT, ev, cr, ab = step(x, y, wx, wy, k, 1.0/32.0, order, False)
            n += 200*ev
        print(f"  {cfg} o{order}: {n/(time.perf_counter()-t1)/1000:.0f}k S2-steps/s")

print(f"self-test wall: {time.perf_counter()-t0:.2f} s")
