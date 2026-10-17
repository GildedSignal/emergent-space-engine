# Predictions — 20261017-0839-dynamics-b966

Written before any `drift` run. Scene `drift`: two gas clusters (n=120 each) at ±140 units
closing at Q/8 each → hulls touch near chronon ~1000; two quiet islands at ±2000 units.
Config: default scheduler, min_region 1, margin 0.5, 3 P + 4 E workers. Instrument:
`crates/allocator/examples/finframe.rs` (this run's patch).

Cases below were NOT tuned on: this is the first execution of the `drift` scene in any mode.

1. **P1 (positive control, `drift chunks 150` to H=1800): crashes** with the shipped
   assert "rollback … would revise its published tick" (`alloc.rs:1451`) some time after
   chronon ~1000, i.e. in chunk ≥ 7. Basis: 9b46's checker showed the trigger class is
   "any conflict discovered after a publication" (their quiet-14k gas-drift, chunk 150).
   If it does not crash, my battery fails to reproduce the trigger and every other verdict
   here is VOID against the crash question.
2. **P2 (decisive, `drift frames 6s` at rate 600, ahead 0.25 s): crashes with the same
   assert.** Basis: in `run_frames` every worker commit publishes (alloc.rs:1759,1777), so
   publication is at least as frequent as chunked batch; the conflict at ~1000 is discovered
   after ~1500 publications. Alternative outcome I can not rule out from the code: the
   `ahead` cap (release_cap) bounds region lag near 150 chronons, which could keep the
   frontier below any clash start and protect frames mode structurally. Discriminator if it
   survives: rollbacks ≥ 1 with frontier at panic-free end ≥ 1000, and `chunks` crashing on
   the same scene — then publication cadence/lag, not conflict presence, decides the crash.
3. **P3 (`drift batch` single call to H=1800): survives.** Basis: 9b46's single-call draws
   show rollbacks ≥ 1 without the crash; the frontier (min verified) lags the clash start
   when no chunk boundary forces synchronized catch-up.
4. **P4 (`quiet frames`): no crash; rollbacks may be ≥ 1 (one observed in the smoke run at
   n=40 with no crash) — rollback without published-tick crossing is the normal path.
5. **P5 (if P2 crashes): the panic's numbers satisfy fin_hi > s0 ≥ ~900** (the clash starts
   near the discovery chronon, not at genesis) — i.e. the crash is the conservative
   stride-hull rollback start crossing published frontier finality, not a light-cone
   finality error.

Kill criterion for my own claim: if P1 fails (no crash in chunks), the battery does not
reach the trigger and nothing here speaks to the page's open question; report as VOID on
the crash question and keep only the schedule observations.
