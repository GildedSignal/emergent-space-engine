# Dossier — 20261009-1259-second-20261009-1210-inversion-c529-154a (lens: second author)

**Claim.** The co-orbital certificate, as the gold specified it ("sort by longitude, watch k≈4
neighbours, rebuild on overtakes"), is **sound at any horizon** (500-orbit clump: 0/20810 events
missed at k=4, rank\*=3, refresh = 2.3 analytic overtakes/orbit) and does **not** need ϖ
coherence at the gold's e-scale (random-ϖ fleet replica: 0/284 missed, rank\*=3) — the first
author's horizon kill attacked a frozen-rank watch the gold never specified, and is retracted;
the watch breaks by exactly one mechanism, **contact pins the pair's mean-longitude gap to
≲ 2× the epicycle scale (differential when ϖ is bunched, total when random), so soundness is
governed by epicycle scale versus longitude spacing** — not by 2ae/ρ (a fleet at 2ae/ρ=200
misses less, 4.4%, than one at 2ae/ρ=20, 35.7%), not by horizon, and ϖ bunching mitigates ~8×
(4.5%) without saving — while crossing traffic still leaves the watch (4.8% of events missed at
perfect refresh, all fleet×rogue/rogue×rogue, rank\*=114) with the Binet cone covering 542/542
encounters and 6000/6000 cross pairs, and the gold's measured **oracle** (distance-rank at
closest approach) holds on all 31,305 events of every scene, including every event the watch
misses (d-rank\*=1 on the worst watch-misses): the freeze gate must test the watch, not the
oracle, with three declared bounds (refresh schedule and cost; epicycle-vs-spacing; rank tier
inside the clump + cone across it, per-pair, never a population trigger).

**Bottleneck.** Same as the first author's: the pre-freeze red-team of the co-orbital
certificate brief (`lab/lenses/b-coorbital-cert.md`). Gain: the brief freezes the correct
validity regime. The checker named one experiment to gold — rerun the horizon leg against the
specified rebuild-on-overtakes certificate, state the refresh schedule and cost, re-issue the
claim on corrected legs. Done, plus the two-sided fleet controls the corrected claim needs.

