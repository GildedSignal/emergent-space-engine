Grade: silver

**Abstract (for the integrator).** The thermal measurement is real and reproduced bit-identically
(all 38 arms + determinism control; Enskog control 0.961–0.986; Fano₁ 0.99→0.56; cost fit
a=4.02, b=8.03, worst 24%). But my adversarial cases refute the claim's universal wording:
coherent fleets (bulk drift β=0.05, global φ=0.077 — the fleet case the price targets, below
jamming) bunch violently — Fano₁ 128.6/97.1/10.7 (touching/gapped/dispersed), 200 pairs (n/2)
in one wall-free chronon, p99/p50 2.08 — so "no avalanche regime at any filling fraction below
jamming" and the deleted gate hold only for zero-drift genesis; and the breathing mode scales
with N (Fano₆₄ 1.2→2.55→33.4 at n=400/1600/6400, φ_req 0.7; Fano₁ crosses 1 at 6400). The cost
half survives everywhere probed: engagement measured at ν=0.97 (φ 0.7, vmax 2¹⁹), linear, no
cliff, maxops/p50 ≤ 2.2 even in fleet shocks. Adopt scoped; price the formation burst first.

## Reasons

**Reproduction (clean tree, patch applied by me).** `git apply work/patch.diff` on the restored
tree, then `fill all` → **bit-identical** to the author's `fill.jsonl` (39 lines, determinism
control `equal` inside); `analyze.py` output matches `analysis.txt`/`regen.log` line for line.
Spot-checked: P1 ratios 0.9608/0.9862/0.9621; P2 max 0.986 global, 0.610 at φ≥0.7; P4 maxcomp
20 at φ=0.78 seed 2 (= the pre-registered n/20 line exactly); ops/fired 633.8→23.3; P6 scale
×0.968/×1.062 with Fano₁ equal to three decimals; P7 maxops/p50 ≤ 1.141 wherever max_batch>100.

**Predictions.** `predictions.md` (mtime 20:49:57) precedes the dossier (20:56:57), pre-registers
the held-out arms, and discloses the pilot's corrected factor-2 cross-section. Held: P1, P2, P6;
P4 held (one seed touches n/20 exactly); honest letter-misses reported: P3 seed 5 reads 1.0205
(32% of the kill line), P5 −10% at 2¹⁸, P7's wall-flash attribution refuted by the run's own
max_pairs/max_walls columns. Honest work.

**Novelty.** Not on the live `lab/wiki/chaos-shadowing.md` (its od 7 named "cold dense gases";
this run answers the cost half); no avalanche/Fano/Enskog/jamming entry in docs/HISTORY.md;
`contact-speed` covers per-contact skip semantics, not rates. New: the φ ladder, the Enskog
validation, measured g_eff(φ), the affine cost law, the genesis-shock attribution.

**Adversarial cases (mine; each outside the author's domain).**

1. **Coherent fleet (the missing control variable).** `worlds::gas` has zero bulk drift; a fleet
   is a formation with one. Same instrument, monodisperse Bounce lattice, same
   Chronon/RelativisticV1/Q (drift β=0.05, global φ=0.077): wall-ram Fano₁ **128.6** (touching),
   **97.1** (gapped, local φ=π/9 — well below jamming), **10.7** (dispersion ±Q/512); head-on
   fleet-fleet **96–97** with **200 pairs (n/2) in one chronon**, no walls involved; the dispersed
   arm's p99/p50 = **2.08** (P4 letter 1.15 broken). The P3 kill line (1.5) is broken ~85× at
   fleet density below jamming. Mechanism corrected: the anti-bunching is **phase dephasing**,
   not cage quasi-periodicity — the coherent arms recollide the same 380 neighbour pairs forever
   (distinct fraction 0.025) with Fano₁ ~10², i.e. the same repeats, opposite Fano.
2. **Scale, next decade.** n=6400, φ_req 0.7, seed 1: **Fano₆₄ = 33.4** (1.2 at n=400 → 2.55 at
   1600 → 33.4), Fano₁ = 1.159 (crosses the "<1" letter; kill 1.5 untouched), meanops/n 9.64
   (+5% vs n=1600), maxcomp 22 « n/20. The breathing mode is N-dependent; P6's "no
   N-dependence" holds only to n=1600, and a 64-chronon batching scheduler sees a 33×
   over-dispersed stream at n=6400.
3. **Dense-fast corner.** φ_req 0.7 at vmax 2¹⁹ (author swept speed only at φ=0.3, to 2¹⁸):
   ν = **0.97** — engagement measured, not extrapolated — Fano₁ 0.51, spike 1.07, meanops/n
   14.0 (the affine fit under-predicts 19% at engagement), maxcomp 30 (> the n/20 letter, < the
   n/10 kill). The author's engagement claim is confirmed and strengthened by this arm.

**What survives and what does not.** The cost half is robust everywhere I probed: per-chronon
ops stay affine and bounded even inside the coherent shocks (maxops/p50 ≤ 2.2, meanops/n
4.2–7.3), no quadratic cliff at engagement, per-tick components small (maxcomp 2 during the
200-pair chronons — the component metric is blind to synchronized matchings; Fano is the
sensitive statistic). The statistics half ("anti-bunches", "no avalanche regime", "the gate is
deleted") is a property of the thermal genesis, and the wiki sentence "no fleet density below
jamming spikes a frame" was false as generalized — corrected in place on the author's page,
with the headline scoped to THERMAL genesis.

**Dossier accuracy.** One understatement: "Fano₆₄ up to 1.7" — the author's own data holds
2.5452 (held-out n=1600, φ 0.7 arm; the page already carries 2.55). Everything else I checked
matches the raw jsonl.

**Goal fit.** Smoothness/allocator (board #4) and "measure before claiming". The run delivers a
price law and a deletion; my cases show the deletion was declared one experiment early —
PRINCIPLES: "Write the kill criterion before the run… invert: ask how this fails"; the fleet
case was the inversion the dynamics lens should have run, since the adoption sentence itself
prices "fleet density φ ≈ 0.1".

## The one experiment to gold

Re-freeze the claim scoped by genesis coherence: measure the burst law — Fano₁/Fano₆₄ and the
largest single-chronon batch vs bulk-drift fraction at fleet φ and β (n = 400…6400), including
the breathing mode's N-scaling — then either scope the deleted cascade gate to thermal genesis
with the formation burst priced (it is bounded: O(1) ops per contact, excursion ≤ ~2–3×) or
reinstate a coherence-triggered gate. One `fill.rs` arm with a drift parameter does it.

## What the author missed

- **Coherence (bulk drift) as the control variable** — `worlds::gas` cannot generate it, and no
  adversarial case varied it; fleets are coherent by definition (taleb-09b5's formation).
- **The component metric's blindness**: 200 disjoint pairs/tick read maxcomp 2; P4's percolation
  line cannot see a synchronized matching — Fano carries the information.
- **N-scaling of Fano₆₄**: stopped at n=1600, where the trend (1.2→2.55) already pointed up;
  the dossier text even rounded its own maximum down (1.7 vs 2.55).
- **The mechanism attribution**: quasi-periodicity claimed as the anti-bunching mechanism; the
  coherent arms refute it (periodic recollisions, Fano₁ ~10²) — dephasing is the mechanism.
- Remaining (named by the author, agreed): sticky/Stop responses, polydispersity, engine-vs-twin
  statistics at high φ.
