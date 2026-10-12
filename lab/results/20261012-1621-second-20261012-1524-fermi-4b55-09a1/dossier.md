# Dossier — 20261012-1621-second-20261012-1524-fermi-4b55-09a1 (second author)

**Claim.** The checker's named experiment is done, and the corrected claim holds
on a record that now regenerates end-to-end: at game scale, live distinguishing
information is created by rebinds through secondaries' spheres of influence and
by the player — co-dominant at ≈10 bits/s each, total H_live ≈ 21 bits/s
(2.6 B/s, 9.3 kB per hour of play) at 10⁹ bodies — while mutual encounters are
informationally inert at ship mass for ~10²⁶ years (m_crit ≈ 4.3×10¹⁸ kg with
the √2 fix), so the 8 GB budget is decided by birth programs (16 MB) plus the
mixed-population entropy after repopulation (the only term that can approach
the budget; ceiling ~3.75 GB at q_v = 10⁻⁵), and repopulation is load-bearing
because scattered singletons saturate in ~76 orbits ≈ 400 game-years.

This upgrades 20261012-1524-fermi-4b55 from "right structure, wrong headline"
to a reconciled record: one code path (`soi_truth.py`) now generates every
headline number, and the superseded values are kept as evidence, not silently
replaced.

**Bottleneck.** The same one the original run targeted: HANDOFF's
"Distinctions created per game-second (H_live) … decide whether 10⁹ fit in
8 GB; not measured yet" (board: `memory-h-live`). The silver verdict's named
blocker was the broken record itself: a 460× headline error (10³ text slip on
a 2.2× instrument bug) that no code path could catch. This run removes it.

## Evidence

Units: doll (GM_star = 1, a = 1, v_K = 1, orbit = 2π); anchor a = 3 AU,
M_star = M☉ → 1 orbit = 1.64×10⁸ s. Quantum q_v = 10⁻⁵ v_K. Belt: 10⁴ bodies,
σ_e = 5.5×10⁻³, a ∈ [1.0, 1.5]; planet μ = 10⁻³ at a_p = 1.25, circular;
R_SOI = 0.0867.

**The truth instrument (new, independent).** `soi_truth.py` counts SOI transit
*episodes* at rising edges of (dist < R_SOI) on a dense time grid — the control
asymmetry the checker named (the number that decided the headline had exactly
one instrument, the one fixed in a hurry):

