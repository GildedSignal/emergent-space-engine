#!/usr/bin/env python3
"""The distinction ledger (H_live) at 1e9 bodies: which memory/throughput term breaks first.

All rates per body per SIMULATED second (game-second). One 300-h game = 1.08e6 game-s.
Belt model: 3D sheet, encounters by gravitational focusing (Chandrasekhar-style flux).
  Gamma(<b) = n * v_rel * pi * b^2           (b < H, 3D)
  Gamma(<b) = sigma_n * v_rel * 2b           (b >= H, 2D sheet, saturating)
  kick dv = 2Gm/(b v_rel)  (b >> b_90);  dv = v_rel (b <= b_90)
First passage of quantum q_v: single-kick rate Gamma(b < b*) with b* = 2Gm/(v_rel q_v),
diffusive rate D/q_v^2 with D = n pi (2Gm)^2/v_rel * ln(b_max/b_min); report max of the two.
"""
import json, math

G = 6.674e-11
AU = 1.496e11
MSUN = 1.989e30
GAME = 300 * 3600  # 300-hour game, game-seconds

def belt(n_bodies, a_au, width_au, sigma_e, m_body):
    a = a_au * AU
    w = width_au * AU
    H = 0.5 * sigma_e * a               # scale height from inclination ~ sigma_e/2
    vol = 2 * math.pi * a * w * 2 * H
    n = n_bodies / vol
    sigma_n = n_bodies / (2 * math.pi * a * w)
    v_kep = math.sqrt(G * MSUN / a)
    v_rel = sigma_e * v_kep             # dispersion-dominated (epicyclic ~ sigma_e)
    return dict(a=a, w=w, H=H, n=n, sigma_n=sigma_n, v_kep=v_kep, v_rel=v_rel, m=m_body)

def gamma_lt(b, B):
    """Rate of encounters within impact parameter b, per body per second."""
    g3 = B["n"] * B["v_rel"] * math.pi * b * b
    g2 = B["sigma_n"] * B["v_rel"] * 2 * b       # sheet saturation at large b
    return min(g3, g2) if b > B["H"] else g3

def crossing_rate(q_v, B, b_min=1.0):
    """Rate of element changes >= q_v (single strong kick + diffusion), /body/s."""
    m, v = B["m"], B["v_rel"]
    b90 = G * m / v**2
    bstar = 2 * G * m / (v * q_v)
    single = gamma_lt(min(bstar, B["H"]), B) if bstar > b90 else gamma_lt(b90, B)
    b_max = B["H"]
    b_lo = max(b_min, b90)
    if b_max > b_lo:
        D = B["n"] * math.pi * (2 * G * m) ** 2 / v * math.log(b_max / b_lo)
        # saturate the diffusivity at the sheet rate beyond H
        D += B["sigma_n"] * 2 * v * (2 * G * m / (B["H"] * v)) ** 2 * 0  # (beyond-H kicks < b90: nil)
    else:
        D = 0.0
    diff = D / q_v**2
    return dict(single=single, diffusive=diff, total=max(single, diff),
                bstar=bstar, b90=b90)

out = {}

# ---- P1: asteroid-mass belt, quantum 1e-6 v_kep ----
B = belt(1e9, 2.5, 1.3, 0.02, 1e15)
q = 1e-6 * B["v_kep"]
r1 = crossing_rate(q, B)
out["P1"] = dict(q_v_ms=q, per_body_per_s=r1["total"],
                 per_body_per_game=r1["total"] * GAME,
                 ledger_bits_per_game_1e9_bodies=r1["total"] * GAME * 1e9 * 50)

# ---- P2: mass needed for the 10^-8 /body/s scar budget ----
def total_rate(m, q_frac=1e-6):
    B2 = belt(1e9, 2.5, 1.3, 0.02, m)
    return crossing_rate(q_frac * B2["v_kep"], B2)["total"]
lo, hi = 1e15, 1e40        # rate ~ m^2 in both regimes
r_lo, r_hi = total_rate(lo), total_rate(hi)
m_need = lo * (1e-8 / r_lo) ** 0.5
out["P2"] = dict(rate_at_1e15=r_lo, rate_at_1e24=total_rate(1e24), rate_at_1e27=total_rate(1e27),
                 mass_for_1e8_budget_kg=m_need,
                 over_stellar=bool(m_need > 1e30 * 1.0))

# ---- P3: collisions (contact radius) in a 1e21 kg belt of 1e9 bodies ----
m_c = 1e21 / 1e9
r_body = (3 * m_c / (4 * math.pi * 2500)) ** (1 / 3)
B3 = belt(1e9, 2.5, 1.3, 0.02, m_c)
g_col = gamma_lt(2 * r_body, B3)
out["P3"] = dict(body_mass_kg=m_c, body_radius_m=r_body, per_body_per_s=g_col,
                 events_per_game_all_bodies=g_col * GAME * 1e9,
                 ledger_bits_per_game=g_col * GAME * 1e9 * 50)

