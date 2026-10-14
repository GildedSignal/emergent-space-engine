#!/usr/bin/env python3
"""The quantum gate on a contiguous belt (float falsifier, orders of magnitude).

Question (board live question 2 / encounters open direction 2): can a gate that
routes an encounter's impulse against the LAW'S OWN key quantum (E: Q48 => one
quantum of E is 2^-48 of E; b29a: a real kick moves E by ~3 Q48 quanta) delete
the ~10^3 of candidate-pair work at 10^9? Below the quantum the encounter is not
an event for the exact tier: it belongs to the accumulator (principle 6,
"influences below one quantum accumulate"; the flux aggregate 62f7 measured
0.87-1.04 of truth).

Anchors from the record:
- c7eb (gold): contact impulse validated (median 0.998 over 1091 RK4 runs);
  m_crit ~= 1.3e-17 M_sun (~1.35-km rock): below it, 0/1000 50-m rocks crossed
  a period tick in 1.7e4 orbits.
- 1738 (awaiting grade): contiguous belt, averaged cadence: 1.65e3-8.2e3 cores
  skin-on per game-second at 10^9, budget 4 cores.
- The belt's candidate set = radially overlapping pairs (cone tier); the gate
  does not shrink the candidate set, it deletes the CONSEQUENCE: a pair whose
  strongest conjunction within the certificate horizon moves neither key by one
  quantum never needs the exact tier at all.

Model (float, planar-Kepler replica like every run in this topic):
- a ~ U[0.95, 1.05] (contiguous belt), e ~ Rayleigh(0.05), phases uniform.
- conjunctions of a candidate pair: at the crossing longitudes; miss distance
  equidistributed in [0, b_max], b_max = v_rel * P_syn / 2 (next conjunction is
  within one synodic period); closest of N_c conjunctions in horizon H:
  b_min ~ b_max * U_(1)/N_c (min of N_c uniforms), N_c = H/P_syn * (#crossings).
- impulse on i: dv_i = 2*mu_j/(b*v_rel) (hyperbolic deflection, c7eb's validated
  coefficient family); dE_i/E = 2*dv_i/v_i (virial, a=1 units).
Controls: RK4 flyby check of the deflection formula; all-large-belt negative
control; all-50m-rocks positive control (must reproduce c7eb's 0/1000).
"""
import numpy as np

rng = np.random.default_rng(20261014)
AU_M = 1.495978707e11
MSUN = 1.989e30
Q48 = 2.0**-48
def mass_of_D(D):
    return D**3 * np.pi / 6 * 2600.0 / MSUN  # rho = 2.6 g/cc, in M_sun

def rk4_flyby_natural(mu, b, vinf):
    """Integrate a hyperbolic flyby in the belt's own units (GM_star = 1, a = 1)."""
    def acc(r):
        r2 = r[0] * r[0] + r[1] * r[1]
        return -mu * r / r2**1.5
    r = np.array([-2000.0 * b, b]); u = np.array([vinf, 0.0])
    dt = 0.02 * b / vinf
    for _ in range(int(2 * 2000.0 / 0.02) + 1):
        k1v = acc(r); k1r = u
        k2v = acc(r + 0.5 * dt * k1r); k2r = u + 0.5 * dt * k1v
        k3v = acc(r + 0.5 * dt * k2r); k3r = u + 0.5 * dt * k2v
        k4v = acc(r + dt * k3r); k4r = u + dt * k3v
        u = u + dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        r = r + dt / 6 * (k1r + 2 * k2r + 2 * k3r + k4r)
    return np.linalg.norm(u - np.array([vinf, 0.0]))
def dohnyani(n, dmin, dmax, slope=3.5):
    """dN/dD ∝ D^-slope, inverse-CDF sample of diameters in metres."""
    lo, hi = dmin**(-(slope - 1)), dmax**(-(slope - 1))
    u = rng.random(n)
    return (lo + u * (hi - lo))**(-1.0 / (slope - 1))

