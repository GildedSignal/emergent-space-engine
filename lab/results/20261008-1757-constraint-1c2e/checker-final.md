Working...
Check complete. `check.md` written; tree restored to clean (patch reverted, my probe example deleted); nothing else in the run folder touched.

**Grade: silver.**

What I did:
- **Reproduced** on a clean tree with `work/patch.diff` applied: kick-bench seeds 1 and 7 (replay digest, memo 807/807/45, all e-percentiles bit-identical; timings within shared-host noise — mean kick 101.7 vs 106.8 µs, compile share 54.4% vs 54%), compile sweep (knots identical at every e, µs within 1%), frame bench (digest identical, engine ~20%, zero hitches >16.7 ms). Verified in source that every cycle rebind pays exactly one `Orbit::compile` with no memo on the path — the 54% is a real share, not a double count.
- **Adversarial:** extrapolated the sweep into the plane's tail (e up to 0.9999999: law holds, 390 knots/286 µs, no CAP bites) — which *contradicts* the dossier's specific p99 attribution (e p99 = 0.9995 compiles at only ~141 µs; 415 µs needs e ≳ 0.9999); re-derived the Fermi (all arithmetic checks); caught the 807/830 denominator slip (52.4% per kick, not 54%).
- **Novelty:** no prior H entry or doc measures the compile cost law, its share of the kick, or the plane's e-mix; the log₂(r_apo/r_peri) shape is B9's bound's law and the 0% exact-memo is the 5 Oct adjudication — both cited honestly.
- **Predictions:** ordering verified against file times; P2 and P3 failed as written and are reported as failed.

Not gold: nothing moved — it prices levers (quantized grid 18× is Julien's call, cadence was already the board's lever, lazy arcs untested) and two of four held-out predictions failed. The named experiment to gold: lazy arcs with a closed-form/quantized period, measured as compile-work removed at unchanged canonical sums. Also flagged: three prose numbers disagree with the run's own JSON (worst 11.2 vs 12.27 ms etc.), and the ~45 µs resolver remainder — the constraint for low-e belts — was left unmeasured.
