# Predictions — 20261009-0521 (second author on 20261009-0401-quant-ea6b)

Written before the decisive runs (m2000 rtf100 warm + cold pairing), after only the digest
control (default args, 23 samples: 11 legacy / 12 clock, digest `dac49af3…` identical clean vs
patched — so these predictions are made with knowledge of the *path split* at default args but
not of the m2000 stage shares; the checker's abstract states 84.8% rebind on the real path,
which I treat as a prior, not a measurement I have made).

The prior run's headline stage table (rebind 59.3%) came from `kick_clock` — 12 of 9192 samples.
The decisive experiment puts the timers on `fn kick` (the path the bench samples) and labels the
register path separately.

1. **Population.** At m2000 rtf100, the legacy `fn kick` path takes ≥ 98% of samples; the clock
   path stays ≈ 12 calls. The leavers on doll 2 dominate (checker: 7601/7640).
2. **Rebind share on the legacy path** (the sampled population): **> 75%** of legacy total_ns.
   Prior expectation ~84.8% (the checker's probe).
3. **Stage ordering on the legacy path:** rebind ≫ gather (secondaries+tide) > readout ≫
   forces_quant; forces_quant < 10%.
4. **Mean and the units audit.** Mean of all kicks lands in 40–60 µs at this load (~0.9); the
   in-record audit `calls × mean` matches `total_ns` within 25% (the prior run's own 10³ gap is
   what betrayed the wrong path).
5. **No-fire dilution.** Some legacy kicks are sub-quantum no-fires (rebind_calls < calls); the
   no-fire fraction is < 20%, and the rebind share stays > 70% even over all calls.
6. **Cold/warm.** Whole-kick cold/warm paired ratio 1.2–1.5×; the warm-phase stage shares inside
   the cold run match the warm run's shares within 5 points (the phase separation working).
7. **The clock path** (≈ 12 calls) reproduces rebind ≈ 55–65% — confirming the prior run's 59.3%
   was this path's number, mislabelled "(all kicks)".

If 2 or 3 fail, the jet/re-anchor lever's pricing changes: I report the shares as measured and
say what the lever is worth on the real path.
