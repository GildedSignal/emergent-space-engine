# predictions.md — 20261011-2235-second-20261011-2132-spacex-91a0-e4cc

Second-author run. The first run's claim (H_live saturates; the store, not information,
bounds 10⁹-in-8 GB; the catalogue is the one unbounded grower) was graded silver for a
record defect only: its metrics.json and dossier say "zero kicks in 2000 game-seconds"
and "ships peak 275", contradicted by its own raw rows. The checker's named experiment
to gold: regenerate the record from shipped rows, correct the kicks statement, fix ships
peak, restate decision (3) on the corrected mechanism. Written before my decisive runs.

## P1 — the record regenerates from shipped code
`git apply work/patch.diff; cargo build --release -p xtask` then the four commands in
metrics.json reproduce the published rows: structural integers (members, distinct counts,
kicks_this_s, contacts, catalogue_live, bytes_per_body) exactly equal at matched
game-seconds; the coder's float bits agree to ~1e-3 (engine-budget jitter only). If any
structural integer differs, the record does not regenerate and the run is VOID-grade, not
correctable by editing.

## P2 — the corrected record (from the rows, not from the author's summary)
- kicks fire throughout, in bursts, to game-second ≈1995–2000; totals in the 10³ range
  per run (the checker named 7443/9160/5277/1113; my extraction from the published rows
  agrees, so this is a reproduction of a known defect, not a fresh prediction);
- ships peak near 360–370 for m400 (author's "275" is wrong);
- catalogue_live gain ≈ cumulative ship-spawn deltas (a churn leak), monotone;
- and the invariant the claim needs: ship tube bits/ship and fleet velocity bits/member
  stay flat (|slope| ≤ 1e-3 bits per game-second in the second half) DESPITE the kicks —
  i.e. kicks fire but accumulate no distinguishing bits under this coder. If instead
  bits/ship climb with a positive steady slope ≥ 0.1, the claim's core is refuted and I
  report a refutation.

## P3 — held-out horizon (not in the shipped record): 4000 game-seconds, seed 1, m400
- catalogue saturates once shedding/spawning stops: flat at its 2000 s value (428) from
  roughly s1500 on — bounded by cumulative ship creation, unbounded only under sustained
  churn (the checker's refinement, which my record must carry as its own number);
- contacts stay zero after their last burst; velocity/state/ship bits stay flat;
- bytes/body stays O(6–7 kB) and is NOT monotone late (bodies die, denominator shrinks);
- kicks keep firing in bursts at ~1–5 per game-second with no bit-growth consequence.

## P4 — held-out N-scaling: members 1600 (clamp raised locally, patch in work/)
- plateau velocity bits/member rises only ~log-quietly, to ≤ 22.5 (collisions absorb the
  log2(N) term; checker measured 22.26 at 1600);
- state bits/member unchanged in shape (log growth);
- catalogue ≈ 28 + cumulative spawns (~1600+), still churn-bounded;
- store bytes/body in the same 6–7 kB band. If instead bits/member grows like log2(N)
  beyond ~24, caveat (b) of the original dossier becomes a real risk and I say so.

## Controls
- determinism: two identical invocations of the s1 m400 command agree on every structural
  integer (if not, budget-order nondeterminism leaks into the record and snapshot
  integers must be quoted as ranges, as the checker noted (v)).

## Kill criteria
- any structural integer fails to reproduce → the record does not regenerate (report as
  such; nothing else matters);
- second-half |slope| of bits per member/ship ≥ 0.1 bits per game-second → the saturation
  claim is refuted;
- catalogue_live decreases anywhere or grows while ships stop spawning → my churn-leak
  reading is wrong.
