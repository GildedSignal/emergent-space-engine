#!/usr/bin/env python3
"""Reconciliation: the flux model against engine-side belt measurements, and the claim at 1e9.

Part A: shipped `encounters verify a` (massless planar rung belts, exact truth) vs the flux
        model's two cross-section forms evaluated at each belt's own geometry.
Part B: the live belt (this folder's `sim`, impulses on shipped machinery) vs the planar
        threshold form 4*sigma_n*mu/q per unit time (per-body kick dv(b) = 2 mu/(b v_rel),
        strip rate 2 sigma_n v b -> v cancels; no fitted constants).
Claim: the dossier's belt (a=2.5 AU, N=1e9, m=1e15 kg, q=1e-6 v_kep, 300-h game), 3-D form
        (ledger.py P1) vs planar form, at 50 bits per quantum-crossing write.
"""
import json

G = 6.674e-11
AU = 1.496e11
MSUN = 1.989e30
GAME = 300 * 3600
BITS = 50
TAU = 2 * 3.141592653589793

out = {}

# ---- Part A: verify a (measured 7 Oct, shipped code; truth_enc / (n*orbits)) ----
A = [
    # (sigma_e, orbits, truth_enc)
    (1e-3, 200.0, 35),
    (3e-3, 100.0, 68),
    (1e-2, 100.0, 189),
    (3e-2, 50.0, 248),
]
rows = []
for sigma_e, orbs, enc in A:
    n = 1000.0
    meas = enc / (n * orbs)
    a_bar, w = 1.25, 0.5           # belt a in [1, 1.5]
    sigma_n = n / (TAU * a_bar * w)
    strip = TAU * sigma_n * sigma_e * 2e-4          # v_rel = sigma_e
    H = 0.5 * sigma_e * a_bar                        # ledger.py's vertical scale
    n3 = n / (TAU * a_bar * w * 2 * H)
    tube = TAU * n3 * sigma_e * 3.14159 * 1e-4**2   # P6's form, true width
    rows.append(dict(sigma_e=sigma_e, measured=meas, strip_vrel_sigm=strip, tube=tube,
                     strip_over_meas=strip / meas, tube_under_meas=meas / tube,
                     vrel_eff=sigma_e * meas / strip))
out["A"] = rows
out["A_p6"] = dict(p6_model=3.1416e-4, p6_rung_remembered=1e-2, p6_gap=1 / 0.0314159,
                   belt_s1em2_measured=189 / (1000 * 100.0),
                   form_plus_width_gap=(189 / (1000 * 100.0)) / 3.1416e-4,
                   remembered_vs_this_belt=1e-2 / (189 / (1000 * 100.0)))

# ---- Part B: live belt (measured 7 Oct, this folder's sim on shipped machinery) ----
# crossings per body per orbit; mu = m/MSUN; sigma_n = N/(TAU*1.25*0.5); q = 1e-6.
B = []
for line in open(__file__.rsplit("/", 1)[0] + "/sim-rungs.json"):
    r = json.loads(line)
    B.append((r["n"], r["m_kg"], r["orbits"], r["crossings"], r["kicks"]))
rows = []
for N, m, orbs, cr, k in B:
    if cr is None:
        continue
    sigma_n = N / (TAU * 1.25 * 0.5)
    mu = m / MSUN
    q = 1e-6
    single = TAU * 4 * sigma_n * mu / q      # per orbit
    rows.append(dict(N=N, m_kg=m, orbits=orbs, crossings=cr, kicks=k,
                     measured=cr / (N * orbs), model_single=single,
                     meas_over_model=cr / (N * orbs) / single,
                     recert_kicks_per_crossing=k / cr))
out["B"] = rows
if len(rows) >= 3:
    import math
    r0, r1, r2 = rows[0], rows[1], rows[2]
    eN = math.log(r1["measured"] / r0["measured"]) / math.log(r1["N"] / r0["N"])
    em = math.log(r2["measured"] / r1["measured"]) / math.log(r2["m_kg"] / r1["m_kg"])
    out["B_exponents"] = dict(in_N_at_1e18=eN, in_m_at_N4000=em)

# ---- The claim at 1e9, both geometries ----
# belt: a=2.5 AU, w=1.3 AU, sigma_e=0.02, N=1e9, m=1e15 kg, q=1e-6*v_kep (ledger.py P1)
v_kep = (G * 1.989e30 / (2.5 * AU)) ** 0.5
q = 1e-6 * v_kep
a, w = 2.5 * AU, 1.3 * AU
sigma_n = 1e9 / (TAU * a * w)
planar_rate = 4 * sigma_n * G * 1e15 / q            # /body/s (threshold form, anchored by B)
p1_3d_rate = 2.6987217330244414e-12                  # ledger.py P1 (diffusive, 3-D volume)
per_game = lambda r: r * GAME
out["claim"] = dict(
    q_ms=q,
    planar=dict(rate_per_body_s=planar_rate, crossings_per_body_game=per_game(planar_rate),
                writes_per_s_at_1e9=planar_rate * 1e9,
                ledger_MB_per_game=per_game(planar_rate) * 1e9 * BITS / 8 / 1e6),
    threeD=dict(rate_per_body_s=p1_3d_rate, crossings_per_body_game=per_game(p1_3d_rate),
                writes_per_s_at_1e9=p1_3d_rate * 1e9,
                ledger_MB_per_game=per_game(p1_3d_rate) * 1e9 * BITS / 8 / 1e6),
    claim_was_MB_per_game=1.0,
    planar_over_claim=per_game(planar_rate) * 1e9 * BITS / 8 / 1e6,
)

print(json.dumps(out, indent=1))
with open("lab/results/20261007-0933-second-20261007-0842-fermi-fc22-a7d0/ledger2-out.json", "w") as f:
    json.dump(out, f, indent=1)
