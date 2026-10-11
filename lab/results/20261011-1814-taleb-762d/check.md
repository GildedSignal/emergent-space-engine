Grade: silver

**Abstract.** Claim: past capacity the plane dips smoothly with bit-identical digests, but below a per-frame budget floor that scales with universe size it stalls silently (delivered RTF 0.00, no error, digest exact). Reproduced bit-for-bit on a fresh build: one digest `fbb0c7d5…adc72` across budgets 5/1/0.2/0.05 ms and pacing; members 4 at 0.2 ms delivers 1239.5×, members 400 delivers 0.00089× (185.8 events/s); level-15 low tail 0.681. Robust on seed 2 and worse than claimed: members 400 stalls at 1 ms too, members 100 stalls at 0.2 ms. But the mechanism is mis-attributed: the author's own events/s scale ~linearly with budget (4.1% of events at 4% of budget), falsifying the "0.2–1 ms prologue before any event"; the floor is event density × causal gating. Gain: a falsified premise of plane foundation 7 plus a guard; adoption cheap but the gate's target term is unproven.

**Reproduction** (fresh `git apply` of `work/patch.diff`, `cargo build --release -p xtask`, same commands, shared box, load ~1.5–1.9):

| claim | author | mine |
|---|---|---|
| digest across 5 budgets/pacing | fbb0c7d5…adc72 | same, all 5 |
| 0.2 ms med (default scene) | 1.643 | 1.561 |
| 0.05 ms med | 0.027 | 0.027 |
| m4 @0.2 ms | 1239.5× | 1239.5× |
| m400 @0.2 ms | 0.00089×, 185.8 evps | 0.00089×, 186.1 evps |
| paced worst frame / low 1% | 12.1 / 7.3 | 12.3 / 2.6 |
| rtf 300000 coast med | 6818 | 6822 (digest 475f4db2… exact) |
| level-15 low 1% | 0.681 | 0.681 (digest exact) |
| frame p99.9 paced | clean | 12.1 ms |
| cost ×6 for ×13 bodies | 6× | 6.3× (C CSVs) |

Digests for 7 distinct scenes reproduced bit-exact across processes and loads; determinism under overload is real. The stall is silent: `refused: 0`, no error field, no hitch (worst 7.3 ms).

**Predictions.** `predictions.md` (18:17) precedes all artifacts (18:19–18:29). P1, P3, P4, P5, P6, P7 held; P2 failed in the letter (×4.5–5 cost rise vs ≤1.5 predicted) and was disclosed; my recomputation gives ×4.8, bounded, no spiral. Honest reporting.

**Adversarial** (mine): (1) m400 at 1 ms also stalls (0.044×) — the floor is ≥1 ms at 371 bodies, not between 0.2 and 1; the N-scaling is stronger than claimed. (2) m100 stalls at 0.2 ms (0.044×) and limpens at 1 ms (311×) — the cliff starts between 32 and 124 bodies. (3) Seed 2: m400 stalls (0.0027×), m4 delivers 1239×, digests change with seed (so the digest discriminates, and the cliff is not a seed artifact). (4) Mechanism attack: events/s at m400 = 186/1212/4527 at 0.2/1/5 ms — linear in budget (4.1% at 4%), and the default scene is superlinear (24% at 4%). A fixed 0.2–1 ms prologue would starve events to ~0 at 0.05–0.2 ms; it does not.

**Novelty.** No prior run measures the budget floor, its N-scaling, or the delivered-RTF tail. H0210 already claimed "one digest across budgets and threads" (extended here to full stalls and 0.05 ms — a re-verification, not new); H0208 saw a 1 s p99 stall in the pre-plane slice; plane.md line 32 already lists RTF lowest 1% as a metric. The falsification of foundation 7's "overflow becomes a brief, smooth dip" at low budgets is new and premise-level.

**Goal fit.** Board #4 (smoothness/allocator). The quoted foundation text exists; the dossier's quote is a faithful paraphrase, not verbatim ("a brief, smooth dip … never a hitch or a visible degradation"). "don't multiply by zero" (P25) applies: 0.00 delivered at 428 bodies is the zero, silent. But the proposed adoption — gate the allocator on an O(1)-in-N per-frame prologue — targets a mechanism the run's own data contradicts; adopting it as stated would build the wrong gate.

**The experiment that would make it gold:** decompose the stall. Measure, per members count, the scene's events per presented game-second and the engine's events per wall-second at each budget (data already in these JSONs), plus one profile of `Universe::advance` at m400 to close out the prologue. If, as the evps ratios indicate, the floor is peak event density ÷ budget-sustainable throughput (with presented time causally gated), the guard becomes a density floor on the budget (or shedding), not an O(1)-in-N prologue audit — a different, adoptable gate.

**What the author missed.** The linear evps-vs-budget evidence sitting in their own JSONs, which already argues against their prologue story. Provenance sloppiness: table row 1 mixes scripted runs (300/3000/30000: med 30000, 269/600) with a coast run (300000), while the reproduce command says `--coast`, which regenerates ~7500/600 for rtf 30000 — the quoted 30000 row is not regenerable as instructed; "engine p50 2.9→8.8 ms" matches no saved column (engine p50 is 0.82→5.24; 2.81 is view, 8.78 is frame); "428 bodies" in the stall row is the 5 ms run's count — the stalled run had 371. No profiling, single seed per row, no threads>1, no paced m400 (all self-disclosed).
