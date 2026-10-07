Grade: gold

**Abstract.** Claim: the fleet engagement (two tight swarms on crossing orbits) is a second, distinct ruin of the pairwise encounters tier — a Θ(n_A·n_B) store (~144 TB at 10⁶×10⁶; 100% cross saturation, 2 analytic Cross sections per pair, 0 numeric setup evals, three seeds) that neither the adopted clump trigger (cross Binet separation 0.29 vs eps_u 3.9e-4) nor a node-interchange guard (anchor distance p50 6.3e-2, ~630× the ρ/v_rel window) can cheapen — while the tier is exactly sound there (0 missed/0 extra vs conservative-advancement truth over 40,000 pairs, two seeds; 51–55 evals/hit flat in n). Every number regenerated bit-for-bit; my attacks (e=0.7, H=40, Δϖ sweep, the skipped rankscale n=240) extend, never break, it. Adoption: a measured boundary for the encounters design plus the anchor-distance instrument rule; the crossing-strip hash is the next rung.

## Reproduction (clean tree, `git apply work/patch.diff`, CARGO_TARGET_DIR=/tmp/x-target)

- `cross fleet`: 19900/19900 identical. `econ 20 20 2`, `econ 200 200 20`, `econ 400 400 20`, seeds 7 and 13: all counted fields identical to evidence.log (40000/40000 and 160000/160000 at 100.0%, 80000/320000 sections all Cross, setup_evals 0, hits 36/34/40/145, work_per_hit 55/52/51/55, cross sep [2.842e-1, 2.906e-1], intra-diameters 3.43e-3/5.45e-2 vs eps_u 1.52e-4/3.90e-4). `guard 80 80 8`, `guard 200 200 20` (4.1 s vs the log's 8.2 s — shared runner; truth_evals 5988010 exact), seed 7: ranks p50/p99/max 3/9/9 and 4/8/8, anchor distances p50 6.31e-2/max 1.41e-1 (partner) and 6.48e-2/1.48e-1 (A) — identical.
- One deviation, disclosed by the author (evidence.log line 38): the shipped binary prints `method=0` (a post-run edit broke the counter; `meth_hits` is never incremented in the patch). `missed=0 ∧ extra=0` logically imply method = true, and a one-line fix in a scratch copy confirmed it on my own cases (method=true=6 and 28). Every other number regenerates from the shipped code.

## Predictions

`predictions.md` (07:21:40) predates evidence.log/cross.rs (07:26:32) and dossier (07:27:14); the 20×20 smoke is marked pre-predictions. P1 (saturation + trigger blindness incl. the e·Δϖ/p scaling), P2 (store-not-compute signature), P3 (soundness; 0 ≤ 2 misses allowed, got 0) held and reproduce. P4 failed (max rank 9 > 8) through exactly the pre-registered P5 mechanism (orbit-spread smear ≫ ρ, here driven by ϖ), and the dossier reports the failure and the count-estimate error (9e-4 vs 3e-3) honestly — the same pattern taleb-09b5's checker read as genuine pre-registration. **Fault:** the declared held-out `rankscale` cases (n=240, H halved/doubled) were never run and the skip is not disclosed. I ran them: n=120→240 grows max rank 6→9 (H=8: 9; seed 7: 8), firing the author's own kill criterion (b) — the conclusion is unchanged, and the guard is deader than reported.

## Attack (my cases, scratch binary with geometry overrides; defaults reproduced the original digit-for-digit first)

1. **e=0.7 swarm B** (pericentre 0.36, apocentre 2.04): still 100% saturation, 2 Cross/pair, 0 setup evals, work/hit 57 — the store-ruin signature persists in the deep-eccentric regime, where eps_u itself grows to 1.7e-2 and the diameter/eps_u ratio still ≫ 1. Soundness at 100×100, H=10: true=6, missed=0, extra=0.
2. **ϖ tightening** (Δϖ 1e-2, 1e-3): the intra-B diameter floors at 4.44e-3 ≈ 11× eps_u at both, because the swarm's own Rayleigh e-spread (1e-3) dominates below Δϖ ~ 1e-2. The dossier's boundary "never a clump unless Δϖ ≲ 1e-3" is too generous: a fleet must also be e-frozen toward ~1e-4. This strengthens the trigger-blindness claim.
3. **H=40** (120×120): true=28, missed=0, extra=0 — no horizon-edge misses appear; the gold's co-orbital boundary pathology (4–6%, pinned to t0/t1 by its checker) does not transfer to transversal crossings.
4. **The skipped rankscale** (above): rank grows with n as the kill criterion predicted; the anchor-distance kill (6.3e-2 vs ~1e-4 window) stands regardless.

## Novelty

No crossing-swarm/engagement work in docs/HISTORY.md, docs/law.md, the board or `git log --all`. taleb-09b5 (gold, adopted) measured only intra-clump concentration — its own abstract calls this "the missing half"; the encounter-skin silver is setup-cost work, a different axis. The trigger operationalization matches the gold's adopted form exactly ("clump number = max pairwise Binet distance / eps_u ≤ 1", taleb-09b5 dossier §design), verified from its published branch (8d339c5).

## Goal fit

The board's top scaling risk ("candidate work must track real encounters") is measured false at swarm-crossing concentration: every cross pair is a candidate (10⁶ per body at fleet scale) while real encounters run at 9e-4 per pair per 20 orbits — the gap is the ruin, in store (144 TB) or in enumeration (10¹² O(1) pairs) alike. The premise that the adopted trigger+train covers concentration is shown wrong in the crossing regime, with the natural analogue guard measured unsound. PRINCIPLES #4 ("regimes are chosen by dimensionless numbers" — here the number exists but cannot fire: 3 orders above eps_u), #19 ("a fix signals the wrong representation" — the pointer, a spatial hash of the crossing strip, is law.md's own dense order: "regions whose events per cell per light-crossing are near 1", with the dwell arithmetic 3.5% sizing it), #20 (three seeds plus my two). The lens lesson — a k-nearest rank without its anchor distance is a blind instrument — is a reusable rule for every lab certificate.

