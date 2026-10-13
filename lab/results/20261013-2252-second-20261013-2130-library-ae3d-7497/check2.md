Grade: gold

**Abstract.** Second, blind check of 7497 (rule 2's falsifier, run on shipped `scenario::plane`): every deterministic number reproduced via `regen.sh` (109 s; counts bit-identical — CV rows, player shares 21.1/17.9/70.6/0.2%, haulers 0–2 kicks, store rows 12.347/48.38 bits, 0 mismatches); digest neutrality re-proven (`e0972a1c…` identical base vs patched, tree clean after). Predictions pre-registered, misses honestly reported. My adversarial cases all confirm: seed 11 idle (tube CV 0.200); burn L15 keys-3 — player 100.0% of body kicks (315,640 in 200 s); 40,000 members, 10× the author's max — member kicks p50 29 = max 29, top-1 0.006%: headless, stronger than at 4,000. Rule 2 is dead on the plane; the promotion bar is a body constant; the head is drivers. Adoption cost: zero — the ladder deletes the rank rungs and surprise-rate instrumentation before building them.

## Reasons

**1. Reproduction.** Clean tree, `regen.sh` end to end in 109 s: all four scene blocks match the dossier line for line (idle s1 9,176/96 kicks, CV 0.179/Gini 0.100/Zipf −0.23; idle s7 10,800/969; burn 2,142/48 with player 1,513 = 70.6%, 816 sub, 89 clock; m4000 78,299/88 with member mean 20.6, max 174, p50 5, per-lived-second Gini 0.549). Orbiter 2 near-constants 212.37/202.04/210.62/212.08 across scenes. Store rows: 12.347 bits at 7–9 ns (run-to-run noise, as the first run's checker found), storm 48.3811 with inference fallen back, 0 mismatches, repacks 2,570, compaction step 1.27–1.30 ms. Timing-only rows vary (convoy hot max 3.85–10.5 µs over three runs) — orders of magnitude, per the lab's Linux/x86 rule. Digest neutrality independently re-verified by diff of the stored base/patched flights and by regen's own gate.

**2. Predictions.** `predictions.md` mtime 22:57 precedes the probe captures (23:15+) and the patch itself (23:11); the content shows real priors (the P3 idle top-1 bar < 20% missed at 21.1% on seed 1 — a miss the author surfaced and diagnosed as frequency-not-surprise; my seeds 7 and 11 give 17.9% and 17.5%, i.e. seed noise at the bar). P1 and P4 held; P2/P5 half-held with the misses owned. Kill criteria were written before the run.

**3. Attack (four cases, two outside the author's range).**
- *Seed 11 idle m48* (author ran 1 and 7): tube CV 0.200, max/med 1.47, top-1 10.5%, player 250.3/orbit flat with the orbiters — holds.
- *Burn L15, keys 3* (author's regime was L12, keys 1): the player takes **100.0%** of body kicks — 315,640 kicks in 200 game-s (1,578/s) — the driver-head claim at its extreme. The tube CV rises to 0.43 there, but on 1–5-kick counts at a 200 s span that is sampling noise, not a tail.
- *40,000 members* (author's max 4,000, next decade): 19,960 handed out, member kicks p50 29, **max 29**, top-1 0.006%, top-10% ≈ the uniform share — the battle stream is even flatter than at 4,000. No rank to promote by, confirmed outside the tested range.
- *Burn seed 7*: player 66.1%, 816 sub, 89 clock — the waterfall reproduces across seeds. The page's "10/38 and 8/37 members with passage sub-kicks" verifies on the author's own captures; seed 11 gives 5/41 (sub 10–76), same sparse due-ness picture.

**4. Novelty.** The nladder page's open direction 1 named exactly this experiment; no earlier run measured the per-body kick distribution on shipped scenes. The flat-bulk half was near-known by construction (27ce: the plane flies 1/128; kick-cadence page) — the author says so in the lens section — so the new content is the measured head (driver-caused: burn 66–100%, battle headless) and rule 2's death. Not a repetition.

**5. The page.** Faithful to the evidence; every number I spot-checked regenerates (12.347/48.38 bits, Gini 0.55, mean 20.6/max 174, 22/3,769 sub-kicks, 2.3× uniform for top-10%). Corrected in place: `step_for` is 1/2⁷ of the period (`Config::step_log2` defaults to 7, the 1/128 of 27ce), not the dossier's 1/2⁶; added seed 11 to the confirmed list. The dossier's "top member 0.07%" is the per-lived-second share (raw-kick share is 0.22%) — the page keeps the rate sense, correctly scoped. Not three gold runs on this topic; the page stays open.

**6. Goal fit.** Board focus 1 (28 bodies against 10⁹), deciding the in-flight ladder's promotion design: it shows a premise is wrong and deletes a design path (rank rungs, surprise-rate instrumentation) before it is built — adoptable in one step at zero cost. PRINCIPLES: "the cheapest compute is compute not done" (a rank nobody needs to measure); "Compute only surprises" (the head is drivers, already light-cone events); #19, one law at every scale — the cadence law already explains the bulk; promotion-by-rank would have been the second convention.

**Why gold despite the construction caveat.** The author's own lens section concedes the flat bulk was near-inevitable given the cadence law; the run's bite is the driver half and the verdict, the falsifier was the one the page itself named, the probe is digest-neutral on a burn flight, the predictions were pre-registered with honest misses, and my out-of-range cases (10× members, deeper burn) confirm rather than break the claim. The claim is properly scoped to the plane, with the belt named as the revival path.

## What the author missed

- The 1/2⁶ slip (it is 1/2⁷; fixed in the page).
- The deep-burn cost regime: L15/keys-3 settles at ~0.42 s wall per game-s, compute-bound on one body's 1,578 kicks/s stream. Distribution-wise still "driver = head", but the ladder's per-frame budget at that extreme is the player, not the fleet (the burst job's territory; recorded as a side observation, not re-measured).
- The 40,000-member settle costs 222 s wall for 300 game-s (hand-out dominated): a ladder data point for rung design at 10⁴–10⁵ bodies, unrecorded.
- The haulers' per-orbit numbers remain 1-kick extrapolations (marked, but the page still prints them to 5 digits).
- The belt/conjunction clustering — rule 2's honest revival path — stays unmeasured, as the dossier admits.
