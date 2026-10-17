#!/usr/bin/env python3
"""Compose the fleet encounter row into the published 10^9 CPU ledger.

Every input is a published constant, cited by run id; no new measurement.
Sources:
  [KC]  lab/wiki/kick-cadence.md current best: composed 10^9 ledger = 10.3 M1 cores
        at flown legality (4-core budget).
  [2373] 20261017-0839-inversion-2373 (encounters page, theirs side):
        fleet standing-rebuild row 36 / 383 / 4,500 cores at F = 1e3/1e4/1e5
        (10^9 ships in fleets, rebuild every 8 intervals of 28,141.5 game-s at
        rtf 100, 3.24 us/checked pair, sigma_e = 1e-2); per-member-kick rebuild
        arm 575 / 6,122 / 72,000 cores; paid occupancy ~97.6-98.9% of the
        complete graph (F = 3e4: 4.45e8 pairs); the answer stays rank-0
        (60 real contacts at F = 400, 55 checked pairs per real contact);
        k-bar = F*(4*e_max + 0.75*da*TAU*H)/TAU (linear in standing horizon H,
        refusal at H* ~ P_syn/2); fleet ceiling F* ~ 100 at sigma_e = 1e-2,
        proportional 1/sigma_e.
  [2B89] 20261017-0839-fermi-2b89 (encounters page, ours side): the live
        velocity word ev = -73 fires every Dohnanyi conjunction (exact tier
        full: 25.8 cores finding + 322 cores rebinds); coarsening 5-15 bits
        (kick still fires to ev ~ -45) moves D* 2.5 m -> 1.6 km and "revives
        f0a2's empty-tier world"; the flux accumulator (62f7) rides the kick
        stream at 4e-6 of the kick impulse (1.5e5 quanta/interval/body at 1e9).
  [f0a2] 20261014-1511-scout-f0a2: at the legacy anchor survivors are partners
        >= ~34 km; D* is the partner-size floor below which conjunctions never
        charge (delete 1.00000 on a Dohnanyi belt).
  [09b5] 20261006-0346-taleb-09b5 (gold, adopted) + coorbital-cert c5ab/a110:
        real contacts lie within phase rank <= 4 (formations); distance-rank is
        rho-bounded and cannot fail; required rank ~ n*sigma_e on dispersed
        fleets; a phase-neighbour certificate at O(n*k) replaces the quadratic
        tier.
  [57c1/8bfa] skin lever 12.6-3.7x; [277d] quantum gate ceiling 14-24x,
        event-scheduled f_r = 0.017-0.025 vs per-refresh 5-7; [fermi-1738]
        topology 2.2e4-1.1e5x, cadence 457x.
"""
import json
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_os.chdir(_HERE)


LEDGER = 10.3          # cores, [KC]
FLEET = {10**3: 36.0, 10**4: 383.0, 10**5: 4500.0}   # cores, [2373]
FLEET_KICK = {10**3: 575.0, 10**4: 6122.0, 10**5: 72000.0}  # cores, [2373]
SIGMA_E = 1e-2         # 2373's in-family dispersion
FLUX_FRAC = 4e-6       # of the kick stream, [2B89]/62f7
D_WORD_COARSE = 1.6e3  # m, [2B89] at ev ~ -45
SHIP = 49.0            # m, the fleet pair size used by [2B89]
PAIRS_COMPLETE_3E4 = 4.45e8  # [2373]
CONTACTS_F400, CHECKED_PER_CONTACT_F400 = 60.0, 55.0  # [2373]
LEVERS = {"slack skin (built)": 12.6, "quantum gate ceiling": 24.0,
          "cadence": 457.0, "topology": 1.1e5}  # x, cited above

out = {}
# P1: fleet share at the fine (live) word
for F, row in FLEET.items():
    tot = LEDGER + row
    out[f"P1 fleet share F={F:g}"] = {
        "composed_cores": round(tot, 1), "fleet_share": round(row / tot, 4)}

# P2: dial span. Coarse end: exact tier empty for same-size fleets -> the row
# is the flux accumulator only, priced as its fraction of the kick stream.
flux_row = FLUX_FRAC * LEDGER
out["P2 dial span"] = {
    "fine_cores": FLEET[10**5],
    "coarse_flux_row_cores": flux_row,
    "span_vs_conservative_0.01_floor": FLEET[10**5] / 0.01,
    "span_vs_flux_pricing": FLEET[10**5] / flux_row}

# P3: what the coarse end deletes. f0a2's survivors rule at the coarse D*.
out["P3 coarse-end deletion"] = {
    "D_star_coarse_m": D_WORD_COARSE,
    "ship_pair_m": 2 * SHIP / 2,  # partner size = 49 m
    "partner_below_D_star_deleted": SHIP < D_WORD_COARSE,
    "only_shipped_fleet_finder": "phase.rs standing certificate (the quadratic row itself; rank cert adopted in design, not the shipped trigger - 5ffb/2373)"}

# P4: paid pairs per real contact, and the horizon law's slope
r400 = CHECKED_PER_CONTACT_F400
r3e4 = PAIRS_COMPLETE_3E4 / CONTACTS_F400
out["P4 hypotheses per answer"] = {
    "F=400": r400, "F=3e4": r3e4,
    "growth_with_F": "monotone (paid ~ F^2 at fixed sigma_e, answer ~ O(F))",
    "kbar_slope_in_H": "linear: k-bar = F*(4*e_max + 0.75*da*TAU*H)/TAU [2373]"}

# P5 handled by verify_quotes.py.

# P6: naive event-driven rebuild does not close the gap
out["P6 per-member-kick arm vs standing"] = {
    F: round(FLEET_KICK[F] / FLEET[F], 1) for F in FLEET}

# Lever ordering on the encounter ledger (the fleet row's two escapes)
rank_cut = 2 * SIGMA_E  # complete-graph reach ~ pi vs required rank ~ F*sigma_e
out["L1 rank-certificate ceiling (sigma_e=1e-2)"] = {
    "cut": round(1 / rank_cut),
    "F=1e3": round(FLEET[10**3] * rank_cut, 2),
    "F=1e4": round(FLEET[10**4] * rank_cut, 1),
    "F=1e5": round(FLEET[10**5] * rank_cut, 1),
    "note": "even rank-certified, F=1e5 at sigma_e=1e-2 stays ~90 cores: the row needs the dial or the birth-constant representation, not a cheaper finder"}
out["lever ordering (x)"] = {k: v for k, v in sorted(LEVERS.items(), key=lambda kv: -kv[1])}
out["lever ordering (x)"]["word-width dial on the fleet row"] = out["P2 dial span"]["span_vs_conservative_0.01_floor"]

print(json.dumps(out, indent=1))
with open("compose_ledger_out.json", "w") as f:
    json.dump(out, f, indent=1)
