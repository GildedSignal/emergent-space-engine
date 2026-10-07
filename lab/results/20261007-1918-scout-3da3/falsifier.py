#!/usr/bin/env python3
"""Scout falsifier: does quantum-gated hierarchical news bound the growing light cone?

Question (Julien OC#50): "the light cone grows continuously meaning that there
will always be a point where we cannot handle the universe anymore". If gravity
is news (law.md, gravity at c) and every source change must reach every consumer
when its light does, causal traffic is O(N) per body and pending/retained news
grows with simulated time T. The candidate says both are bounded:
  - traffic: consumers aggregate distant material at cell size s ~ theta*D
    (Barnes-Hut opening angle; principle 33), a source aggregate's multipole
    random-walks, and news is sent only when it crosses the consumer's field
    quantum (dead-reckoning thresholds, DIS IEEE 1278; below-quantum
    accumulation, AMR refluxing);
  - memory: the observer's light cone fixes snapshot ages (a body at distance d
    is always seen d/c ago), so MVCC-style reclamation bounds retained history
    at rate x (galaxy light-crossing time), independent of T (GVT/fossil
    collection).

Model (float traffic model, no orbit integration): Mestel disk, G=v0=1,
Sigma=1/(2 pi r), r in [0.05,1], M_enc(r)=r. Populations: stars (1024 bodies,
mass 0.5) and ships (N variable, total mass 0.01), same profile. Element
diffusion per orbit from impulse encounters: Var_dv = 8 pi G^2 r sum_j n_j
m_j^2 ln Lambda_j. A member's kick changes its mean motion by dn=3 dv/r, so the
aggregate dipole of a cell with n members random-walks with per-orbit variance
s^2 = n (3 m sigma)^2 (random directions). First-passage rate to a threshold
p_q is s^2/p_q^2 per orbit (2-D random walk), saturated at the source's own
event granularity (nu kicks per orbit: a consumer cannot use finer news).
Consumer quantum: q = eps v0^2 / r_c; a dipole change p at distance D gives
delta g ~ G p / D^3, so p_q = q D^3.
Configurations:
  B  pairwise news (negative control): every body's every kick reaches every
     body: N^2 nu per orbit.
  C  hierarchical quantum-gated news (candidate): measured here.
Time unit: r_out/v0 (= 10 kpc / 220 km/s ~ 44 Myr); c = 1000 v0 (v/c ~ 1e-3).
"""
import json
import numpy as np

G = v0 = 1.0
R0, R1 = 0.05, 1.0
NSTAR, MSTAR_TOT = 1024, 0.5
MSHIP_TOT = 0.01
NU = 8.0                      # engine kick cadence per orbit (measured, q-cadence dossiers)
C_LIGHT = 1000.0
NR = 14                       # consumer rings
THETA = 0.5                   # opening angle: source cell size s = theta*D
LN_TOTAL = np.log(R1 / R0)
edges = np.geomspace(R0, R1, NR + 1)
r_mid = np.sqrt(edges[:-1] * edges[1:])
wmass = np.diff(np.log(edges)) / LN_TOTAL


def diffusion(N_ship, r):
    """per-orbit velocity variance and population data at radius r"""
    A_star, A_ship = MSTAR_TOT / LN_TOTAL, MSHIP_TOT / LN_TOTAL
    Sig_star, Sig_ship = A_star / (2 * np.pi * r), A_ship / (2 * np.pi * r)
    m_star, m_ship = MSTAR_TOT / NSTAR, MSHIP_TOT / N_ship
    n_star, n_ship = Sig_star / m_star, Sig_ship / m_ship
    acc = 0.0
    for n_j, m_j in ((n_star, m_star), (n_ship, m_ship)):
        b_min = max(2.0 * G * m_j / v0**2, 1e-12)
        b_max = min(r, 1.0 / (2 * np.sqrt(n_j)))
        lnL = max(np.log(max(b_max / b_min, np.e)), 1.0)
        acc += n_j * m_j**2 * lnL
    return 8 * np.pi * r * G**2 * acc, n_star, n_ship, m_star, m_ship


