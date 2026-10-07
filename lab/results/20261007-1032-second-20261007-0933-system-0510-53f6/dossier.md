# Dossier — 20261007-1032-second-20261007-0933-system-0510-53f6 (second author, system lens)

**Claim.** The checker's named experiment cleanly refutes the parent claim as
shipped — the unified conjunction kick (B) loses the away-set tail test at
every pre-registered compiled-frequency width (belt p90 rate error 13–19 vs
A's 0.61–0.67, 20–28 of 90 wrong-sign, 3 seeds) — but for a different reason
than the checker suspected: the failure set is disjoint from the resonances
(0 of 33 failures inside the band at B17's width; particles within 0.2% of
the 7:3 and 1.4% of the 5:2 pass at 0.03–0.16) and is the **(de, dϖ) Gauss
form's O(μ/e) window residual** (log-error correlation ρ = 0.70–0.90 with
1/e₀, −0.11–0.39 with resonance detune/width): the synodic window is not an
integer number of particle orbits, so the quadrature of dϖ/dt — which carries
a 1/e prefactor — leaves a non-cancelling residual that wrong-signs ϖ at low
e. The same event in the **eccentricity-vector representation** (B2:
increments of e·cos ϖ, e·sin ϖ, regular at e→0, a one-line change) fixes the
precession rate completely — belt med/p90/max = 0.036/0.228/0.489 vs A's
0.547/0.671/0.720, zero wrong-sign on all three seeds, B2's worst particle
better than A's worst — while leaving the r4 v1/v2 first-order over-pump
(1.21–2.08× where REF pumps 1.0–1.3×) on the 2:1's approach flank (detune
6–14%), which no honest compiled-frequency width guards: the e-envelope tail
clears A's only at 4× B17's width, which carves 56% of this belt out of the
away layer. The unification therefore stands for the rate at cadence parity
(0.56–0.60 events/orbit, B2 = B) but is not yet a whole away-layer
replacement: the flank needs phase feedback (law.md's rotating doll / normal
form), not a wider guard.

**Bottleneck.** Board focus 1 (kicks dominate; the lever is cadence —
q-cadence) and focus 3 (encounters without per-orbit work). The parent
proposed deleting the kick-cadence chooser by riding the encounter tier's
conjunction calendar. This run keeps that deletion alive only in the
e-vector form: the conjunction event is the right event (its rate accuracy
beats the orbit-averaged incumbent 15× at the median with zero wrong-sign),
but the impulse must be written in the eccentricity vector, and the
conjunction law near resonance still lacks phase feedback — exactly where
law.md already routes that regime.

**Evidence** (Linux x86 cloud, orders of magnitude only; 9 decisive runs +
summary, each run ~35 s single core, ~40 MB; commands in [run.log](run.log),
all artifacts in this folder).

Scene and REF/A identical to the parent (Sun + Jupiter μ=9.55e-4, circular
a=5.2; 30-particle belt a 2.60–3.15, e 0.02–0.15, + 7-particle 2:1 scan;
H=24000 ≈ 322 perturber orbits; REF leapfrog 96 steps/orbit). Port validated:
seed 20261007/B/on reproduces the parent's decisive.json in every physics
field. Regime selection: law.md's compiled-frequency test p·n − q·n_J ≈ 0
over reduced pairs q ≤ 14, order k = q−p ≤ 8; half-width in mean-motion
ratio W_k(e) = C·√(μ·e^k) anchored at B17's frozen W = 2.5·μ^(2/3) at
e₀ = 0.02 (C₀ = 5.55); verdicts at C₀/2, C₀, 2·C₀, sensitivity to 6·C₀.

Belt away-set tails, pooled over 3 seeds (90 particles; B2 = e-vector, off-memo):

| law | width | n_excl | rate med/p90/max | wrong-sign | env p90 (B vs A) |
|---|---|---|---|---|---|
| B (shipped) | C₀ | 2 | 0.121 / **13.18** / 33.20 | **20** | 0.044 vs 0.145 |
| B | 2·C₀ | 16 | 0.109 / **12.86** / 33.20 | **16** | 0.044 vs 0.114 |
| B no-memo | C₀ | 2 | 0.087 / **18.48** / 48.97 | **28** | 0.030 vs 0.145 |
| A (incumbent) | C₀ | 2 | 0.547 / 0.671 / 0.720 | 0 | 0.145 |
| **B2 e-vector** | C₀ | 2 | **0.036 / 0.228 / 0.489** | **0** | 0.320 vs 0.145 |
| B2 | 2·C₀ | 16 | 0.027 / 0.139 / 0.305 | 0 | 0.190 vs 0.111 |
| B2 | 4·C₀ | 50 | — / 0.072 / — | 0 | 0.130 vs 0.144 (first width where B2 ≤ A) |

