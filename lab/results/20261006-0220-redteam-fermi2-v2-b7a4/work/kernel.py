#!/usr/bin/env python3
"""The decisive experiment: the corrected Schwarzschild-Fermi tide kernel table,
window->0, and the epoch rule derived from it.

Three independent paths for the kernel:
  (G) geodesic-only: pair differences of exact members, quadratic fit, Richardson
      in the window h -> 0 (no Riemann code anywhere);
  (S) einsum: coordinate Riemann (sign FIXED: R_{r phi r phi} = -M/r^3) projected
      on the numerically parallel-transported tetrad;
  (C) closed form of run 20261002-0539-q-fermi2-tide-0dee, with
      Phi(tau) = -int omega dtau accumulated independently of the transport.

Epoch rule: re-kick when the held kernel drifts by eps = 2^-8:
  axis rule   N = 256 * int |d(eigenaxis angle)|      (per true orbit / passage)
  tensor rule N = 256 * int ||dE||_F / ||E||_F        (the honest rule)
with exact axis references (unwrap on the doubled angle; no mixed inertial vectors).
"""
import json, math
import numpy as np
import importlib.util

spec = importlib.util.spec_from_file_location("p", "probe-orig.py")
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
M = p.M
TRAP = np.trapz

# ---------------------------------------------------------------- fixed Riemann
_BASE2 = {(0, 1, 0, 1): -2.0, (0, 2, 0, 2): 1.0, (1, 2, 1, 2): -1.0}
RT2 = np.zeros((3, 3, 3, 3))
for a in range(3):
    for b in range(3):
        for c in range(3):
            for d in range(3):
                for perm, chi in p._GRP:
                    q = (a, b, c, d)
                    key = (q[perm[0]], q[perm[1]], q[perm[2]], q[perm[3]])
                    if key in _BASE2:
                        RT2[a, b, c, d] = chi * _BASE2[key]
                        break

# ---------------------------------------------------------------- closed form
def rdot2(E, L, r): return E*E - (1 - 2*M/r)*(1 + L*L/(r*r))

def tide_boosted(E, L, r, s):
    f = 1 - 2*M/r; m = M/r**3; lam = L*L/(r*r); G2 = E*E - f
    rd = s*math.sqrt(max(rdot2(E, L, r), 0.0))
    C22 = m - 3*M*E*E*L*L/(r**5*G2)
    C33 = -2*m + 3*M*f*L*L/(r**5*G2)
    C23 = -3*M*E*L*rd/(r**4*G2)
    C11 = m*(1 + 3*lam)
    return np.array([[C11, 0, 0], [0, C22, C23], [0, C23, C33]])

def omega_cf(E, L, r): return E*L*M/(r*r*(E*E*r + 2*M - r))

def CP(E, L, r, Phi, s):
    """in-plane 2x2 closed-form kernel in the parallel frame at angle Phi."""
    C = tide_boosted(E, L, r, s)          # indices 1,2 <-> (lambda2', lambda3')
    c, sn = math.cos(Phi), math.sin(Phi)
    R = np.array([[c, sn], [-sn, c]])     # parallel = boosted rotated by Phi
    C2 = C[1:, 1:]
    return R @ C2 @ R.T

def unwrap_axis(E):
    th2 = np.arctan2(2*E[:, 0, 1], E[:, 0, 0] - E[:, 1, 1])
    return np.unwrap(th2)/2.0             # unwrap the DOUBLED angle, then halve

# ---------------------------------------------------------------- geodesic path
def einsum_E(origin):
    n = origin.tau.size
    U = np.empty((n, 3)); E1 = np.empty((n, 3)); E2 = np.empty((n, 3))
    for i in range(n):
        r = origin.r[i]
        U[i] = p.to_orth(origin.Y[3:6, i], r)
        E1[i] = p.to_orth(origin.Y[6:9, i], r)
        E2[i] = p.to_orth(origin.Y[9:12, i], r)
    w = M/origin.r**3
    Ehat = np.einsum("acbd,nc,nd->nab", RT2, U, U)
    E = np.empty((n, 2, 2))
    E[:, 0, 0] = w*np.einsum("na,nab,nb->n", E1, Ehat, E1)
    E[:, 0, 1] = w*np.einsum("na,nab,nb->n", E1, Ehat, E2)
    E[:, 1, 0] = E[:, 0, 1]
    E[:, 1, 1] = w*np.einsum("na,nab,nb->n", E2, Ehat, E2)
    return E

