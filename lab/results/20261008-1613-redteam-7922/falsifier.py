#!/usr/bin/env python3
"""Red-team falsifier A1: the cycle-derivative jet near the separatrix.

Model: Kepler (the two-body doll's weak-field limit at belt scale), GM = 1,
periapsis p = 1 fixed (B18b's belt: banded p, Rayleigh e).

  exact  : after each orbit-averaged kick the orbit is re-solved exactly;
           periapsis epoch t_exact(n) = sum_{k<=n} T(E_k).
  jet    : the memo path of law.md — cycle compiled once from (E0, L0),
           offsets carried exactly, cycle updated by the stored derivative
           dT/dE (multiply-add); t_jet(n) = n*T0 + T'(E0)*sum_{k<=n}(E_k-E0).

Kicks are correlated (same sign, secular) unless stated. The floor is law.md's
1e-6 relative. n*(e) = kicks survived before the epoch error crosses the floor.
"""
import json
import numpy as np

GM, P, EPS = 1.0, 1.0, 1e-7          # kick dE = EPS * GM/(2 a0), a0 = p
FLOOR = 1e-6
NMAX = 2_000_000
DEL = np.float64(0.5 * EPS * GM / P)  # absolute kick per orbit

def T_of_E(E):
    """Kepler radial period from binding energy E<0: T = 2*pi*a^{3/2}, a = GM/(2|E|)."""
    a = GM / (-2.0 * E)
    return 2.0 * np.pi * np.sqrt(a) ** 3

def horizon(e, sign=+1.0, rng=None):
    """Kicks survived before |t_jet - t_exact| / T crosses FLOOR."""
    E0 = -(1.0 - e) * GM / (2.0 * P)
    T0 = T_of_E(E0)
    dT = (1.5 * T0 / -E0)                    # dT/dE at E0 (the stored derivative)
    n = np.arange(1, NMAX + 1, dtype=np.float64)
    if rng is None:                           # correlated (secular) kicks
        dE = sign * DEL * n
    else:                                     # random-sign control
        dE = DEL * np.cumsum(rng.choice((-1.0, 1.0), NMAX))
    E = E0 + dE
    alive = E < 0
    t_exact = np.cumsum(T_of_E(np.where(alive, E, -np.inf)))
    # t_jet(n) = n*T0 + T'(E0) * sum_{k<=n} (E_k - E0)
    if rng is None:                           # correlated: sum_k dE_k = DEL*sign*n(n+1)/2
        sum_off = DEL * sign * n * (n + 1) / 2.0
    else:                                     # random walk: cumsum of the offsets
        sum_off = np.cumsum(dE)
    t_jet = n * T0 + dT * sum_off
    err = np.abs(t_jet - t_exact) / T_of_E(np.where(alive, E, E0))
    bad = np.nonzero(alive & (err > FLOOR))[0]
    return (int(bad[0]) + 1) if len(bad) else None

def crossings(e, m=16):
    return 2 * m * np.log2((1 + e) / (1 - e)) + 8

print(f"kick dE = {DEL:.3e} per orbit (EPS={EPS}), floor {FLOOR:.0e}")
es = [0.0, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 0.99, 0.995]
rng = np.random.default_rng(7922)
rows = {}
print(f"{'e':>6} {'n*_corr':>8} {'n*_rand':>8} {'cross/cyc':>9} {'comp/kick':>9} {'cost/orbit':>10}")
for e in es:
    nc = horizon(e)
    nr = horizon(e, rng=rng)
    c = crossings(e)
    ck = 1.0 / nc if nc else 0.0
    cost = 0.3 * ck * c          # compile-crossings per orbit (0.3 kicks/orbit, H0190)
    rows[e] = dict(n_corr=nc, n_rand=nr, crossings=c, compiles_per_kick=ck, cost_per_orbit=cost)
    print(f"{e:>6} {nc if nc else '>2e6':>8} {nr if nr else '>2e6':>8} {c:>9.1f} {ck:>9.4f} {cost:>10.3f}")

# angle channel: GR 1PN advance per cycle 6*pi*GM/(c^2 * L^2) depends on L only;
# rel error of the first-order jet in the angle channel = (dL/L)^2 at the horizon
print("\nangle channel at each horizon (rel err = (sum dL/L)^2, dL/L = EPS per kick):")
for e in es:
    n = rows[e]['n_corr']
    if n:
        print(f"  e={e:<5} n*={n:<7} angle err ~ {(min(EPS*n,1))**2:.2e}  (floor {FLOOR:.0e})")

