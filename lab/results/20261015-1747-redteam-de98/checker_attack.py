#!/usr/bin/env python3
"""Checker adversarial cases for de98. Imports the author's instrument as-is."""
import sys, json
import numpy as np
sys.path.insert(0, ".")
import eob_doll as I

print("== 0. doll closed form (exact Schwarzschild): k = (1-6/L^2)^-1/2 - 1 ==")
worst = 0.0
for pb, e, nu in [(20, 0.6, 0.25), (50, 0.1, 0.25), (120, 0.9, 0.01), (15, 0.3, 0.1)]:
    lab = I.adm_orbit_label(pb, e, nu)
    hhat, j = lab
    E = 1.0 + hhat + 0.5 * nu * hhat * hhat
    dq = I.doll_k_T(E, j)
    kcf = (1.0 - 6.0 / (j * j)) ** -0.5 - 1.0
    rel = abs(dq[0] - kcf) / kcf
    worst = max(worst, rel)
    print(f"  pbar={pb} e={e}: quad={dq[0]:.10f} closed={kcf:.10f} rel={rel:.2e}")
print(f"  worst doll-half error: {worst:.2e}")

print("== 1. derived quantities vs dossier claims ==")
d = json.load(open("eob_data.json"))
sw = d["sweep"]
for pb in (50, 80, 120, 30):
    row = [s for s in sw if s["nu"] == 0.25 and s["pbar"] == pb]
    base = [s.get("ek_base") for s in row]
    cor = [s["ek"] - s.get("ek_base") for s in row if "ek" in s and s.get("ek_base") is not None]
    print(f"  pbar={pb}: baseline range {min(base)*100:+.2f}%..{max(base)*100:+.2f}%  corrected {min(cor)*100:+.2f}..{max(cor)*100:+.2f}%")
# nu-ratio at fixed pbar,e
for pb, e in [(50, 0.3), (80, 0.6), (120, 0.1)]:
    r25 = [s for s in sw if s["nu"] == 0.25 and s["pbar"] == pb and s["e"] == e][0]
    r01 = [s for s in sw if s["nu"] == 0.01 and s["pbar"] == pb and s["e"] == e][0]
    c25 = r25["ek"] - r25["ek_base"]; c01 = r01["ek"] - r01["ek_base"]
    print(f"  nu-ratio at pbar={pb},e={e}: {c25/c01:.1f}")
# pbar^2 scaling at fixed e,nu between 50 and 100-ish
r50 = [s for s in sw if s["nu"] == 0.25 and s["pbar"] == 50 and s["e"] == 0.6][0]
r120 = [s for s in sw if s["nu"] == 0.25 and s["pbar"] == 120 and s["e"] == 0.6][0]
c50 = r50["ek"] - r50["ek_base"]; c120 = r120["ek"] - r120["ek_base"]
print(f"  pbar-scaling e=0.6 nu=0.25: err(50)/err(120)={c50/c120:.2f} (p^2 predicts {(120/50)**2:.2f})")

print("== 2. next decade: pbar 200, 400 (outside the author's sweep) ==")
for pb in (200, 400):
    for nu in (0.25, 0.01):
        r = I.compare(pb, 0.6, nu)
        c = r["ek"] - r["ek_base"]; b = r["ek_base"]
        print(f"  pbar={pb} e=0.6 nu={nu}: corrected={c*100:+.3f}% baseline={b*100:+.3f}%")

print("== 3. off-grid nu: 0.2 and 0.05 at pbar=50, e=0.6 (nu-linearity) ==")
r25 = I.compare(50, 0.6, 0.25); r2 = I.compare(50, 0.6, 0.2); r05 = I.compare(50, 0.6, 0.05)
c25 = r25["ek"] - r25["ek_base"]; c2 = r2["ek"] - r2["ek_base"]; c05 = r05["ek"] - r05["ek_base"]
print(f"  corrected: nu=0.25 {c25*100:+.3f}%  nu=0.2 {c2*100:+.3f}%  nu=0.05 {c05*100:+.3f}%")
print(f"  c(0.25)/c(0.05)={c25/c05:.1f} (linear predicts 5.0)")

print("== 4. extreme e=0.99 (outside e<=0.9) ==")
for pb in (30, 50):
    r = I.compare(pb, 0.99, 0.25)
    if "ek" in r:
        print(f"  pbar={pb} e=0.99 nu=0.25: corrected={(r['ek']-r['ek_base'])*100:+.2f}% baseline={r['ek_base']*100:+.2f}%")
    else:
        print(f"  pbar={pb} e=0.99: label/plunge status: fab={r.get('doll_plunge_fabricated')}")

print("== 5. baseline convergence nu=1e-6 vs 1e-9 at pbar=50,30 ==")
for pb in (50, 30):
    l6 = I.adm_orbit_label(pb, 0.6, 1e-6); l9 = I.adm_orbit_label(pb, 0.6, 1e-9)
    k6 = I.adm_k_T(*l6, 1e-6)[0]; k9 = I.adm_k_T(*l9, 1e-9)[0]
    print(f"  pbar={pb}: k_ADM(nu=1e-6)={k6:.8f} k_ADM(nu=1e-9)={k9:.8f} rel diff={abs(k6-k9)/abs(k9):.1e}")

