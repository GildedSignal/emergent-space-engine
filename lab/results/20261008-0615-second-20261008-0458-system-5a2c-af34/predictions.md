# predictions.md — run 20261008-0615-second-20261008-0458-system-5a2c-af34

Written before the decisive run (`python3 reband.py sim`), after the harness was built and
calibrated only (quantization unit-checked against exact rationals; shipped-codec fixed
overhead 512 B; a harness crash at T=541 exposed no numbers).

Scene: -0458's belt (originals arm, 2047 bodies) + Jupiter, heliocentric leapfrog 775
steps/P_J, mean-element billing (boxcar 2 reference orbits), keys at the crate's true
`quantize(12)` (truncation, 2048 points/octave — 2× coarser than -0458's grid).
Store: records = occupied key cells, common-mode median tracking, reband every k orbits;
scars priced by shipped `shipmem::program::Program::seal_from` (Elias–Fano + block codec).

## Predictions (kill criteria in brackets)

1. **Static arms saturate.** frozen (birth cells never updated): scar fraction ≥ 0.9 within
   ~150 orbits [if it stays < 0.5 at 541, the claim's "static program saturates" is wrong on
   mean keys at the crate width]. tracked (common-mode, never regrouped): ≥ 0.6 by 541,
   scar bits/body ≥ 10 (the claim's "measures nothing"). [if tracked < 0.3 at 541, the
   shear at the crate width is too weak to matter and the reband is not needed.]
2. **Rebands bound the residue.** f_scar at cycle age k falls roughly linearly in k: ~0.3–0.6
   at k=200, ~0.05–0.25 at k=25. [if f(k=25) > 0.5, rebands cannot hold the belt and the
   claim's mechanism fails.] Steady-state scar bits/body at k=50: 1–6 bits; total (records
   + scars) < 10 bits/body for some k ≤ 100 [if no k ≤ 100 reaches < 15 bits/body total,
   the 0.5–2 GB billing claim at 10⁹ is refuted at this scene].
3. **Convergence.** At fixed k ≤ 100, per-cycle f_scar at the same cycle age is flat or
   falling over the last 200 orbits (no secular growth across rebands). [if it grows > 2×,
   the reband does not converge and only delays saturation.]
4. **Shipped Form P rejects the belt.** `shipmem::program::infer` on the members (birth
   order or key-sorted) returns None at every reband: no majority affine program exists for
   a belt; the reband's program family must be records/counter-mix, not `Prog::Affine`.
   [if infer returns Some, the shipped family suffices and the record layer is unnecessary.]
5. **Controls.** No-Jupiter: f_scar < 0.02 at every k ≥ 25 (the loop's noise floor ≈ 0;
   splits are Jupiter's). [if zero-Jupiter f(k=25) > 0.1, my loop mints scars from
   integrator noise, invalidating the decisive run.] Jupiter/10: f(k) ≈ f(10k) of the
   decisive run (forcing-linear aging).
6. **Occupancy stationary.** R (occupied cells) drifts < 20% over 541 orbits. [R growing
   > 2× means the belt spreads in key space and rebands pay rising record costs.]
7. **Cadence invariance (fixed dtest).** Matched-time off-birth fractions at 775 vs 1550
   steps/P_J agree within 0.02 absolute at orb ≥ 48 on mean keys. [if they disagree > 0.05,
   the decisive cadence is unconverged and the run is VOID on this instrument.]
