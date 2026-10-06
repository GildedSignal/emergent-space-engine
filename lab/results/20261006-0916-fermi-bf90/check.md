Grade: silver

At 10⁹ bodies the M1 is not kick-bound: the board's "190 cores" pairs B9's ceiling cadence (512/orbit) with the cheap 2 µs event cost and matches today's honest bill (172–549 cores) only by cancellation; at the designed point (0.3/orbit) kicks cost 0.11 core and the binding terms are encounter-candidate setup (0.44–2.7 cores), the O(N) view gather (dead ×200 even at 1 ns/item) and scar reabsorption (≥ 0.9 MB/s or 3.2 GB/h). Reproduced bit-for-bit: bench digests `9c549447…`/`b0ff4c23…`, medians 39/101 µs on my rerun vs 35/91 (author's), exact-memo hit 0.000 on three seeds, refused 0; floor 26 ns (author 24); `model.py` output byte-identical. Adoption: no code; it re-ranks the queue. Not gold: the "kicks are banked" row omits the non-averageable (resonant) fraction — at 5% non-averageable and today's 29 µs, kicks alone are ~10 cores.

## Reproduction (clean tree, patch.diff empty)

- `xtask universe --kick-bench --seconds 10 --rtf 100`: digests and replay digests **bit-identical**; samples 682/137/545, memo block identical (663 rebinds, exact hit 0.0, quantized 0.932). Timings on my rerun slightly *higher* (made median 38.97 vs 35.33; leavers 100.8 vs 91.1 µs) — no understatement; shared-machine OoM as the lab rules allow.
- `rustc -O kick_floor.rs`: **26.1–26.5 ns/kick** hot and stream (author 24, "identical hot and streaming" — confirmed; compute-bound).
- `python3 model.py`: output **byte-identical** to `model-out.json`. I re-derived every table row by hand (189.6, 171.9, 549.3, 0.111, 2.667, 16 GB ×3.2, 12.1 GB/s, 208.3M scars, 0.889 MB/s, 3.2 GB/h) — all correct.
- Anchors all verified in the repo: 29 µs kick and 83% gather and 190 µs/item (HANDOFF L41–43); tube 16 B and 2.5–24 µs/pair (law.md L39); 0.19 core/10⁶ (redteam-out #14); 0.126 bits/body (components-98bc); 32/0.3 kicks per orbit (H0190); "76 emitters" = 28 bodies + 48 fleet members (`universe --describe`), giving 0.83×16.7 ms/76 = 182 µs/item ✓.
- The bench is repo code (`xtask/src/universe/kick_bench.rs`), not author-written, and its dedupe by pending-kick time respects the 5 October distinct-kicks lesson; its printed scope matches the code.

## Predictions

`predictions.md` (09:19:05) precedes `kick_floor.rs` (09:19:56), the bench artifact (09:22:31) and `model-out.json` (09:22:31). P1 ✓ (35.3 µs in 10–60; rebind 97% ≥ 40%; exact-key hit 0.000). P2 missed low and is honestly reported (24 ns vs 50–500 predicted — the bound is *better*). P3 ✓, P4 ✓, P5 ✓ (0.0011 core).

## Attacks

1. **Seed/duration robustness** (`--seed 7`, `--seed 3 --seconds 30`): medians 39–40 µs made / 80–100 µs leavers, exact hit 0.000, rebinds ≈ all cycles, refused 0. The measured picture survives.
2. **Resonance hole (the one that bites).** law.md forbids orbit-averaging near resonance, so those bodies keep the un-averaged 32/orbit cadence — 107× the designed cadence. The model has no such term. Computed: at today's 29 µs, a 1% non-averageable fraction costs 3.3 cores, 5% costs 10.1 cores, 25% costs 44 cores; even at the 2 µs target, 25% eats the whole 4-core budget. So "per-body arithmetic is a non-problem" is *conditional on ≳ 95–99% averageability*, a number no run has measured. The author's miss-list names quantum crossings, not resonance.
3. **H_live coherence.** law.md L36: the origin's fall is "one uniform vector per kick epoch" — shared by every member. With epoch groups of ~48, the 0.9 MB/s distinction rate drops to ~0.07 MB/s (0.27 GB/h); the requirement's *form* (reabsorb at the distinction rate) survives, but the quoted constant is the incoherent adversarial corner presented as if general.
4. **Range bookkeeping.** The claim's "0.7–2.7 cores" for setup does not bracket the model's own k=4 × (2.5–24 µs) = 0.56–5.3 cores (the table used the 12 µs midpoint). Direction unaffected; the top of law.md's open range is 2× worse than claimed.

## Novelty

The 512 × 2 µs arithmetic is the red-team's own (redteam-out #8, cited by the author), and the board already ranks candidate work as the top scaling risk (5 October) with q-skin and taleb-3ec1 queued against setup cost — so "encounter setup is expensive" was known. New here: the cancellation reconciliation (190 ≈ 172–549 by accident of paired errors), the honest-today pairing, the priced 10⁹ core table, the "O(N) gather dead even at 1 ns/item" statement, and the 0.9 MB/s reabsorption requirement. No HISTORY entry does this.

## Goal fit

Moves board #3 and the 5 October scaling risk by re-ranking: the 10–100× is already banked in the design, so the next 10× must come from the O(N) terms and reabsorption, not kicks. "Measure before claiming" (10) and "Fermi estimates spot issues early, not an oracle" are both respected. Zero code-adoption cost.

## The one experiment that would make it gold

Measure the averageable fraction: on a real population (the plane's scene or a belt), count kicks that fail law.md's resonance test from the compiled frequencies, across seeds. That single number decides whether the designed kick bill is 0.11 core or ~10, i.e. whether this dossier's headline sentence stands as stated.

## What the author missed

- The non-averageable/resonant fraction (attack 2) — the denominator of the headline.
- The setup anchors (2.5–24 µs, k = 4) are imported from law.md's *open* estimate and taleb-09b5's formation case, not measured here; k is unbounded for sparse high-e belts (the author's (c) concedes this).
- Coherent epoch kicks amortize H_live (attack 3).
- Dossier numbers not in the shipped artifact: p99 "478 µs" and model.py's 36.0/92.7 µs anchors come from an earlier unsaved bench pass (my reruns' p99: 391–416 µs); regenerable in OoM but not from the saved file.
- Margins ×36/×43 are median-based; at p99 costs (4–5× median) the designed row passes with ~×8, not ×36 — the lens names this and the model stops at medians.
- Trivial: the gather tag's "933" changed items should be 926 (55,556/60); `kick_floor.rs` carries dead scaffolding (unused `base`, a `0..0` loop, a no-op touch loop) — cosmetic, timing loop itself is sound (all keys verified to hit the memo).