def consumer_traffic(N_ship, eps):
    """news deliveries received per consumer ring, per unit time"""
    Dmin = 3.0 * 0.2 * r_mid          # consumers closer than ~3 local cell extents: encounters tier
    out = []
    for k, r_c in enumerate(r_mid):
        Var_dv, n_star, n_ship, m_star, m_ship = diffusion(N_ship, r_c)
        sig = np.sqrt(Var_dv)
        Ds = np.geomspace(Dmin[k], 2 * R1, 60)
        rate_orbit = 0.0
        star_rate, ship_rate = 0.0, 0.0
        for D in Ds:
            area = (THETA * D) ** 2   # aggregate cell at opening angle
            n_s_cell = n_ship * area
            n_t_cell = n_star * area
            s2 = n_s_cell * (3 * m_ship * sig) ** 2 + n_t_cell * (3 * m_star * sig) ** 2
            p_q = (eps / r_c) * D**3
            rate = min(s2 / p_q**2, 1.0)
            # number of aggregate cells in the shell [D, D*step)
            step = np.exp(np.log(Ds[1] / Ds[0])) if len(Ds) > 1 else 1.3
            n_cells = 2 * np.pi * D * (D * (step - 1)) / area
            # restrict to cells that exist (galaxy is finite): shell at D from
            # consumer at r_c lies inside the disk; crude cap by disk area
            n_cells = min(n_cells, np.pi * (R1**2) / area)
            rate_orbit += n_cells * rate
            star_rate += n_cells * rate * n_t_cell * (3 * m_star * sig) ** 2 / max(s2, 1e-300)
            ship_rate += n_cells * rate * n_s_cell * (3 * m_ship * sig) ** 2 / max(s2, 1e-300)
        out.append(dict(r=r_c, w=wmass[k], rate_per_orbit=rate_orbit,
                        rate_per_time=rate_orbit / (2 * np.pi * r_c),
                        star_share=(star_rate / max(rate_orbit, 1e-300))))
    return out


def run(N_ship, eps):
    rows = consumer_traffic(N_ship, eps)
    # each consumer *cell* receives its ring's rate; cells per ring ~ 2*pi r / (0.2 r)
    cells_per_ring = [2 * np.pi * r / (0.2 * r) for r in r_mid]
    total = sum(row["rate_per_time"] * c for row, c in zip(rows, cells_per_ring))
    per_body = total / (N_ship + NSTAR)
    kick_ref = NU / (2 * np.pi * 0.5)
    window = 2 * R1 / C_LIGHT
    return dict(N=N_ship, eps=eps, total_rate=total, per_body=per_body,
                kick_rate_ref=kick_ref, ratio=per_body / kick_ref,
                star_share=np.average([row["star_share"] for row in rows], weights=[row["rate_per_time"] for row in rows]) if total > 0 else 0.0,
                mem_sliding_events=total * window, mem_sliding_MB=total * window * 8 / 1e6,
                naive_pairwise_per_body=(N_ship + NSTAR) * NU / (2 * np.pi * 0.5),
                naive_mem_after_T1_events=(N_ship + NSTAR) ** 2 * NU / (2 * np.pi * 0.5) * 1.0,
                )


def cascade(eps, dv_scale=1.0):
    """one star kick at r=0.5: arrival times of its news across the disk"""
    r_src = 0.5
    Var_dv, *_ = diffusion(10**6, r_src)
    m_star = MSTAR_TOT / NSTAR
    dv = np.sqrt(Var_dv) * dv_scale
    Vdot = 3 * m_star * dv
    ts = []
    for r_c in r_mid:
        Dmin = 3 * 0.2 * max(r_src, r_c)
        for D in np.geomspace(Dmin, min(2 * R1, 1.9), 50):
            p_q = (eps / r_c) * D**3
            ts.append(D / C_LIGHT + p_q / Vdot)
    ts = np.array(ts)
    bins = np.linspace(0, ts.max() * 1.05, 400)
    hist, _ = np.histogram(ts, bins)
    return dict(dv=dv, first=ts.min(), last=ts.max(),
                peak_per_unit_time=hist.max() / np.diff(bins).mean())


def main():
    out = {}
    Ns = [10**3, 10**4, 10**5, 10**6]
    res = [run(N, 1e-6) for N in Ns]
    out["C_eps1e-6"] = res
    pb = np.maximum([r["per_body"] for r in res], 1e-300)
    out["exponent_per_body_vs_N"] = float(np.polyfit(np.log(Ns), np.log(pb), 1)[0])
    out["eps_sweep_N1e6"] = [run(10**6, e) for e in (1e-4, 1e-6, 1e-8)]
    out["cascade_1sigma"] = cascade(1e-6)
    out["cascade_100x_kick"] = cascade(1e-6, 100.0)   # a struck/thrusting star
    out["memory_vs_T"] = dict(
        sliding_events=res[-1]["mem_sliding_events"], sliding_MB=res[-1]["mem_sliding_MB"],
        naive_events_after_1_unit=res[-1]["naive_mem_after_T1_events"],
        note="naive: live(T)=rate*T unbounded; sliding: rate*2R/c flat in T")
    print(json.dumps(out, indent=1, default=float))
    with open("falsifier-out.json", "w") as f:
        json.dump(out, f, indent=1, default=float)


if __name__ == "__main__":
    main()