def window_E(origin, i0, m_steps, eps):
    """Geodesic-only kernel at tau[i0] over window of m_steps grid steps."""
    n = len(origin.tau)
    idx_w = np.clip(i0 + np.round(np.linspace(0, m_steps, 9)).astype(int), 0, n-1)
    u, e1, e2 = origin.Y[3:6, i0], origin.Y[6:9, i0], origin.Y[9:12, i0]
    P0 = np.array([origin.t[i0], origin.r[i0], origin.ph[i0]])
    h = origin.tau[idx_w[-1]] - origin.tau[idx_w[0]]
    def series(X0):
        P = P0 + X0[0]*e1 + X0[1]*e2
        mem = p.Member(np.concatenate([P, u.copy()]), h + 5.0)
        mem.X0n = float(np.linalg.norm(X0))
        if mem.plunged or not np.all(np.isfinite(mem.rs)): return None
        Xt, prev = [], None
        for i in idx_w:
            out = p.fermi_X(mem, origin, int(i), prev)
            if out is None: return None
            Xt.append(out[0]); prev = (out[1], float(np.linalg.norm(out[0]))+1e-12)
        return np.array(Xt)
    cols = []
    for d in (0, 1):
        sP = series(np.array([eps, 0.0]) if d == 0 else np.array([0.0, eps]))
        sM = series(np.array([-eps, 0.0]) if d == 0 else np.array([0.0, -eps]))
        if sP is None or sM is None: return None
        xi = (sP - sM)/2.0
        tt = origin.tau[idx_w]
        A = np.vstack([tt**0, tt - tt[0], (tt - tt[0])**2]).T
        c = np.linalg.lstsq(A, xi, rcond=None)[0]
        cols.append(2*c[2])
    E = np.empty((2, 2))
    E[:, 0] = -cols[0]/eps; E[:, 1] = -cols[1]/eps
    return 0.5*(E + E.T), h