**Evidence.** All numbers regenerate from shipped code: `regen.sh` applies the first author's
`work/patch.diff` (verbatim) plus this run's `work/patch2.diff` (`crates/encounters/src/bin/
inversion2.rs`), builds, and reruns everything; every command ≤ 60 s. Reproduction of the
first author's record is bit-identical modulo wall-clock (diffs in `regen.sh` pass). Truth =
the crate's `truth_pair` (per-pair conservative advancement, refined closest-approach times)
over the radial superset; watch = symmetric-min rank in mean-longitude order **at the event
time** (λ linear in t ⇒ this is exactly rebuild-on-overtakes; between overtakes the order is
piecewise-constant); oracle = symmetric-min rank in true distance at the same instant.

| scene | ρ | orbits | events | miss@k4 (events) | rank\*λ | rank\*d | cross (missed) | cone | overtakes/orbit |
|---|---|---|---|---|---|---|---|---|---|
| C1 gold shape | 1e-3 | 50 | 2202 | 0 (0%) | 2 | 2 | — | — | 2.1 |
| **H1 = C1, horizon 500** | 1e-3 | 500 | 20810 | **0 (0%)** | **3** | 3 | — | — | **2.3** |
| E1 equal-period σ_e=1e-2 | 1e-3 | 20 | 560 | 200 (35.7%) | 8 | 1 | — | — | **0 (frozen)** |
| E2 equal-period σ_e=3e-3 | 1e-3 | 20 | 480 | 20 (4.2%) | 5 | 1 | — | — | 0 |
| **E3 = E1, ϖ bunched ±0.1** | 1e-3 | 20 | 440 | 20 (4.5%) | 6 | 1 | — | — | 0 |
| E1b = E1, seed 13 | 1e-3 | 20 | 580 | 120 (20.7%) | 7 | 1 | — | — | 0 |
| **G1 gold fleet replica** (a_hw 1e-5, e~Rayleigh(1e-3), ϖ±0.1, λ uniform) | 1e-4 | 100 | 255 | 0 (0%) | 3 | 1 | — | — | 0.3 |
| **G1b = G1, random ϖ** | 1e-4 | 100 | 284 | **0 (0%)** | **3** | 1 | — | — | 0.3 |
| **G1c = G1, e×10** (2ae/ρ=200, ϖ bunched) | 1e-4 | 100 | 272 | 12 (4.4%) | 6 | 1 | — | — | 0.5 |
| M1 fleet+20 rogues | 1e-3 | 50 | 2744 | 132 (4.8%) | 114 | 2 | 542 (132) | **542/542, 6000 pairs** | 3113 |
| M1b = M1, rogue seed 11 | 1e-3 | 50 | 2678 | 92 (3.4%) | 105 | 2 | 476 (92) | 476/476 | 2919 |

1. **The named experiment (horizon leg, retracted).** H1 under the specified watch: zero
   misses at k=4, rank\*=3 — orbital shear never uncovers a far partner because contact at
   k=4 happens near λ-alignment; the first author's 71.8%-of-pairs number measured a watch
   frozen at t=0. Refresh cost, stated for the brief: overtakes are analytic (λ linear;
   the probe counts them exactly), 2.3/orbit on the 300-body clump, 3113/orbit on M1 — each
   an O(1) adjacent swap plus O(k) watch repair, so the watch stays O(n·k + overtakes).
2. **The binding scalar (E1/E2/E3/G1/G1b/G1c).** Equal periods freeze the order (0 overtakes:
   no refresh cadence exists), and E1 misses 35.7% of events at rank\*=8 — reproducing the
   first author's frozen numbers exactly, as must be. G1b (random ϖ at the gold's e~1e-3)
   misses nothing: ϖ coherence is not required. G1c (ϖ bunched, 2ae/ρ=200) misses less than
   E1 (2ae/ρ=20): 2ae/ρ is not the scalar. E3 vs E1: bunching cuts the miss rate 8× (4.5% vs
   35.7%) but does not save (rank\*=6 > 4). Audit (Python, independent): the G1c worst pair
   (89/107) contacts 4× sub-ρ (d_min 8.8e-6) at a mean-λ gap of 0.77 spacings with 5 bodies
   inside the arc, |Δϖ| = |Δf| = 0.0397 at contact (the compensation mechanism, visible); the
   E1 pair (33/259) sits at 2.42 spacings, rank 8, order frozen. Watch-soundness bound for the
   brief: 2·e_scale ≲ k·(2π/n) with e_scale = Δe (bunched ϖ) or Σe (random ϖ).
3. **Traffic (M1/M1b).** Even with perfect refresh the wholesale λ-watch misses 4.8% of
   events — every missed event is non-intra (fleet×rogue or rogue×rogue; rank\*=114: a rogue's
   equation of center at e≈0.3–0.5 spans ~30–70 spacings), while the fleet's own 2202 events
   are all caught. Cone composition is exact: 542/542 encounters, 6000/6000 radially
   overlapping cross pairs; τ_band 0.938 vs 1.000 stays trigger-blind. Per-pair ΔU
   classification, as before.
4. **Oracle vs watch.** Distance-rank > 4 on 0 of 31,305 events across all 11 scenes; on the
   worst watch-misses the partner is the *nearest* body by true distance (d-rank\*=1). The
   gold's measurement was never wrong; its cheap watch is what needs the bounds above. A gate
   that judges the oracle cannot fail any of these scenes.

**Predictions** (`predictions.md`, written before any `inversion2` run). Held: H1 (0 missed,
rank\*≤4), C1, E2, G1 (255 events in [60,600], rank\*≤4, d\*≤4), **G1b (0 missed, rank\*≤4 — the
held-out refutation of ϖ-coherence-as-binding)**, **G1c (0%<miss<50%, rank\*∈[4,16], below E1
despite 10× 2ae/ρ)**, M1 (all cross missed-events, cone 542/542, ~3·10³ overtakes/orbit),
oracle d>4=0 everywhere. Soft misses, all stated: E1/E1b came in at 35.7%/20.7% against my
45–55%/35–50% — my ranges anchored on the checker's attack numbers, which used a different
rank convention (their E1 = 50% of pairs vs the first author's 35.7% on the identical scene);
with the order frozen my refresh numbers equal the first author's frozen numbers exactly,
which is the convention the record uses. E3 missed low (4.5% vs my >10%): bunching mitigates
8×, more than my Δe/Σe≈2.5 estimate; direction and rank\* (6 ∈ [5,12]) held. M1b rank\*=105 vs
the checker's 13 on the same rogue seed: unexplained beyond their attack code (mine reproduces
audit3-verified rank machinery; conclusion unaffected).

**What would make it wrong.** (1) Rank convention: I use the first author's symmetric-min;
an asymmetric (max) reading raises E1 to the checker's 50% — conclusions are unchanged, and
the brief must pin the convention. (2) Planar, unperturbed Kepler: kicks that re-sort elements
between overtakes, inclination, and 3D nodes untested (stated by the first author too). (3)
One seed per held-out scene family (E1b, M1b cover the two seed-sensitive legs; G1b/G1c/E3 are
single-seed, but their effect is a 0-vs-miss and a 4.4%-vs-35.7% contrast, not a threshold
pass/fail). (4) k=4 as the watch width: the mechanism gives the bound as a function of k; only
k=4 was measured, per the gold's spec.

**Cost of adopting.** Nothing in the crate changes (probe is a separate bin, reverted by the
harness). The certificate brief gains the corrected gates: (i) rebuild-on-overtakes is *in*
the specified design and the horizon scene passes — drop the horizon worry, keep the analytic
overtake counter; (ii) declared watch validity: 2·e_scale ≲ k·2π/n (ϖ bunching modulates the
constant, ~8× on rate), gate scenes E1 (kill, any cadence) and G1b (pass, no coherence needed);
(iii) rank tier only inside the clump + Binet cone across (M1: 4.8% wholesale miss at perfect
refresh vs 0 for composition), per-pair ΔU, population triggers deleted; (iv) the gate must
measure the watch (λ-rank at contact), never the oracle (distance-rank), which passes
everywhere including the kills.

**PRINCIPLES fit.** "A failed expectation is not automatically a failed method: diagnose which
one broke" — the gold's measurement (oracle) stands everywhere; its watch needed bounds, now
measured; the first author's horizon leg failed by testing an unspecified watch. "Write the
kill criterion before the run, with controls on both sides" — G1b/G1 vs E1, E3 vs E1 are the
two sides of each scalar. "Agreement is not independence: several results from one harness
share its bugs" — enforced twice below (lens).

**The lens (what second-authoring made me nearly ship).** Two instrument bugs of my own,
both caught by the audits they were checking: my first Python audit used n = TAU/a^1.5 instead
of the crate's a^-1.5 (a 2π time-warp that silently shrank the horizon 6.3× while preserving
all distances), and my first population audit generated G1c with G1b's seed — its rank
agreement with Rust was a coincidence between two wrong populations, and only a digit-level
element comparison exposed it. Both are the board's 5 October lesson recurring inside one run.
What I may have missed: the checker's E1/M1 rank conventions are inferred (asymmetric reading),
not reproduced from their (deleted) attack code; and I did not test k≠4 or a sweep-refresh
(the lazy re-rank the first author's dossier proposed) — the λ(t) machinery for both is
already in the probe if the freeze wants them.
