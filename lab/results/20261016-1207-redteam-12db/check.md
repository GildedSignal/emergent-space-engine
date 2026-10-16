Grade: silver

**Abstract.** Claim: representation.md still teaches three refuted premises, and its kick row ("a multiply-add", "~50 ns") is ~700× shipped code (median 34.8 µs made, 203 µs leavers, exact memo reuse 0.0%). Reproduced: regen digest-stable; my held-out arms (seeds 7/42, rtf 100/3000) give 14,219 rebinds, zero exact reuse, made median 34.6–35.4 µs, refused 0. Gain: deletes false premises from the input doc every builder reads; cost: one integrator editing pass, no code. Not gold: the refutation is the record's own — b063 (gold, 11 Oct, frame-cost page) already measured 75.6 µs vs a 42–56 ns floor (~1,800×) with exact memo 0%, uncited by the author. New: the six-premise census and the guard-gap map (r5/r6 never created, no kick-cost rung). Silver: adopt the edit; freeze the missing kick-cost rung next.

## Reasons

**1. Reproduction (clean tree at base cab6188, empty patch — measurement run on shipped code).**
- Runner's regen.sh exit 0; I re-ran the arms myself. kickbench.json: made median 34.766 µs (695× the doc's 50 ns), leavers 203.2 µs, memo 2262 rebinds / 2262 distinct exact shapes / exact_hit_rate 0.0 / quantized 0.9797 over 46 shapes, refused 0, digest 09e7816937eb0998 stable across both regen runs.
- Numbers that differ from the dossier: made p99 50.7 (dossier 53–63), leaver p99 394.8 (dossier 399–408) — timing noise on the shared box, same order; medians match to 0.1 µs.
- Every doc/code citation checked and stands: representation.md L32 ("primary in-cell solution"), L57 ("crosses once"), L67 (multiply-add), L113, L114 (~50 ns); law.md L20 (Darwin replaced the band map), L36 (jet retired by three golds; quantized memo refused), L39 (r3 v3's numbers verbatim), ~L90 (r5/r6 assigned to GLM); ENVELOPE.md L141 and QUADRATURE.md L139 ("prediction… recompilation remains authoritative"); rung inventory has no r5, no r6, and no kick-cost rung; B8/B9/B10/B11/B19 as characterized; wiki citations (6eae, 5977, 8be2, 0fe0, a616-ungraded, a4ed, 3294, 6254, 8e84, binet-cells' four broken channels, "the lab has still never graded r1") all present and correctly quoted.

**2. Predictions.** predictions.md predates the decisive run (file order consistent: predictions → regen.sh → bench outputs), and the author's honest self-report of the arithmetic miss (predicted 10⁵–10⁶×, actual ~7×10²) corroborates genuine pre-registration. Held: the µs range (20–300; measured 34.8/203), zero reuse, no fast path (no "jet"/derivative update exists in crates/space; the bench's exact_shapes == cycle_rebinds proves it behaviourally). One miss the dossier does not acknowledge: prediction 2's literal "kick_us ≈ kick_us_all ≈ kick_us_leavers to within noise" failed — leavers are 6× the made median (203 vs 35 µs), not noise, though not a memo effect (exact reuse is 0 everywhere).

**3. Adversarial arms (mine; three outside the author's seed-1/rtf-600 domain).**
- Seed 7, rtf 600: exact 0.0 (2751/2751 distinct), quantized 98.2%, made 35.2/44.8, leavers 175.7/402.5, refused 0.
- Seed 42, rtf 600: exact 0.0 (2575/2575), quantized 98.1%, made 35.0/44.8, leavers 162.2/370.8, refused 0.
- rtf 100 (30 s) and rtf 3000, seed 1: exact 0.0 (1109 and 7784 rebinds), quantized 96.0–99.2%, made 34.6–35.4 µs, leavers 203.1 and 365.3 µs, refused 0.
- 14,219 rebinds across arms, zero exact reuse, no population under ~35 µs median anywhere: the ~700× refutation is robust, and the leaver median is pace-dependent (162–365 µs — consistent with frame-cost's 199 µs record), which the page should scope.

**4. Novelty — this is what keeps it from gold.** The decisive physics content is the record's own, at gold grade, and the closest prior is uncited: **20261011-1729-components-b063 (gold): "kick 75.6 µs vs 42–56 ns floor (~1,800×); the refit is 84–89%; exact memo 0%"** (lab/wiki/frame-cost.md, Runs). Also prior: 97ce (0/203,017 memo hits), 3367 (1125/1125 fresh fits), 7055 (0/3,225), c01c/0c44 (43–52.8 µs, zero reuse — cited), three jet golds (cited), the 5-October taste-log correction 0%/94.5% (cited), and law.md L36 has said "a kick recompiles its cycle exactly… the kick's cost is the frame-cost bottleneck" since 12 October. Per the lab's own rule, a repetition is not gold however well done. What no page held, and what this run delivers: the six-premise census of the doc itself; the guard-gap map (no rung exists for any kick-cost row; r5/r6 named in law.md and never created — verified against lab/rungs/); and the both-sides memo squeeze (exact 0.0 / quantized ~98% in one shipped instrument). The instrument (`xtask universe --kick-bench`) is shipped since 1 October (1932f6c8), correctly used, not modified (empty patch).

**5. Page.** Faithful to the evidence; corrected in place for three overstatements: the Refuted entry now cites b063 and the earlier zero-reuse runs (the refutation is the record's; this run regenerates it); the census's "the §6 cost table has no rung or gate at all" is narrowed to the kick row (B9 gates the undisturbed row's letter, B10 gates cost-vs-N, r7-ai-cost exists — none gates per-kick cost); the leaver median is marked pace-dependent with my arms folded in. New topic, first run, no closure.

**6. Goal fit.** Yes, on the documentation axis: the doc is the input to every specialist and lab run (law.md assigns its falsifiers to GLM), and principle 10 ("Measure before claiming") is violated by a §6 estimate that now contradicts three golds and shipped code; principle 19's alarm applies to the document. PRINCIPLES respected: no edits to main/docs/crates/frozen evidence, lab machine, orders of magnitude only, honest lens section (the DRAFT-status defence is named and answered). It moves no physics bottleneck and deletes no code component — the adoption is an integrator editing pass, which is also why it is not gold.

## The one experiment that would make it gold

Freeze the falsifier the census names as missing: a kick-cost rung on the shipped bench (e.g. r11: made-kick median µs and exact-reuse rate against frozen thresholds, positive control = the doc's ~50 ns multiply-add path reconstructed, negative = shipped rebind), so representation.md's cost row is guarded by a frozen criterion instead of by three golds the doc ignores. The doc amendment itself is the integrator's one-step adoption of this silver.

## What the author missed

- b063 (gold) already measured the same refutation six days earlier at ~1,800× with exact memo 0% — the strongest prior, uncited; the claim sentence should credit it and scope this run's novelty to the census.
- Prediction 2's made≈leavers equality failed by 6× and went unacknowledged.
- "The §6 cost table has no rung or gate at all" is overbroad (B9/B10/r7 touch three of its six rows); the true gap is the kick-cost row (and r5/r6).
- "Not rewritten since 29 September": last substantive edit was 30 September 16:34 (d46b4ab0); 6 October touched links only. Immaterial to the claim.
- The two surviving premises' named flanks (4: comparable-mass strong field vs a 1PN-only oracle; 5: the replay gate's toothlessness) are correctly flagged but unmeasured — either is the natural successor run.
