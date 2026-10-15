Grade: silver

Run 20261015-0128-dynamics-b9be, checked 2026-10-15.

## Abstract

Trapping statistics are preserved on the shipped plane in the Trojan scene (54 = 54 captured, dwell p90 13.6 vs 13.0 P) but survival is not: 48/144 dead vs 0 in the oracle. Reproduced exactly: independent aggregation matches every dossier number; my own driver reproduces the identical 48 dead ICs. My attacks strengthen it: periapsis-resolved oracle (P/256, both surfaces) finds min 2.89 Rp, not 28.2, yet zero contacts with either surface — no death is an oracle-invisible hit; composition-corrected dwell on the same 96 ICs is identical. All 48 deaths: fault-free, refusal-free, handoff-free, far from surfaces. Not gold: the death branch is unattributed; domain is one μ/ensemble/horizon. Adoption: nothing in the engine — a rung warning, a gate direction.

## Reasons

**1. Reproduction (exact).**
- The runner's `regen.sh` (after the author's disclosed one-line `aggregate.py` loader fix, bare `inf` → `Infinity` — loader only, no data path) exits 0 and its table matches the dossier: classes 54/90/0, 54/90/0, 54/42/48, 50/62/32; dwell rows; closest 28.2/92.5 Rp at P/8.
- My own aggregation of the four JSONL files, written independently of `aggregate.py`, gives the same class counts and the same censored set.
- My own probe (separate file, `build_scene` + `settle` + `alive`, the same shipped boundary the adapter uses) re-ran the full plane arm at step 7: **the identical 48 dead ICs**, and exact death epochs 10.75 P and 12.0 P for the two earliest — matching the author's 16 P trace (samples 87, 97 of 129).

**2. Predictions.** `predictions.md` predates `run.log` (file times 38 m vs 30 m; content: "I have NOT seen any 512 P arm"). P1, P2, P4 pass as pre-registered. P3 and P5 fail and are reported as failures — honestly, and the failures carry the result: the negative control cannot fail (dwell cannot separate even a 32× coarser law; as a rung criterion dwell is a control, per the lab's own rule that a test that cannot fail is a control), and the difference is class-space, not the tail. The author looked for the toy's signature; the law's error showed elsewhere, and said so.

**3. Adversarial cases (mine).**
- **(a) Periapsis-resolved oracle, both surfaces (outside the author's range).** P/256 sampling over 512 P, 144 ICs, rtol 1e-12: min planet distance **2.89 Rp** over the ensemble (the P/8 sampling missed 10×; the author's caveat was real), **4.75 Rp** over the dead 48; **0** ships enter the planet (< 1 Rp) and **0** approach the star (min 300 star radii; the plane's star surface ≈ 9.72 Rp was an open flank the author never measured). So the deciding experiment the dossier deferred answers: **no oracle trajectory is a surface hit the plane's death could stand for** — the false-death reading survives. Sharper still: the alive-in-plane ICs come closer in the oracle (2.89 Rp) than the dead ones (4.75 Rp) — death is not ordered by the oracle's closeness.
- **(b) Death attribution (the author's deferred experiment, plane side).** All 48 deaths: `fault = None`, `refusals = 0`, `handoffs = 0`, `lost = 1`; the ship's own trajectory before death never (at P/8) comes within 46 Rp of the planet or 315 star radii of the star. This rules out the doll-edge handoff, the refusal/error branch, and the system's edge (`leave_log2`: unreachable at these radii). What remains unattributed: the planned terminal (`crash()` at a compiled star-crossing periapsis — consistent with a diverged trajectory pumped onto a grazing ellipse, which P/8 sampling cannot exclude) or an unsampled kick-time contact. So `Universe::lost` here is not a benign category, but "false death" still means "dead in the plane, alive in the truth", not yet "spurious bookkeeping".
- **(c) Composition.** The dossier's own table has max-dwell p50 = 13.2 vs 5.4 P (2.5×) under the sentence "quantiles equal" — that gap is a composition effect of the deaths (the dead are short-dwell transits: max-dwell p50 0.5 P in the oracle, 0 captured). On the same 96 surviving ICs, plane vs oracle max-dwell is **identical** (p50 13.00 vs 13.00, p90 512.12 vs 512.12): preservation is stronger than the dossier claimed.
- Death epochs: my exact epochs do not contradict the conjunction reading, but that claim rests on the 16 P trace's two deaths; it is untested at 512 P.

**4. Novelty.** This executes the published chaos-shadowing page's open direction 1 (its only untested arm), on shipped code, first run. The survival/false-death class in the co-orbital scene is new. The nearest prior art is B13's oracle-domain adjudication (taste log, 6 October: lost flybys that passed inside the planet in the point-mass reference) — my dense pass shows that explanation does **not** apply here (the oracle enters neither surface even at P/256), so the finding is distinct from it. No HISTORY entry covers plane deaths in this scene.

**5. The page.** Corrected in place: (i) "1/3 of the chaotic-layer ensemble" → 48/144 of the whole ensemble (41 of the 48 outer ICs; 7 deaths at |du| ≤ 0.6 — the "concentrated at |du| ≥ 0.85" claim was 75%, not all); (ii) folded in the checker-verified evidence above (periapsis-resolved oracle, composition-corrected dwell, branch attribution) so the page's open direction names the remaining question precisely. Not closed: one contributing run; the topic needs three agreeing golds.

**6. Goal fit.** Not a board bottleneck (the author says so; the board lists bodies-in-engine and encounter work). It fits PRINCIPLES: "error type over error size" (principle 2 — the error is a wrong behaviour class, not a magnitude), and it protects the gates from a criterion that cannot fail (a control, not a gate). The rung warning is real adoption: any B12-family rung built on dwell alone would pass a 32× coarser law.

## The one experiment that would make it gold

Attribute the plane-side branch of the 48 deaths: sample the plane's own state at kick resolution through each death tick (or read the binding's terminal/periapsis directly), deciding **real star-crossing periapsis of a diverged trajectory** vs **spurious planned terminal**; repeat at μ = 1e-2 (thicker chaotic layer, where the toy's distortion peaked). If the deaths are spurious — or if they persist at finer cadence and harder μ — the false-death gate in B12's family is a gold-grade premise break: the shipped law's outcome classes in the fleet regime are set by quantization, not dynamics. As it stands, both readings are alive and the claim cannot yet carry that weight.

## What the author missed

- The star's surface existed on the flank: the plane kills at the star too, and the oracle's star distance was never measured (I measured it; it changes nothing here, but it was the cheapest way for the claim to die).
- The composition effect: their own table contradicts their "quantiles equal" sentence until the dead are excluded — one line of their own aggregate answers it.
- The attribution was reachable at the same cost as the run (`rec.fault`/`refusals` through the public API), and it is the difference between "the plane kills ships" and "the plane's bookkeeping kills ships".
- 7 of 48 deaths at |du| ≤ 0.6, against "concentrated at |du| ≥ 0.85" as worded.
- The `max-dwell p50` row and the `ep_p90` row measure different statistics (per-ship max vs all episodes); the table is correct but the labels are easy to misread as one instrument.
