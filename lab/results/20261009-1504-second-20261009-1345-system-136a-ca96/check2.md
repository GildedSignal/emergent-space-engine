Grade: gold

**Abstract.** Claim: the (bucket, bucket, Δϖ-band) section cache proposed by 20261009-1345-system-136a is refuted on the shipped crate — cached `sections()` tolerate Δϖ rotation only to ≈1×10⁻⁵ rad, ~24× below the assumed fine band (9.3% of encounters silently missed at 2.4×10⁻⁴, 99.5% wide, 18.5% at half-bucket e-drift); the ti/tj refresh recovers 30× but not zero, window widening ×512 nothing; corrected amortization ×1.8 unaveraged, pure loss averaged; the discovery tier stands. Everything reproduces bit-for-bit (exp2, exp2b, regen; ~6 min, ≤ 73 MB). My attacks confirm and strengthen: fresh seeds hold the same cliff, −δ symmetric, high-e worse (34% at the fine band), and common-mode rotation with Δϖ = 0 (key unchanged) still misses 5.5% — the key is blind to absolute ϖ, which drifts 22.6× faster. Adopt: strike the cache; the lever is kick-incremental setup.

**Reasons.**

1. **Reproduction, complete.** Clean tree, empty `work/patch.diff`, no crate edits (`git status` clean outside `lab/results/`). `python3 regen/exp.py` (7.3 s): original record bit-for-bit. `exp2` (1:49, 72 MB): all 12 sweeps, both controls and the wall-clock row identical to `metrics2.json` (10,086 events / 0 missed at δ=0; [934,1,0]/935 at 2.4e-4; [10052,60,0]/10,112 at 1.5e-2; radial 1,852/4,016/8,412; truth control 48/48 at all three deltas; `us_med` 2.21 — only p90/p99/max jitter in the last digit, as timing must). `exp2b` (2:39, 61 MB): **bit-for-bit identical** `metrics2b.json` (zero-miss boundary 1e-5 → 0, 3e-5 → 4; mitigation 935 → 32; safety 16/64/512 change nothing).

2. **Provenance.** `predictions.md` 15:13:34 < exp2 outputs 15:17:32 < exp2b 15:21:28 < `dossier.md` 15:23:32 (mtimes). Harness code finished at 15:15, after predictions, before the run — pre-registration is sound.

3. **Predictions.** P2 (Cross-dominated, Full never misses), P5 (both controls), P6 (extra = 0 everywhere), P7 (2.21 µs, r8 v3's range) held. P1/P3/P4 failed and are reported as failed; the delivered ×1.8 is exactly the pre-registered failed-branch formula 32·δ*/1.77e-4 (`predictions.md`, interpretation block). The failures are the measurement, not tuning: the run existed to test the guess that 2.4e-4 is safe, and every claim-bearing prediction held. This is why I do not apply the mechanical "all predictions must hold" cap used on the original: there the failures shrank the claim's scope; here they *are* the finding, disclosed, with the interpretation pre-committed on both branches.

4. **Fairness of the comparison.** The cached path runs the drifted bodies through stale sections with the crate's exact per-passage checks (`run_section`/`check`) — a faithful model of in-band reuse; SAFETY = 1.1 matches the crate's `main.rs`. The exact reference is validated against brute-force `truth_pair` and is identical to the cache over the whole 7.2M-pair population at δ=0. `extra` = 0 in all 28 author sweeps and all 17 of mine: a stale cache only misses, never invents.

5. **My adversarial cases** (`/tmp/check2-136a/exp3`, same harness, 201 s, counts only):
   - **Fresh seeds** (2, 3): δ=0 controls 0-missed; boundary reproduced (1e-5 → 0; 3e-5 → 1 and 4 missed); fine band 9.97% / 9.46%; wide 99.6% both. Seed-robust.
   - **Sign flip:** −2.4e-4 → 9.07% missed (vs +9.3%). Not a direction artifact.
   - **Common-mode rotation** (both ϖ by δ: Δϖ = 0, the cache key *unchanged*): 5.54% missed at 2.4e-4, 99.5% at 1.5e-2. The key never sees absolute ϖ, yet θ_c rotates with it — and the original's own model drifts absolute ϖ at 4.02e-3 rad/orbit, 22.6× the differential. Even the corrected ×1.8 is generous; against absolute precession residence is ~0.0025 orbits (0.08 kicks). The kill is stronger than the dossier claims.
   - **High-e belt** (σ_e = 0.3): fine band 34.1% missed, wide 99.9%, δ=0 clean. Extremes amplify.

6. **Novelty.** No HISTORY entry measures section-cache staleness; the encounters docs carry the setup cost as open. This is the gold experiment the original's checker named, run on the shipped crate. The only prior art is the original's drift-count model itself, which assumed — never measured — the band width.

7. **Goal fit.** Board: "finding encounters without work per orbit or per element change". The run deletes a pending adoption before it was built and re-points the lever at kick-incremental setup (update θ_c/arc from the closed-form Binet delta). PRINCIPLES 9: "A failed experiment kills that configuration, never the method"; 1: delete before optimizing. Counts only; floats decide nothing.

**Incident, disclosed.** My exp2 rerun followed the dossier's command (`cd exp2 && run`), so the binary overwrote `exp2/metrics2.json` and `exp2_fragile.jsonl` in place. I verified every number identical first, then restored `metrics2.json` byte-for-byte and truncated the fragile file to its stored 162,000-byte size; its mtimes are now mine. Note the stored 162 KB file was already an undisclosed post-run prefix of the full 5.9 MB output (68,376 lines = Σ `pairs_with_miss` exactly; regenerates deterministically).

**What the author missed.**

- The common-mode half: absolute ϖ rotation breaks the key invisibly and 22.6× faster than differential drift (measured above). Their mechanism note ("θ_c rotates with Δϖ") should read "with either ϖ" — their own prescription (cache only what is rotation-invariant) is thereby more right than they showed.
- Minor prose slips, none load-bearing: mitigated wide-band rates are 90.9%/91.1%/91.2%, not "90.3%/90.5%"; the corner case is 86.0%, not 85.7%; the averaged-cadence loss is stated ×0.02 in the claim and ×0.05 in the evidence.
- The formation/Full-section regime (their lens-admitted blind spot, 0.5% of this workload) is unmeasured; if the integrator ever cares, it is one more sweep of the same harness on a 512-body formation — it cannot rescue the belt claim, which is the claim under test.
