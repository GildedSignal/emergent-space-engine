Grade: gold

Abstract: Second-author fix of the clock bug (force clock at 1.5× body rate — verified: ratio 1.4998, lead 119.3 Jovian revs/1000 orbits) plus a quantize-and-carry control. The record regenerates bit-exact from one command (13.6 s). Impulse deferral is killed: energy walks (exp 1.01–1.11) at every quantum that saves renewals, and survives my 3000-orbit and e=0.6 extensions; at the true 2:1 it scrambles ψ (−5.9…+6.2) and ejects hyperbolic at 32·dvr, inside a distortion band 24–34·dvr (pump ≥ 6.5). Checker caveat: quantcarry's "bounded" is q-scoped — at 128·dv it walks (exp 0.96, 2.4× worse than deferred at equal q), firing the author's own pre-registered split criterion. Adopt: the renewal quantum never lives on the impulse side (naive impulse debt). Cost: zero code.

## Reproduction

- `python3 deferral.py deferral-check.json` in a clean tree: **bit-exact** (`cmp` clean), 13.6 s, ~60 MB. Every dossier number matches `deferral.json` cell-for-cell (Scene A, A2, B, probes, the 28–46× and 22.4/1.87/856/10.6 figures).
- Clock bug verified twice: in code (`deferral-orig.py` lines 106/125/127 advance `t` by 3×0.5·H per H of drift) and empirically (spied force time/body time = 1.4998 at kick 1200); the lead is analytic: 0.5·1000·(2/5.2)^1.5 = 119.3 revs. The corrected clock evaluates the force at (i+0.5)·H, and a₀ = 5.2·2^(−2/3) makes n/N_J = 2 exactly.
- `predictions.md` (mtime …307) precedes `deferral.json` (…322), consistent with the 12 s run; the author disclosed the predictions were informed by checker 2's probes. Predictions held within their stated scope; letter misses (#1 exp 0.54, #4 mid-ladder, #5's 2.9×) are reported as misses, retractions stated as retractions.

## Adversarial cases (all run here)

1. **3000-orbit horizon, q=32·dv (the exp-0.54 letter miss):** deferred max|ΔE| 5.6e-3 → 1.19e-2, exp 0.78, error still growing at the end (last ≈ max). The dossier's "saturates early at a plateau" explanation is wrong — it is slow growth, and the walk claim holds over the longer window, stronger than reported.
2. **e=0.6 (B9's edge):** deferred exp 0.94/0.77 vs quantcarry 0.57/0.39 with negative late-window slopes. The split holds at the edge.
3. **Scene B q-sweep (16–64·dvr):** pump ≥ 6.5 across 24–34·dvr (e_max 0.66–1.07, ejection at 32·dvr, near-ejection 0.82 at 30·dvr); but 16·dvr looks benign (pump 1.10, ψ −0.12) at 16× renewal savings — non-monotonicity extends below the author's ladder. The ejection-as-existence-proof framing is correct; the kill at resonance rests on the band and the energy walk, not monotonicity.
4. **Quantcarry at large q (the miss, below):** q=128·dv → max|ΔE| 1.45e-2, exp 0.96 — 2.4× *worse* than deferred at the same q (6.03e-3); q=32·dv over 3000 orbits grows ~t^0.34 (1.19e-3 → 2.2e-3), late-half slope 2.9.

## Novelty

Not previously done. The deferred mode is Julien's own impulse-debt idea (docs/reference/original-conversation.md, "accumulated_effect = 0.73 quantum", "the residual/impulse-debt idea … is foundational"); this measures its naive form and kills it for the binding layer. Distinct from components-4643 (encounter-*setup* deferral, 6 October) and from H0159/H0174's contact energy-residual carry (exact carry in contacts, consistent with quantcarry's moderate-q boundedness). Citations verified: archive/engine.md "secular drift: forbidden"; law.md's resonance guard; the pump band [0.8, 1.25] is B17's, so the instrument is law-native.

## Goal fit

Deletes a patch class before it is built — the cheapest-looking route to fewer renewals — and corrects the record that would have justified it. Principle 2 ("error type over error size"): timing walks, magnitude dithers — now measured with the right clock. Principle 9: the configuration dies, the method lives. Board focus 1 and 3.

## Why gold despite the qualification

The load-bearing claim (deferral walks at every saving q; the renewal quantum has one home, off the impulse side) is reproduced bit-exact, robust under three adversarial extensions, and adoptable at zero cost — and my probe #4 *reinforces* it: even carried magnitude quantization drifts at large q. What falls is only the unscoped strength of the instrument claim. The integrator should adopt the kill plus the sharpened rule below, not the reading "magnitude rounding with carry is safe at any q."

## What the author missed

- **No quantcarry q-ladder.** "Stays bounded" was asserted from q ≤ 8·dv alone; at 128·dv quantcarry walks (exp 0.96 ≥ the author's own pre-registered 0.8 walk threshold, at a q where deferred saves 2600× renewals) — the sentence "the pre-registered kill criterion for the split rule did not fire" is true only inside the untested ladder. The carry bounds the instantaneous momentum error, not the energy drift, which is second order in q but nonzero and walking.
- **The plateau explanation at q=1.4e-4** (error "saturates") is a windowing artifact; the walk resumes by 3000 orbits (exp 0.78). The honest letter-miss was actually a held prediction over a longer horizon.
- **"quantcarry exp −0.01…0.44" mixes metrics:** −0.01 is expE (scene A2), 0.44 is expW (scene A); the pure expE range is −0.01…0.39. Regenerable, but loosely cited.
- Minor: prediction #1's renewals "within 30%" is violated at q=5.5e-4 (0.024 vs 0.04, 40%) and not listed among the letter misses; checker 2's numbers (the 1.87, the 8·dvr ejection) are unverifiable in this container — the original run folder is absent — and rest on the dossier's word.