# ---- P4: a 1e6-ship formation at 2.5 AU ----
a = 2.5 * AU
V = 2 * math.pi * a * 1e5 * 1e4          # ribbon 100 km wide, 10 km thick
n_f = 1e6 / V
v_f = 1.0                                 # m/s station-keeping dispersion
g_f = n_f * v_f * math.pi * (1e3) ** 2    # within 1 km
dv_f = 2 * G * 1e9 / (1e3 * v_f)
out["P4"] = dict(density_per_m3=n_f, per_ship_per_s=g_f, events_per_game=g_f * GAME * 1e6,
                 dv_ms=dv_f, ledger_bits_per_game=g_f * GAME * 1e6 * 50)

# ---- P5: kick throughput at 1e9 bodies, 2^7 kicks/orbit ----
per_au = {0.39: None, 1.0: None, 2.5: None, 5.2: None}
for a_au in per_au:
    P_s = math.sqrt(a_au**3) * 3.156e7
    per_au[a_au] = dict(period_s=P_s, kicks_per_body_s=128 / P_s,
                        kicks_per_s_at_1e9=128 / P_s * 1e9,
                        averaged_0p3_per_s_at_1e9=0.3 / P_s * 1e9)
out["P5"] = per_au

# ---- P6: calibration against r8 v2's measured ~1e-2 encounters/body/orbit ----
# rung units: a=1, GM=1 (v_kep=1), N=1e3, sigma_e=1e-2, rho=1e-4, belt width 0.1 (guess: 10 sigma_e spread)
B6 = dict(a=1.0, w=0.1, H=0.005, n=1e3 / (2 * math.pi * 1 * 0.1 * 2 * 0.005),
          sigma_n=1e3 / (2 * math.pi * 1 * 0.1), v_kep=1.0, v_rel=1e-2, m=0.0)
g6 = gamma_lt(1e-4, B6)
out["P6"] = dict(per_body_per_s=g6, per_body_per_orbit=g6 * 2 * math.pi,
                 rung_measured=1e-2, ratio_to_rung=g6 * 2 * math.pi / 1e-2)

# ---- P7: tiered store arithmetic ----
near_bodies = 1e6
out["P7"] = dict(
    budget_bytes_per_body=8.0,
    births_bits_per_body=0.126, births_total_MB=0.126 * 1e9 / 8 / 1e6,
    tube_only_GB=16 * 1e9 / 1e9,
    measured_today_TB=2349 * 1e9 / 1e12,
    tiered_GB=(near_bodies * 2349 + 1e9 * 4) / 1e9,          # 1 system live + 4 B coarse words
    tiered_tube_floor_GB=(near_bodies * 16 + 1e9 * 4) / 1e9, # same, live system at raw tube cost
)

import random
random.seed(20261007)
# (a) 3D flux tail: with b uniform in area on [b_lo, b_max], P(dv > x) = ((K/x)^2 - b_lo^2)/(b_max^2 - b_lo^2) ~ x^-2
NMC = 400000
b_lo, bmax = 0.1, 1.0
bs = [math.sqrt(b_lo**2 + (bmax**2 - b_lo**2) * random.random()) for _ in range(NMC)]
dvs = [1.0 / b for b in bs]
xs = [1.2, 2.0, 5.0]
tail = {str(x): sum(1 for d in dvs if d > x) / NMC for x in xs}
tail_pred = {str(x): ((1 / x)**2 - b_lo**2) / (bmax**2 - b_lo**2) for x in xs}
out["MC_tail"] = dict(measured=tail, x_minus2_predicted=tail_pred)

# (b) sensitivity: a 30x tighter belt (P6's gap to the rung) and a fine near-cone quantum
Bt = belt(1e9, 2.5, 1.3 / 30, 0.02, 1e15)
rt = crossing_rate(1e-6 * Bt["v_kep"], Bt)
Bf = belt(1e6, 2.5, 1.3, 0.02, 1e15)
rf = crossing_rate(1e-9 * Bf["v_kep"], Bf)
out["P_sens"] = dict(
    tight_belt_rate_x30=rt["total"],
    tight_belt_ledger_bits_per_game=rt["total"] * GAME * 1e9 * 50,
    near_fine_q_per_body_per_s=rf["total"],
    near_fine_q_ledger_MB_per_game=rf["total"] * GAME * 1e6 * 50 / 8 / 1e6,
)

# (b) first passage of a random walk with step variance s2 per unit time: rate ~ s2/q^2 (factor ~1-3)
q = 1.0
s2 = 1e-3
T = 200000
pos = 0.0
crossings = 0
for _ in range(T):
    pos += random.gauss(0, math.sqrt(s2))
    if abs(pos) >= q:
        crossings += 1
        pos = 0.0   # reabsorb: re-quantize (the ledger records the level crossing only)
out["MC_walk"] = dict(measured_rate=crossings / T, predicted=s2 / q**2)

print(json.dumps(out, indent=1))
with open("lab/results/20261007-0842-fermi-fc22/ledger-out.json", "w") as f:
    json.dump(out, f, indent=1)
