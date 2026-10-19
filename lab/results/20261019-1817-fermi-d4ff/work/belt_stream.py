#!/usr/bin/env python3
"""The belt's own interaction stream at 1e9, from shipped constants only.

Citations (shipped code, this tree):
- crates/universe/src/scenario.rs: AU = 101_300_000 root units ("The sun's M is
  1.477 km: one root length unit"); the belt genesis (a uniform in [2,3) AU at
  2^-8 root-unit quanta, e Rayleigh sigma 0.07 re-drawn above 0.4, uniform
  angle/phase); ship radius Scalar::raw(34, -10) root units.
- crates/universe/src/encounter.rs: ENCOUNTER_LOG2 = 10; reach = r_i + r_j;
  an encounter is within 2^10 * reach, a contact within reach.
- crates/universe/src/world.rs: doll units with G = c = 1, the star's GM = 1,
  so v_circ = a^(-1/2) and the root time unit = root length / c.
- 0659 (page-cited): clock cadence lambda = 3.55e-5 per body per game-s.

Method: sample the exact integer genesis (splitmix64 lanes ported verbatim),
place every sample at random phases over realizations, build the time-averaged
radial density n(r) and local mean relative speed <|dv|>(r), and integrate the
2D kinetic rate Gamma(d) = 2d * n(r) * <|dv|>(r) per body for d = contact and
d = encounter reach. Pure estimate layer: floats explore, the genesis integers
are exact.
"""
import json
import math
import random
import sys

MASK = (1 << 64) - 1
ROOT_KM = 1.477                 # one root length unit (GM_sun / c^2), km
C_KM_S = 299792.458
AU = 101_300_000                # root units (scenario.rs)
ROOT_T_S = ROOT_KM * 1e3 / (C_KM_S * 1e3)   # root time unit = root/c, seconds
LAMBDA = 3.55e-5                # 0659 clock cadence, /body/game-s
ITEM_US_X86 = 82.5              # 3aec: fired kick item stage, us/call x86
X86_TO_M1 = 208 / 355           # 3aec's x86->M1 anchor

# ---- the genesis, ported verbatim from scenario.rs -------------------------

def mix64(z):
    z = (z + 0x9E3779B97F4A7C15) & MASK
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK
    return z ^ (z >> 31)

def draw(seed, k, lane):
    return mix64(mix64(seed ^ 0x5DEECE66D1CE4E5B) ^ ((k * 0x9E3779B97F4A7C15) & MASK) ^ ((lane << 56) & MASK))

def rayleigh_q48(u, sigma_milli):
    d = (1 << 32) - (u & 0xFFFFFFFF)
    k = d.bit_length() - 1
    x = d << (62 - k)
    frac = 0
    for _ in range(32):
        x = (x * x) >> 62
        frac <<= 1
        if x >= (2 << 62):
            x >>= 1
            frac |= 1
    l2 = (32 << 32) - ((k << 32) | frac)
    ln = (l2 * 2_977_044_472) >> 32
    e2 = ((ln * 2 * sigma_milli * sigma_milli) << 64) // 1_000_000
    return math.isqrt(e2)       # e * 2^48

def belt_ship(seed, k):
    """(a in root units, e, periapsis in root units) of ladder belt ship k."""
    d1, d2, d3 = draw(seed, k, 1), draw(seed, k, 2), draw(seed, k, 3)
    a_q8 = ((2 * AU) << 8) + (d1 % ((AU << 8)))
    e = rayleigh_q48((d2 >> 32) & 0xFFFFFFFF, 70)
    lane = 16
    while e > (2 << 48) // 5:   # re-drawn above e = 0.4
        e = rayleigh_q48((draw(seed, k, lane) >> 32) & 0xFFFFFFFF, 70)
        lane += 1
    p_q8 = a_q8 - ((a_q8 * e) >> 48)
    return a_q8 / 256.0, e / float(1 << 48), p_q8 / 256.0, d3

def kepler_state(a, e, phase, theta):
    """Position/velocity at time-fraction `phase` since periapsis (G = 1)."""
    M = 2.0 * math.pi * phase
    E = M
    for _ in range(40):         # Newton; e <= 0.4 converges fast
        f = E - e * math.sin(E) - M
        E -= f / (1.0 - e * math.cos(E))
    cosE, sinE = math.cos(E), math.sin(E)
    r = a * (1.0 - e * cosE)
    s = math.sqrt(1.0 / a)
    vr = s * e * sinE / (1.0 - e * cosE)
    vt = s * math.sqrt(1.0 - e * e) / (1.0 - e * cosE)
    nu = math.atan2(math.sqrt(1.0 - e * e) * sinE, cosE - e)
    phi = theta + nu
    c, sn = math.cos(phi), math.sin(phi)
    return (r * c, r * sn), (vr * c - vt * sn, vr * sn + vt * c), r

