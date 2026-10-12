# Dossier: the jet's measured ceiling on the plane's kick path (second author on 20261011-2306-system-3367)

**Claim.** The checker's named gold experiment, done on the shipped record: the rebind (fit + fresh
cycle compile + readout + residual) is 33–36% of a made-body or player kick and 66–74% of a fleet
leaver's (49–62% the compile alone), so the law's jet — fold Δv into the residual, keep the cycle,
re-anchor at drift ≥ √(floor/C) — pays **0.002–0.012 compiles per kick** but drops the kick path's
time by only **1.3–1.5× (made, player) and 3.0–3.8× (leavers)**, converging everyone to a ~26 µs
floor of fictitious-clock law machinery: **the expected ~10× deletion does not exist at the plane's
scale**, and after the memo/jet lands, that machinery — not the fit, not the compile, not the i128
register — owns the kick path.

**Bottleneck.** Board focus line 1 (kicks dominate the engine's cost). The prior run priced the
adopted memo hook in shape counts (~95% of fits share 51 quantized keys); this run prices it in
time, which is what the queue's ordering needs. Expected gain now measured: ≤ 3.8× on leaver kicks,
≤ 1.5× on made/player kicks — the deletion is real but bounded, and the next bottleneck after it is
named and sized (~26 µs/kick of readout + forces + sigma-delta + planning).

## Evidence

Commands regenerate the whole record from this tree (patch = the prior run's plus this run's
`kick_bench.rs` extension; each ≤ 60 s, Linux/x86, 8 vCPU, load 2.4–4.3; orders of magnitude only):

```
cargo build --release -p xtask --features emergent-space/profile
$CARGO_TARGET_DIR/release/xtask universe --bench --rtf 100 --seconds 30                # bench-rtf100.json
$CARGO_TARGET_DIR/release/xtask universe --kick-bench --rtf 100 --seconds 30           # kickbench-rtf100.json
$CARGO_TARGET_DIR/release/xtask universe --kick-bench --seed 7 --rtf 100 --seconds 30  # kickbench-seed7.json
$CARGO_TARGET_DIR/release/xtask universe --kick-bench --rtf 1000 --seconds 10          # kickbench-rtf1000.json
$CARGO_TARGET_DIR/release/xtask universe --kick-bench --members 200 --rtf 100 --seconds 10 # kickbench-fleet200.json
```

The prior record's defect is fixed: the feature flag is in the build line. Bit-exact regeneration:
bench digest `41343a143a92f956…` at cut 609076340; kick replay `0e02bf0f34481650…`; ship memo 1125
rebinds / exact 0.0% / 51 quantized keys / 95.47% — all identical to run 20261011-2306's saved JSONs.

Method (all bench-side, public API only; no crate, gate or `main` edits): per distinct pending kick,
time `step::process` (the shipped path), then re-measure the component the jet deletes —
`Rebinding::from_state` on the resolver's own exact post-kick state — and `Orbit::compile` alone on
the key it fitted; the jet's replacement (fold Δv into the residual, threshold, occasional anchor)
is timed directly. `implied_jet_kick_us = whole − from_state + fold + anchor`. Input equivalence is
checked, not assumed: **from_state reproduced the resolver's own new-entry key 1284/1284, 1644/1644,
1805/1805, 3306/3306** across the four runs (100%).

1. **Attribution (medians, µs per distinct kick, rtf 100 / seed 7 / rtf 1000 / fleet 200).**
   - made ships (n = 365/365/1165/137): whole 38.6/38.6/38.3/38.7; rebind 12.9 (33%, 34%, 34%, 33%);
     compile alone 3.9 (10%).
   - fleet leavers (n = 793/1142/681/3197): whole 101.6/80.4/106.9/94.5; rebind 74.7/53.1/78.7/67.4
     (74/66/74/71%); **compile alone 63.3/43.6/52.6/57.5 (62/54/49/61%)** — the leaver rebind is the
     fresh cycle compile (the quadrature's knot count scales it).
   - player (n = 159/159/26/54): whole 39.3/39.3/54.0/40.0 on the pure resolver — **not** the
     ~569–1009 µs/item the live loop charges (`engine_cost_by_kind`, 296 items); rebind 33–36%.
     The live per-item figure is dominated by the surrounding per-frame machinery (the re-plan path
     behind the 5 October correction), not by the fit: the dossier's "could not attribute" resolves
     to *neither fit nor register — the machinery around them*.
2. **The jet, timed.** implied jet kick (medians): made 25.8/25.8/25.5/25.9 (drop 1.5×); leavers
   27.6/27.1/28.5/27.0 (**drop 3.7/3.0/3.8/3.5×**); player 26.1/26.1/40.6/26.8 (1.5/1.5/1.3/1.5×).
   The fold itself is ~0.1 µs (whole − rebind − jet ≈ 0.1 µs residual arithmetic + threshold).
   Anchors: 14/1158, 14/1507, 10/1846, 7/3334 kicks = **0.0121/0.0093/0.0054/0.0021 per kick**,
   against the red-team's bound of 0.05. Per-kick |Δv|/|v| medians are 2.3×10⁻⁹–1.2×10⁻⁸ (tides);
   the anchors come from 7–41 single large impulses (burns, battle Δv), not accumulation — at
   threshold/100 the count stays 7–41, so the rule is impulse-dominated in this scene.
3. **The 10× is refuted.** Even deleting the entire rebind (fit + compile + readout + residual,
   measured at 100% key fidelity) leaves every population at ~26 µs (player rtf 1000: 40.6): the
   fictitious-clock law machinery — readout, the perturbing potential, sigma-delta, planning — is
   the kick path's floor at the plane's scale. The prior run's "the memo deletes ~95% of its cycle
   fits" is true in shapes (94.5–97.1% across these runs; player 57–87% over 10–20 keys) and worth
   at most 3.8× in time.
4. **The memo integers hold everywhere** (ships: 1125/1485/1779/3252 rebinds, exact 0.0%, quantized
   95.5–97.1%); the profiler finding stands (`cycle_compile_ns` stages are zeros: the shipped
   profiler instruments `compile_sums`, a path the plane never calls — now documented inside the
   JSON with the bench-side attribution beside it).

## Predictions

`predictions.md` was written before the first extended-bench run (run-log records the order).
Outcome: **P3 held** (anchors ≤ 0.05/kick: 0.002–0.012); **P4 held exactly** (key match 100%, not
≥ 95%); **P1 half-held** (rebind ≥ 60% true for leavers 66–74%, false for made/player at 33%; the
compile ≥ 40% clause true only for leavers 49–62%); **P2 missed** (the ≥ 10× drop is 3.0–3.8× on
leavers, 1.3–1.5× on made/player — the honest ceiling, reported as the headline); **P5 missed**
(the player's distinct kick is 39 µs with a 34% rebind share; the ~1 ms live figure is machinery
outside the kick resolver, so the memo does not extend to it by the fit either).

## What would make it wrong

- `from_state` re-measured bench-side omits the law's `bind()` bookkeeping (tube fit, clock fit,
  `Arc`), so the true deleted component is slightly *larger* than measured — the ceiling is a lower
  bound on the deletion, which strengthens the refutation. The anchor path passed `None` as the
  passage edge (only periodic cycles rebounded here: 100% of key checks were `Cycle`).
- The drift proxy |Δv|/|v| stands in for the red-team's fractional (E, L) drift; at these sizes
  (≤ 10⁻⁸) both are far under √(floor/C) = 7.3×10⁻⁴, and anchors are single-impulse events either
  way. A scene with inspiraling or resonance-locked bodies (the red-team's Peters row) anchors
  every orbit and the jet's time gain there is unmeasured here.
- If the ~26 µs machinery floor is itself deletable (e.g. the planning half-kick reuse the memo
  finding flagged: the plane re-times a pending kick every frame), the *combined* deletion could
  exceed 3.8× — that is a separate mechanism, not the jet, and would need its own measurement.
- x86 medians on a loaded box: ratios (33/74%, 1.5/3.7×) held across four configurations; absolute
  µs re-measure on the M1.

## Cost of adoption, fit with PRINCIPLES

Adoption is still ordering advice, now with the honest number: land the memo hook (in flight), then
re-point the queue's v2-extending builds at the ~26 µs law-machinery floor instead of the fit. The
instrument lives in the kick bench (`rebind_attribution` + `jet` blocks regenerate with every run).
Principle 10 ("Measure before claiming"): the ~10× was a claim; it measures at 3.8×. Principle 1
("the cheapest compute is compute not done"): the jet deletes the compile for real (0.002–0.012
compiles/kick) — and the measurement says the next compute-not-done is in the kick's own planning
machinery. Principle 22 ("the simulation tells us what's next not us"): the queue's order now reads
off measured per-mechanism costs, including the player's, which this run separates from its live-loop
accounting.

## The lens

What the second-author lens may have missed: the jet prototype times the rebind path but does not
run the jet's *bits* end-to-end (no long-horizon error growth on the integer resolver — that stays
with the red-team's C·drift² law and the re-anchor rule; the 730-kick correlation regime is
unmeasured here). The implied jet arithmetic subtracts a re-measured component rather than running a
jet-resolver frame loop, so second-order cache effects between the law machinery and the deleted
compile are not captured (they would only *raise* the true jet time, strengthening the refutation).
And the player's live-loop 0.5–1 ms is attributed by elimination (pure-resolver replay vs
`engine_cost_by_kind`), not by instrumenting the frame loop itself.

## Files

`bench-rtf100.json`, `kickbench-rtf100.json`, `kickbench-seed7.json`, `kickbench-rtf1000.json`,
`kickbench-fleet200.json`, `predictions.md`, `run-log.txt`. Tree edit (saved as this run's patch):
`xtask/src/universe/kick_bench.rs` — the prior run's patch plus the attribution/jet extension
(player replay kept out of the digest, ships' memo and replay digest bit-identical to the record).
