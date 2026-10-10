#!/usr/bin/env python3
"""Controls for r1w_run.py (each <= 60 s). Commands are inline in controls.txt."""
import math, sys
import numpy as np
import r1w_run as R

print("C1. determinism of metrics.json is checked outside this script (hash compare).")
print("C2. shipped-record tie-out is repro-output.txt vs shipped-probe-output.txt (diff, host line only).")

# C3: (8, 0.95) first-cycle deviation, the shipped probe's P5 case (it saw 1.17e-11)
u0, L2, E = R.setup_bound(8.0, 0.95)
s = dict(rp=8.0, e=0.95, u0=u0, L2=L2, E=E, ua=u0 * (1 - 0.95) / 1.95)
r = R.banded_bound_case(s, 16, n_cycles=40)
med = sorted(r['cyc_d'])[len(r['cyc_d']) // 2]
dev = max(abs(x - r['cyc_d'][0]) / r['cyc_d'][0] for x in r['cyc_d'][1:])
devm = max(abs(x - med) / med for x in r['cyc_d'])
print(f"C3. (8,0.95) m16, 40 cycles: max dev from cycle1 = {dev:.2e}, from median = {devm:.2e} "
      f"(shipped probe P5 saw 1.17e-11 from median)")

# C4: banded period quadrature: Gauss-8 (in r1w_run) vs Gauss-16 on the worst case (7,0.99) at m32
u0, L2, E = R.setup_bound(7.0, 0.99)
L = math.sqrt(L2)
bands = R.Bands(32, L2=L2)
def sweep_quad(ng):
    xs, ws = np.polynomial.legendre.leggauss(ng)
    u, up, t = u0, 0.0, 0.0
    n = 0
    while n < 3:
        st, dphi, kind, ue = R.next_event(bands, u, up, ((s['ua'] if False else u0 * 0.01 / 1.99) / 4.0, 'escape'))
        if st[0] == 'e':
            _, k, w, ustar, lo, hi, Rr, th0 = st
            for xg, gw in zip(xs, ws):
                uu = ustar + Rr * math.cos(w * xg * dphi - th0)
                t += gw * R.ft(uu, E, L)
            t *= 1.0  # (scaled below)
            t_per = t  # placeholder
        # do it properly: accumulate per segment
        n += 1
        break
    return None
# simpler: monkeypatch GAUSS8 lists to a 16-node rule and re-run banded_bound_case
g16x, g16w = np.polynomial.legendre.leggauss(16)
R.GAUSS8_X, R.GAUSS8_W = [float(x) * 0.5 + 0.5 for x in g16x], [float(w) * 0.5 for w in g16w]
s2 = dict(rp=7.0, e=0.99, u0=u0, L2=L2, E=E, ua=u0 * 0.01 / 1.99)
r16 = R.banded_bound_case(s2, 32)
R.GAUSS8_X = [0.09501250983763744, 0.2816035507792589, 0.45801677765722737, 0.6178762444026438,
              0.7554044083500303, 0.8656312023878316, 0.9445750230732326, 0.9894009349916499]
R.GAUSS8_W = [0.1894506104550685, 0.18260341504492358, 0.16915651939500254, 0.14959598881657674,
              0.12462897125553394, 0.09515851168249279, 0.062253523938647894, 0.027152459411754095]
r8 = R.banded_bound_case(s2, 32)
print(f"C4. banded period (7,0.99) m32: Gauss-8 {r8['cyc_t'][2]:.6f} vs Gauss-16 {r16['cyc_t'][2]:.6f} "
      f"rel diff {abs(r8['cyc_t'][2]-r16['cyc_t'][2])/r8['cyc_t'][2]:.2e} (model error at this point is 4.75e-3)")

# C5: m-sweep law on the m16 precession-failing low-e seed (r_p=15.70, e=0.0106): does m^-2 hold there too?
u0b, L2b, Eb = R.setup_bound(15.70, 0.0106)
sb = dict(rp=15.70, e=0.0106, u0=u0b, L2=L2b, E=Eb, ua=u0b * (1 - 0.0106) / 1.0106)
i = None
for m in (16, 32, 64):
    r = R.banded_bound_case(sb, m)
    print(f"C5. (r_p=15.70, e=0.0106) m={m}: crossings/cycle={r['crossings']:.0f}", end=" ")
    if i is None:
        pass
# oracle for the same case
dO, tO, _ = R.oracle_bound_vec(np.array([u0b]), np.array([L2b]), np.array([Eb]), np.array([math.sqrt(L2b)]))
pres, pers = [], []
for m in (16, 32, 64):
    r = R.banded_bound_case(sb, m)
    pers.append(abs(r['cyc_t'][2] - tO[0]) / tO[0])
    pres.append(abs((r['cyc_d'][2] - 2 * math.pi) - (dO[0] - 2 * math.pi)) / abs(dO[0] - 2 * math.pi))
slp = float(np.polyfit(np.log([16, 32, 64]), np.log(pres), 1)[0])
slt = float(np.polyfit(np.log([16, 32, 64]), np.log(pers), 1)[0])
print()
print(f"C5. prec errs {pres[0]:.2e}/{pres[1]:.2e}/{pres[2]:.2e} slope {slp:.3f}; "
      f"period errs {pers[0]:.2e}/{pers[1]:.2e}/{pers[2]:.2e} slope {slt:.3f}")
