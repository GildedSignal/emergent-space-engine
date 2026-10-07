# Predictions (written before the post-edit runs; baselines measured 01:34–01:37 UTC)

Baselines on this box (8 vCPU, load ~0.4, release build):
- `behave --law echo --gates B17`: PASS, 9.13 s.
- `behave --law plane --gates B17 --plane-step 6`: PASS, 45.62 s (serial legs).
- `behave --law plane --gates B17` (default step 7): FAIL timeout, killed at 60.0 s.
- `behave --law space --gates B17`: FAIL timeout, killed at 60.0 s.

The patch: `Law: Sync` (Space's `RefCell` memo becomes a `Mutex`, three test laws' closures
carry `+ Sync`, one test's `Cell` an atomic), and `b17` runs its independent legs on up to four
threads with the truths' own work-stealing pattern; verdicts are read off in case order.

## Held-out predictions

1. **plane, default step 7 (the named gate):** PASS, wall 20–35 s on this box
   (serial legs ≈ 80 s at twice step 6's cadence, ÷4 threads, + truths ≈ 5 s).
   Detail line: same shape as step 6's, pumps near [0.999, 1.001], regime 34/34,
   controls 5/5, 0 unanswered, 1 of 41 not converged.
2. **echo:** PASS, and the detail line is **bit-identical** to the baseline line
   (`[0.999999, 1.000001] … 1.000 … 34/34 … 5/5; 0 unanswered, 1 of 41`), because each
   leg is an independent call and rows are re-sorted by case index. Wall ≤ 9.1 s.
3. **space:** PASS under 60 s (baseline: timeout) — its legs are independent dense
   integrations; the memo Mutex only serializes the shared shape cache.
4. **plane step 6 after:** PASS with the detail line identical to the baseline step-6
   numbers (same legs, same answers, only the schedule changed), wall ≈ 15–25 s.
5. **Planted laws keep their verdicts:** the resonance and amendment test modules pass
   unchanged (Averaged fails B17, the unanswered-case law still reports exactly
   "1 unanswered", echo passes); the full `cargo test --release -p xtask` behave suite passes.
6. **Memory:** peak RSS of the plane run stays ≈ 4× a serial leg's working set (four
   universes in flight, ≈ 0.5 GB at most), far under the 2 GB budget.

## What would make it wrong

Any difference in a detail line's numbers between serial and parallel runs of the same law
(would mean a leg is not independent — a shared-state bug in a law, not a scheduling fact);
a planted verdict flipping; plane B17 still over 60 s with legs measured ÷4 (would mean the
truths dominate the phase, not the legs — then the fix is in the reference, not the harness).
