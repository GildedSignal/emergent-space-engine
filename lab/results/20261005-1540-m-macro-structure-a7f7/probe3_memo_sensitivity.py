#!/usr/bin/env python3
"""P3 — Self-sizing memo keys: the sensitivity map of the Schwarzschild cycle map.

The law's cycle memo is keyed by (E, L); sharing one compiled cycle across a
cell is safe only if the map (E,L) -> (Dphi, Dt, Dtau) varies by <= 1 output
quantum across the cell. law.md line 14 already stores d/dE and d/dL with each
cycle. Claim under test: those stored derivatives, measured at compile time,
size the memo's own keys (a dyadic adaptive key), and the first-order jet
(offset + stored derivatives) is exact to the quantum over most of the bound
plane. This probe maps where that holds, in float (behaviour/statistics only).

Darwin phase: u(psi) = c + A cos psi, c=(u_p+u_a)/2, A=(u_p-u_a)/2,
dphi/dpsi = 1/sqrt(2(u_3 - u)), dt/dpsi = dphi/dpsi * E/(L u^2 (1-2u)),
dtau/dpsi = dphi/dpsi * 1/(L u^2).  M=1; L^2(du/dphi)^2 = 2L^2 u^3 - L^2 u^2
+ 2u + (E^2-1), so Vieta gives u_3 = 1/2 - u_a - u_p and
L^2 = 1/(u_a u_p + u_a u_3 + u_p u_3), E^2 = 1 - 2 L^2 u_a u_p u_3.
"""
import json
import numpy as np

GL_N = 512
_x, _w = np.polynomial.legendre.leggauss(GL_N)
PSI = 0.5 * (np.pi) * (_x + 1.0)      # half cycle [0, pi]; full = 2x (mirror)
W = 0.5 * np.pi * _w

def roots_from_E_L(E, L):
    if not (np.isfinite(E) and np.isfinite(L) and E > 0 and L > 0 and E < 1):
        return None
    P = np.array([2.0*L*L, -L*L, 2.0, E*E - 1.0])
    r = np.roots(P)
    r = np.sort(r.real[np.abs(r.imag) < 1e-9])
    if len(r) != 3 or r[0] <= 0 or r[2] <= r[1] or r[1] <= r[0]:
        return None
    u_a, u_p, u_3 = r[0], r[1], r[2]
    if u_a <= 0 or u_p <= u_a or u_3 <= u_p:
        return None
    return u_a, u_p, u_3

def cycle_from_E_L(E, L, n=GL_N):
    rr = roots_from_E_L(E, L)
    if rr is None:
        return None
    u_a, u_p, u_3 = rr
    c = 0.5*(u_p + u_a); A = 0.5*(u_p - u_a)
    psi = PSI if n == GL_N else None
    assert n == GL_N
    u = c + A*np.cos(psi)
    dph = 1.0/np.sqrt(np.maximum(2.0*(u_3 - u), 1e-18))
    dphi = 2.0*float(np.sum(W*dph))
    denom = L*u*u*(1.0 - 2.0*u)
    dt = 2.0*float(np.sum(W*dph*E/np.maximum(np.abs(denom), 1e-18)*np.sign(denom if False else 1.0))) \
        if False else 2.0*float(np.sum(W*dph*E/denom))
    dtau = 2.0*float(np.sum(W*dph/(L*u*u)))
    return dphi, dt, dtau

def sensitivities(E, L, h=1e-7):
    base = cycle_from_E_L(E, L)
    if base is None:
        return None
    out = {}
    for var, idx in (('E', 0), ('L', 1)):
        p = [E, L]; p[idx] += h
        m = cycle_from_E_L(*p)
        p = [E, L]; p[idx] -= h
        mm = cycle_from_E_L(*p)
        if m is None or mm is None:
            return None
        out['d'+var] = tuple((m[k]-mm[k])/(2*h) for k in range(3))
    return base, out

