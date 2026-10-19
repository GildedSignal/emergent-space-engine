Grade: lead

**Abstract.** Checker withdraws the headline: the ~1,057–1,090 bits/body first-kick cost (t_p ~1,020–1,041) is an instrument artifact. The Rice stand-in caps its width search at w ≤ 23 while the t_p departures sit at E|q| = 2³³ (optimal width 32): the cap alone yields 1,040.74; the optimal width gives 35.2 and the shipped codec's own cost model 34.1. Corrected totals: 72.9–84.1 bits/body — the driven-worst scale, not 8× above it — so "in-place absorbability is dead as the row is built" does not stand. Reproduced bit-identically and real: departure magnitudes (δt_p p50 3.5×10⁹ quanta), exact controls (μ=0, round-trip, step-halving), predictor irrelevance, resonance census, element-space lever ~1.5–1.9× (not 22–28×). Nothing to adopt; the page is corrected in place.

## Reproduction

- `python3 absorb.py` in a clean tree: **bit-identical** to `run-out.txt` and to every dossier number (1,089.67/1,057.25 totals, per-column bits, controls, census). regen.sh exit 0.
- Pre-registration order verified by file times: `predictions.md` 17:02:47 → `absorb.py` 17:07:59 → `dossier.md` 17:08:52 → regen 17:09:52. `work/patch.diff` empty; no shipped code touched.
- Shipped constants checked at source: belt.rs `P_LO = 2048<<16`, `P_BITS = 25` (p quantum 0.5/2²⁵ over [2,2.5) — exact), `T_BITS = 44` (t_p), ω u32, σ = 0.07 with the e > 2/5 redraw (scenario.rs ladder draw); μ = 1/999 = `Mass::ratio(1,999)`. The e column is Rayleigh-quantile-coded, not linear 32-bit — a ~2–8× quantum error on the *smallest* column, immaterial.

## The finding that breaks the claim (adversarial case 1: the instrument)

`absorb.py rice_bits` searches widths `range(0, 24)`. The t_p departures have E|q| = 8.53×10⁹ = 2³³·⁰ (p10 1.2×10⁸, p50 3.5×10⁹, p99 1.1×10¹⁰, max 7.8×10¹² at the wrap edge); the optimal Rice width is 32. Reproduced exactly:

- capped search (w ≤ 23): **1,040.74 bits/body** — the dossier's number is the cap, not the physics;
- optimal width (w = 32): **35.21 bits/body**;
- the shipped codec's own cost model (`codec.rs choose`: n·w + patched byte-length exceptions, w searched down from maxb, no cap): **34.10 at w = 34**.

Corrected per-column (inside/outside): t_p 35.2/34.1, totals **84.1/72.9** (Rice) and 84.0/75.5 (shipped model). Two independent instruments agree. The corrected total sits between the self-stirred 21–40 and the driven-worst 126: the first kick costs *the driven-worst scale from the start* — it neither kills in-place absorbability nor shows the row is free. The element-space landing is a ~1.5–1.9× lever, not 22–28×.

## Adversarial cases 2–3 (outside the author's range)

- **μ sweep 10⁴×** (μ = 1/99 … 1/999999, both arms): corrected t_p moves only 34.1 → 35.4. The author's "magnitude-robust" observation inverts: the cost is pinned at ≈ log₂(departure scale) — robustly ~34 bits, not robustly ~10³. (Under their own capped code the 22×-weaker arm "lost" 21 bits; a magnitude-driven code must lose only ≈ log₂ 22 ≈ 4.5 — the anomaly was visible in their table.)
- **Distribution shape**: |δt_p| spans 10⁸–10¹³ with the max at the ±0.5 wrap edge; the p50 (3.5×10⁹ ≈ 5.9 h on a ~6 ms grid) and the phase-projection mechanism are real and stand.

## Predictions

P1's failure is honest and correctly diagnosed (the quantum head-conversion slip; the Gauss-level physics checks out). P2 "held" only under the broken code — t_p is still the largest single column (~35 of ~84) but not 95% of the total. P3/P5: the author's own P5 voiding was the warning sign and they did not follow it to the width cap; worse, the scramble control is *near-tautological* under any per-member magnitude code (its cost is a symmetric function of the magnitude multiset; only the held-subset changes), so it could never have detected structure as designed. Keeping every magnitude-derived bits number after voiding the instrument was the inconsistency that sank the run.

## Novelty and goal fit

The measurement (first-kick departure bits on the shipped grids) is new — no HISTORY or wiki entry prices it. But the corrected result lands where memory-h-live's 0820 floor analysis already pointed (t_p as fresh phase ≈ 64 bits/sample; 4-field floor 125.5–126.1 bits/body): a 1,040-bit departure for that column was impossible on its face and should have tripped a sanity bound. The question aimed at budget-1e9's open-2 successor, a real board bottleneck, and the framing (find the water for the fish) is the right one — the instrument failed it. PRINCIPLES 2 ("'Exact' means deterministic and reproducible") and the checker brief's own clause ("a headline the log contradicts … the run loses its grade") decide the grade.

## What the author missed

1. The width cap — one `range(0, 24)` — produced the entire headline; no cross-check against the shipped `choose()` it claimed to stand in for ("codec.rs's uv-length measure").
2. Voiding the instrument via P5 and then quoting its magnitude-derived numbers anyway.
3. The scramble control's tautology under magnitude codes.
4. The 0820 floor as a plausibility bound.
5. What survives is worth a re-run: the corrected first-kick price (~73–84 bits ≈ driven-worst), predictor irrelevance (VoP-residual 34.94 vs 35.21), the census, and the ~1.5–1.9× element-space lever. The gold path is the named next anyway — accumulation over many kicks and the `mix()` finalizer, measured on the shipped encoder end-to-end, not a stand-in.

The proposed page overstated on the artifact numbers; corrected in place (NEW block, mid-page bracket, Refuted entry now records the withdrawal, both open-direction annotations, Contradictions, Runs line). The author's cross-page sync closing 9fd1's item via e828/73b5 was verified against the published encounters page and kept.