def belt(n, dmin=50.0, dmax=3e5, belt_mass_ratio=1e-6):
    a = rng.uniform(0.95, 1.05, n)
    e = rng.rayleigh(0.05, n).clip(max=0.35)
    D = dohnyani(n, dmin, dmax)
    # belt mass normalisation: total = belt_mass_ratio * M_star
    m = D**3 * np.pi / 6 * 2600.0 / MSUN  # rho=2.6 g/cc, in M_sun
    m *= belt_mass_ratio / m.sum()
    return a, e, m

def candidate_pairs(a, e, m, npairs):
    """Sample pairs whose radial bands overlap (the cone tier's candidate set)."""
    peri_i, apo_i = a * (1 - e), a * (1 + e)
    i = rng.integers(0, len(a), npairs * 3)
    j = rng.integers(0, len(a), npairs * 3)
    ok = (i != j) & (peri_i[i] < apo_i[j]) & (peri_i[j] < apo_i[i])
    return i[ok][:npairs], j[ok][:npairs]

def conjunction_gate(a, e, m, i, j, H_orbits=1e3, ncross=2, quant=Q48):
    """Per candidate pair: strongest impulse within horizon vs the key quantum.

    Returns dE/E for each member at the pair's closest conjunction in horizon.
    """
    ai, aj, ei, ej = a[i], a[j], e[i], e[j]
    mi, mj = m[i], m[j]
    # synodic clock (a=1, GM=1 => n = a^-1.5)
    ni, nj = ai**-1.5, aj**-1.5
    nsyn = np.abs(ni - nj)
    # encounter speed: ~ shearing-sheet relative speed |dv| ~ v * sqrt((3/2 da/a)^2 + (e_i+e_j)^2)-ish;
    # use the standard encounter-speed estimate sqrt((3 da /2a)^2 + (ei+ej)^2 + 2 ei ej) ~ O(e v)
    da = np.abs(ai - aj)
    vrel = np.sqrt((1.5 * da / ((ai + aj) / 2))**2 + (ei + ej)**2).clip(1e-3)
    Psyn = 2 * np.pi / np.maximum(nsyn, 1e-12)  # in orbital periods at a=1
    Nc = np.maximum(H_orbits / np.minimum(Psyn, H_orbits) * ncross, 1e-9)
    # cap: number of conjunctions in horizon
    Nc = np.minimum(H_orbits / Psyn * ncross, 1e4)
    bmax = vrel * np.minimum(Psyn, H_orbits) / 2.0  # in a=1 units
    bmin = bmax * rng.random(len(i)) / np.maximum(Nc, 1.0)
    bmin = np.maximum(bmin, 1e-9)
    # deflection impulse on i from j: dv = 2 mu_j / (b v_rel)   (c7eb family)
    dvi = 2 * mj / (bmin * vrel)
    dvj = 2 * mi / (bmin * vrel)
    vi, vj = ai**-0.5, aj**-0.5
    dEi = 2 * dvi / vi  # dE/|E| virial at a=1
    dEj = 2 * dvj / vj
    return dEi, dEj, bmin, vrel

def gate_fraction(a, e, m, npairs=200_000, **kw):
    i, j = candidate_pairs(a, e, m, npairs)
    dEi, dEj, bmin, vrel = conjunction_gate(a, e, m, i, j, **kw)
    deleted = (dEi < Q48) & (dEj < Q48)
    return deleted.mean(), len(i), bmin, vrel

# ---------- control 1: RK4 validation of the deflection formula ----------

def check_deflection():
    out = []
    for mu in [1e-12, 1e-10, 1e-8]:
        for bb in [1e-6, 1e-4]:
            vinf = 0.05
            pred = 2 * mu / (bb * vinf)
            got = rk4_flyby_natural(mu, bb, vinf)
            out.append((mu, bb, pred, got, got / pred if pred > 0 else np.nan))
    return out