def richardson(origin, i0, m0, eps):
    """window->0: E(h), E(h/2), E(h/4), E(h/8) then two Richardson levels."""
    m0 = max(16, (m0//16)*16)
    Es, hs = [], []
    for k in range(4):
        out = window_E(origin, i0, m0 >> k, eps)
        if out is None: return None
        E, h = out
        Es.append(E); hs.append(h)
    R = [(4*Es[k+1] - Es[k])/3.0 for k in range(3)]
    Er = (16*R[2] - R[1])/15.0
    return Es, hs, Er

def eig2(E):
    a = 0.5*(E[0, 0] + E[1, 1]); d = 0.5*(E[0, 0] - E[1, 1])
    r = math.hypot(d, E[0, 1])
    return a - r, a + r

def fmt(E):
    return f"[{E[0,0]:+.6f} {E[0,1]:+.6f}; {E[1,1]:+.6f}]"

def relF(A, B):
    return float(np.linalg.norm(A - B)/max(np.linalg.norm(B), 1e-300))

# ---------------------------------------------------------------- scene helpers
def unbound_y0(E, L):
    # periapsis launch: rdot = 0 -> E^2 = f (1 + L^2/r^2); rp = OUTER turning
    # point (largest r with g(r) >= E^2), found by scan + bisection.
    def g(r): return (1 - 2*M/r)*(1 + L*L/(r*r))
    rs = 3.0 + np.arange(0, 197.0, 0.05)
    gs = g(rs)
    cand = rs[gs >= E*E]
    assert cand.size > 0, "no turning point"
    lo = float(cand.max())           # outermost r with g >= E^2 (inside)
    hi = lo + 0.05                   # just outside: g < E^2
    for _ in range(120):
        mid = 0.5*(lo + hi)
        if g(mid) >= E*E: lo = mid
        else: hi = mid
    rp = 0.5*(lo + hi)
    return np.array([0.0, rp, 0.0, E/(1 - 2*M/rp), 0.0, L/rp**2]), rp

def conserved(origin):
    f = 1 - 2*M/origin.r
    E = f*origin.Y[3, :]
    L = origin.r**2*origin.Y[5, :]
    return float(np.median(E)), float(np.median(L)), float(np.std(E)), float(np.std(L))

RESULTS = {"scenes": [], "circ_scan": [], "notes": {}}

print("="*100)
print("PART 1: kernel table (G=geodesic h->0 Richardson, S=einsum fixed sign, C=closed form)")
print("="*100)

def kernel_scene(name, y0, Ecf, Lcf, meas_points, T_label, leak=None):
    o = p.Origin(p.tetradize(y0), T_label, n_dense=4000)
    Es = einsum_E(o)
    Eint, Lint, dE, dL = conserved(o)
    # Phi from closed form along the measured r(tau) (independent of transport)
    om = omega_cf(Ecf, Lcf, o.r)
    Phi = -np.concatenate([[0.0], np.cumsum(0.5*(om[1:] + om[:-1])*np.diff(o.tau))])
    dr = np.gradient(o.r, o.tau); s = np.where(dr >= 0, 1.0, -1.0)
    Cg = np.empty((len(o.tau), 2, 2))
    for i in range(len(o.tau)):
        Cg[i] = CP(Ecf, Lcf, o.r[i], Phi[i], s[i])
    maxSC = max(relF(Cg[i], Es[i]) for i in range(0, len(o.tau), 40))
    # dPhi/dtau (measured from transport) vs closed omega: angle of the closed-form
    # boosted axis lambda2' = v_ph e_r - v_r e_ph in the transported frame
    f_ = 1 - 2*M/o.r
    v_r = dr/Ecf; v_p = Lcf*np.sqrt(f_)/o.r/Ecf
    a1 = np.empty_like(o.tau); a2 = np.empty_like(o.tau)
    for i in range(len(o.tau)):
        r = o.r[i]; f = 1 - 2*M/r
        L2c = np.array([0.0, v_p[i]*math.sqrt(f), -v_r[i]/r])
        a1[i] = p.gdot(L2c, o.Y[6:9, i], r)
        a2[i] = p.gdot(L2c, o.Y[9:12, i], r)
    Phi_meas = np.unwrap(np.arctan2(a2, a1))
    dPhi_num = np.gradient(Phi_meas, o.tau)
    core = slice(50, len(o.tau)-50)
    # angle(lambda2' in P) = -Phi = +int omega dtau  -> tracks +omega
    om_dev = float(np.max(np.abs(dPhi_num[core] - om[core]))/np.max(np.abs(om[core])))
    rec = dict(name=name, tau_end=float(o.tau_end), E_cons=dE, L_cons=dL,
               max_S_vs_C=maxSC, omega_dev=om_dev, points=[])
    print(f"\n-- {name}: tau_end={o.tau_end:.4g} E,L conserved to {dE:.1e},{dL:.1e};"
          f" S-vs-C max relF={maxSC:.2e}; dPhi/dtau+omega rel dev: {om_dev:.2e}")
    for tag, i0, m0 in meas_points:
        eps = min(0.02, 0.004*o.r[i0])
        out = richardson(o, i0, m0, eps)
        if out is None:
            print(f"   {tag}: measurement failed"); continue
        Es_h, hs, Er = out
        r0 = o.r[i0]; w = M/r0**3
        cl = Cg[i0]
        ein = Es[i0]
        lams = np.linalg.eigvalsh(tide_boosted(Ecf, Lcf, r0, float(s[i0])))
        dG = relF(Er, cl); dS = relF(ein, cl)
        seq = [f"{eig2(E)[0]/(2*w):+.5f}@h={h:.3f}" for E, h in zip(Es_h, hs)]
        rec["points"].append(dict(tag=tag, r=float(r0), tau=float(o.tau[i0]),
            E_rich=[[float(x) for x in row] for row in Er],
            E_closed=[[float(x) for x in row] for row in cl],
            relG=dG, relS=dS,
            eig_geo=[float(x) for x in eig2(Er)],
            eig_closed=[float(x) for x in eig2(cl)],
            eig_boosted_closed=[float(x) for x in lams],
            h_seq=[float(h) for h in hs],
            rad_seq_2w=[float(eig2(E)[0]/(2*w)) for E in Es_h]))
        print(f"   {tag:14s} r={r0:7.3f}  G{fmt(Er)} relG={dG:.2e} relS={dS:.2e}")
        print(f"                  eigen/2w G: {eig2(Er)[0]/(2*w):+.5f} {eig2(Er)[1]/(2*w):+.5f}"
              f"  C: {eig2(cl)[0]/(2*w):+.5f} {eig2(cl)[1]/(2*w):+.5f}"
              f"  | seq: {' '.join(seq)}")
        print(f"                  boosted-frame eigs (C11,C22ish,C33ish): {lams}")
    if leak is not None:
        i0, m_full = leak
        w = M/o.r[i0]**3
        out = window_E(o, i0, m_full, min(0.02, 0.004*o.r[i0]))
        if out is not None:
            Efull, hfull = out
            rec["leak_full"] = dict(h=float(hfull), rad_2w=float(eig2(Efull)[0]/(2*w)))
            print(f"   LEAKAGE: full window h={hfull:.3f} radial/2w = {eig2(Efull)[0]/(2*w):+.4f}"
                  f" (h->0 closed: {eig2(Cg[i0])[0]/(2*w):+.4f})")
    RESULTS["scenes"].append(rec)
    return o, Es, Cg, Phi, Ecf, Lcf

# ---- circular scenes
for r0 in (6.0, 4.0, 3.1):
    L = r0*math.sqrt(M/(r0 - 3*M)); Tp = 2*math.pi*r0**2/L
    dtau = (2*math.pi*r0**1.5)/3999
    m_quarter = int(round((Tp/4)/dtau))
    m0 = max(8, int(round(0.02*r0**1.5/dtau)))
    leak = (0, int(round(Tp/dtau))) if r0 == 3.1 else None
    kernel_scene(f"circ-r{r0}", p.circular_y0(r0), (1-2*M/r0)/math.sqrt(1-3*M/r0), L,
                 [("tau=0", 0, m0), ("tau=Tp/4", m_quarter, m0)],
                 2*math.pi*r0**1.5, leak=leak)

# ---- eccentric: the prior run's scene is in fact a rosette (r in [6.5,7.5]);
#      keep it under its true label and add a genuinely eccentric orbit.
L, rp = 3.5, 6.5
Ecc = math.sqrt((1 - 2*M/rp)*(1 + L*L/rp**2))
kernel_scene("rosette-rp6.5-L3.5", p.ecc_y0(rp, L), Ecc, L,
             [("peri", 0, 40), ("outbound", 800, 60)], 2*math.pi*56.3**1.5)
# rp=6.5, ra=20: E^2 = f(ra)(1+L^2/ra^2) = f(rp)(1+L^2/rp^2) -> L
ra = 20.0
L2 = (f_ := (1-2*M/ra)*(1) ) and ((1-2*M/rp) - (1-2*M/ra)) / ((1-2*M/ra)/ra**2 - (1-2*M/rp)/rp**2)
Lc = math.sqrt(L2); Ec = math.sqrt((1-2*M/rp)*(1 + L2/rp**2))
print(f"\n[ecc2: rp=6.5 ra=20 -> L={Lc:.6f} E={Ec:.6f}; check ra root: "
      f"{(1-2*M/ra)*(1+L2/ra**2):.8f} vs E^2={Ec*Ec:.8f}]")
kernel_scene("ecc-rp6.5-ra20", p.ecc_y0(rp, Lc), Ec, Lc,
             [("peri", 0, 40), ("apo", 2216, 80)], 1700.0)

# ---- unbound scenes
y0, rp = unbound_y0(1.0, math.sqrt(18.0))
kernel_scene("parab-rp6", y0, 1.0, math.sqrt(18.0),
             [("peri", 0, 30), ("outbound", 900, 60)], 80.0)
y0A, rpA = unbound_y0(1.05, 6.5)
kernel_scene("hypA-E1.05-L6.5", y0A, 1.05, 6.5, [("peri", 0, 40)], 150.0)
y0B, rpB = unbound_y0(1.2, 6.5)
kernel_scene("hypB-E1.2-L6.5", y0B, 1.2, 6.5, [("peri", 0, 40)], 150.0)

print("\n" + "="*100)
print("PART 2: E-independence at r=20, same L=6.5, E=1.05 vs E=1.2 (closed form + geodesic)")
print("="*100)
for En, nm in ((1.05, "hypA-E1.05-L6.5"), (1.2, "hypB-E1.2-L6.5")):
    y0, rp = unbound_y0(En, 6.5)
    o = p.Origin(p.tetradize(y0), 260.0, n_dense=6000)
    i20 = int(np.argmin(np.abs(o.r - 20.0)))
    dtau = 260.0/5999
    out = richardson(o, i20, max(8, int(round(0.02*20**1.5/dtau))), 0.02)
    Es_h, hs, Er = out
    lam = np.linalg.eigvalsh(tide_boosted(En, 6.5, 20.0, +1))
    print(f"  {nm}: rp={rp:.4f} r(i20)={o.r[i20]:.4f} G-eig(m units): "
          f"{eig2(Er)[0]*8000:+.6f} {eig2(Er)[1]*8000:+.6f}  closed: {lam[0]*8000:+.6f} {lam[1]*8000:+.6f} {lam[2]*8000:+.6f}")
    RESULTS["notes"][f"eindep_{nm}"] = dict(rp=float(rp), r=float(o.r[i20]),
        eig_geo_m=[float(x*8000) for x in eig2(Er)],
        eig_closed_m=[float(x*8000) for x in lam])

print("\n" + "="*100)
print("PART 3: epoch rule (eps=2^-8 per kick; per TRUE orbit)")
print("="*100)
print(f"{'scene':20s} {'axis_true':>9s} {'axis_naive':>10s} {'tensor_C':>9s} {'tensor_S':>9s} {'tensor_exact':>12s}")
print("-"*80)
for r0 in (1000.0, 50.0, 20.0, 10.0, 6.0, 5.0, 4.0, 3.1):
    L = r0*math.sqrt(M/(r0 - 3*M)); Tp = 2*math.pi*r0**2/L
    Ecf = (1 - 2*M/r0)/math.sqrt(1 - 3*M/r0)
    o = p.Origin(p.tetradize(p.circular_y0(r0)), 2*math.pi*r0**1.5, n_dense=1600)
    Es = einsum_E(o)
    ax = unwrap_axis(Es)
    dax = np.gradient(ax, o.tau)
    N_ax_true = 256*TRAP(np.abs(dax), o.tau)*Tp/o.tau_end
    a1 = np.empty_like(o.tau); a2 = np.empty_like(o.tau)
    for i in range(len(o.tau)):
        r = o.r[i]
        rh = np.array([0.0, math.sqrt(1 - 2*M/r), 0.0])
        a1[i] = p.gdot(rh, o.Y[6:9, i], r); a2[i] = p.gdot(rh, o.Y[9:12, i], r)
    th_r = np.unwrap(np.arctan2(a2, a1))
    N_ax_naive = 256*TRAP(np.abs(np.gradient(th_r, o.tau)), o.tau)*Tp/o.tau_end
    Phi = -(math.sqrt(M/r0**3))*o.tau
    Cg = np.stack([CP(Ecf, L, r0, float(Phi[i]), +1) for i in range(len(o.tau))])
    nrm = np.linalg.norm(Cg, axis=(1, 2))
    N_C = 256*TRAP(np.linalg.norm(np.gradient(Cg, o.tau, axis=0), axis=(1, 2))/nrm, o.tau)*Tp/o.tau_end
    nrmS = np.linalg.norm(Es, axis=(1, 2))
    N_S = 256*TRAP(np.linalg.norm(np.gradient(Es, o.tau, axis=0), axis=(1, 2))/nrmS, o.tau)*Tp/o.tau_end
    x = M/r0; f = 1 - 2*x; g = 1 - 3*x
    N_ex = 512*math.pi*math.sqrt(2)*3*f*math.sqrt(g)/math.sqrt((2 - 3*x)**2 + g*g)
    print(f"circ-r{r0:<10g} {N_ax_true:9.0f} {N_ax_naive:10.0f} {N_C:9.0f} {N_S:9.0f} {N_ex:12.1f}")
    RESULTS["circ_scan"].append(dict(r=r0, axis_true=float(N_ax_true), axis_naive=float(N_ax_naive),
                                     tensor_closed=float(N_C), tensor_einsum=float(N_S),
                                     tensor_exact=float(N_ex), Tp=Tp))

def epochs_noncircular(Ecf, Lcf, o):
    om = omega_cf(Ecf, Lcf, o.r)
    Phi = -np.concatenate([[0.0], np.cumsum(0.5*(om[1:] + om[:-1])*np.diff(o.tau))])
    dr = np.gradient(o.r, o.tau); s = np.where(dr >= 0, 1.0, -1.0)
    Cg = np.stack([CP(Ecf, Lcf, o.r[i], Phi[i], float(s[i])) for i in range(len(o.tau))])
    nrm = np.linalg.norm(Cg, axis=(1, 2))
    rate = np.linalg.norm(np.gradient(Cg, o.tau, axis=0), axis=(1, 2))/nrm
    N = 256*TRAP(rate, o.tau)
    ax = unwrap_axis(Cg)
    Nax = 256*TRAP(np.abs(np.gradient(ax, o.tau)), o.tau)
    return float(N), float(Nax), float(np.max(nrm))

for nm, Lx, rp_, tlab in (("rosette-rp6.5-L3.5", 3.5, 6.5, 2*math.pi*56.3**1.5*1.06),
                          ("ecc-rp6.5-ra20", Lc, 6.5, 1700.0)):
    Ex = math.sqrt((1 - 2*M/rp_)*(1 + Lx*Lx/rp_**2))
    o = p.Origin(p.tetradize(p.ecc_y0(rp_, Lx)), tlab, n_dense=6000)
    imin = [i for i in range(1, len(o.tau)-1) if o.r[i] < o.r[i-1] and o.r[i] < o.r[i+1]]
    tau_per = o.tau[imin[0]] if imin else o.tau_end   # first periapsis after launch
    nper = o.tau_end/tau_per
    N, Nax, pk = epochs_noncircular(Ex, Lx, o)
    print(f"{nm:20s} per radial period (tau_per={tau_per:.1f}, r in [{o.r.min():.2f},{o.r.max():.2f}]):"
          f" tensor={N/nper:.0f} axis={Nax/nper:.0f}  peak||E||={pk:.4f}")
    RESULTS["notes"][f"epochs_{nm}"] = dict(tau_per=float(tau_per), nper=float(nper),
        tensor_per_period=float(N/nper), axis_per_period=float(Nax/nper), peak=float(pk),
        r_min=float(o.r.min()), r_max=float(o.r.max()))

def epochs_passage(Ecf, Lcf, rmax=200.0, n=40000):
    y0, rp = unbound_y0(Ecf, Lcf)
    rs = np.linspace(rp + 1e-6*(rmax-rp), rmax, n)
    dtau_dr = 1.0/np.sqrt(np.maximum(rdot2(Ecf, Lcf, rs), 1e-18))
    dom_dr = -omega_cf(Ecf, Lcf, rs)*dtau_dr
    Phi = np.concatenate([[0.0], np.cumsum(0.5*(dom_dr[1:] + dom_dr[:-1])*np.diff(rs))])
    Cg = np.stack([CP(Ecf, Lcf, rs[i], Phi[i], +1) for i in range(n)])
    nrm = np.linalg.norm(Cg, axis=(1, 2))
    rate = np.linalg.norm(np.gradient(Cg, rs, axis=0), axis=(1, 2))/nrm
    N = 2*256*TRAP(rate, rs)   # x2: inbound + outbound
    return float(N), float(np.max(nrm)), float(rp)

for Ecf, Lcf, nm in ((1.0, math.sqrt(18.0), "parab-rp6"), (1.05, 6.5, "hypA-E1.05-L6.5")):
    N, pk, rp = epochs_passage(Ecf, Lcf)
    print(f"{nm:20s} per full passage (rp={rp:.2f} -> 200M and back): tensor={N:.0f} peak||E||={pk:.4f}")
    RESULTS["notes"][f"epochs_{nm}"] = dict(N_passage=N, peak=float(pk), rp=float(rp))

# sign check P3: circ6 at tau=Tp/4, closed form with Phi=-om*tau vs +om*tau
r0 = 6.0; L = r0*math.sqrt(M/(r0-3*M)); Ecf = (1-2*M/r0)/math.sqrt(1-3*M/r0)
Tp = 2*math.pi*r0**2/L
om = math.sqrt(M/r0**3)
Cminus = CP(Ecf, L, r0, -om*Tp/4, +1); Cplus = CP(Ecf, L, r0, +om*Tp/4, +1)
print(f"\nP3 sign check at circ-r6, tau=Tp/4: closed(Phi=-om*tau)={fmt(Cminus)}  closed(+)= {fmt(Cplus)}")
RESULTS["notes"]["sign_check"] = dict(Cminus=[[float(x) for x in r_] for r_ in Cminus],
                                      Cplus=[[float(x) for x in r_] for r_ in Cplus])

with open("kernel-table.json", "w") as fh:
    json.dump(RESULTS, fh, indent=1)
print("\nwrote kernel-table.json")
