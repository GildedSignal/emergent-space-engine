#!/usr/bin/env python3
"""The checker's named experiment for gold, run 20261012-1524-fermi-4b55:
(1) an independent brute-force dense-time truth for planet-SOI transits
    (episodes at rising edges, dt-convergence control, second seed, window
    stability), replacing the sign-flipped Newton that decided the headline;
(2) the run's own Newton with the one-line sign fix, as a cross-instrument;
(3) the 10^9 headline table regenerated IN CODE from the measured rate, so
    JSON, dossier and abstract share one path (the original had none);
(4) the checker's two minor slips fixed: doll length = 3 AU in the contact
    radius, and v_rel = sqrt(2) sigma_e in mu_crit.

Belt sampler and Kepler solver are verbatim from the run's h_live_fermi.py
(same instruments, same seeds). Units: doll (GM=1, a=1, v_K=1, orbit=2pi);
anchor a=3 AU, M_star=M_sun, T_orbit=1.64e8 s.
"""
import json
import math
import numpy as np

R = {}


def make_belt(n, sigma_e, a_lo, a_hi, seed):
    rng = np.random.default_rng(seed)
    a = rng.uniform(a_lo, a_hi, n)
    e = np.minimum(sigma_e * np.sqrt(-2.0 * np.log(1.0 - rng.random(n))), 0.5)
    pom = rng.uniform(0, 2 * np.pi, n)
    lam = rng.uniform(0, 2 * np.pi, n)
    return a, e, pom, lam


def kepler_pos(a, e, pom, lam, n, t):
    M = (lam + n * t - pom) % (2 * np.pi)
    E = M.copy()
    for _ in range(4):
        f = E - e * np.sin(E) - M
        E = E - f / (1 - e * np.cos(E))
    r = a * (1 - e * np.cos(E))
    c, s = np.cos(E), np.sin(E)
    fac = np.sqrt(np.maximum(1.0 - e * e, 1e-18))
    nu = np.arctan2(fac * s, c - e)
    th = nu + pom
    return r * np.cos(th), r * np.sin(th)


def true_long(a, e, pom, lam, n, t):
    M = (lam + n * t - pom) % (2 * np.pi)
    E = M.copy()
    for _ in range(3):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    fac = np.sqrt(np.maximum(1.0 - e * e, 1e-18))
    return np.arctan2(fac * np.sin(E), np.cos(E) - e) + pom


MU_P, A_P = 1e-3, 1.25
R_SOI = A_P * (MU_P / 3.0) ** (1 / 3)
NPP = A_P ** -1.5
SIGMA_E = 5.5e-3


# ---------- (1) brute-force truth: episodes at rising edges -------------------

def brute_force(seed, horizon, dt):
    a, e, pom, lam = make_belt(10_000, SIGMA_E, 1.0, 1.5, seed)
    nb = a ** -1.5
    steps = int(horizon / dt)
    xp_all = A_P * np.cos(NPP * (np.arange(steps) + 0.5) * dt)
    yp_all = A_P * np.sin(NPP * (np.arange(steps) + 0.5) * dt)
    episodes = np.zeros(len(a), dtype=np.int64)
    inside = None
    for s in range(steps):
        t = (s + 0.5) * dt
        x, y = kepler_pos(a, e, pom, lam, nb, t)
        now = np.hypot(x - xp_all[s], y - yp_all[s]) < R_SOI
        if s == 0:
            episodes += now          # in-SOI at t=0 counts as one episode
        else:
            episodes += now & ~inside  # rising edge only
        inside = now
    n_ep = int(episodes.sum())
    return n_ep, n_ep / (len(a) * horizon / (2 * np.pi))


HOR = 20 * 2 * math.pi
print(f"R_SOI={R_SOI:.4f}  belt 1e4 sigma_e={SIGMA_E} a in [1,1.5]")
R["brute"] = {}
for dt in (0.3, 0.15, 0.075):
    n, rate = brute_force(42, HOR, dt)
    R["brute"][f"dt{dt}"] = {"episodes": n, "rate": rate}
    print(f"  seed42 20orbits dt={dt:<6} episodes={n:5d} rate={rate:.3e}/body/orbit")
n43, rate43 = brute_force(43, HOR, 0.15)
R["brute"]["seed43_dt0.15"] = {"episodes": n43, "rate": rate43}
print(f"  seed43 20orbits dt=0.15  episodes={n43:5d} rate={rate43:.3e}/body/orbit")
for hor_orb in (60, 200):
    n, rate = brute_force(42, hor_orb * 2 * math.pi, 0.15)
    R["brute"][f"win{hor_orb}orbits"] = {"episodes": n, "rate": rate}
    print(f"  seed42 {hor_orb:3d}orbits dt=0.15 episodes={n:5d} rate={rate:.3e}/body/orbit")

RATE = R["brute"]["dt0.15"]["rate"]          # adopted truth rate


# ---------- (2) the run's Newton, sign fixed ----------------------------------
# crosscheck.py S2 had: dn = npp - nb; residual dth = lam_body - npp*t, whose
# derivative is nb - npp = -dn; so 't -= dth/dn' diverges. Fix: t += dth/dng.

