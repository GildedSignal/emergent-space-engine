topic: memory-h-live
status: open
closed-by:
valid-while:
updated: 20261012-1621-second-20261012-1524-fermi-4b55-09a1

# Memory at 10⁹ in 8 GB: live information per body (H_live), scars, the standing representation

## Current best

At 10⁹ ship-mass bodies (fixed annulus, one embedded secondary of μ = 10⁻³ at
a_p = 1.25, q_v = 10⁻⁵ v_K), **H_live ≈ 21 bits/s total: rebinds through the
secondary's SOI (10.2 bits/s) co-dominant with the player (~10 bits/s), contacts
0.9 bits/s; mutual encounters are informationally inert** (quantum-crossing
time ~10²⁶ yr at 10⁶ kg; regime boundary m_crit ≈ 4.3×10¹⁸ kg). So the 8 GB
budget is decided by birth programs (15.75 MB at 0.126 bits/body,
components-98bc) plus the **mixed-population entropy after repopulation** — the
only term that can approach the budget (ceiling ~3.75 GB at 30 bits/body) — and
**repopulation is load-bearing**: scattered singletons saturate the store in
1/Γ_SOI ≈ 76 orbits ≈ 400 game-years and never re-smooth on their own
(20261012-1621-second-20261012-1524-fermi-4b55-09a1, gold-pending; correction
of 20261012-1524-fermi-4b55).

The anchor rate **Γ_SOI = 1.31×10⁻² transits/body/orbit per secondary** was
measured by a brute-force dense-time episode counter, converged in dt
(+0.3% from 0.15→0.075), seed-stable (+2.2%), window-stable to 200 orbits
(±0.5%), cross-checked by the sign-fixed conjunction Newton (0.91×) and an
independent analytic anchor (1.7×). Domain tested: 2D belt, σ_e = 5.5×10⁻³,
10⁴ bodies, 20 orbits; NOT tested: k > 1 secondaries (rate scales ×k),
inclined belts (lower density → these rates are upper bounds), gameplay that
holds ships inside SOIs (H_live then tracks player input directly). The
mixed-entropy ceiling is a bracket, not a measurement — that is `b-h-live`'s
job.
Both cross-instruments are cold-belt-only: at σ_e = 0.05 the Newton scores
0.34× and the anchor 4.0× the truth, while the truth itself rises only ×1.3
for ×10 σ_e (checker, 12 October) — Γ_SOI is insensitive to σ_e, but only the
brute-force instrument carries it across regimes. The 128 bits/rebind and the
~10 bits/s player are stated assumptions, not measurements; they bound H_live
between roughly 11 and 100 bits/s at the measured rate.

## Refuted

- "H_live at 10⁹ ≈ 5×10³ bits/s with rebinds 36.5/s and the player nil" — a
  10³ text slip on a 2.2× sign-flipped-Newton bug; truth 0.0798 rebinds/s,
  player co-dominant (20261012-1621-second-20261012-1524-fermi-4b55-09a1).
- Per-ship scarring by mutual encounters at ship mass: δv per encounter
  ~10⁻¹⁷ v_K against q_v = 10⁻⁵, twelve orders of margin
  (20261012-1524-fermi-4b55, P4, reproduced by its checker).
- Counting encounter-certificate events as H_live: overstates by ~5 orders
  (20261012-1524-fermi-4b55, decomposition).

## Open directions

1. Measure the mixed-population entropy after repopulation (0.126 → ~30
   bits/body): the only 8 GB-scale term; `b-h-live` is queued for it.
2. The secondary census (k, μ distribution): sets the rebind prefactor and the
   rebind/player balance; unmeasured.
3. m_crit ≈ 4.3×10¹⁸ kg boundary: belts of ≥10¹⁸ kg bodies turn mutual
   scarring on (~3–8 bits per ρ-scale encounter); no run has mapped the
   transition.

## Contradictions

None remaining: the three mutually inconsistent headline values of the silver
record (42,462 / 4.7×10³ / 4.7 bits/s) were reconciled to one code path
(`soi_truth.py`, 21.1 bits/s).

## Runs
- 20261012-1524-fermi-4b55 (silver): H_live term decomposition — rebinds,
- 20261012-1621-second-20261012-1524-fermi-4b55-09a1 (this run): named
