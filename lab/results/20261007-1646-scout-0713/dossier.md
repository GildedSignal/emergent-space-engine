# Dossier — 20261007-1646-scout-0713 (scout lens: cadence from outside fields)

**Claim (one sentence):** Per-body self-triggered kick cadence — next kick
decided at each kick from the body's own osculating orbit, as in self-triggered
control and Berger–Oliger subcycling — does NOT beat one global fixed cadence
at equal behaviour in this scene family: all three trigger families
(absolute, net-impulse-normalised, path-impulse-normalised) either fail to
transfer across (mu_r, e) or transfer but over-spend 1.4–30x, and the
measured reason is that the behaviour budget is set by phase cancellation
between the kick grid and the perturbation's orbital-frequency structure,
which no orbit-local magnitude bound can see — so the q-cadence rule, if it
exists, must be built on the compiled frequencies (resonance distance), not
on the tide's strength.

## Bottleneck

The board's live question #1: "fewer kicks per orbit at the same behaviour;
kicks dominate the engine's cost". The plane kicks every body at ONE fixed
`2^step_log2` per radial period; the integrator's q-cadence lens asks for a
per-body rule from local dimensionless numbers (gold: 4x fewer total kicks at
equal behaviour). This run hands q-cadence the candidate class with its
transfer behaviour measured, its kill criteria pre-registered, and the
mechanism-level reason the class fails.

## The candidates, and where they are stolen from

- **Self-triggered control** (Heemels et al., "An Introduction to
  Event-triggered and Self-triggered Control", ~2014; existence verified via
  Springer/diva-portal): compute the NEXT sampling instant ahead of time at
  each event — no polling, no tick. The lab's "no work for no reason, so no
  ticks" (principle 14) and "the simulation tells us what's next not us" (22).
- **Lebesgue/level-triggered vs periodic sampling** (Åström & Bernhardsson
  1999, IFAC Proc. Vol. 32, 5006-5011, DOI 10.1016/s1474-6670(17)56852-4;
  existence verified): event-based beats periodic at equal deviation for
  first-order stochastic systems. Their numeric gain does NOT import here —
  UNVERIFIED for our scheme and, per this run's result, structurally
  inapplicable (see below).
- **Berger–Oliger AMR subcycling** (Berger & Oliger 1984, J. Comp. Phys.;
  existence verified): per-unit step from a local error estimator in
  power-of-two ratios — the shape of a per-body `2^step_log2`.

**Mechanism mapped to the law:** at each kick (an event, so cadence changes
only at events, exactly decidable): tabulate the perturbing acceleration
along the UPCOMING osculating orbit — closed form in the eccentric anomaly,
i.e. readable from the compiled cycle's own (E, L) data; choose the next
kick phase from a budget bound; round to the cycle's phase grid. Three
families were tested: bound on sup|a| (A/B), on sup|Delta a| normalised by
the per-orbit NET impulse |int a dt| (ruleRA/ruleRB), and by the per-orbit
PATH impulse int|a| dt (rulePA/rulePB).

## Evidence

