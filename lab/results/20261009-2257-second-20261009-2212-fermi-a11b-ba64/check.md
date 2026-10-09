Grade: gold

**Abstract.** Second-author record verified end to end and reproduced bit-exactly: digests m48/m248/m448 identical across the author's runs, the original run's stored evidence and this check. The 10⁹-in-8 GB budget binds on memory: 6.8–6.9 KB live per hot body (427–429× the 16 B tube; 1.17×10⁶ hot bodies today), ~5×10⁻² events/body/game-s warm → N_hot ≈ 1.3×10⁴ (box) to 2.7×10⁴ (M1 kick), cold free (15.8 MB per 10⁹; horizon 1.143 orbits/100 h); "190 cores" re-derives as 175 — a regime, not N. Predictions pre-registered and held; budget.py reads only evidence and regenerates run.log. Attacks: bytes/body is non-monotone in N (7048 at 361 bodies), and the "steady" rate halves by 30 s (2.9×10⁻²) — N_hot understated ~2×, conclusions unchanged. Adopt: zero code, one dashboard/ranking step.

## Reproduction (clean tree a838a28, patch.diff empty, xtask build current)

Every stated command rerun; every quoted number traced.

- **Digests, three sessions, bit-identical.** m48 `09e4085904c7…` and m448 `aadaa1c81e2b…` match the author's evidence, the original run's stored evidence (`origin/claude/lab-20261009-2212-fermi-a11b`), and my reruns; m248 `0fde55d85f3f…` matches the author's two repeats and mine. Same command twice more: same digest, same cut, same bytes/body — the simulation is deterministic at the cut.
- **Rates and slopes.** Full-total 6.125/5.013/4.867/5.048×10⁻² per body per game-s at 71/166/263/410 bodies (author: 6.13/5.01/4.87/5.07); the 410-body kicks+slices+leavers subtotal is 3.71×10⁻² here — the original's 3.9×10⁻² was indeed a subtotal, and the consistent full-total confirms no drop. Two-endpoint slope 6833 B (author 6852), OLS 6841 (author 6857) → 427–429× the 16 B tube. Transient (rtf 1, 30 game-s) 1.630/body/game-s = 32×, identical.
- **The record regenerates.** `budget.py` reads only `evidence/*.json`; its stdout equals run.log's numbered sections bit-for-bit (the only run.log extras are two frame-summary lines whose numbers match the JSONs). Dossier quotes match the JSONs exactly (kick medians 59.956/48.813/46.643/47.789/47.730/48.097 → "46.6–48.8, run 1 at 60.0"; ship 60.5 µs, fleet 29.5; p99 10.08; bpb 6564).
- **Anchors verified.** H0190 K1 32.5 kicks/orbit (HISTORY:2809), H0210 kicks 29 µs (HISTORY:3106), law.md:12 tube 16 B, 0.126 bits/body (HISTORY:3130). Arithmetic recomputed: 175 cores, 0.0299 at belt cadence, 15.8 MB, 2.6×10⁻² cores, 1.143 orbits → 1.1×10⁻³ e-foldings, 1.17×10⁶ ceiling, N_hot 1.32/2.72×10⁴ (worst kick median used — robust), ~40 bits/game-s.
- **Provenance.** stat: predictions.md 22:59:21 < first evidence 22:59:37 < budget.py 23:02 < dossier 23:03. run.log discloses even its failed first redirect attempts. Predictions held on the author's data (the one band exit, kick run 1 at 60.0, reported, not tuned).

## Adversarial cases (mine)