a, e, pom, lam = make_belt(10_000, SIGMA_E, 1.0, 1.5, 42)
nb = a ** -1.5
dn = NPP - nb
dl = lam % (2 * np.pi)
hits = 0
K = int(np.ceil(np.abs(dn).max() * HOR / (2 * np.pi))) + 1
for k in range(-1, K + 1):
    with np.errstate(divide="ignore", invalid="ignore"):
        tk = (dl + 2 * np.pi * k) / dn
    good = np.isfinite(tk) & (tk > 0) & (tk <= HOR)
    if not good.any():
        continue
    t = tk[good]
    dng = dn[good]
    for _ in range(3):
        dth = true_long(a[good], e[good], pom[good], lam[good], nb[good], t) - t * NPP
        dth = (dth + np.pi) % (2 * np.pi) - np.pi
        t = t + dth / np.where(dng != 0, dng, 1.0)      # SIGN FIX (was '-')
    t = np.clip(t, 0.0, HOR)
    x, y = kepler_pos(a[good], e[good], pom[good], lam[good], nb[good], t)
    xp, yp = A_P * np.cos(t * NPP), A_P * np.sin(t * NPP)
    hits += int((np.hypot(x - xp, y - yp) < R_SOI).sum())
rate_fix = hits / (10_000 * 20)
R["newton_sign_fixed"] = {"hits": hits, "rate": rate_fix,
                          "vs_brute": rate_fix / RATE}
print(f"sign-fixed Newton: hits={hits} rate={rate_fix:.3e} "
      f"({rate_fix / RATE:.2f} x brute truth)")


# ---------- (2b) analytic anchor (independent of both instruments) ------------
# A body transits iff its radial range [a(1-e), a(1+e)] overlaps
# [a_p - R_SOI, a_p + R_SOI]; then it gets |dn|/n synodic chances per orbit.
rng = np.random.default_rng(7)
nsamp = 2_000_000
aa = rng.uniform(1.0, 1.5, nsamp)
ee = np.minimum(SIGMA_E * np.sqrt(-2.0 * np.log(1.0 - rng.random(nsamp))), 0.5)
ok = (aa * (1 - ee) <= A_P + R_SOI) & (aa * (1 + ee) >= A_P - R_SOI)
dnA = np.abs(A_P ** -1.5 - aa ** -1.5)
rate_ana = float(np.mean(np.where(ok, dnA / aa ** -1.5, 0.0)))
R["analytic_anchor"] = {"rate": rate_ana, "vs_brute": rate_ana / RATE,
                        "eligible_fraction": float(ok.mean())}
print(f"analytic anchor: rate={rate_ana:.3e} ({rate_ana / RATE:.1f} x truth), "
      f"eligible fraction {ok.mean():.2f}")


# ---------- (3) the 10^9 headline table, one code path ------------------------
T_ORBIT_S = 1.64e8
M_SUN = 1.989e30
SIGMA0 = 1e4 / (math.pi * (1.5 ** 2 - 1.0))     # bodies per doll^2 at 1e4
AU3 = 4.49e11                                   # doll length = 3 AU, in metres
rho_phys = 10.0 / AU3                           # 10 m contact radius  [3 AU fix]
v_rel = math.sqrt(2) * SIGMA_E
sig9 = SIGMA0 * 1e5                             # fixed annulus at 1e9
cont_rate_bo = sig9 * 2 * rho_phys * v_rel * 2 * math.pi
cont_per_s = cont_rate_bo * 1e9 / T_ORBIT_S
rebind_per_s = RATE * 1e9 / T_ORBIT_S
h_rebind = rebind_per_s * 128                   # a 16-byte tube per rebind
h_contact = cont_per_s * 256
h_player = 10.0                                 # stated assumption (~10 decisions/s)
h_total = h_rebind + h_contact + h_player
sat_orb = 1.0 / RATE
mu_crit = 1e-5 * 5.5e-5 * v_rel / 2             # [sqrt2 fix] q_v rho v_rel / 2
R["table_1e9"] = {
    "truth_rate_per_body_per_orbit": RATE,
    "rebinds_per_game_second": rebind_per_s,
    "H_live_rebind_bits_per_s": h_rebind,
    "contacts_per_game_second": cont_per_s,
    "H_live_contact_bits_per_s": h_contact,
    "H_live_player_bits_per_s": h_player,
    "H_live_total_bits_per_s": h_total,
    "bytes_per_s": h_total / 8,
    "kB_per_hour_of_play": h_total / 8 * 3600 / 1024,
    "singleton_saturation_orbits": sat_orb,
    "saturation_game_years": sat_orb * T_ORBIT_S / 3.15e7,
    "saturation_wall_years_at_rtf100": sat_orb * T_ORBIT_S / 3.15e7 / 100,
    "birth_program_bytes_at_1e9": 0.126 / 8 * 1e9,
    "mixed_entropy_ceiling_bytes_at_1e9_30bits": 30 / 8 * 1e9,
    "mu_crit_sqrt2_fixed": mu_crit,
    "m_crit_kg_sqrt2_fixed": mu_crit * M_SUN,
}
print("\n10^9 table (from truth rate):")
for k, v in R["table_1e9"].items():
    print(f"  {k:44s} {v:.4e}")

with open("soi_truth_results.json", "w") as f:
    json.dump(R, f, indent=1)
print("\nwrote soi_truth_results.json")