`cadence_probe.py` (float probe; Linux x86, 8 vCPU, load 3.2–5.2 — orders of
magnitude only). Scene: planar restricted 3-body, external circular perturber
(the parent's tide: the dominant kick source for belts and moons far from
secondaries). Truth: RK4 at 2048 steps/orbit, convergence 1.1e-5 relative.
Kick model: exact Kepler drift + exact impulse along the arc (8-pt
Gauss–Legendre in E), KDK split — second order, verified (8 -> 64
kicks/orbit: slope error 2.4e-2 -> 2.7e-4, ~88x for 8x). Budget (behaviour,
B14's flavour, fixed before held-out runs): varpi-slope relative error
<= 0.10, |dq|/q <= 0.02, |de| <= 0.01.

Commands (each <= 200 s wall, from this folder):
`python3 cadence_probe.py {selftest,calib,cal,h1,h2,h3,mixed} [eps]` and the
post-hoc sets `{calibr,scener <s>,mixedr}` / `{calibp,scenep <s>,mixedp}`.
Outputs in `out_*.json`, `calibr*.json`. (The pre-registered A/B mixed run
and a first ruleR mixed run were killed by the 240 s command timeout under
load; both families were already dead on the singles, and ruleP's mixed run
completed the record. Reproducibility spot-check: `scenep h2` re-run gives
identical kick counts and verdicts.) Scenes: cal e=0.3 mu=0.05 D=12;
h1 e=0; h2 e=0.7 D=30; h3 e=0.5 mu=0.01; mixed 192 bodies e in
Rayleigh(0.1)+U[0.15,0.7], mu=0.05, D=25, 32 orbits. Each rule family's ONE
constant is calibrated on cal alone (geometric bisection at the budget
boundary); everything else is held out.

**1. The disagreement zone, reproduced and explained (positive result).**
Robust minimal fixed cadence (smallest N that holds, with all larger N
holding): cal 8, h1 1, h2 8, h3 4. The lab's four run disagreements
(4/8/16 across scenes, q-cadence lens) are scene-dependent robust minima,
not noise. NEW: low-N ladders are NON-MONOTONE — the kick grid phase-locks
to the orbit (cal: fixed2 passes at 7.9% while fixed4 fails at 10.6%; h2:
fixed1 passes at 5.9% while fixed2 and fixed4 fail at 34% and 14%). A plane
with one global cadence must sit at the robust minimum of its WORST body
class, and an evaluation that samples a single N per scene can land on a
passing fluke.

**2. Absolute threshold (pre-registered A/B; KILLED).** eps_v = 3.56e-5
(ruleA 5.35, ruleB 6.15 kicks/orbit on cal, budget held). Held out: h2 -> 1.6
kicks/orbit at 33% slope error (FAIL); h3 -> 2.9 at 44% (FAIL); h1 -> 5.5/orbit
when 1 holds (over-spend). An absolute velocity threshold cannot transfer
across mu_r and e because the budget is relative. Trigger quantity, not
trigger machinery, decides transfer.

**3. Scale-free thresholds (post-hoc, labelled; both fail the cut).**
- ruleR (normalise by per-orbit NET impulse |int a dt|; eps=0.161): ruleRB
  holds all four scenes (cal 9.90, h1 29.73, h2 6.15, h3 7.44) — transfer
  FIXED — but over-spends 30x on h1 (the net impulse nearly cancels at e=0,
  shrinking the threshold) and cuts nothing (vs robust fixed: 0.81x, 0.03x,
  1.30x, 0.54x). ruleRA fails h3 (24.7%).
- ruleP (normalise by non-cancelling PATH impulse int|a|dt; eps=0.0422):
  rulePB holds all four (cal 12.40, h1 12.81, h2 10.75, h3 11.67) but never
  cuts (0.65x, 0.08x, 0.74x, 0.34x). rulePA fails h3 marginally (10.3%).
- The pre-registered kill criteria in `predictions.md` fire: mixed-scene cut
  cannot reach 2x when every per-scene cut is <= 1.3x.

**4. Mixed scene (192 bodies, e in Rayleigh(0.1)+U[0.15,0.7], 32 orbits).**
The single global fixed cadence that holds EVERY body is 8/orbit (fixed8
holds 192/192; fixed4 holds 37.5%, fixed2 0%, fixed1 7.8% — the population
scale shows the same non-monotonicity: fixed1 holds MORE bodies than fixed2).
The per-body spread is real (some bodies need 1, others need 8) — the
information a per-body rule could exploit exists. Measured: rulePA holds
192/192 at a mean 7.77 kicks/orbit -> total cut vs global fixed 8: **1.03x**
(no cut); rulePB holds 192/192 at 12.25 -> **0.65x** (worse than fixed).
The pre-registered kill criterion (< 2x) fires; P12 confirmed.

**Why the class fails (mechanism, not anecdote).** A sufficient orbit-local
bound (sup|a| or sup|Delta a| times dt^2/2 vs any per-orbit normaliser)
prices each interval by the perturbation's MAGNITUDE, but the budget-relevant
error is dominated by PHASE CANCELLATION between the kick grid and the
perturbation's orbital-frequency structure — the same structure the
non-monotone fixed ladders expose directly (fixed1 and fixed2 can beat
fixed4). A bound that cannot see phase can only be conservative, and the
measured conservatism is 1.4–30x — more than the 2–4x a per-body rule could
have won. Consequence for the lens: the rule q-cadence looks for must
predict WHERE THE GRID LOCKS, from the compiled frequencies (its own list
already names the quantity: "the distance to the nearest resonance"), not
from the tide's strength. The imported forms (event-decided, integer,
power-of-two, changed only at events) remain sound; the imported GAIN does
not exist here.

## Predictions

`predictions.md`, all written before each family's held-out runs. What
happened: P1 violated in the informative direction (over-spend, not
failure); P2's ruleA-fails-on-h2 did not materialise — both rules failed h2
AND h3; P3 failed with ruleB (44% on h3); P7-P9 (ruleR) partially held
(transfer yes, cut no — P9's kill fired); P11-P12 (ruleP) as written — P12's kill confirmed by the mixed run (1.03x).
Sequencing disclosure: Addendum 2 (ruleP) was written after ruleP's SINGLE
scenes had run but before its mixed run; the mixed command had been launched
about a minute before the addendum landed. P12's content was already forced
by the singles, but the checker should weigh that.

## What would make it wrong

- The probe is float, 2D, one perturber class (smooth external tide). A
  different perturbation (secondaries' 1/r^2 kicks, encounters) could have
  MORE magnitude-correlated error, where a self-triggered bound would cut;
  that is a different experiment. Resonance bands (no cadence works,
  20261003-0520-dynamics-a9c2) are out of scope.
- Kick evaluation is idealised (exact impulse along the arc). The real
  rebinding cost (~24 us median, opus-math memo) is per kick, so a rule that
  adds kicks (rulePB) would be even worse in the plane than here.
- The budget line is this probe's own (B14-flavoured); B12/B14/B17 as frozen
  may sit elsewhere. The negative claim is about the RULE CLASS against
  magnitude-style bounds, not about any specific gate.

## Cost of adoption, and fit with PRINCIPLES

Nothing to adopt as a cadence rule — the deliverable is the kill plus the
mechanism. What IS adoptable: (a) the non-monotonicity warning for every
cadence evaluation (sample several N, judge the robust minimum, never a
single N); (b) the pointer that the cadence selector must key on compiled
frequencies (resonance distance), matching the lens's own variable list.
Fit: "A failed experiment kills that configuration, never the method" (9);
"a test that cannot fail is a control" (the fixed ladders and the e=0 scene
were the controls, and they are what failed the rules); "the right question,
then the representation" (18) — the right quantity is phase structure, not
magnitude.

## The lens

Scout's blind spot bit exactly where warned: "the literature optimizes for
its own requirements, which are not ours." Åström's Lebesgue gain presumes
the trigger sees the controlled quantity; our controlled quantity (relative
apsidal drift over many orbits) is not the bounded quantity (instantaneous
deviation), and that gap is the whole result. What the lens nearly missed:
the positive by-product (non-monotone ladders / phase locking) came from the
CONTROLS, not the candidates.