- Failures vs resonances (B, 3 seeds): 33 belt failures (relerr > 2), **0**
  excluded by the compiled-frequency test at C₀ (5 at 2·C₀); the shipped
  seed's 8 failures sit 2.5–12 half-widths from every compiled frequency
  (e.g. a=2.732, ~10 widths from 13:5), all with e₀ ≤ 0.065; correlations
  ρ(log relerr, log 1/e₀) = 0.70/0.90/0.79 vs ρ(log detune/W) =
  −0.11/0.39/0.14.
- B2's residual envelope tail: 22 belt particles on the 2:1's inner flank
  (a 3.006–3.148, detune 6–14%, env error > 0.15), pump_B2 1.21–2.08 vs
  pump_ref 1.0–1.3, rate fine (≤ 0.49) — the first-order-in-μ phase-feedback
  defect, unmasked because B's wrong-sign ϖ scramble stopped corrupting it
  (inside the band B2 over-pumps 1.87–2.37 vs B's 1.45–1.93).
- Cadence 0.562–0.601 events/orbit on every seed, B2 = B (same calendar);
  memo hit 0.56–0.64 (binned, on). The no-memo control is now a saved,
  regenerable artifact (run-*-off-B.json); the parent's unsaved 0.106
  regenerates as belt median 0.097–0.099.

Reproduce: `python3 exp2.py --H 24000 --seed S --memo M --law L --out
run-S-M-L.json` (9 combinations in [run.log](run.log)), then
`python3 summarize.py` → `verdict.json`. All < 60 s each.

**Predictions** ([predictions.md](predictions.md), written before the
decisive runs; seen beforehand: the parent's shipped seed and one H=2000 B2
smoke). Held: E1 in full — exclusions per seed (0–1 at C₀), failures
disjoint (≤1 excluded), B loses every tail at every width (p90 ≥ 9.6, ws
≥ 5 vs A 0.67/0), mechanism correlations (ρ(1/e) > 0.5: 0.70–0.90), memo
0.56–0.64. E2: wrong-sign 0 (best of predicted 0–2), rate med ≤ 0.15, p90 ≤
1.2, max ≤ 3, cadence parity, inside-band over-pump 1.87–2.37 (predicted
1.2–2.4) — all held; **the e-envelope clause failed** (0.19–0.37 vs
predicted ≤ 0.05): the flank over-pump was beyond my pre-registered widths,
so the pre-stated rescue criterion fails on env while neither kill criterion
triggers. Disclosed as the run's one honest miss.

**What would make it wrong.** The away-set split uses each particle's
*initial* (a, e): a drifts by ~1e-3 under B/B2, and a guard that re-tested
per conjunction would move a few flank particles; the conclusion does not
turn on it (the failure/rate tables at C₀/2 and 2·C₀ bracket it). The width
anchor C₀ inherits B17's ambiguity (a- vs frequency-normalized) — covered by
the C₀/2…2·C₀ sensitivity, and the envelope verdict needs 4×C₀, far outside
that band. ϖ-rate fits use the same polyfit as the parent (unwrapped ϖ on
every 5th event); a near-zero REF rate can inflate a single relerr — none of
B2's zero wrong-sign or its 0.49 max is a denominator artifact (min
|rate_ref| over the belt 3.96e-5, an order above the tail magnitudes), but
at other horizons it could be. One author wrote REF, B, B2 and the detector:
three derivations, one harness.

**Cost of adoption.** The parent's deletion argument survives only in the
e-vector form: the per-pair conjunction record (already paid by the encounter
tier) carries a kick whose rate beats the orbit-averaged layer everywhere it
applies, dissolving the cadence chooser. What must be built: (1) the e-vector
impulse (a representation change, not a new component — the parent's
(de, dϖ) form is deleted); (2) the resonance guard stays — law.md's
compiled-frequency test, at B17's width, is sufficient for the *rate* but
not for the *envelope* on the 2:1's flank, which needs either phase feedback
(the rotating doll already in law.md for the non-hierarchical three-body
regime) or a flank carve-out that this data prices at 56% of a belt edge-on
to a strong first-order resonance. The binned impulse memo stays dead
(parent's finding; smooth integer form still unbuilt, unmeasured here).

**PRINCIPLES fit.** "A fix signals the wrong representation" (19): the
parent's B was fixing neither — it was *expressed* in the wrong coordinates,
and the 1/e singular Gauss pair (de, dϖ) was the bandaid; the eccentricity
vector is the regular representation of the same event, and it "does the job
like cutting butter" (same quadrature, same calendar, one line). "Look at
the worst cases" / never trust an average where tails decide (20, "How to
work"): the parent's median hid 10–20× wrong-sign errors; the checker was
right, and this run extends the same rule to B2's envelope. "Behaviours
matter, not trajectory identity" (2): judged on precession rates, wrong-sign
counts and e-envelopes against a dense reference.

**The lens may have missed:** the guard-width scan beyond the pre-registered
band is post-hoc (a measurement of adoption cost, not a prediction); the
flank over-pump might shrink at higher quadrature order or under the
second-order term the parent's map drops — untested; multi-planet and
eccentric-perturber scenes, where forced-e geometry moves the flank, are
untouched; and the parent's memo hit-rate claim (0.59 warm) was not
re-examined for B2 keys.
