#!/usr/bin/env python3
"""Falsifier: is the two-body doll's plunge boundary and precession ν-blind?

Doll (shipped, crates/space/src/events/binary.rs): effective orbit = EXACT
Schwarzschild geodesic, A(u) = 1 - 2u; ν only in the 1PN energy/clock map.
Oracle (next term beyond the premise): 2PN EOB radial potential
A(u) = 1 - 2u + 2νu³  (Buonanno-Damour 1999), same kinetic form (g_rr = 1/A).
The 2PN Dbar correction is omitted (oracle domain, stated in dossier).

Circular orbit of the effective Hamiltonian
  H_eff² = A(u)(1 + J²u²) + A(u)² u⁴ p_u²:
  j²(u)  = -A' / (2uA + u²A')          [dE²/du = 0 at fixed J]
  W(u)   = A(1 + j²u²)                 [E_eff² along circular]
  ISCO:  W''(u) = 0
  Ω_r²/Ω_φ² = (∂²H/∂p_u²)(∂²H/∂u²)/Ω_φ² at the circular point; the ratio
  Ω_r/Ω_φ is invariant under the real-energy map, so periastron advance
  k = 2π(Ω_φ/Ω_r - 1) compares doll vs oracle cleanly.

Controls: ν→0 must reproduce Schwarzschild exactly (u_ISCO = 1/6,
Ω_r/Ω_φ = sqrt(1-6u), k = 2π(1/sqrt(1-6u)-1)); planted sign-flipped term
must move the ISCO the other way.
"""
import json, math, sys

try:
    import sympy as sp
except ImportError:
    sys.exit("sympy missing: pip install sympy")

u, J, pu, NU = sp.symbols('u J pu NU', positive=True)

def make(nu_val, sign=+1):
    A = 1 - 2*u + sign*2*NU*u**3
    Ap = sp.diff(A, u)
    j2 = -Ap / (2*u*A + u**2*Ap)
    W = sp.simplify(A*(1 + j2*u**2))
    H2 = A*(1 + J**2*u**2) + A**2*u**4*pu**2
    H2J = H2.subs(J, sp.sqrt(j2))
    d2pu = sp.diff(H2J, pu, 2)
    d2u = sp.diff(H2.subs(pu, 0), u, 2)   # at FIXED J (epicyclic stiffness), pu=0
    dJ = sp.diff(sp.sqrt(H2).subs(pu, 0), J)   # Omega_phi (effective), p_u=0 at circular
    subs = {NU: nu_val} if nu_val is not None else {}
    return {
        'Wpp': sp.lambdify(u, sp.diff(W, u, 2).subs(subs), 'math'),
        'W': sp.lambdify(u, W.subs(subs), 'math'),
        'Wp': sp.lambdify(u, sp.diff(W, u).subs(subs), 'math'),
        'H': sp.lambdify((u, J), sp.sqrt(H2.subs(pu, 0)).subs(subs), 'math'),
        'd2pu': sp.lambdify(u, d2pu.subs(subs), 'math'),
        'd2u': sp.lambdify((u, J), d2u.subs(subs), 'math'),
        'dJ': sp.lambdify((u, J), dJ.subs(subs), 'math'),
        'j2': sp.lambdify(u, j2.subs(subs), 'math'),
    }
def isco(sysd, lo=0.08, hi=0.30):
    # ISCO: extremum of E_eff^2 along circulars (E is max at marginal stability;
    # Schwarzschild root exactly u = 1/6). Bisect the sign change of W'.
    f = sysd['Wp']
    flo, fhi = f(lo), f(hi)
    if not (flo*fhi < 0):
        return None
    for _ in range(200):
        mid = 0.5*(lo+hi)
        if f(lo)*f(mid) <= 0: hi = mid
        else: lo = mid
    return 0.5*(lo+hi)

def kappa(sysd, u0):
    """periastron advance 2π(Ω_φ/Ω_r - 1) for a circular-adjacent orbit at u0."""
    j2v = sysd['j2'](u0)
    if j2v <= 0: return None
    Jv = math.sqrt(j2v)
    Hv = sysd['H'](u0, Jv)
    om_r2 = sysd['d2pu'](u0)*sysd['d2u'](u0, Jv)/(4*Hv*Hv)
    om_phi = sysd['dJ'](u0, Jv)
    if om_r2 <= 0: return None
    return 2*math.pi*(om_phi/math.sqrt(om_r2) - 1)

