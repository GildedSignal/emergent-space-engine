Working...
Check complete. `check.md` written with `Grade: gold`; nothing else in the run folder touched, no commits.

**Verdict summary:**

- **Reproduced bit-exact.** `jet` on seeds 2–3: identical digests, counts, hit rates, drift/divergence stats to `jet-heldout.txt`; `kick`/`frame` reproduce the prior record's `heldout.txt` digests; `jet 2` twice is deterministic. Only timings moved (shared-box noise; 13 MB peak RSS).
- **Mechanism verified in the crate, not trusted from prose.** `from_shape` refuses shape/key mixing (`Error::Topology`, orbit.rs:526), `QuantizedMemo` builds from the *decoded* coarsened key (so bits change by construction), the universe digest hashes `key.k`/`key.periapsis`/periapsis time+angle, and `fleet.rs` never compiles.
- **Pre-registration holds.** Last source edit 16:25:07 < `predictions.md` 16:25:36 < held-out run 16:25:41; tuning ran on seed 1 only (the smoke file still shows the pre-fix instrument, fixed before the decisive run). Kill criteria sat at 0 against their 5% thresholds; one soft miss (weak-branch 98.8–99.1% vs 100%) disclosed.
- **My adversarial cases held.** Fresh seeds 6–7 (0 exact repeats, 95.5/95.8% quantized hits, 0 bit-equal pairs, 0 anchors); independent recomputation of the ≈1.25× frame estimate (reproduces on the quiet box — the prior session's 198 µs/item was load); all headline arithmetic checks out.
- **Gold because it shows a premise is wrong, adoptably.** The prior silver's named gold condition (digest-identical jet wiring) is unsatisfiable — 0 of 4,367 key recurrences, 0 of 3,266 bit-equal consecutive compiles at ~10⁻⁹ ≈ 4×10⁹ Scalar ulps — and the law's recorded jet cadence (0.05 compiles/kick) is mis-sized for the plane by ~2500× (n* ≈ 10⁵). The honest prize is `QuantizedMemo` at ~70×/use as a B-gate law change. Flagged as missed: H0212/H0213 citations for the already-known 0%/95% substrate, the cadence-regime reconciliation, and the excluded non-weak ~1% close-encounter kicks.
