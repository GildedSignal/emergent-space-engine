# Predictions (written before the decisive gate runs; the new tests alone have been run)

The change: the queue's key is each event's image on the root clock (its doll tick plus the doll chain's
simultaneity shear `sinh(η)·x̂_axis`, integer shears, frozen per entity at its requeue). Root-doll
events keep their ticks exactly; child-doll events move by `γ·(w·x)`.

## Held out (not tuned on)

1. **B13 (`--law plane`)**: the gate's ships live in the root doll for their whole flybys (v2 step 1
   disabled capture), so their keys are the identity and no code path they touch changes. Prediction:
   the detail line is **identical** to the baseline — `60/64 judged flybys within 1e-2 … worst ΔE
   2.12e-2 ΔL 2.12e-2`, same replaced draws.
2. **B17 (`--law plane`)**: same argument (root-doll ships). Prediction: FAIL by **timeout ≈ 60 s** on
   this Linux box, as before (the M1 passes it in time; the box does not).
3. **B8 (the universe suite)**: all 22 tests pass. The plane's Home-doll bodies (player, orbiters,
   leavers, fleet origin) get keys shifted by about ±0.5–5 ticks and the moon's by ±26, so the
   universe's digest **changes** relative to main — but every suite test compares runs with each other
   (schedules, threads, budgets), not against a frozen digest, and:
   - every doll centre's tube is frozen across every test's horizon (the planets' first kick is
     ~10^10 ticks out; the largest horizon in the suite is 5×10^14 on a one-planet scene with no
     forces), so the frozen keys are pure functions of committed state and every schedule reads one;
   - the moon (the only same-doll source with a big δ spread, ±26 ticks) has its next item ~3×10^9
     ticks out — beyond every horizon — so no read ever straddles the gap.
   Held-out risk I accept: if any test did compare against a frozen digest, it would fail; I know of none.
4. **Cost**: the extra work is one centre readout plus one `Frame::of` (a square root) per requeue of a
   **child-doll** entity only; root-doll entities (the planets, the B12/B13/B17 ships, most of the
   plane's haulers) add nothing. Prediction: the suite's wall time stays within ±10% of the baseline
   268 s.
5. **P6's falsifiability**: on main's keying (the doll tick), P6(a) fails for every member with
   |γ·(w·x)| > 0.5 ticks — most of the 1,000 (the spread is ±8,300) — and the order test resolves both
   members or neither at the between-keys cut.
