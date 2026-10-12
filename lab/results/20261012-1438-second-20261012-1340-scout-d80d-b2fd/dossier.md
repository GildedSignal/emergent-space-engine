# Dossier — second-author run 20261012-1438 (on 20261012-1340-scout-d80d, silver)

**Claim.** The checker's named experiment is done in its cheapest decisive
form, and it splits the original claim in two: the twin-rate framing
**does** predict the engine's sealed-scar *memory* (held-out first-half fit
→ retained stock: 96–98% of totals, 91–92% of bodies exact, Spearman 0.82),
but it **does not** predict event-based scar *traffic* (λ and log-model
predictions miss by 80–4·10⁵×; gross crossings exceed retained levels 203:1,
98% of them reabsorbed), and the original headline "99.9% regenerable" is a
horizon artifact that hides a **departed class** — 1.8% of the belt
permanently off its program at ~40 bits each — so the honest engine measure
is three per-body numbers (envelope bits, λ/wander spectrum, departed flag),
not one rate class; forced memory at weak drive is 0.76 bits/body, 67× under
the 51-bit ceiling.

## Bottleneck

Same as the parent run: H_live, the distinctions-per-game-second that decide
whether 10⁹ bodies fit in 8 GB. The parent defined the measure; this run
cross-validates it against the engine's own event semantics (shipmem
`shelf.rs`: events → hot tier, `compact` seals exact deltas from the packed
base, a body back at base is reabsorbed) — exactly the divergence the parent
dossier named as its last risk and the checker named as the one experiment
to gold.
All from one decisive run: same belt and ICs as the shipped record
(`bodies_match_A005: true`; belt seed 20261012, phase stream identical),
T = 3·10⁴ periods (3× the shipped horizon), A = 0.05, free twin at 64
quadratic checkpoints, plus scar twins scanned once per period at correction
quanta b* = 8 and 16 bits, counts split at the half. Scripts:
`work/second.py` (instrument), `work/analyze2.py` (all numbers below),
`work/diag.py` (fine-cadence reabsorption check), `work/analyze.py`
(first-pass, kept as the record of S4-as-written).

Reproduce (Linux x86, shared 8-vCPU box; orders of magnitude only):

```
cd lab/results/20261012-1438-second-20261012-1340-scout-d80d-b2fd/work
python3 hlive.py 10000 0.05 d A005repro    # shipped record regenerates: 44 s,
                                           # differs only in tag + wall_s
python3 second.py 30000 0.05 T3e4          # decisive run: 173 s (over the 60 s
                                           # preference; the horizon claim needs
                                           # 3x the shipped horizon)
python3 analyze2.py                        # ~4 s, prints/writes everything below
python3 diag.py                            # ~23 s, reabsorption evidence
```

## Evidence


1. **Record regeneration (independently re-verified).** summary-A005repro
   identical to summary-A005 in every field except `wall_s`; per-body npz
   bit-identical. Matches the checker's bit-for-bit result.

