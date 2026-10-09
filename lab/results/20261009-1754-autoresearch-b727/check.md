Grade: lead

**Abstract (for the integrator).** Claim: five bit-identical kernel changes to `crates/space` buy ≤3%, so per-kick rebuild cost is representation-bound, not kernel-bound. Reproduced: both digests match (`1f057b83…` tuning, `854b4b51…` held-out = `heldout_before.txt`); all 97 space+universe release tests green; interleaved A/B min-of-4: bank from_state −1.6%, compile −0.8%, state −0.7%; strong-field −4%; shipped `xtask universe --kick-bench` bit-identical with median −1.3% (noise). My attacks found zero divergence (3.3M-case add differential, 8.0M-input isqrt property, 72-combo adversarial bank). But the genre is already tried: commit 1932f6c (1 Oct, gpt-6.1-sol, integrated) did bit-identical micro-optimization of the same crate (−8% kick median) and added that kick-bench; the taste log already holds "the lever is cadence". Cost to adopt: trivial; keep or drop.

**Reasons.**

1. **Reproduction (clean tree, patch applied by me).** Dossier commands all regenerate: bank `400 all` → from_state 18.1 µs / compile 30.9 µs / state 34.0 µs, digest `1f057b8337399608ffa4224da12d3c95`; `200 heldout` → digest `854b4b514191ee6db8ad74db1e6056e3`, matching `heldout_before.txt` line for line. `cargo test --release -p emergent-space -p emergent-universe`: 51 + 46 tests, 0 failures (the `lattice-metal` failure is indeed in neither crate). Both digests identical on base and patched binaries.

2. **Timing, done adversarially.** I built base and patched binaries and interleaved them (4 rounds). Bank: −0.7…−1.6% (min-of-4), at or below the ±5–8% noise. Strong-field HO5 compile: base min 18 794 ns vs patched 18 054 ns (−4%, direction consistent). HO6 near-separatrix flat (46.9 µs both) — panel-bound as predicted. The dossier's circular −13% (3813→3325) is baseline inflation: my base interleaved min is 3307 ns, i.e. the real gain is ~−3%. Conclusion unchanged (everything ≤ noise–4%), but that specific number overstates.

3. **Bit-identity attacked with my own cases (all clean).**
   - `Scalar::add`: 3.3M-case differential vs the reconstructed original (`raw((hi<<gap)+lo, lo.exp−62)`), splitmix randoms biased to gaps 0/1/63/64/65/70 plus structured edges (h=l=2^63−1, carry boundary, gap 64, operand order, exponents −400…32767, mixed signs): **0 mismatches**. The exponent-32767 fallthrough errors identically on both paths.
   - `isqrt`: property test y²≤x<(y+1)² on 8 000 391 inputs (powers of two ±1, near-squares ±δ, u128::MAX, randoms): **all exact**.
   - Whole pipeline: my own 72-combo bank (p ∈ {1…2^52} × e ∈ {0…(1<<48)−1}, incl. near-parabolic k≈1 which reserves 768 knots, `Orbit::newtonian`'s separately-cached `half_time`, `Rebinding` at two time scales, error paths hashed) → identical digest `f2bf24070e5a2cfeffefc5856faddc1e` on base and patched.
   - Plane level: shipped `xtask universe --kick-bench --seconds 3` → identical digest `e2c0530442782681…` and replay digest `f34d62df…`; kick median base 42.8 vs patched 42.3 µs (−1.3%, noise).

4. **Predictions.** `predictions.md` (mtime 40m) predates `heldout_before.txt` (39m) and the dossier (written at the end); order consistent with pre-registration. Held: digest invariance, strong-field flat, near-separatrix panel-bound, stop rule fired. Honestly reported failure: H1's 15–35% on weak shapes (weak shapes take `weak_quad`, which already used `div_word` — I verified this dispatch in the source). Both disclosed intermediate breaks (lost `sum[0] += w·g1`; the `gap==64` masked shift) are consistent with the final state I measured.

5. **Novelty — the decisive point.** Commit `1932f6c` (1 Oct 2026, gpt-6.1-sol, integrated): "crates/space: cheaper kicks, exactly … normalized 63-bit products with a one-bit carry … certified bank and digests identical. Kick median 25.75 → 23.71 µs, p99 36.75 → 32.21 µs" — the same bit-identical micro-optimization genre, same crate, and it added the shipped kick-bench. Its −8% already showed the marginal-returns curve; this run's ≤3% completes it. The board/taste log already holds "the lever is cadence" (five runs, 5 Oct). What is genuinely new here is only the explicit "exhausted" measurement (diffuse cost, no hotspot >15%) and the stop rule — worth one board line, as the author says, not a bottleneck move.

6. **Goal fit.** Board item 1 (fewer kicks per orbit) is untouched: no 10×, no component deleted, no premise killed that the integrator did not already hold. PRINCIPLES fit is good — via negativa ("The cheapest compute is compute not done"), "measure before claiming", and honest disclosure of both caught breaks.

**Why lead, and what would change it.** Real, reproduced, bit-identical, honestly reported — but marginal (≤3% everywhere incl. the plane) and in an already-tried genre (1932f6c; taste log). No single experiment upgrades this dossier: the next lever is a different question (the panel-count/representation changes the author correctly defers as law changes). Had the author cited 1932f6c and run its kick-bench, this would still be lead; it would just have been cheaper to read.

**What the author missed.**
- `1932f6c` and the shipped `xtask universe --kick-bench` (added by that very commit): the numbers were not regenerable by the shipped bench. I ran it: bit-identical, no gain — this closes the author's own "run one plane scenario" gap.
- The circular −13% is single-run baseline inflation; interleaved min-of-N gives ~−3%.
- `at_radius` widened `pub(crate)`→`pub` unnecessarily (nothing outside the crate calls it; the harness does not).
- The knots-capacity comment overstates: `16·(49−bitlen(2k−1))` under-reserves for mid eccentricities (e 0.9 → estimate 8–16 vs ~68 real panels; harmless — capacity never changes values — but it avoids little churn where churn lives).
- Minor: `from_shape` still recomputes `time(half)` for `increments[1]` after just having cached `half_time` via the temporary.
