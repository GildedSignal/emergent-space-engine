# Predictions — 20261008-2113-second-20261008-2031-constraint-4b27-08f7 (written before the decisive runs)

The repair under test (checker's named experiment): the author's one-probe cap (curvature at
t_e ± 8192, τ²-scaled to a 1e-4 rad bound) is replaced by **measured checkpoints**: the gate
extrapolates the linear model and, whenever the span tau crosses a checkpoint, probes the true
state at the current crossing tick (always readable: t_e + tau ≤ t_now), measures the actual
deviation of the linear model, refreshes the model from the probe, and re-arms the next
checkpoint at tau·(tol/2dev)^(1/4) (quartic-safe aim: even if the deviation grows with power 4
between checkpoints, it lands at ~tol). If a checkpoint measures dev > ½tol the crossing is
re-solved exactly that frame. The upfront ±S curvature probe and `measured_cap` are deleted.
One display quantum, consistently derived: **tol_len = 1e-4 · dist** bounds both |Δdirection|
(rad, ≈ Δpos⊥/dist) and relative |Δlight_seconds| (≈ Δpos∥/dist); shift stays second-order
(bound 1e-3). The author's 1e-5 ls bound was the mis-derivation (position error enters ls at
full relative size, not the distance ratio).

Held-out cases (not tuned on; the tuning set is one 1800-frame rtf-100 run used to debug
compile errors only):

1. **5400 frames, rtf 100** (the checker's failing case, max_dir 1.675e-4, max_rel_ls
   1.641e-4 before): max_dir ≤ 1e-4 and max_rel_ls ≤ 1e-4, worst offender no longer the
   planet Home late in the run (its long arc is now checkpointed). If the quartic-safe aim
   still leaks, it leaks on the body with the fastest curvature growth, and by less than the
   old 1.7× (the checkpoint measures the actual deviation at least every few frames).
2. **rtf 400, 1800 frames** (checker: over_cap 2, readouts 7, error ~1e-4 before): same
   bounds hold; readouts rise above the author's 7 (checkpoints fire ~4× more often per
   frame) — I predict ≤ 25 median; gather p50 stays ≤ 250 µs (baseline ~700).
3. **rtf 1, 1800 frames**: readouts ~0–2 (checkpoints almost never fire; marks dominate),
   gather p50 ≤ 60 µs, errors within bounds.
4. **Seeds 2 and 3 at 5400 frames, rtf 100** (the author hardcoded seed 1): same bounds
   hold; the mechanism is seed-independent by construction, so a bound breach on any seed
   would falsify the arming rule, not the seed.
5. **Readouts/frame at rtf 100 drop from 62 to ≤ 20 median** (the price of measured bounds:
   ~4–6 checkpoints per cold-body span instead of the author's 1 blind probe); warm gather
   p50 ≤ 250 µs (author claimed 86 µs with the blind cap; baseline ~690 µs).
6. **Digest identity**: baseline vs gated `xtask universe --bench --seconds 30 --rtf 100`,
   run back-to-back at one machine state, same seed — identical universe digest; the two
   cache-purity view tests still fail at ~1e-4 (the contract price, unchanged).
7. **Matched-state frame gain** (the checker's correction of the 7× headline): frame p50
   between 2× and 4×; gather p50 between 3× and 8×. If the frame gain is < 2× the economics
   of the gate are dead and I report that.

Kill criteria: any max_dir or max_rel_ls > 1e-4 on cases 1–4 kills the checkpoint arming as
built (not the diagnosis); readouts > 25 median at rtf 100 kills the economics; a digest
mismatch kills the read-only claim.