def main():
    seed = 1                    # the record's own scene seed
    S = 20000                   # genesis samples
    R = 8                       # realizations (random phases/orientations)
    rng = random.Random(20261019)

    ships = [belt_ship(seed, k) for k in range(300, 300 + S)]  # skip the locals
    es = [s[1] for s in ships]
    per = [s[2] for s in ships]                # periapsis (p = a(1-e)), root units
    lanes = (AU << 8)

    # bins: 0.05 AU shells over the occupied annulus
    pts = []                    # (r, vx, vy) across realizations
    rs = []
    for a, e, p, d3 in ships:
        theta = ((d3 & 0xFFFFFFFF) / 2**32) * 2 * math.pi
        for _ in range(R):
            phase = rng.random()
            pos, v, r = kepler_state(a, e, phase, theta)
            pts.append((r, v[0], v[1]))
            rs.append(r)
    rmin, rmax = min(rs), max(rs)
    n_sh = 60
    dw = (rmax - rmin) / n_sh
    shells = [[] for _ in range(n_sh)]
    for r, vx, vy in pts:
        shells[min(n_sh - 1, int((r - rmin) / dw))].append((vx, vy))

    nprof, dvprof, weight = [], [], []
    for i, sh in enumerate(shells):
        r_in, r_out = rmin + i * dw, rmin + (i + 1) * dw
        area = math.pi * (r_out**2 - r_in**2)
        n = len(sh) / (R * area)          # density per root unit^2 per ship -> scale by N/S later? no: absolute per-body density uses N
        nprof.append(len(sh) / area)      # points per root^2 (S bodies, R realizations folded in count)
        # local <|dv|>: random pairs inside the shell
        if len(sh) >= 2:
            m = min(400, len(sh) * 2)
            acc = 0.0
            for _ in range(m):
                (ax, ay), (bx, by) = sh[rng.randrange(len(sh))], sh[rng.randrange(len(sh))]
                acc += math.hypot(ax - bx, ay - by)
            dvprof.append(acc / m)
        else:
            dvprof.append(None)
        weight.append(len(sh))
    wsum = float(sum(weight))
    # normalize density: each of S ships appears R times -> n at population N:
    # n_true(r) = nprof(r) * (N / S)   [R cancels: count = S_body-appearances]

    def mean_dv_global():
        acc, m = 0.0, 0
        for sh in shells:
            if not sh:
                continue
            for _ in range(20):
                (ax, ay), (bx, by) = sh[rng.randrange(len(sh))], sh[rng.randrange(len(sh))]
                acc += math.hypot(ax - bx, ay - by); m += 1
        return acc / m

    g_dv = mean_dv_global()

    r_s = 34 * 2.0**-10                       # ship radius, root units
    d_contact = 2 * r_s                       # center distance for a contact
    d_enc = (1 << 10) * d_contact             # encounter reach (2^10 * (ri+rj) = 2*rs*2^10)

    def gamma_bar(d):
        """per-body rate (root time units^-1) at N = 1, scaled later."""
        tot = 0.0
        for i in range(n_sh):
            if dvprof[i] is None:
                continue
            tot += (weight[i] / wsum) * 2 * d * (nprof[i] / (R * 1.0)) * (dvprof[i] if dvprof[i] else g_dv)
        return tot / S                        # nprof counts S*R points; /S leaves per-one-body density

    N = 10**9
    per_root_contact = gamma_bar(d_contact)   # per body per root-tu, N=1... careful: gamma uses n ~ S bodies; scale linearly
    # gamma_bar already divides by S, so it is the per-body rate for a population of 1: multiply by (N-1) ~ N
    g_c = per_root_contact * N / ROOT_T_S     # per body per game-s at N (encounters involving me)
    g_e = gamma_bar(d_enc) * N / ROOT_T_S

    pair_contact_s = N * g_c / 2.0            # pair events per game-s universe-wide
    pair_enc_s = N * g_e / 2.0

    lam = LAMBDA

    # closed-form cross-checks (independent of the shell machinery)
    # 1. <|dv|> for CIRCULAR orbits uniform in a over [2,3) AU, random phases:
    acc, m = 0.0, 0
    for _ in range(200000):
        v1 = math.sqrt(1.0 / ((2.0 + rng.random()) * AU))   # circular at a in [2,3) AU, root units
        v2 = math.sqrt(1.0 / ((2.0 + rng.random()) * AU))
        phi = 2 * math.pi * rng.random()
        acc += math.hypot(v1 - v2 * math.cos(phi), v2 * math.sin(phi)); m += 1
    dv_circ = acc / m
    # 2. global-mean kinetic rate (no shell correlation), for comparison
    area_occ = math.pi * (rmax**2 - rmin**2)
    n_bar = N / area_occ
    g_e_global = 2 * d_enc * n_bar * g_dv * N / ROOT_T_S / 2.0   # pair events per game-s

    conj_per_root = pair_enc_s / d_enc            # pair events/game-s per root unit of reach (linear in d)
    # the stream row's true addition: CONTACTS ONLY fire items (ships are massless test
    # bodies on exact orbits: a 100-km pass changes no orbit). Priced at the fired cost.
    rtf = 100.0
    item_us_m1 = ITEM_US_X86 * X86_TO_M1
    contact_cores_today = pair_contact_s * rtf * 2 * item_us_m1 * 1e-6
    contact_cores_floor = pair_contact_s * rtf * 2 * 6e-6
    # concentration thresholds
    C_contact = lam / g_c                          # contacts = the members' own clock stream
    C_enc_belttemp = lam / g_e                     # belt-temperature mixing zone
    F = 1e6
    n_belt = n_bar
    side_km = math.sqrt(F / (C_contact * n_belt)) * ROOT_KM

    out = {
        "units": {"root_unit_km": ROOT_KM, "root_time_s": ROOT_T_S,
                  "ship_radius_m": r_s * ROOT_KM * 1e3,
                  "contact_reach_km": d_contact * ROOT_KM,
                  "encounter_reach_km": d_enc * ROOT_KM,
                  "orbit_period_2p5AU_game_s": 2 * math.pi * (2.5 * AU) ** 1.5 * ROOT_T_S},
        "genesis": {"samples": S, "realizations": R,
                    "mean_e": sum(es) / len(es),
                    "rayleigh_sigma07_mean_prediction": 0.07 * math.sqrt(math.pi / 2),
                    "max_e": max(es),
                    "a_range_AU": [min(s[0] for s in ships) / AU, max(s[0] for s in ships) / AU],
                    "periapsis_range_AU": [min(per) / AU, max(per) / AU],
                    "occupied_r_AU": [rmin / AU, rmax / AU],
                    "lanes": lanes,
                    "mean_rel_speed_km_s": g_dv * C_KM_S,
                    "dv_circular_closed_form_km_s": dv_circ * C_KM_S},
        "rates_at_1e9": {
            "note": "pair events per game-s, shipped annulus, rate linear in reach d",
            "conjunction_pair_events_per_game_s_per_root_reach": conj_per_root,
            "encounter_pair_events_per_game_s_100km": pair_enc_s,
            "contact_pair_events_per_game_s": pair_contact_s,
            "contact_per_body_per_game_s": g_c,
            "encounter_per_body_per_game_s": g_e,
            "enc_events_over_clock_stream": pair_enc_s * 2 / (N * lam),
            "contact_items_over_clock_stream": pair_contact_s * 2 / (N * lam),
            "global_mean_crosscheck_enc_events": g_e_global,
            "filling_factor": n_bar * math.pi * r_s**2},
        "thresholds": {
            "contact_wakeup_N_per_game_hour": N * math.sqrt(1.0 / 3600.0 / pair_contact_s),
            "C_contact_equals_own_clock": C_contact,
            "C_encounter_belttemp_equals_own_clock": C_enc_belttemp,
            "fleet1e6_side_km_at_C_contact": side_km,
            "colane_pair_fraction_at_1e9": 1.0 / lanes},
        "ledger_fold": {
            "rtf": rtf, "item_us_x86": ITEM_US_X86, "item_us_m1": item_us_m1,
            "stream_row_addition_cores_today_cost": contact_cores_today,
            "stream_row_addition_cores_6us_floor": contact_cores_floor,
        "census_reconciliation": {
            "naive_uniform_expectation_at_1e4_in_1e3_gs": 1e4 * 1e3 * lam,
            "note": "uniform-rate expectation (355 at 1e4) OVERPREDICTS the census: f80a measured the belt's first clock wave at gs 11k-16k (onset), so a 1e3-gs census window (10 s wall, rtf 100) sees zero belt kicks by construction; the long arms then read 8.03 bindings/body at 174k gs = 1.30 x lambda (P2)"},
        },
        "p2_crosscheck": {"bindings_per_body": 8.03, "game_s": 174000,
                          "eff_rate": 8.03 / 174000.0, "ratio_to_lambda": (8.03 / 174000.0) / lam},
    }
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