# belt arithmetic: Rayleigh sigma=0.3 (B18b), per-body cost distribution
sig = 0.3
egrid = np.linspace(0.001, 0.995, 4000)
# interpolate n*(e) on the (1-e)^{2/3} law from measured points, then cost(e)
measured = np.array([[1 - k, rows[k]['cost_per_orbit']] for k in es if rows[k]['n_corr']])
lc = np.polyfit(np.log(measured[:, 0]), np.log(measured[:, 1]), 1)
cost_s = np.exp(np.polyval(lc, np.log(1 - egrid)))
pdf = (egrid / sig**2) * np.exp(-egrid**2 / (2 * sig**2))
total = np.sum(cost_s * pdf) / np.sum(pdf)
cdf = np.cumsum(pdf) / np.sum(pdf)
med = cost_s[np.searchsorted(cdf, 0.5)]
p99 = cost_s[np.searchsorted(cdf, 0.99)]
p999 = cost_s[min(np.searchsorted(cdf, 0.999), len(egrid)-1)]
share99 = np.sum(cost_s[egrid > 0.9] * pdf[egrid > 0.9]) / np.sum(cost_s * pdf)
print(f"\nbelt (Rayleigh s={sig}): fit cost ~ (1-e)^{lc[0]:.2f}")
print(f"  median cost/orbit {med:.3f} crossings; p99 {p99:.2f} ({p99/med:.0f}x median); "
      f"p99.9 {p999:.1f} ({p999/med:.0f}x)")
print(f"  bodies e>0.9 ({np.exp(-0.9**2/(2*sig**2))*100:.1f}% of belt) carry "
      f"{share99*100:.0f}% of total compile crossings")
print(f"  compiles/kick at e=0.99: {rows[0.99]['compiles_per_kick']:.2f} (law.md budget: 0.05)")
print(f"  scaling checks: n*(0.99)/n*(0.5) = {rows[0.99]['n_corr']/rows[0.5]['n_corr']:.3f} "
      f"vs (1-e)^(2/3) = {((0.01)/(0.5))**(2/3):.3f}; "
      f"n*(0)/n*(0.5) = {rows[0.0]['n_corr']/rows[0.5]['n_corr']:.3f} vs 2^(2/3) = {2**(2/3):.3f}")
print(f"  random/correlated horizons: " + ", ".join(
    f"e={e}:{rows[e]['n_rand']//max(rows[e]['n_corr'],1)}x" if rows[e]['n_corr'] else f"e={e}:inf"
    for e in [0.0, 0.5, 0.9]))

# A2: strong deflection / photon ring (Darwin 1959)
bc = 3 * np.sqrt(3)  # critical impact parameter, M=1
C0 = np.log(216 * (7 - 4 * np.sqrt(3))) - np.pi
print("\nA2 deflection alpha(b) = -ln(b/bc-1) + C0, C0 = %.3f" % C0)
print(f"{'b/bc-1':>10} {'alpha (rad)':>11} {'windings':>8}")
for epsb in [1e-1, 1e-2, 1e-4, 1e-6, 1e-8]:
    a = -np.log(epsb) + C0
    print(f"{epsb:>10.0e} {a:>11.2f} {a/ (2*np.pi):>8.2f}")
print("image n offset from shadow edge at r_o (1080p, 60deg FOV -> ~1e-3 rad/pixel):")
for ro in [4.0, 6.0, 10.0]:
    th_sh = np.arcsin(bc * np.sqrt(1 - 2 / ro) / ro)
    dth1 = np.exp(C0 - 2 * np.pi) * bc * np.sqrt(1 - 2 / ro) / ro
    print(f"  r_o={ro:>4}M: shadow {th_sh*1e3:.0f} mrad, 1st relativistic image "
          f"+{dth1*1e3:.2f} mrad ({dth1/1e-3:.1f} px)")

json.dump({"rows": {str(k): v for k, v in rows.items()},
           "belt": dict(sigma=0.3, fit_exponent=lc[0], median=med, p99=p99, p999=p999,
                        tail_share_e_gt_09=share99),
           "darwin_C0": C0},
          open("metrics.json", "w"), indent=1)
