Grade: silver

Abstract for the integrator: the claim reproduces. Clean-tree `--kick-bench`: 97.3 µs median, digest `13cfe88b…`, 682 samples. Patched `--jet-bench` (seed 1): counters bit-identical (663 cycles, 653 key changes, 45 bodies), timings within 1% — compile 62.1 µs (64.5%), rebind 75.8 (78.7%), forces 8.4 (8.8%), from_shape 0.465 µs. Adversarial (seeds 3/7, 30 s): compile 51–65%, rebind 71–81%, trivial reuse 0.8–1.5% — the cheap jet stays dead everywhere. The measured lever is 3.3–4.4× per kick (4.4× is the top, not the typical), a priced ceiling, not a built jet. Adopt by building law.md's offset jet; the pricing and decomposition are already adoption-grade evidence.

## Reproduced

- Clean tree, shipped `xtask universe --kick-bench --rtf 100 --seconds 10`: kick_us_all median **97.29 µs** (dossier 97.4), samples 682, refused 0, digest `13cfe88b452d…` — equal to both author JSONs and to my patched run. Memo baseline matches too (663 cycle rebinds, exact hit 0.0, quantized hit 0.932, 45 quantized shapes).
- `git apply work/patch.diff`, build (5 warnings, see below), `--jet-bench --rtf 100 --seconds 10`: every deterministic counter bit-identical to jet-r1/r2 (663 cycles, 19 passages, 653 shape-key changes, 10 same, 45 bodies, 0 cell changes, same digest). Timings: full 96.3 (author 97.2/96.3), compile 62.1 (61.3/61.4), rebind 75.8 (75.9/75.8), forces 8.45 (8.6/8.5), readout 3.69 (3.7/3.7), from_shape 0.465 (0.461/0.464); parts sum 91.3% (author 91%). Two reruns by the author agree within 1%; mine sits inside that band.
- `Orbit::compile` verified memo-free in the shipped source (fresh `OrbitShape::bound` quadrature every call), so the separately-timed compile cannot be a cache hit; `bind` verified as fit(`from_state`, containing the compile) + residual, so the decomposition tracks the shipped structure.
- Timeline: predictions.md mtime 02:42:48 precedes jet-r1/r2.json 02:51:12/13 by ~8.5 min; the dossier (02:52:23) post-dates the JSONs it describes.

## Predictions

Held: P1 (compile ≥60%: 63–64.5% on the 10 s window), P2 (rebind ≥70%: 78–79%), P3 (forces ≤15%: 8.8%), P4 (from_shape ≤10% of compile: 0.75%; jetted ≤35%: ~23%), P6 (parts sum 91%, reruns agree). P5's letter held (cells never change in-window, median 7 kicks/cell) but its useful interpretation failed: the exact ShapeKey moves on 98.5% of kicks, so trivial reuse covers 1.5% — reported by the author as the run's sharpest result, not buried. The pre-registered kill criterion (compile <30%, reuse >30% of compile) is nowhere near triggered.

## Adversarial cases (mine)

1. `--seed 3 --seconds 10`: compile 63.8%, rebind 81.4%, forces 8.9%; trivial reuse 5/597 = 0.8%; cell-change rate 0.0. Shares robust.
2. `--seconds 30` (seed 1): compile 56.9%, rebind 74.5%; **cell-change rate 0.00089/kick** (≈1 change per 1125 kicks; median run 10, p99 141). "0 cell changes" is a 10 s-window artifact, not a structural invariant — but the measured rate supports a re-anchor cadence ≥ the 730 kicks imported from redteam-df81, so the jet ceiling survives, now with on-scene evidence.
3. `--seed 7 --seconds 30`: compile 51.0%, rebind 70.8%; cell-change 0.00067/kick; trivial reuse 16/1485 = 1.1%. Recomputed jet ceiling across these scenes: **3.3–4.4×** — the dossier's "~4.4×" is the favourable end of an honest range, fine under the orders-of-magnitude rule but not the typical value.
4. `--level 15` produced a digest bit-identical to the base run: the plane script never burns in 10 s, so thrust level is an unexercised axis on this scene (noted; no bearing on the claim).

## Novelty

The exact memo never hitting was known (taste log 5 Oct; H0212/H0214 correction) and the author correctly marks it baseline, not finding. law.md "Not adopted" already specifies the offset jet and the ~730-kick cadence (redteam-df81). New here: the per-kick decomposition itself (nobody had split the shipped kick), the 0.46 µs vs 61 µs pricing of the reuse path that already exists in the crate, and the measurement that trivial shape reuse is worthless (1.5%) while the quantized cell is stable for ~10³ kicks — i.e. the jet must be the derivative-offset variant, and its cadence assumption now has on-scene support. Distinct from gold components-4643 (that decomposed the encounters window-setup path, not the rebind).

## Goal fit

Board focus 1 and bottleneck 3 (cheaper events): a measured 3.3–4.4× per kick that multiplies any cadence win, at any N. PRINCIPLES: "The cheapest compute is compute not done" (1); "Cost follows change and entropy. Nothing is evolved that can be derived when looked at" (3) — the band table is re-integrated per kick from invariants that move sub-quantum; "a fix signals the wrong representation" (19) — compile-per-kick is the wrong representation of a slowly drifting orbit.

## Why silver, not gold

Gold needs 10×, a deletion, or a premise overturned, adoptable within one step. This is a real 3.3–4.4× ceiling whose artifact (the jet) is unbuilt and unpriced at its offset arithmetic — the author says so themselves. **The one experiment that would make it gold:** build the minimal jet (stored last-compiled shape + derivative-offset tables + re-anchor at the accumulated-offset bound) in `crates/space`/`crates/universe` and measure the jetted kick end-to-end against the exact rebind, with B5/B8/B9 as the judges — turning the 22 µs ceiling sum into a measured number and pricing the offsets. Cheaper prelude the same run should include: the offset-error growth against exact rebinds on this scene (the author names it as the natural next run).

## What the author missed

- The patch **replaces** `mod kick_bench` with `mod jet_bench` instead of adding alongside: with it applied, the shipped `--kick-bench` flag is parsed but dead (falls through to a paced universe run), and the build emits 5 unused-variable warnings. The dossier's "no behaviour change — visibility and one accessor only" is true of the universe (digests prove it) but understates the patch's xtask rewiring. Hygiene, not measurement error — I reproduced the cross-check on the clean tree as the dossier instructs.
- "Every body stays inside one quantized cell for its whole sampled life" invites over-reading: the 30 s window (0.4 s wall — cheap) shows changes at ~0.07–0.09%/kick. Reporting that rate would have strengthened, not weakened, the cadence claim.
- The drift population mixes plane-made bodies and fleet members (no made/leaver split, unlike kick_bench); the from_shape p99 prints as `null` (NaN refusals) without a note in the dossier table.