def main():
    # grid in (p, e): u_p=(1+e)/p, u_a=(1-e)/p  (quasi-Kepler parametrization)
    ps = np.geomspace(7.0, 1000.0, 36)
    es = np.linspace(0.01, 0.99, 25)
    QUANTUM = 2.0**-32          # one ulp of a 32-bit output
    JET_QUANTUM = 2.0**-32
    res = {'grid': {'p': ps.tolist(), 'e': es.tolist()}, 'w_safe': [], 'jet_ok': [], 'ok': []}
    w_table = np.full((len(ps), len(es)), np.nan)
    jet_table = np.full((len(ps), len(es)), np.nan)
    n_ok = n_tot = 0
    for i, p in enumerate(ps):
        for j, e in enumerate(es):
            u_p = (1+e)/p; u_a = (1-e)/p
            u_3 = 0.5 - u_a - u_p
            if u_3 <= u_p:
                n_tot += 1
                continue      # at/past the plunge separatrix: not a bound cycle
            L2 = 1.0/(u_a*u_p + u_a*u_3 + u_p*u_3); E2 = 1 - 2*L2*u_a*u_p*u_3
            if not (L2 > 0 and 0 < E2 < 1):
                n_tot += 1
                continue
            L = np.sqrt(L2); E = np.sqrt(E2)
            s = sensitivities(E, L)
            n_tot += 1
            if s is None:
                continue
            base, der = s
            n_ok += 1
            # max safe relative cell half-width per input: w_i = min_k q*|out_k| / |d out_k/d i|
            ws = []
            for var in ('E', 'L'):
                wv = min(QUANTUM*abs(base[k])/abs(der['d'+var][k])
                         for k in range(3) if abs(der['d'+var][k]) > 0)
                ws.append(wv/abs(E if var == 'E' else L))
            w = min(ws)
            w_table[i, j] = np.log2(max(w, 1e-40))
            # jet validity at w: second-order term (estimated by evaluating at +w and
            # comparing base + w*d against the true value)
            for var, idx in (('E', 0), ('L', 1)):
                step = w*abs(E if var == 'E' else L)
                if step <= 0:
                    jet_table[i, j] = np.nan
                    continue
                q = [float(E), float(L)]; q[idx] += step
                m = cycle_from_E_L(*q)
                if m is None:
                    continue
                lin = tuple(base[k] + step*der['d'+var][k] for k in range(3))
                err2 = max(abs(m[k]-lin[k]) for k in range(3))
                rel = err2/max(max(abs(base[k]) for k in range(3)), 1e-300)
                jet_table[i, j] = max(jet_table[i, j] if not np.isnan(jet_table[i, j]) else -np.inf,
                                      np.log2(max(rel, 1e-40)))
            res['ok'].append([i, j])
    # summaries
    valid = ~np.isnan(w_table)
    frac = valid.mean()
    # area-weighted stats over the bound plane grid
    big = (w_table >= -12) & valid
    small = (w_table < -20) & valid
    res['summary'] = {
        'grid_points_ok': f'{n_ok}/{n_tot}',
        'median_w_safe_bits': float(np.nanmedian(w_table)),
        'p10_w_safe_bits': float(np.nanpercentile(w_table, 10)),
        'p90_w_safe_bits': float(np.nanpercentile(w_table, 90)),
        'frac_w_safe_ge_2^-12': float(big.sum()/max(valid.sum(), 1)),
        'frac_w_safe_lt_2^-20': float(small.sum()/max(valid.sum(), 1)),
        'median_jet_residual_bits': float(np.nanmedian(jet_table)),
        'frac_jet_residual_lt_2^-32': float((jet_table < -32).sum()/max(valid.sum(), 1)),
    }
    # where is it bad? report the p of every column with w < 2^-20
    bad = []
    for i, p in enumerate(ps):
        col = w_table[i, :]
        v = col[~np.isnan(col)]
        if len(v) and np.median(v) < -20:
            bad.append((float(p), float(np.median(v))))
    res['bad_columns_p_medianbits'] = bad
    # smoothness: total variation of median over log p
    meds = np.array([np.nanmedian(w_table[i, :]) if np.any(~np.isnan(w_table[i, :])) else np.nan
                     for i in range(len(ps))])
    okm = ~np.isnan(meds)
    tv = float(np.nansum(np.abs(np.diff(meds[okm]))))
    net = float(abs(meds[okm][-1] - meds[okm][0]))
    res['summary']['tv_over_net_medbits'] = tv/max(net, 1e-9)
    # convergence check: GL_N 512 vs 2048 on the worst point (max sensitivity)
    ii, jj = np.unravel_index(np.nanargmin(np.where(valid, w_table, np.inf)), w_table.shape)
    p, e = ps[ii], es[jj]
    u_p = (1+e)/p; u_a = (1-e)/p; u_3 = 0.5-u_a-u_p
    L2 = 1.0/(u_a*u_p + u_a*u_3 + u_p*u_3); L = np.sqrt(L2); E = np.sqrt(max(1-2*L2*u_a*u_p*u_3, 0))
    global GL_N, PSI, W
    a = cycle_from_E_L(E, L)
    GL_N2 = 2048
    x2, w2 = np.polynomial.legendre.leggauss(GL_N2)
    PSI2 = 0.5*np.pi*(x2+1); W2 = 0.5*np.pi*w2
    b = None
    # recompute with 2048 nodes by temporarily swapping globals
    old = (PSI, W)
    globals()['PSI'], globals()['W'] = PSI2, W2
    globals()['GL_N'] = GL_N2
    b = cycle_from_E_L(E, L, n=GL_N2)
    globals()['PSI'], globals()['W'] = old
    globals()['GL_N'] = 512
    res['convergence_check_worst_point'] = {
        'p': float(p), 'e': float(e),
        'dphi_512': a[0], 'dphi_2048': b[0],
        'rel_diff': float(abs(a[0]-b[0])/b[0]),
        'dt_rel_diff': float(abs(a[1]-b[1])/abs(b[1])),
    }
    np.save('probe3_wtable.npy', w_table)
    with open('probe3_out.json', 'w') as f:
        json.dump(res, f, indent=1, default=float)
    print(json.dumps(res['summary'], indent=1))
    print('bad columns (p, median w bits):', bad)
    print('convergence:', res['convergence_check_worst_point'])

if __name__ == '__main__':
    main()
