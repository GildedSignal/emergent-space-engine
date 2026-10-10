# Check — 20261010-0814-second-20261010-0656-autoresearch-cc88-8ce2

Grade: silver

**Abstract.** Claim: cc88 regenerates (−16.5%, digests bit-identical, refused 0), and the re-anchored jet, implemented on the shipped integer compiler, holds df81's criterion for the Δφ advance (7×10⁻¹⁵ at θ=7.3×10⁻⁴) but not for the period (3.2×10⁻⁴) or position readout (9.0×10⁻⁴ at e=0.3; 1.5 and 156 at e=0.9/0.99), and the plane's cadence is churn-limited (0.073 compiles/kick). Everything reproduces: E1 −15.6% here with identical digests; E2 digit-identical (618 kicks, 45 anchors, dk max 1.305×10⁻⁷); E3 errors/anchors exact; suites green. My probe: the plane's kicked bodies sit at median e=0.94, where at the plane's own kick sizes the readout errs 4.4 relative with zero refusals — the deletion stands for the advance increment only, not for every consumer. Cost to adopt: tests + bench instrumentation; the jet is not wired into bind.

## Reproduction (clean HEAD, `git apply` keep.patch then work/patch.diff; /tmp target)

- **E1.** Baseline seed 1: median 87.7 µs, replay `59ea996999a74c67`, universe `13cfe88b452d2116`, refused 0, memo negative (663 distinct shapes / 663 rebinds, exact hit 0.0, 45 quantized). keep.patch: 74.0 µs (−15.6%; author −16.5%, cc88 −15.6%), same digests. Reproduced.
- **E2.** Deterministic: kicks 618, anchors 45, 0.0728 compiles/kick, the dk distribution identical to the digit. Recomputed stats: median 1.16×10⁻¹⁰, p99 9.9×10⁻⁸, max 1.305×10⁻⁷, zero above 10⁻⁶ — as claimed. The churn arithmetic is airtight: even all 618 kicks on one body accumulate 8.1×10⁻⁵ < θ, so no drift anchor can fire; all 45 anchors are churn. Reproduced.
- **E3.** All error/anchor numbers reproduce exactly (only timings shift on this shared box: compile 37–60 µs vs author's 47–75). Frozen control 7.297×10⁻⁴, quadratic ratio 2.7, both green. Suites with the jet in-tree: space 55 passed (+ my 3 probes = 58), universe 54, 0 failed. Reproduced.
- `predictions.md` (08:23) precedes `e2_seed1.json` (08:29) and `e3_jet_tests_output.txt` (08:55). P1 held; P2 wrong in number, right in direction (disclosed); P3's miss is reported as the finding — honest; P4 held.

## Attack (my cases)

1. **Held-out seed 2 (E2).** Digests equal cc88's seed-2 records; churn-limited again (0.137 compiles/kick — 1.9× the headline number; dk max 2.2×10⁻⁷; cumulative max 8.4×10⁻⁵ < θ). The order holds; the 0.073 headline is seed-1-specific.
2. **The plane's eccentricity mix — the variable the run never measured.** I instrumented the same cadence hook to record e = 2⁴⁸/k − 1 per kicked weak-shape body: **median e = 0.94** (seed 1; 0.61 seed 2), max 0.999. Joined with the run's own C_r (1.7×10³ at e=0.3 → 2.8×10⁶ at 0.9 → 2.9×10⁸ at 0.99), the readout budget at the plane's mix is ~10⁻⁷, at or below the p99 per-kick drift (10⁻⁷). Direct run at the plane's own kick size (ε=1.3×10⁻⁷, one 45-kick churn window, θ never reached): **radius error 4.36 at e=0.99, 1.97×10⁻⁴ at e=0.9, zero refusals.** So "the deletion stands for the plane's real workload" is true for the advance increment only; under df81's criterion (Δφ **and** Δt) and for the position readout, the jet as implemented fails at the plane's actual e-mix. The dossier's "on the plane it changes nothing (churn-limited either way)" is asserted, never measured, and false for those consumers at that mix.
3. **The refusal story at e ≥ 0.9 is contradicted by the run's own evidence.** With a refusal counter: refusals = 1 (e=0.9) and 2 (e=0.99) per 10,000 kicks at ε=10⁻⁶; anchors 15/16 are drift anchors (10⁴·10⁻⁶/7.3×10⁻⁴ ≈ 13.7 + 1). The dossier's "jet_update refuses each kick" and the table's "anchors ≈kicks (refusals)" are wrong: the high-e failure is **silent** (shift-clamped/overflowed derivative alignment, no refusal, no signal) — a worse failure mode than the one disclosed. The E3 table's e≥0.9 row also mixes the θ_r campaign's period/radius (9–99×10⁻⁶, ≤0.55) into the df81-θ table whose actual values are 7.1×10⁻³–1.3×10⁻¹ and 1.5–156.
4. **Random-sign kicks (df81's second mode, untested here):** e=0.3 radius 6.1×10⁻⁵ (15× better than systematic — the first-order cancellation df81 measured); e=0.9 radius 1.5×10⁻² — still 15× above the floor. The high-e breakage is not a systematic-drift artifact.

## Novelty

law.md line 35: the jet clause is the adopted strong-field reuse mechanism, "(Graded gold by one checker; the second never ran)" — this run is that second check, and the first anywhere on the shipped integer compiler (df81 was float numpy). No jet-on-compiler entry in docs/HISTORY.md or the docs (the HISTORY "jet" hits are the GEM delay/bend jets, another subsystem). The memo negative is the 5 October taste-log entry, correctly cited, not re-claimed. Novel.

## Goal fit

Board focus line 1 (kicks dominate); this is the checker-named gold experiment on that bottleneck. The finding that df81's θ does not transfer to the shipped compiler for Δt and the readout is a premise-level correction to law.md's clause ("error grows as C·drift² … cost about 0.05 compiles per kick" — the constant and the budget are consumer- and e-dependent, by 5 orders across the plane's own e range). PRINCIPLES 10 ("Measure before claiming") is served for E1/E3 and violated once in E2's adoption sentence (the e-mix was never measured); 13 (errors never compound) is respected — the run tightens the budget instead of accepting the error; 9 — a falsified expectation is reported, not patched around. The disclosed near-miss (a dropped accumulation briefly "confirming" the jet) is exactly the honesty the lab wants.

## Why silver, not gold

The load-bearing adoption claim — compile falls to 0.073 compiles/kick on the plane, so the deletion stands there — is (a) decomposed, not wired into bind, and (b) decided by a variable the run never measured: the plane's kicked e-mix, which my probe puts at median 0.94, squarely inside the regime the run's own E3 shows breaking the period and readout floors even at the plane's tiny kick sizes. On the run's own criterion (df81's, including Δt), the jet does not delete the plane's rebind compile at the law's 10⁻⁶ floor; it deletes it for the advance increment. One dossier claim (per-kick refusals at e ≥ 0.9) is contradicted by the run's own output. Everything that was measured reproduces exactly, and the falsification of df81's θ for Δt/readout is real and adoptable as a correction to law.md — that is silver-grade work, one experiment short.

## The one experiment for gold

Re-run E2's cadence with the per-body budget θ(e) = √(floor/C_r(e)) (C_r is now measured at three e's) on the plane's kicked population, deciding the deletion per consumer on the real e-mix, and wire the jet into `bind` for the end-to-end kick median. If the readout/Δt consumers hold there, gold; my probe predicts they fail at e ≥ 0.9, so gold then requires the e-gated jet or the second-order term — either outcome closes the question the run opened.

## What the author missed

- The plane's e-mix (median 0.94) — the one variable that joins E3 to E2; without it "churn-limited either way" is an assumption, and it is the assumption that fails.
- The silent failure mode at e ≥ 0.9 (misaligned derivative accepted, no refusal) — the run names a clean refusal that its own anchor counts refute; the shift-clamp/overflow path in `jet_table`'s alignment is the actual hazard and is unflagged in code.
- The E3 table's e≥0.9 row mixes the θ_r campaign's period/radius into the df81-θ table.
- The frozen negative control was run only at ε=10⁻⁶ (df81's control at 10⁻⁴ fails in 1–2 cycles; unrun here).
- `e2_seed1.json`'s kick_us_all median (88.0) shows E2 ran without cos4 in the tree — immaterial for the cadence, but the dossier's evidence table quietly mixes the two trees' timings.
- Suite counts in the dossier ("space 14", "universe 10 + 6") are per-binary; the full suites are 55 and 54 — the same record-hygiene slip that cost cc88's record clarity.