| control | result | bound (predicted) | verdict |
|---|---|---|---|
| dt convergence 0.3 / 0.15 / 0.075 | 2600 / 2619 / 2626 episodes → 1.300 / 1.310 / 1.313×10⁻² | < 5% per halving | +0.7%, +0.3%: held |
| second seed 43 | 1.339×10⁻² | ± 10% | +2.2%: held |
| window 60 / 200 orbits | 1.303 / 1.305×10⁻² | ± 10% of 20-orbit | ±0.5%: held |
| sign-fixed Newton (the run's own §2, one-line fix) | 2380 hits = 1.190×10⁻² | within 15% of truth | 0.91×: held |
| analytic anchor (radial-overlap × synodic rate) | 2.186×10⁻² | factor ~2 | 1.7×: held |

**Adopted truth: Γ_SOI = 1.310×10⁻² transits/body/orbit** (seed 42, 20 orbits,
dt = 0.15). It lands inside the original pre-registered P3 range 0.01–0.05:
the prediction had held all along; the instrument had not. The as-shipped
Newton's 1197 hits (5.985×10⁻³) reproduce from `orig/crosscheck.py` unchanged;
the sign flip (`dn = npp − nb` against residual `λ_body − npp·t`, whose
derivative is `−dn`) is confirmed as the sole defect: fixed, the same machinery
scores 0.91× the truth.

**The regenerated 10⁹ table** (`soi_truth.py` → `soi_truth_results.json`;
every number below is code-generated from Γ_SOI, the path the original lacked):

| quantity | value |
|---|---|
| rebinds at 10⁹ | 7.98×10⁻² /game-second |
| H_live (rebinds, 128 bits) | 10.2 bits/s |
| H_live (player, ~10 decisions/s) | 10 bits/s — **co-dominant, not nil** |
| H_live (contacts, 10 m, 3 AU anchor fixed) | 0.87 bits/s (3.38×10⁻³ contacts/s) |
| **H_live total** | **21.1 bits/s = 2.64 B/s = 9.27 kB per hour** |
| singleton saturation 1/Γ | 76.4 orbits = 398 game-years = 4.0 wall-years at rtf 100 |
| birth programs | 15.75 MB (components-98bc, 0.126 bits/body) |
| mixed-entropy ceiling (30 bits/body) | 3.75 GB — the only 8 GB-scale term |
| m_crit (√2 fix) | 4.25×10¹⁸ kg (was 3.0×10¹⁸; regime boundary shifts by √2) |

The three mutually inconsistent headline values of the silver record
(42,462 / 4.7×10³ / 4.7 bits/s) are replaced by one: **21.1 bits/s**, 460×
below the original headline and ~2² above the bare rebind floor — with the
player's input a floor, not a rounding error, which is how `b-h-live` must
bound H_live.

**Reproduce** (each ≤ 60 s except the originals as noted; Linux x86 shared
runner, 8 vCPU, load 0.5–1.4, all runs < 200 MB):
```
cd lab/results/20261012-1621-second-20261012-1524-fermi-4b55-09a1
python3 soi_truth.py    # 46 s: truth + all controls + the 10^9 table
cd orig && python3 h_live_fermi.py   # 139 s: regenerates h_live_results.json bit-for-bit
cd .. && python3 orig/crosscheck.py  # 75 s in orig/: as-shipped bug, 1197 hits (5.985e-3)
```
`regen.sh` runs all three and diffs the originals' JSONs against the stored
copies; `soi_truth_results.json` is the record of record.

**Predictions.** See `predictions.md` (written before any run). All six groups
held: truth ∈ [1.0, 1.6]×10⁻² (measured 1.310×10⁻²); dt drift < 5% (0.7%/0.3%);
seed 43 within ±10% (+2.2%); sign-fixed Newton within 15% (0.91×) and strictly
above as-shipped (2380 > 1197); windows ±10% (±0.5%); table values as predicted
(rebinds 10.2 bits/s ≈ player 10 bits/s co-dominant, total ≈ 20–21 bits/s,
saturation ≈ 77 orbits ≈ 400 game-years). No falsifier fired.

## What would make it wrong

- More embedded secondaries: Γ_SOI is per-secondary; k planets → k× rebinds
  (k = 10 → ~100 bits/s ≈ 93 kB/h — still ~4 orders under any memory pressure,
  but the "player co-dominant" balance is k = 1).
- A quantum much finer than 10⁻⁵ v_K: encounter crossing times scale as q_v²,
  but rebind dominance is q_v-independent below ~0.1 v_K.
- Ships kept inside SOIs by gameplay: H_live then tracks player decisions
  directly (still input-bounded).
- The mixed-entropy ceiling (~30 bits/body) is a bracket, not a measurement —
  exactly what `b-h-live` must measure; if reality lands at 1 bit/body the
  whole budget question closes at 125 MB.
- Toy-to-10⁹ extrapolation is linear in N at fixed surface density with one
  secondary; the real universe's secondary census sets the prefactor.

**Cost of adoption.** None in code: this fixes a record, not the engine. What
`b-h-live` inherits: (1) H_live ≈ 21 bits/s per secondary at 10⁹ with the
player as a co-dominant floor — measure quantum-crossing deviations, not
certificate-event counts (overstates by ~5 orders); (2) repopulation is
load-bearing (76-orbit saturation); (3) the only term that can approach 8 GB
is post-repopulation mixed entropy.

**Fit with PRINCIPLES.** #24 "the memory floor is information": the corrected
floor is 21 bits/s of live distinctions, ~9 orders below the singleton store.
#6 "influences below one quantum accumulate": re-confirmed — the accumulation
lives in the field, not per-ship scars (P4, reproduced by the checker). #10
"Measure before claiming": the silver run's lesson, closed here — every
headline number now has exactly one generating code path. #33 regimes by
dimensionless numbers: μ/m_crit ≈ 4.25×10¹⁸ kg decides belt inertness.

**The lens (what the second-author lens may have made me miss).** I validated
the checker's correction rather than challenging it — the risk is shared
framing, so I added instruments the checker did not run (dt-convergence,
second seed, analytic anchor), and all agree; the residual risk is in the
inherited *assumptions*: 128 bits per rebind, ~10 player bits/s, one secondary,
2D belt (inclinations lower real density, so rates here are upper bounds).
Those are stated, not measured.

## Wiki

`wiki/memory-h-live.md` folds this result into the topic's first real page.
