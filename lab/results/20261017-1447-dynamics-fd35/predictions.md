# Predictions — 20261017-1447-dynamics-fd35

Written before the decisive matrix (the seed × replicate arms below). Probes already run
(scene-finding only): the instrument builds, logs HAZ/PRE/RB, and the churn class produces
masses of rollbacks with every realized clash at `fin_hi == s0` exactly.

## The instrument

- `HAZ` (every publish): frontier, `F` = max published fin_hi, `S` = deepest live truth
  start, `g = F − S`, and `A` = the per-pair armed margin — max over (busy stride B) ×
  (live truth L) with B's hard-speed reach hull not separated from L's box, of
  `fin_hi(desc(B) ∪ desc(L)) − min(s_B, s_L)`.
- `PRE` (every finished stride, before certify): the same pair scan with the measured
  truth hull; `D > 0` ⟺ the upcoming certify clash fires the assert (modulo the
  descendants superset of rollback's snapshot closure).
- `RB`/`FIRE` (every rollback): the exact assert inputs.

## Arms (decisive matrix)

- churn-loaded: n=3000/cluster, sp=40, vmax=64, sab=3, min=1, rate=2400, ahead=1.0, 4 s —
  seeds 11, 15, 21, 2 (the page's propensity-skewed seeds) + 2 replicates on 11 and 15.
- fast-dispersal: n=1000, sp=100, vmax=160, sab=3, min=1, rate=600, ahead=1.0, 6 s —
  seeds 11, 15, 21, 2, ×2.
- controls: churn-loaded with min_region=32 (the page's clean knob), seeds 11, 15;
  single gas vmax=2 (already run: seeds 11/15/21, clean).

## Pre-registered predictions

- **P1 (0-crash):** no arm fires the assert (my classes are not the firing class; 0 of
  ~14 arms). If one fires, P5 applies.
- **P2 (armed never positive):** `max A = 0` over every publish of every arm; publication
  rides the contact boundary and never crosses it in these classes.
- **P3 (the equality law):** every realized clash has `fin_hi − s0 = 0` exactly (all RB
  margins `m = 0`, all `D = 0`); no negative margins either (publication never lags a
  restorable clash).
- **P4 (the knob):** min_region=32 arms have ≈ 0 rollbacks (the knob deletes the
  conflicts) and never arm.
- **P5 (if anything fires):** the FIRE pair's `fin_hi − s0` is ≤ the max armed margin seen
  at an earlier publish of the same draw (the race was visible in state first), and the
  PRECERT D of the firing stride is > 0 (same commit).