2. **Horizon ladder — the checker's missed point 1, confirmed.** Same
   bodies, shipped gates on windows [T_h/16, T_h]: chaotic fraction
   0.81% (33) at 10³ → 0.20% (8) at 3·10³ → 0.098% (4, exactly the shipped
   run's four) at 10⁴ → 0.024–0.05% (1–2) at 3·10⁴; 33 of the 33 reclassify.
   The rate-class label is horizon-dependent, as the checker said.

3. **The departed class — new, and it corrects the headline.** 75 bodies
   (1.83%) end at 35–42 bits with flat curves: their twins completed a
   finite-time macrostate departure (separatrix-side ambiguity of the birth
   quantum), after which the slope gates call them regular forever. The
   histogram is bimodal with an empty 30–35 gap, so the class is clean, not
   a threshold artifact. 72% have D < 1 (belt: 6.8%), max D 1.19; of the
   shipped run's 4 chaotic, 2 survive as sticky and 2 become departed.
   Total unpredictable set at 3·10⁴: 77/4096 = 1.9%, not 0.1% — the
   original headline undercounted the memory-relevant population ~19×.

4. **Retained-memory cross-validation (the adoption claim, held-out).**
   Engine sealed-scar stock per body = envelope bits ÷ quantum (net levels;
   equivalence witnessed at period cadence in `diag.py`: up−down = 1 per
   level for all 24 diagnostic bodies). Predicted from first-half log-fits
   only: b*=8 totals 8087 vs 8243 actual (98%), 91.3% of bodies exact,
   ρ = 0.820; b*=16: 3862 vs 4018 (96%), 92.1% exact, ρ = 0.820.

5. **Traffic — where the framings diverge, as named.** Gross crossings at
   b*=8: 1.77·10⁶ over 3·10⁴ periods; 98.0% from the shear class, whose
   gross:net ratio is 203:1 — nearly every body (4017/4021) crosses
   constantly while retaining 2 levels. Traffic is non-stationary
   (h2/h1 = 2.0, first-half rates under-predict), and even for the two
   sticky bodies λ under-predicts traffic ~80× (body 68: 389 actual vs 4.7
   predicted): sustained traffic is set by wander frequency across the
   quantum, not by λ; λ governs only when retained levels increment.

6. **Budget.** Forced memory (departed + sticky envelopes) = 3123 bits =
   0.76 bits/body — 67× under the 51 bits/body ceiling. The shear bulk's
   20.4 bits/body envelope is regenerable by running the law (compute, not
   store) — the allocator's actual decision, worth 27× the forced stock.
   The allocator-relevant tail, replacing the estimator the parent
   discredited: 1.9% of bodies carry 100% of forced memory.

7. **Record corrections (checker points 2, 4, 5).** λ range at 10⁴ was
   0.00083–0.00181 nats/period (Lyapunov 553–1204 periods), not 553–831;
   the boundary body (idx 647, 41.85 bits at 10⁴) is *departed*, not a
   fifth chaotic (41.34 bits at 3·10⁴, flat); "D < 0.74" should read 0.7447
   for the sticky set and D ≤ 1.19 once the departed class is counted.

## Predictions (see predictions.md)

S1 confirmed (33→1 across the ladder, 33 reclassified). S2 split: the
log-floor exists (median second-half slope 1.59·10⁻⁴ bits/period vs own-fit
floor 1.24·10⁻⁴) but 16% of shear bodies run above 3× their own floor —
super-log beat growth; the hidden-band bound must use the measured slope
distribution, and at the measured floor, 10⁶ periods would accumulate ~124
bits, so a λ ~ 10⁻⁵ population stays invisible at this horizon (the
checker's number, now measured, not literature memory). S3 failed in letter
and resolved better: not saturated, departed. S4 **failed as written**
(ρ = 0.17, totals off up to 4·10⁵×) — the pre-registered kill criterion
fired for *traffic*; the corrected retained-memory variant (item 4) passes.
S5 half: shear ratio 31.9 (≥30 ✓), sticky ratio 17.6 (≤4 ✗). S6 confirmed
(forced share 0.04% ≪ 1%).

## What would make it wrong

The retained equivalence (net crossings = envelope/quantum) is witnessed at
period cadence on 24 bodies, not all 4096; a scan blind to sub-period dips
would undercount traffic. The departed class is measured at one drive and
one horizon: its feeding rate from the D < 1 zone (0.9% per decade of time
here) decides forced memory at game horizons, and I did not measure it at
10⁵+. The λ ~ 10⁻⁵ band remains invisible (T = 3·10⁴; the floor itself is
measured, not the band). Shipmem's real codec quantizes per-coordinate, not
as a single phase-space scalar b*; a per-coordinate quantum changes the
level arithmetic by O(1) factors, not the 203:1 or the three-class split.
One belt seed (index alignment was the point); the checker already ran seed
777 adversarially on the parent.

## Cost of adoption, and fit

Cheap: no engine change. What b-h-live should measure falls out directly —
per body: envelope bits (retained stock, reabsorbable against recompute),
λ/wander spectrum (re-check cadence), departed flag (permanent scar). The
event counter alone would mislead: it sees 203× the memory and calls the
whole belt active. PRINCIPLES: "Store the generator, not the generated" (6)
— the departed flag is exactly the generator's failure boundary;
"Compute only surprises" (3) — gross crossings are not surprises, net
levels are; "the memory floor is information" (24) — the floor is the
retained spectrum (0.76 forced bits/body here), not 157 and not the traffic.

## The lens (what the second-author lens may have missed)

I ran the cross-validation inside the parent's local form, not on the
plane's scene with shipmem wired end-to-end — the checker's full ask; the
203:1 and the three-class split should be re-measured there before the
numbers are load-bearing, though the mechanism (area-preserving beats,
separatrix-side ambiguity) is representation-independent. The horizon
ladder's gate-window sensitivity flips 1–2 bodies at the 3·10⁴ edge
(full-window classify: 2 chaotic, windowed: 1); disclosed, immaterial at
the reported precisions. Fine-cadence diagnostics sampled 24 bodies chosen
by class, not at random.

**Grade sought: silver-or-gold for the integrator to judge** — the named
experiment's decisive part is done, the parent's claim is corrected rather
than refuted (memory: predicted; traffic: divergent, 203:1; headline:
1.9% not 0.1%), and every number regenerates from the shipped scripts.
