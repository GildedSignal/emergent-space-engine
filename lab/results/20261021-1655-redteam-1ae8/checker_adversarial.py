#!/usr/bin/env python3
"""Checker adversarial cases for 1ae8. Reuses the author's module verbatim."""
import importlib.util, math, json, time

spec = importlib.util.spec_from_file_location(
    "peters", "lab/results/20261021-1655-redteam-1ae8/peters.py")
# load without executing __main__ body? peters.py runs everything at import.
# Instead: re-implement the 4 functions identically (they are 30 lines).
M = 1.0
P_END = 6.0
SPC = 128

def F(e):
    e2 = e * e
    return (1.0 + (73.0 / 24.0) * e2 + (37.0 / 96.0) * e2 * e2) / (1.0 - e2) ** 3.5

def rates(a, e, nu):
    mu = nu * M
    dadt = -(64.0 / 5.0) * mu * M * M / (a * a * a) * F(e)
    dedt = -(304.0 / 15.0) * e * mu * M * M / (a ** 4) \
           * (1.0 + (121.0 / 304.0) * e * e) / (1.0 - e * e) ** 2.5
    return dadt, dedt

def period(a):
    return 2.0 * math.pi * math.sqrt(a ** 3 / M)

def run_truth(a0, e0, nu, spc=SPC, count_cycles=False):
    a, e, t, c = a0, e0, 0.0, 0.0
    p = a * (1.0 - e * e)
    while p > P_END:
        dt = period(a) / spc
        dadt, dedt = rates(a, e, nu)
        k1a, k1e = dadt, dedt
        k2a, k2e = rates(a + 0.5 * dt * k1a, e + 0.5 * dt * k1e, nu)
        k3a, k3e = rates(a + 0.5 * dt * k2a, e + 0.5 * dt * k2e, nu)
        k4a, k4e = rates(a + dt * k3a, e + dt * k3e, nu)
        an = a + (dt / 6.0) * (k1a + 2 * k2a + 2 * k3a + k4a)
        en = e + (dt / 6.0) * (k1e + 2 * k2e + 2 * k3e + k4e)
        pn = an * (1.0 - en * en)
        if pn <= P_END:
            p0step = p
            s = (p0step - P_END) / (p0step - pn) if p0step != pn else 1.0
            t += s * dt; c += s / spc
            a, e = an, en
            break
        a, e, p = an, en, pn
        t += dt; c += 1.0 / spc
        if a <= P_END * 0.5:
            break
    return (t, a, e, c) if count_cycles else (t, a, e)

def run_letter(a0, e0, nu, sub=1):
    """sub = kicks per radial cycle (sub=1 is the author's letter arm)."""
    a, e, t, cyc = a0, e0, 0.0, 0
    mx = 0.0
    while a * (1.0 - e * e) > P_END:
        dadt, dedt = rates(a, e, nu)
        P = period(a)
        h = P / sub
        for _ in range(sub):
            dadt, dedt = rates(a, e, nu)
            da, de = dadt * h, dedt * h
            mx = max(mx, abs(da) / a)
            a += da; e += de; t += h
        cyc += 1
        if cyc > 2_000_000:
            break
    return t, cyc, a, e, mx

t0 = time.time()
print("=== A: outside e-range, e0=0.99 (next decade of the swept number) ===")
for (p0, nu) in [(30.0, 0.25), (65.0, 0.25), (200.0, 0.25)]:
    e0 = 0.99
    a0 = p0 / (1.0 - e0 * e0)
    tt, at, et, ct = run_truth(a0, e0, nu, count_cycles=True)
    tl, cyc_l, al, el, mx = run_letter(a0, e0, nu)
    print(f"p0={p0:5.0f} e0=0.99 nu={nu}: dtt {100*(tl-tt)/tt:+8.2f}%  cyc {cyc_l} vs {ct:.1f}"
          f"  maxDa/a {mx:.2f}  p_end_letter {al*(1-el*el):+.2f}")

