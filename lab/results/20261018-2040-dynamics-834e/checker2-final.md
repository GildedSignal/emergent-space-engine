Working...
Check complete. **Grade: silver** — written to `lab/results/20261018-2040-dynamics-834e/check2.md`, with the author's wiki page corrected in place.

**What I did**

- **Reproduced** from a clean tree (applied `work/patch.diff` myself, ran `fill all` + `analyze.py`): **bit-identical** to the author's `fill.jsonl` — all 38 arms, determinism control included; analysis output matches line for line. Every dossier number I spot-checked holds (P1 Enskog 0.961–0.986, cost fit a=4.02/b=8.03, maxcomp 20 = the pre-registered n/20 line, P6 scale ×0.97/×1.06).
- **Predictions audit**: `predictions.md` predates the decisive run, pre-registers held-out arms, discloses the pilot's factor-2 fix. Held on the tuned domain; the two letter-misses (seed-5 Fano 1.0205, speed −10% at 2¹⁸) were honestly reported.
- **Novelty**: confirmed — nothing on the live `chaos-shadowing` page, HISTORY.md, or `contact-speed` (per-contact skip, complementary).
- **Adversarial cases** (all outside the author's domain):
  1. **Coherent fleet** (bulk drift β=0.05, global φ=0.077, below jamming): Fano₁ **128.6/97.1/10.7** (touching/gapped/dispersed), head-on fleet-fleet **96–97** with 200 pairs (n/2) in one wall-free chronon, p99/p50 2.08 — the P3 kill line broken ~85×. The anti-bunching is **phase dephasing**, not cage periodicity: the coherent arms recollide the same 380 pairs forever with Fano₁ ~10².
  2. **n=6400**: the breathing mode is N-dependent — Fano₆₄ 1.2 → 2.55 → **33.4** (400/1600/6400), Fano₁ crosses 1; "no N-dependence" holds only to 1600.
  3. **Dense-fast corner** (φ 0.7, vmax 2¹⁹): ν = 0.97 — engagement *measured* — Fano₁ 0.51, linear cost (fit under-predicts 19%), no cliff. Strengthens the author's engagement claim.
- **Verdict**: the cost half (affine, bounded ops, no quadratic cliff) survives everywhere I probed; the statistics half ("no avalanche regime at any filling fraction", the deleted gate) is a thermal-genesis property — the wiki's "no fleet density below jamming spikes a frame" was false for formations, which is exactly the fleet case the pricing targets. One experiment from gold: the burst law vs coherence (a drift parameter on `fill.rs`).

Tree restored (scratch examples removed; only `?? lab/results/` remains, as found; no commits made).
