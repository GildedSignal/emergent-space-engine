Grade: silver

The plane pays a fresh exact orbit compile on every kick while the quantized memo its own `law.md` declares sits unwired; wiring it cuts the rebind 3.7× (quadrature), bit-exact at the event. Reproduced: memo_bench cutover 3.55× (37.3→10.5 µs) vs the author's 3.74×, codeΔ and hit-rate columns identical (0.000/0.190/0.667; flyby hit 0.000), residuals flat, all 22,000 exactness asserts pass; kick-bench 23 samples/0 refused; 50/0 tests. Gain: ~3.7× per rebind now; the ≥10× needs the fit deleted (readout is 3.3 µs). Adopt: one wire into `crates/universe` bind plus B-gate/digest re-freeze. The "key change rate ≈0" certificate holds only at e ≤ 0.6 with tide-sized kicks: my e = 0.95 at 2⁻²⁴ gives codeΔ 0.724, near-parabolic e = 0.999 gets nothing (hit 0.407).

## Reasons

**Reproduction (clean tree, patch applied by me).**
- `memo_bench`: all six streams behave exactly as reported. My timings (shared container): ecc-planet 37.29/10.49 µs (cutover 3.55×; author 29.2/7.8, 3.74×), weak-planet 14.64/10.37 (1.41×; author 1.47×), strong-ship 40.68/11.31 (3.60×; author 3.75×). The deterministic columns match digit for digit: codeΔ 0.000/0.190/0.000/0.667, hits 1.000/0.999/1.000/0.988, flyby hit 0.000, residual h1≈h2 on every stream. All `reconstruct() == input` asserts pass both paths.
- Kick-bench: 23 samples, 0 refused; median 49.0 µs, p99 89.6 (author 40.4/66.9; HANDOFF 29 µs on the M1 — same order, cloud timings are order-of-magnitude).
- `cargo test --release -p emergent-space`: 50 passed, 0 failed (the patch is additive; the author said 45 — counting method, not substance).
- The patch is minimal and honest: `from_state_memoized` is `from_state` with `Orbit::compile(key)` → `memo.get(key)`, shared `finish`; fit unchanged. The plane's `bind_in` (crates/universe/src/bind.rs:185) calling the exact path per kick is confirmed.

**Predictions.** `predictions.md` (15:31) predates `dossier.md` (15:39); `run.log` is empty, so the log order cannot be audited — a hole, but the reporting is internally convincing: P3 is reported *held-failed* (3.7×, not 10×) and P2's weak-branch miss (32% vs ≥ 50%) is admitted. A post-hoc author predicts 3.7×.

**My adversarial cases.**
- *A1, the unmeasured cost:* the bucket itself changes the between-event worldline. Exact compile vs `memo.get` on the same key: relative period error up to **4.4×10⁻⁴ (≈ 2⁻¹¹, the 11 fraction bits)**, precession error ≤ 2.7×10⁻⁷·TAU, encode/decode round-trips. With 64 kicks/cycle and an exact re-fit at every event, the between-event phase error stays ~10⁻⁵ and bounded — but this is the number the B-gate re-freeze judges, and the author never measured it.
- *A2, the certificate's domain:* the headline "key change rate ≈0" fails well inside the author's own risk envelope. At e = 0.95 with their *smallest* kicks (2⁻²⁴): codeΔ **0.724** (39 buckets revisited; the memo still pays 60.8→8.1 µs, 7.5×). Strong-field e = 0.6 at 2⁻²⁰: codeΔ **0.923** (the author ran only weak-field at that size: 0.19). Bound near-parabolic e = 0.999: hit 0.407, 1,186 shapes for 2,000 kicks, **no gain at all** (120.5 vs 120.9 µs) — the memo's hard case is not only flybys but the bound near-parabolic population, untested by the author.
- *A3, aliasing:* seven nudged keys through the shared-shape path reconstruct bit-exactly (asserted).

**Novelty.** The memo's existence, widths and weak-field hit rate are prior art: bba2d57 (Astra's envelope) already measured "keys 12+12 bits in 44 (weak-field shape hits 99.1%); p99 compile 26 µs", and `law.md`'s State already declares tubes keyed by the quantized memo. Sol's kick arithmetic is on main (1932f6c, 25.75→23.71 µs). What is new and measured: the cutover inside the kick rebind with event-exactness via the residual, the per-kick key-change rate (the certificate idea), the fit-dominated 7.8–10.5 µs floor with readout at 3.3 µs, and the flyby/near-parabolic negatives. It refines a premise (the lever is kick *cost*, not only kick *count*) without showing one wrong.

**Goal fit.** Board focus 1 and HANDOFF bottleneck 3, directly. PRINCIPLES 6: "Store the generator, not the generated" — the compile regenerates what 12+12 bits already identify. PRINCIPLES 3: "Nothing is evolved that can be derived when looked at." The plane reimplementing its law's declared state while the memo sits in the same crate is exactly the principle-19 smell, correctly diagnosed.

**Why silver, not gold.** The 10× bar fell by the author's own P3 (3.7× measured, 3.55× here), and no component is deleted (misses and passages still compile). Real, reproduced, adoptable within one step — one experiment short.

## The one experiment for gold

Wire `QuantizedMemo` into `crates/universe`'s bind path (thread-local or `Ctx`), add the certificate step (hold the tube, recompile only when the key moves; kick ≈ readout 3.3 µs + integer residual add), re-run the frozen B-gates and universe digests — with high-e (e ≥ 0.9) and near-parabolic populations in the digest mix, since my A2 shows the certificate's domain ends there. Gold if the digests hold and the measured kick cost drops ≥ 10× on the plane's own replay.

## What the author missed

- The between-event worldline error the bucket introduces (A1: ~2⁻¹¹ in period) was never quantified; it is the number the re-freeze judges.
- The certificate's failure arrives much earlier than the dossier's risk paragraph implies: e = 0.95 at 2⁻²⁴ (not "kicked hard at 2⁻¹⁶") and strong-field at 2⁻²⁰ already move the key on most kicks; "information production per kick is zero" is a statement about weak-to-moderate-e orbits only.
- Bound near-parabolic orbits (e → 1) behave like flybys (hit 0.407, no gain) — a real population class, not just the doll-crossing edge case.
- The claimed "45 tests" is 50 by `cargo test`; and the empty `run.log` left the pre-registration unauditable.
