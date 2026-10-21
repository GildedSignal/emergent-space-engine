#!/usr/bin/env python3
"""Falsifier for representation.md L67: "Perturbations (tides, neighbours, inspiral
by Peters' formula) are kicks on E and L", applied once per radial cycle.

Truth : the same Peters (1964) orbit-averaged rates integrated continuously (RK4,
        dt = P/128, stop-time interpolated by secant; convergence vs P/1024 reported).
Letter: zero-order hold -- at each cycle start, apply rate(a,e) * P(a,e) to (a,e).
This isolates the kick-vs-generator channel from the multiply-add jet (df81/6164/ee08).

Stop for both arms: p = a*(1-e^2) <= 6M (the plunge handover band; Peters has no plunge).
Units: G=c=1, M=1.  Target < 5 min single core.
"""
import math, time, json

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
        if pn <= P_END:  # secant on p across this step
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

def run_letter(a0, e0, nu):
    a, e, t, cyc = a0, e0, 0.0, 0
    mx_da, mx_de = 0.0, 0.0
    while a * (1.0 - e * e) > P_END:
        dadt, dedt = rates(a, e, nu)
        P = period(a)
        da, de = dadt * P, dedt * P
        mx_da = max(mx_da, abs(da) / a); mx_de = max(mx_de, abs(de))
        a += da; e += de; t += P; cyc += 1
        if cyc > 2_000_000:
            break
    return t, cyc, a, e, mx_da, mx_de

t0 = time.time()
rows = []
print("controls")
# C1 positive: circular truth vs Peters closed form t = (a0^4 - aend^4)/(4k).
a0c, nu_c = 15.0, 0.25
t_rk, _, _ = run_truth(a0c, 0.0, nu_c)
k = (64.0 / 5.0) * nu_c * M * M * M
t_cf = (a0c ** 4 - 6.0 ** 4) / (4.0 * k)
c1 = abs(t_rk - t_cf) / t_cf
print(f"[C1] circular truth vs closed form: {c1:.3e} (bar < 1e-9)")

# C2 convergence at the two stiffest eccentric cases.
convs = {}
for (p0, e0) in [(15.0, 0.0), (15.0, 0.9), (65.0, 0.9)]:
    a0 = p0 / (1.0 - e0 * e0)
    tA, _, _ = run_truth(a0, e0, 0.25, SPC)
    tB, _, _ = run_truth(a0, e0, 0.25, 1024)
    convs[f"p{p0:.0f}e{e0}"] = abs(tA - tB) / tB
print("[C2] truth P/128 vs P/1024: " + ", ".join(f"{kk} {vv:.2e}" for kk, vv in convs.items()))

# C3 negative: the letter must differ by > 1% in the strong-field circular band.
tl, cyc_l, al, el, _, _ = run_letter(15.0, 0.0, 0.25)
c3 = abs(tl - t_cf) / t_cf
print(f"[C3] letter vs closed form at 15M circular: {c3:.3e} (bar > 0.01)")

# ---- held-out plane --------------------------------------------------------
P0 = [15.0, 20.0, 30.0, 50.0, 65.0, 100.0, 200.0]
E0 = [0.0, 0.3, 0.6, 0.9]
print(f"\n{'p0/M':>6} {'e0':>4} {'nu':>5} | {'t_truth':>12} {'t_letter':>12} {'dtt%':>8} "
      f"{'cyc_t':>9} {'cyc_l':>7} {'dcyc%':>8} {'maxDa/a':>9} {'p_end_l':>8} {'sign':>6}")
for nu in (0.25, 0.5):
    for p0 in P0:
        for e0 in E0:
            a0 = p0 / (1.0 - e0 * e0)
            tt, at, et, ct = run_truth(a0, e0, nu, count_cycles=True)
            tl, cyc_l, al, el, mx, mde = run_letter(a0, e0, nu)
            dtt = (tl - tt) / tt
            pl_end = al * (1.0 - el * el)
            print(f"{p0:6.0f} {e0:4.1f} {nu:5.2f} | {tt:12.4e} {tl:12.4e} {100*dtt:8.2f} "
                  f"{ct:9.1f} {cyc_l:7d} {100*(cyc_l - ct)/ct:8.2f} {mx:9.2e} "
                  f"{pl_end:8.2f} {'late' if dtt > 0 else 'early':>6}")
            q0 = abs(rates(a0, e0, nu)[0]) * period(a0) / a0
            rows.append(dict(p0=p0, e0=e0, nu=nu, t_truth=tt, t_letter=tl, dt_rel=dtt,
                             cycles_truth=ct, cycles_letter=cyc_l,
                             dcyc_rel=(cyc_l - ct) / ct, max_da_over_a=mx, max_de=mde,
                             q0=q0, p_end_letter=pl_end, e_end_truth=et, e_end_letter=el))
    if nu == 0.25:
        print("-" * 106)

with open("peters_out.json", "w") as f:
    json.dump(dict(rows=rows, c1=c1, c3=c3, conv=convs), f, indent=1)
print(f"\nwall {time.time()-t0:.1f} s")
