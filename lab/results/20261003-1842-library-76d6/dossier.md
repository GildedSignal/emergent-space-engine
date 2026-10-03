# dossier.md — 20261003-1842-library-76d6 (library lens)

READWISE_TOKEN is **unset** in this container; Gutenberg/archive.org fetches failed,
so the book list plus knowledge was used and **every quote below is UNVERIFIED**.

## Claim
Measured on the engine's own cost structure (exact compiled drift, kicks the only
cost), higher-order splits need **more** kicks per orbit than plain symmetric
leapfrog at the same behaviour — Forest–Ruth 2.25×, Yoshida-6 1.75× — so the
board's "higher-order splits" candidate for fewer kicks is falsified; the lever is
correctors that add zero kicks, not compositions that multiply them.

## Bottleneck
Focus item 1 ("fewer kicks per orbit at the same behaviour"; H0211 "the bigger
lever is fewer kicks", queued `q-correctors`). Expected gain from killing the
candidate: one branch of the queue dies before anyone builds it (a whole builder
window saved); expected gain from the redirect: the kick budget of H0190's 32
kicks/orbit drops to 8 at e≤0.1 at identical behaviour — a 4× cut of the engine's
dominant cost — by using the *measured* smallest integer, not an order-of-integrator
rule of thumb.

## Evidence
Wisdom–Holman probe: exact Kepler drift + J2 impulse kicks, equatorial orbit,
200 orbits, oracle Δϖ/orbit = 3π·J2·(R/p)². Pass band: precession rel error ≤ 1%
and |Δe| ≤ 1e-4. Controls: positive y6@896 kicks/orbit matches oracle to 1e-4;
negative lf2@4 fails (12.5%). Minimal kicks/orbit in band, compared at **equal
kick counts** (composition multiplies kicks per step: y4 ×3, y6 ×7):

| case | lf2 | y4 | y6 |
|---|---|---|---|
| e=0.1, J2=1e-3 | **8** | 18 | 14 |
| e=0.6, J2=1e-3 (held out) | **32** | 72 | 56 |
| e=0.1, J2=1e-2 (held out) | **8** | 18 | 14 |

Energy error bounded (no walk) everywhere, including y4's negative substep: the
exact drift makes backward steps free and reversible. Reproduce:
`cd lab/results/20261003-1842-library-76d6 && python3 kicks.py` (44 s, numpy).
Order-independence across perturbation strength (P3) held. Lesson: composition
buys order in (nh), but its price is more force evaluations — profitable only when
the force is expensive; here the drift is free and the kick is the unit of cost,
so the trade inverts. That is why Forest–Ruth (stolen from beam physics, where
every force evaluation costs a field solve) does not transfer (principle 26, with
its caveat in plain view). My first oracle was 2× wrong (Vallado's 6π form vs the
central-force 3π); the numerics caught it before any claim — measure before claiming.

## Predictions (predictions.md, written first)
P1 falsified (predicted y4/y6 at ≥4× fewer; measured 2.25×/1.75× *more*).
P2 falsified in direction (predicted y4 ≥2× fewer at e=0.6; measured 2.25× more;
"y6 falls below y4" held). P3, P4, P5 held. The honest summary: my integrator
intuition was wrong about this cost structure; the experiment did its job.

## What would make it wrong
A regime where the outer step must resolve a fast angle and the error is *not*
pericenter-dominated (near-resonance is already killed separately, r4); or if
kicks were cheaper than drifts (not our engine: drift is a compiled lookup).
Cheapest adversarial test: rerun with a neighbour's tide (r9's regime) and with
the SyMBA changeover active. Adoption cost: negative — delete a candidate, keep
the engine as is; the numbers table is directly adoptable as compiled per-class
kick counts (8 and 32, integers, per principle "floats may explore; only integers
decide"). Fit: "the simulation tells us what's next not us" (principle 22); "a
failed experiment kills that configuration, never the method" (9); "measure
before claiming" (10).

## The lens
Analogies are cheap and quotes are unverified; the mechanism evidence is numerical,
not textual. The library lens reads practitioners' *cost structures*, and the one
measured here is the engine's, not theirs. A likely miss: real symplectic
correctors (Wisdom / Laskar–Robutel near-identity pre/post transforms, zero extra
kicks) were argued for but not measured — that experiment, not this one, is the
gold candidate.

## The 5 lessons (each: quote UNVERIFIED · mechanism · change · cheapest test)

1. **Poincaré, *Science and Method*** — "It is by logic that we prove, but by
   intuition that we discover." Mechanism: composition buys order in (nh), paid in
   force evaluations; profitable only when force is the expensive operator (beam
   physics), harmful when the drift is free and the kick is the cost. Change:
   strike "higher-order splits" from bottleneck 1's candidate list (measured 1.75–
   2.25× penalty, table above). Test: done, `kicks.py`; rerun with a neighbour tide.
2. **Gauss (Dunnington, *Titan of Science*)** — Ceres: he predicted where to look
   from a fitted theory, not a finer integrator. Mechanism: corrections as a *fit*
   on residuals — near-identity corrector applied once per window, zero extra
   kicks (Wisdom/Laskar–Robutel correctors). Change: aim `q-correctors` at zero-
   kick correctors only. Test: same probe + one pre/post transform, same band,
   count unchanged kicks: pass at 8→2 per orbit?
3. **Gordon, *Structures*** — load follows definite paths; material sits on the
   path, not spread evenly. Mechanism: kick density should follow the tide's
   phase gradient (pericenter), a compiled palindromic phase grid, not uniform
   time. Change: candidate per-body kick grid from e. Test: my `kicks-grid.py`
   probe was inconclusive (drifts e; script left); redo in the engine's own KDK.
4. **Simon, *Models of My Life*** — satisficing: stop at the first integer that
   passes, not the smallest error. Mechanism: the pass-band integer (8, 32) is a
   behaviour-gate property, not an accuracy property; energy residual can look
   fine while behaviour is wrong (r4 v2). Change: store the per-class kick count
   in the population program (shipmem) as compiled integers. Test: adopt the
   table, run B7–B14 unchanged.
5. **Kelly Johnson, *Kelly: More Than My Share of It All*** — simplicity so the
   shop can build it. Mechanism: a kick costs 29 µs, 15 in rebinding; any new
   corrector must ride the existing kick event, not add a second event type.
   Change: constraint on `q-correctors` designs. Test: gate = kick-cost per orbit
   unchanged or lower in `xtask universe --bench`.
