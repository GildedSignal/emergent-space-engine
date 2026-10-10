Grade: silver

**Abstract.** Claim: the belt population scar layer (H_live) is a logarithmic crawl on the shipped `shipmem` store — ≈3 bits per doubling of kicks absorbed (½-log per action column, 1.5-log phase), not a walk to ruin — so the 10⁹-in-8 GB risk is empty at play horizons and re-anchoring machinery is unneeded. Reproduced bit-for-bit (`cargo run --release`, 18.8 s); slopes robust to a fresh seed (2.81 / 5.09 / 0.02 bits/doubling for G2/G4/G1) and to a systematic common-mode drift (absorbed natively: 0.655 B/body at k=4096, same as without drift). Extrapolation: ≤2.2 GB at 10⁹ bodies, 10 h, μ=10⁻⁴. One evidence claim failed reproduction: the wrapped-phase "trap" (+1.6 B/body) is not regenerable from the shipped code. Cost to adopt: none.

## Reproduction

- `cd .../scarwalk && cargo run --release` (18.8 s): every data line identical to `run.csv`; `cargo test` passes (roundtrip 2e4 elements, <1e-12). `work/patch.diff` is empty and the tree is clean — the instrument lives wholly in the run folder with a verified path dependency on the shipped `crates/shipmem` (`Program::seal_from`, `Enc::new(true)`, Elias–Fano), so the bytes measured are the shipped codec's, not a copy.
- Dossier numbers re-derived from the CSV: G2 slope 2.81 bits/doubling (theory 3.0), G3 3.06, G4 5.08; per-column at k=4096 (3.53/3.53/3.53/6.04 B); G1 control flat 0.63→0.68 B; N-independence 15.32 vs 15.22 B at N=4096 vs 16384; P1≡P0 to every digit on every generator; physics control 2.001e-4 vs 2.000e-4. All match.
- Predictions: `predictions.md` mtime 08:25:00 < build 08:29 < final source edit 08:45:33 < `run.csv` 08:45:52 — pre-registration holds, and the shipped source regenerates the shipped numbers. Held: 1, 2, 3, 5, 6, 7. Prediction 4's saturation half refuted and honestly disclosed as refuted.

## Adversarial cases (mine)

1. **Fresh seed** (0xDEADBEEF…): G2 9.717→15.218 B (slope 2.81, identical), G4 slope 5.09, G1 flat 0.02 bits/doubling. The k=1 point moves 0.2 B (seed noise); every law claim is seed-robust. Only differing number found.
2. **Systematic common-mode drift** (+1e-3 per orbit on every body — 12σ accumulated by k=4096, far nastier than the zero-mean G1): 0.632→0.655 B/body, byte-cost indistinguishable from no drift. "No re-anchoring machinery needed" survives its strongest form: the block codecs' base/delta/median normalization cancels any common mode.
3. **The wrapped-phase trap — NOT reproduced.** With the natural wrapping (quantized deviation reduced mod 2³², one period = 2³² quanta): the actual 4-column joint seal gives **9.717 vs 9.926 B/body at k=1 (wrapping is free — marginally cheaper) and 15.218 vs 15.222 at k=4096**. A single-column φ seal costs +0.75 B at k=1 (4.633 vs 3.880) and +0.08 B at k=4096. No configuration I could construct yields the dossier's 11.5 B (+1.6 B/body), and no wrapped variant exists in the shipped code (`patch.diff` empty). Direction survives (wrapping never helps); magnitude and "poisons the store" do not. Mechanism the author missed: at small k the phase deviation is exactly linear in the a-column, and the joint seal's cross-column codecs (CHORD/TIED) absorb the wrapped bimodality that a column-wise analysis pays for.
4. **Calibration at large k:** the joint seal implies ≈3.9 bits/column overhead at k=4096 (121.8 bits measured vs Σlog₂σ = 106.3), not "+2.05 within ~1 bit" — `analyze.py`'s own docstring says 1–2 bits/column. The game-scale table therefore carries ≲ +1 B/body systematic; the 8 GB crossing moves roughly 5× earlier (still thousands of hours of 100× play), so the conclusion stands but the dossier text overstates the calibration's tightness.

## Novelty and fit

HANDOFF L70 names this exactly ("H_live … not measured yet"); no prior measurement exists in HISTORY (H0173's ~4 bits per collision is butterfly divergence of a ship gas; H0212's 0.126 bits/body is the birth program, not scars). The directed `b-h-live.md` build is a different, unstarted deliverable (dashboard measure in xtask); this run answers the underlying board question. It deletes candidate machinery (periodic re-anchoring, H_live-driven repacking) — gold-type "delete a component / kill a premise" — and respects PRINCIPLES 6 and 24 as quoted. Physical constants are a shearing-sheet self-gravity floor (no secular resonances), scoped honestly in "What would make it wrong".

## Why silver, not gold

The core is gold-grade: bit-identical reproduction, controls on both sides (G1 positive, G4 tail stress), pre-registered predictions that held, a real deletion. But the Evidence section contains a number the shipped code cannot regenerate (the 11.5 vs 9.93 trap), and it is one of the two stated adoptions ("keep the phase deviation unwrapped, since wrapping poisons the store"). By the lab's own record standard (taste log: silvers fell short "on the record, not the physics: results that the shipped code could not regenerate"), this is silver. The rule itself is still safe — unwrapped is never worse — but the recorded justification would be false.

## The one experiment that would make it gold

Commit the wrapped-variant probe (two lines: `rem_euclid(1<<32)` on the φ quantization) alongside `scarwalk`, re-measure, and correct the trap paragraph to what the shipped codec actually does (≈0 B joint-seal cost; +0.75 B single-column at k=1); while there, recalibrate the per-column constant at k≥512 (≈3.9 bits) and fix the dossier's "within ~1 bit". Ten minutes; everything else already qualifies.

## What the author missed

- The joint seal's cross-column codecs make the wrapped-phase question mostly moot; a column-wise entropy analysis (the lens's attractor instinct again) misprices the store's actual behavior.
- The extrapolation assumes temporally uncorrelated kicks; a correlated (resonant) δa series would steepen the φ walk beyond k^1.5 — acknowledged only as "resonances not modelled", not as a slope risk.
- The N-sensitivity law (Var ∝ μ²/N) is asserted from the MC's construction and sealed only at N=4096/16384; the 10⁹ row is unsealed extrapolation (acceptable, but worth saying).