print("\n=== B: outside nu-range, nu=0.01 (extreme mass ratio; galaxy-scale regime) ===")
for (p0, e0) in [(15.0, 0.0), (15.0, 0.9), (65.0, 0.0)]:
    nu = 0.01
    a0 = p0 / (1.0 - e0 * e0)
    tt, at, et, ct = run_truth(a0, e0, nu, count_cycles=True)
    tl, cyc_l, al, el, mx = run_letter(a0, e0, nu)
    line = f"p0={p0:5.0f} e0={e0} nu=0.01: dtt {100*(tl-tt)/tt:+8.3f}%  cyc {cyc_l} vs {ct:.1f}  maxDa/a {mx:.4f}"
    if e0 == 0.0:  # exact closed form cross-check of the truth itself
        k = (64.0 / 5.0) * nu * M ** 3
        t_cf = (a0 ** 4 - P_END ** 4) / (4.0 * k)
        line += f"  | truth vs closed form {100*abs(tt-t_cf)/t_cf:.2e}%  letter vs closed form {100*(tl-t_cf)/t_cf:+.3f}%"
    print(line)

print("\n=== C: circular closed form as RK4-independent oracle (letter error exactly) ===")
for nu in (0.25, 0.5):
    for p0 in (15.0, 20.0, 30.0, 50.0, 65.0, 100.0, 200.0):
        k = (64.0 / 5.0) * nu * M ** 3
        t_cf = (p0 ** 4 - P_END ** 4) / (4.0 * k)
        tl, cyc_l, al, el, mx = run_letter(p0, 0.0, nu)
        print(f"nu={nu} p0={p0:5.0f}: letter vs closed form {100*(tl-t_cf)/t_cf:+7.3f}%  (author's RK4-truth deltas: "
              f"+8.80/+3.97/+1.55/+0.44/+0.23/+0.08/+0.01 at nu=0.25)")

print("\n=== D: sub-cycled kicks (does a modest cadence save the kick form?) ===")
p0, e0, nu = 15.0, 0.9, 0.25
a0 = p0 / (1.0 - e0 * e0)
tt, _, _, ct = run_truth(a0, e0, nu, count_cycles=True)
print(f"truth: t={tt:.4e} cycles={ct:.1f}")
for sub in (1, 2, 4, 8, 16, 32):
    tl, cyc_l, al, el, mx = run_letter(a0, e0, nu, sub=sub)
    print(f"sub={sub:3d} kicks/cycle: dtt {100*(tl-tt)/tt:+8.2f}%  cyc {cyc_l} vs {ct:.1f}  p_end_l {al*(1-el*el):+.2f}")

print("\n=== E: the 0.1% license bar arithmetic (dossier says p0 >= 230M) ===")
# measured circular deltas from THIS script's C arm, fit |dtt| = C * p^-2.5
pts = []
for nu in (0.25,):
    for p0 in (30.0, 50.0, 65.0, 100.0, 200.0):
        k = (64.0 / 5.0) * nu * M ** 3
        t_cf = (p0 ** 4 - P_END ** 4) / (4.0 * k)
        tl, _, _, _, _ = run_letter(p0, 0.0, nu)
        pts.append((p0, abs(tl - t_cf) / t_cf))
for p0, r in pts:
    print(f"p0={p0:5.0f}: |dtt|/q0 = {r / (80.4248 * 0.25 * p0 ** -2.5):.2f}")
import numpy as np
xs = np.array([math.log(p) for p, _ in pts]); ys = np.array([math.log(r) for _, r in pts])
slope = np.polyfit(xs, ys, 1)[0]
r100 = dict(pts)[100.0]
for bar in (1e-3, 1e-4):
    p_bar = 100.0 * (r100 / bar) ** (1.0 / 2.5)
    print(f"bar {bar*100:.2f}% => p0 ~ {p_bar:.0f}M (slope {slope:.2f})")

print(f"\nwall {time.time()-t0:.1f} s")