print("== 6. ADM quadrature vs fixed RK (the author's broken C1b) ==")
from scipy.integrate import solve_ivp
def rk_adm_fixed(hhat, j, nu, tmax=4000.0):
    g = lambda r: I.H_adm(r, 0.0, j, nu, 2) - hhat
    tp = I.solve_turning(g, *I.newton_turning_guesses(hhat, j))
    if tp is None: return None
    rp = tp[0]
    def rhs(t, y):
        r, phi, pr_ = y
        return [I.dH('pr', r, pr_, j, nu, 2), I.dH('j', r, pr_, j, nu, 2), -I.dH('r', r, pr_, j, nu, 2)]
    def peri(t, y): return y[2]
    peri.direction = 1; peri.terminal = True
    s0 = solve_ivp(rhs, [0, 0.05], [rp, 0.0, 1e-12], rtol=1e-12, atol=1e-14, dense_output=False)
    sol = solve_ivp(rhs, [0.05, tmax], s0.y[:, -1], events=peri, rtol=1e-12, atol=1e-14, max_step=0.05)
    if len(sol.t_events[0]) < 2: return None
    return sol.t_events[0][1] / (2 * np.pi) - 1
for pb, e, nu in [(20, 0.6, 0.25), (50, 0.6, 0.25), (30, 0.6, 0.25), (20, 0.6, 1e-6)]:
    hhat, j = I.adm_orbit_label(pb, e, nu)
    q = I.adm_k_T(hhat, j, nu)
    kr = rk_adm_fixed(hhat, j, nu)
    if q and kr:
        print(f"  pbar={pb} nu={nu}: quad k={q[0]:.8f} RK k={kr:.8f} rel={abs(q[0]-kr)/abs(kr):.2e}")
    else:
        print(f"  pbar={pb} nu={nu}: quad={q[0] if q else None} RK={kr} (RK failed)")

print("== 7. re-derive the three un-regenerated controls ==")
# (a) Newtonian closure: k of pure Kepler problem is 0 -> use 1PN-free reduction is impossible
#     with H_adm; instead verify the transcription: 2PN test-particle limit in isotropic coords
#     expanded matches H_exact isotropic test-mass Hamiltonian to 2PN order symbolically-ish:
#     check nu=0 1PN term -3/8 p^4 - 3/(2r) p^2 + 1/(2r^2) matches expansion of exact isotropic H.
#     Exact test-mass Hamiltonian in isotropic Schwarzschild (M=1): H = (1-1/(2r))^2 sqrt(1 + p^2 (1+1/(2r))^4 / (1-1/(2r))^2) - 1 ... use E relation:
#     (1-1/(2r))^2 (1+p^2 (1+1/(2r))^4)/( (1+1/(2r))^2 ... ) -- do it numerically instead:
def H_exact_iso(r, pr, j):
    # exact Schwarzschild in isotropic coords, M=1: alpha=(1-1/2r)/(1+1/2r); gamma=(1+1/2r)^2... hmm
    # Energy: E^2 = alpha^2 + (p^2 gamma^2 ... )/... we use the standard form:
    # E^2 = ((1-1/(2r))^2/(1+1/(2r))^2) * (1 + p^2 (1+1/(2r))^4)
    # with p^2 = pr^2 + j^2/r^2. H = E - 1.
    w = 0.5 / r
    p2 = pr * pr + j * j / (r * r)
    E2 = ((1 - w) ** 2 / (1 + w) ** 2) * (1 + p2 * (1 + w) ** 4)
    return np.sqrt(E2) - 1.0
r, pr, j = 12.0, 0.3, 4.4
h2pn = I.H_adm(r, pr, j, 0.0, 2)
hexa = H_exact_iso(r, pr, j)
print(f"  (a) nu=0: H_ADM2PN={h2pn:.8f} H_exact_iso-1={hexa:.8f} (2PN truncation gap {abs(h2pn-hexa):.2e} = expected O(3PN))")
print("      NOTE: H_adm(nu=0) includes the constant +? -- check Newtonian level:")
h0 = 0.5 * (pr*pr + j*j/(r*r)) - 1.0/r
print(f"      H_N={h0:.8f}; exact-Newtonian gap {abs(h0 - (np.sqrt(((1-0.5/r)**2/(1+0.5/r)**2)*(1+(pr**2+j**2/r**2)*(1+0.5/r)**4))-1)):.2e}")
# (b) weak field: doll quadrature at large pbar vs series
lab = I.adm_orbit_label(100, 0.3, 1e-9)
hhat, j = lab
E = 1.0 + hhat + 0.5e-9 * hhat * hhat
kq = I.doll_k_T(E, j)[0]
print(f"  (b) weak field pbar=100 e=0.3: k_quad={kq:.6f} series 3/p+27/2p^2={3/100+27/2/1e4:.6f} exact-closed-form(L)={(1-6/j**2)**-0.5-1:.6f} L^2={j*j:.4f}")
# (c) turning-point coordinate map at nu->0 for pbar=20, e=0.6
l0 = I.adm_orbit_label(20, 0.6, 1e-6)
h0v, j0 = l0
E0 = 1.0 + h0v + 0.5e-6 * h0v * h0v
tp_adm = I.solve_turning(lambda r: I.H_adm(r, 0.0, j0, 1e-6, 2) - h0v, *I.newton_turning_guesses(h0v, j0))
tp_dol = I.doll_turning(E0, j0)
map_iso_to_areal = lambda r: r * (1 + 0.5 / r) ** 2
print(f"  (c) nu=1e-6 pbar=20 e=0.6: ADM tp(iso)={tp_adm} -> areal {map_iso_to_areal(tp_adm[0]):.2f},{map_iso_to_areal(tp_adm[1]):.2f}; doll tp(areal)={tp_dol[0]:.2f},{tp_dol[1]:.2f}")