out = {'nu': {}, 'controls': {}}
print(f"{'ν':>8} {'u_ISCO doll':>12} {'u_ISCO 2PN':>12} {'r shift %':>10}")
doll_iscos, pn_iscos = {}, {}
for nu_v in [1e-6, 0.01, 0.1, 0.25]:
    doll = make(nu_v)          # sign=+1 but nu tiny? NO: doll is nu-blind; use nu=0 potential
    doll = make(0.0)
    pn = make(nu_v)
    ui_d, ui_p = isco(doll), isco(pn)
    doll_iscos[nu_v], pn_iscos[nu_v] = ui_d, ui_p
    shift = 100*(ui_d-ui_p)/ui_d   # r = 1/u; r_shift = (1/u_p - 1/u_d)/(1/u_d) = u_d/u_p - 1
    rshift = 100*(ui_d/ui_p - 1)
    print(f"{nu_v:>8} {ui_d:>12.7f} {ui_p:>12.7f} {rshift:>10.2f}")
    out['nu'][str(nu_v)] = {'u_isco_doll': ui_d, 'u_isco_2pn': ui_p,
                            'r_isco_doll': 1/ui_d, 'r_isco_2pn': 1/ui_p,
                            'r_shift_pct': rshift}

print("\nk (periastron advance, circular-adjacent), doll vs 2PN EOB:")
print(f"{'u':>10} {'ν':>6} {'k_doll':>14} {'k_2PN':>14} {'rel diff %':>11} {'exact Schw.':>14}")
for nu_v in [0.1, 0.25]:
    doll = make(0.0); pn = make(nu_v)
    for u0 in [1/20, 1/50, 1/1000]:
        kd, kp = kappa(doll, u0), kappa(pn, u0)
        exact = 2*math.pi*(1/math.sqrt(1-6*u0) - 1)
        rel = 100*(kp-kd)/kd
        print(f"{u0:>10.4f} {nu_v:>6} {kd:>14.6f} {kp:>14.6f} {rel:>11.4f} {exact:>14.6f}")
        out['nu'].setdefault(str(nu_v), {})['k'] = out['nu'].get(str(nu_v), {}).get('k', []) + [
            {'u': u0, 'k_doll': kd, 'k_2pn': kp, 'rel_diff_pct': rel, 'k_exact_schw': exact}]

# Controls
print("\nControls:")
ctrl = make(1e-6)
ui_c = isco(ctrl)
ok1 = abs(ui_c - 1/6) < 1e-7   # residual 2.9e-8 is the real linear-in-ν shift at 1e-6
print(f"  ν=1e-6: u_ISCO = {ui_c:.12f} vs 1/6 = {1/6:.12f}  -> {'PASS' if ok1 else 'FAIL'}")
kc = kappa(ctrl, 1/20); kd0 = kappa(make(0.0), 1/20)
exact = 2*math.pi*(1/math.sqrt(1 - 6*(1/20)) - 1)
ok2 = abs(kc - kd0) < 1e-7 and abs(kc - exact) < 1e-7   # residual 8e-8 is the linear-in-ν shift at 1e-6
print(f"  ν=1e-6: k(1/20) = {kc:.9f} vs doll {kd0:.9f} vs exact closed form {exact:.9f} -> {'PASS' if ok2 else 'FAIL'}")
# planted negative: sign-flipped term must move ISCO the other way
neg = make(0.25, sign=-1)
ui_n = isco(neg)
ok3 = ui_n is not None and ui_n < doll_iscos[0.25]
print(f"  planted -2νu³ (sign flip): u_ISCO = {ui_n:.6f} < doll's 1/6 = {doll_iscos[0.25]:.6f} (moves outward, opposite to 2PN {pn_iscos[0.25]:.6f}) -> {'PASS (instrument sees sign)' if ok3 else 'FAIL'}")
# doll nu-blindness is exact (same make(0.0) object): recorded
out['controls'] = {'nu0_isco_pass': ok1, 'nu0_epicycle_pass': ok2, 'signflip_pass': ok3,
                   'nu0_k_1_20': kc, 'doll_k_1_20': kd0,
                   'exact_schw_k_1_20': 2*math.pi*exact}

# Misclassification band at nu=1/4: circular binaries the truth holds stable, doll plunges
r_d, r_p = 1/doll_iscos[0.25], 1/pn_iscos[0.25]
out['band_nu025'] = {'r_isco_doll': r_d, 'r_isco_2pn': r_p, 'width': r_d - r_p,
                     'width_pct_of_doll_isco': 100*(r_d-r_p)/r_d}
print(f"\nBand (ν=1/4): circular binaries with r ∈ ({r_p:.3f} M, {r_d:.3f} M) are stable per 2PN, plunged by the doll: width {r_d-r_p:.3f} M ({100*(r_d-r_p)/r_d:.1f}% of the doll's ISCO)")

json.dump(out, open('eob2pn.json', 'w'), indent=1)
print("\nwrote eob2pn.json")