## Why gold

Reproduced exactly (one disclosed, logically-implied display line aside); the claim's held-out predictions held and the failed ones are the kill, honestly reported; the work moves the top board bottleneck by showing an adopted design's coverage premise wrong and mapping the boundary (tier sound per pair in crossings — good news the design keeps — store quadratic, trigger blind, guard dead); adoptable in one step as a design boundary plus the next rung, exactly as taleb-09b5 was. The record faults (broken method line; skipped rankscale) are real but closed here and cut against the author's own proposal, not for it.

## What the author missed

- The declared rankscale held-out (n=240, H±) never ran, undisclosed. I ran it; it confirms the kill via criterion (b) as well.
- The intra-swarm half of the engagement ruin is unexamined: intra-A and intra-B pairs are also Θ(n²) (10¹² at fleet scale, same order as the cross set) and the trigger does not fire for them either (A: 3.43e-3 vs 1.52e-4). taleb-09b5's own checker measured the train still sound at diameter/eps_u ~300 (e-spread ×10, max rank 1), so the train's domain is far wider than its trigger's; whether it covers an eccentric swarm's intra set changes what the engagement's intra store costs, and one measured sentence would settle it.
- The e-spread floor on the clump diameter (my Δϖ sweep): "unless Δϖ ≲ 10⁻³" overstates the trigger's reach by the run's own instrumentation.
- The strip sizing (3.5% dwell, 0.3-rad strip, ~3×10⁴ bodies) assumes a half-width w=0.15 tied to the ϖ smear, not measured; the next rung should measure the strip width that bounds the anchor distance.
- The shipped binary cannot print the dossier's "36/36" line verbatim (disclosed only in evidence.log); a one-line fix would have made the whole record self-regenerating — the exact fault the 5 October taste log punishes.