1. **Unchosen slope point, members 348 → 361 bodies: bytes/body 7048, repeatable (7048 = 7048).** The ladder is non-monotone in N: 5189/5687/5959/**7048**/6564. The dossier's "monotone, slightly convex" and the "0.2%" two-endpoint/OLS agreement are artifacts of the four chosen points: the 5-point OLS is 7186 B. By the author's own pre-registered rule the marginal needs an error bar bigger than its spread — it gets one (6833–7186 B, i.e. 427–449× tube); the level claim survives.
2. **Window length, m248 at 30 s (3000 game-s): cumulative full-total 2.94×10⁻², half the 10-s 4.87×10⁻².** Every kind declines in the late window (kicks 2872 → 2332 per 1000 game-s, slices 6464 → 3190, leavers 235 → 8; bodies 263→271, no depletion). The quoted "steady-state" 5×10⁻² is a warm-up window; the settled rate is ~2–3×10⁻², so N_hot is understated ~1.7–2×. Direction is safe (capacity underestimated; the 10⁹ conclusion strengthened), but "a steady-state number" mislabels a decaying continuum between the 32× spawn spike and the quiet tail.
3. **Transient divisor.** rtf-1 rate divides by final bodies (39); the population fell 71→39, so average bodies (55) gives 23×, not 32×. Still ≥10× as predicted; the regime caveat stands.
4. **Kick cost this session: 60.2 and 55.6 µs** — outside the author's 40–50 band, matching their cold run 1 (60.0) and inside their disclosed cross-session family (42–66). N_hot(box) already used the worst median (59.96), so it moves <1%. Single-session µs remain soft, exactly as the dossier concludes; only digest-backed counters are hard.
5. **Counter completeness and determinism.** `dissolved` exists in Stats but is outside `EVENT_KINDS` — 0 in all evidence and all my runs, so no undercount today, but "full-total" means "all non-zero kinds". Stats wobble ±0.06% across identical-command runs (slices 11681 vs 11677) while the digest stays identical — counter noise outside the cut, immaterial at three significant figures.

## Novelty

No HISTORY entry (latest H0215); the original run (20261009-2212-fermi-a11b) is unrecorded, and HANDOFF:70 still reads "H_live … not measured yet" — this partially measures it. The live-store figure is the plane's first (the old path's 88 B/body in representation.md is a different representation). The run adds no physics by design; it is the record the first checker asked for, which is what the lab's second-author slot exists to produce (HANDOFF:18).

## Goal fit

Board items "fitting 10⁹ in 8 GB" and "cost at a billion": the binding constraint today is memory (1.17×10⁶ hot bodies), the memory lever (428×) outranks the slack skin (12.6×), and the board's "190 cores" is shown to be a regime choice (unaveraged, low orbit, rtf 1; belt cadence 0.03 cores) — a premise about N corrected. PRINCIPLES: (3) "Compute only surprises. Cost follows change and entropy"; (24) "The memory floor is information"; (33) "An ant cares about a raindrop but the lion does not"; (10) "Measure before claiming." Zero code to adopt; one step: dashboard gains marginal bytes/body and events by kind, now labelled by regime **and window length**.

## Why gold

The first checker named this exact experiment as the one for gold — stated commands run as written, outputs quoted exactly, `budget.py` reading only evidence, the missing slope points, the regime and the clamp stated — and every item on that list is now done and independently verified to the byte, including the digest chain to the original's stored evidence. My attacks move no quoted number by more than a factor ~2, in the direction that strengthens the conclusion; the two they do bruise are structural sentences, recorded below, not the claim. Physics believed once, record clean now, pre-registered predictions held: gold.

## What the author missed

- bytes/body is non-monotone in N (m348: 7048 > m448's 6564, repeatable); the four-point monotone ladder and the "0.2%" slope agreement are point-choice luck. Quote the marginal with its point-choice spread (6.8–7.2 KB).
- The "steady-state" rate is window-length dependent: 4.87×10⁻² at 1000 game-s falls to 2.94×10⁻² cumulative by 3000 (late-window ~2×10⁻²). N_hot ≈ 1.3–2.7×10⁴ is a warm-window bound; the settled capacity is ~2× higher. The regime label should say "warm-up window", and the dashboard ask should include window length alongside kind.
- The transient's 32× uses final bodies; average bodies give 23×.
- The kick-median band (40–50 µs) was too tight for this shared box — their own six repeats and my two both straddle it; the family (42–66) is the honest unit.
- `dissolved` is not in `EVENT_KINDS` (harmless at 0 today); stats counters carry ±0.06% wobble across identical runs while the digest holds — worth one code comment so no future run mistakes the counters for the cut.