if __name__ == "__main__":
    print("== control 1: deflection formula vs RK4 (natural units, mu in GM=1) ==")
    for mu, bb, pred, got, r in check_deflection():
        print(f"  mu={mu:.0e} b={bb:.0e} pred={pred:.3e} rk4={got:.3e} ratio={r:.3f}")

    n = 200_000
    a = rng.uniform(0.95, 1.05, n); e = rng.rayleigh(0.05, n).clip(max=0.35)

    print("\n== control 2 (positive, c7eb anchor): every body a real 50-m rock ==")
    m50 = np.full(n, mass_of_D(50.0))
    fr, _, _, _ = gate_fraction(a, e, m50)
    print(f"  deletable fraction = {fr:.6f} (c7eb: 0/1000 crossed a tick -> expect ~1.0)")

    print("\n== control 3 (negative): every body a 10-km body ==")
    fr, _, _, _ = gate_fraction(a, e, np.full(n, mass_of_D(1e4)))
    print(f"  deletable fraction = {fr:.6f} (prediction: < 0.5)")

    print("\n== decisive: 10^9-body belt, dN/dD ∝ D^-3.5 (candidate pairs are mass-blind; ==")
    print("   masses drawn per body from the spectrum; belt mass falls out)")
    for (dmin, dmax, tag) in [(70.0, 4.7e5, "real-belt-like (Ceres top, N(>1km)~1.5e6)"),
                              (70.0, 3e5, "300-km top"),
                              (50.0, 3e5, "50-m floor, 300-km top")]:
        D = dohnyani(n, dmin, dmax)
        m2 = mass_of_D(D)
        belt_mass = m2.mean() * 1e9
        fr, npairs, bmin, vrel = gate_fraction(a, e, m2)
        i, j = candidate_pairs(a, e, m2, 100_000)
        dEi, dEj, _, _ = conjunction_gate(a, e, m2, i, j)
        keep = ~((dEi < Q48) & (dEj < Q48))
        dkeep = np.median(D[i[keep]]) if keep.sum() else float('nan')
        print(f"  D∈[{dmin:.0f}m,{dmax:.0f}m] {tag}: belt mass {belt_mass:.1e} M_sun"
              f" | deletable {fr:.6f} | surviving {1-fr:.3e} of candidates"
              f" | surviving member D med {dkeep:.0f} m"
              f" | bmin med {np.median(bmin):.2e}, vrel med {np.median(vrel):.3f}")
        for base in [1.65e3, 8.2e3]:
            print(f"    ledger: ungated {base:.2e} cores -> gated {base * (1 - fr):.2e} cores (budget 4)")

    print("\n== spectrum sensitivity (the content dial) ==")
    for dcrit_note, dmin in [("floor 100 m", 100.0), ("floor 500 m", 500.0), ("floor 2 km", 2e3)]:
        D = dohnyani(n, dmin, 4.7e5)
        fr, _, _, _ = gate_fraction(a, e, mass_of_D(D))
        print(f"  D_min {dmin:>6.0f} m ({dcrit_note}): deletable {fr:.6f}")

# ---------- part A: group-certificate vacuity on random-phase belts ----------
def phase_vacuity():
    """Cell-pair worst case over member phases: min miss at a crossing longitude.

    Two cells of crossing orbits (a, e fixed per cell, random member phases):
    the miss at the shared crossing longitude is b = |dt| * v_rel with dt the
    arrival-time offset, equidistributed over the synodic sequence. The min over
    K sampled member-phase pairs scales as 1/K -> 0: no phase-free group
    certificate can skip a crossing cell pair.
    """
    rng2 = np.random.default_rng(7)
    # two crossing orbit families: periapsis/periapsis bands overlap at a crossing
    a1, e1, w1 = 1.00, 0.05, 0.0
    a2, e2, w2 = 1.05, 0.05, np.pi  # crossing longitudes exist by construction
    n = np.array([a1**-1.5, a2**-1.5])
    vrel = 0.1  # O(e v), same order as conjunction_gate's estimate
    # arrival time at a crossing longitude ~ uniform over each orbit's period,
    # so dt modulo the synodic period is equidistributed for random member phases
    out = []
    for K in [10, 100, 1000, 10000, 100000]:
        dt = rng2.uniform(-0.5, 0.5, K) * (2 * np.pi / abs(n[0] - n[1]))
        out.append((K, np.min(np.abs(dt)) * vrel, 1.0 / K))
    return out

if __name__ == "__main__" and False:
    pass
