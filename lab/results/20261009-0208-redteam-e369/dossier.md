# Dossier — 20261009-0208-redteam-e369 (premise red-team)

**Claim.** The fleet doll's Clohessy–Wiltshire closed form (representation.md §1)
is a law for a fraction of one parent orbit, not a session: model-vs-truth
error is 7.7× a member's own offset after one period even on a circular
parent, worse by ~e^1.3–1.5 on the belt's eccentric orbits, and grows
without saturation — so quiet (coasting, unthrusted) members cannot live in
it, and the "undisturbed ≈ 0" cost row fails inside fleet dolls; they must be
parent-doll tubes, leaving the CW frame to the interacting core only.

**Bottleneck.** Board focus item "fitting 10⁹ in 8 GB" / the cost table's
first row ("undisturbed orbits ≈ 0"): the gain at stake is the difference
between 0 true-state evaluations per member per orbit (tube) and O(10–10³)
(CW re-anchoring). It deletes a representation (the fleet doll as a home for
quiet members), it does not add one.

## Evidence

Float, single thread, 10.7 s wall on the shared 8-vCPU Linux runner (load
~1/8 during the run). Truth = exact star-only two-body RK4 (converged:
half-step run identical to 4 decimals); parent = analytic Keplerian marker;
model = the standard CW closed form with the mean motion, verified against a
numerical CW integration to 4×10⁻¹²·a over 100 periods. Member offset
a/R = 0.01 (the doc's own scale, H0203's dr/R). Error = |CW − truth|/a in
the parent's rotating frame, identical physical initial states for model and
truth (the "rest" family; the "ellipse" family additionally reported but its
e > 0 numbers are IC-conditioned — the closed form has no eccentric-parent
periodic solution to initialize from, which is itself part of the finding).

| case (rest) | 1 P | 2 P | 10 P | 100 P | law |
|---|---|---|---|---|---|
| e=0.0 | 7.7a | 29a | 473a | 3818a | ~38a/period linear at long range |
| e=0.1 | 23a | 59a | 494a | 3855a | |
| e=0.3 | 91a | 161a | 377a | 3863a | |
| e=0.7 | 430a | 504a | 615a | 3847a | error(1P) excess ∝ e^1.3–1.5 |

The matched formation (CW ellipse, e=0): error 0.091a per period, exactly
3π(a/R)·a, linear — 9.1a after 100 periods. The one-period circular number
7.7× is H0203's number, reproduced; what H0203 did not measure is that it is
the first step of an unbounded linear drift, and that eccentricity (the
belt's Rayleigh-e norm, B18b) multiplies it by 3–56× within one period.

Consequence: holding a quiet member to its own offset inside a CW doll costs
~13 re-anchors per orbit (e=0, rest), ~90+ (e=0.3) — each a full true-state
evaluation, i.e. the integration cost the doll existed to delete. The doc's
hedges do not cover it: "re-anchor to the frame at events" fails for quiet
members (no events — that is what quiet means), and "carry the quadratic
term" is sized for the circular second-order drift; at e > 0 the linearized
law is Tschauner–Hempel, which has no closed form to carry.

Reproduce: `python3 lab/results/20261009-0208-redteam-e369/falsifier_cw.py`
(≈11 s; writes the same JSON to stdout as `run-output.json`).

## Predictions

`predictions.md` was rewritten before any run of the experiment (the first
draft's with-planet cases were dropped as out of scope — a member inside a
real planet's Hill sphere is a planet-doll member, not a fleet-doll member).
What happened:
- **P1 FAILED** (the useful failure): I predicted the circular case stays
  under 10⁻²·a over 100 periods; measured 9.1a (ellipse) and 3818a (rest).
  The second-order drift is linear in time, not a bounded ripple.
- **P2 HELD**: e=0.3 exceeds a within ≤10 periods (91a after 1); e=0.7 within
  ≤3 (430a after 1).
- **P3 HALF-HELD**: circular does not need "≥500 periods" (measured: ~13
  re-anchors/orbit to stay within a); e=0.3 needs far more than 1/orbit —
  sub-period cadence, as predicted in shape.
- **P4 HELD**: closed form vs numerical CW 4×10⁻¹²; step halving identical;
  the e=0 "instrument" check is the finding itself, not instrument error.
- **P5 did not trigger**: the premise did not survive.

## What would make it wrong

A member whose offset is far smaller (a/R = 10⁻⁴) pushes the drift down
linearly in a/R (the 3π(a/R)·a law), so dolls that only ever span tight
formations suffer proportionally less; and a design that re-anchors every
member each parent period bounds the error at ~a regardless. Both rescues
concede the claim: the closed form is not the law of the doll between
anchors. The truth model omits the planet's own gravity (a real fleet doll
near a planet has strictly more error, not less), and it omits mutual
gravity between members (same direction).

## Cost of adopting

One sentence in representation.md §1 plus the rung: the CW frame is scoped to
the interacting core (the same dimensionless selector §3 already uses for the
dense order: events per cell per light-crossing ≈ 1); quiet members are
parent-doll tubes (already the live path — the co-orbital certificate of the
6 October gold). No new component; it deletes a use of an existing one.

## Fit with PRINCIPLES

- 13 ("errors never compound… divergence is not a joke and it compounds"):
  the CW drift is linear-in-time divergence, the exact type the law forbids.
- 33 ("a raindrop is an event for an ant and nothing for a lion"): the fix is
  the same principle — the doll resolves only interactions; quiet members
  belong to the parent's scale.
- 19 ("if you find yourself fixing things that's oftentimes a signal that it
  is the wrong representation"): re-anchoring cadences are the bandaid; the
  tube is the boat.

## Ranked attacks (the lens deliverable)

1. **Fleet-doll CW closed form (§1)** — run above; player-visible as fleets,
   convoys and debris coasting through a system for an hour. **No rung
   catches it**: r5 as planned ("a Clohessy–Wiltshire frame with lattice
   contacts") judges bit-identity, not drift, over short horizons; H0203
   stopped at one period; r9 killed tori; m-meso covers encounters only.
   r5 needs a drift criterion: model-vs-restricted-3-body error versus
   periods, positive control a parent-doll tube, negative control the closed
   form.
2. **Kick→cycle multiply-add near the separatrix** (§3): ∂²Δφ/∂E² diverges as
   e→1 and at the ISCO, so certificate lifetimes collapse exactly where the
   belt's Rayleigh tail lives; B12 (the stability judge) is miscalibrated
   and q-cadence is queued — nothing currently measures the recompile rate.
   Not run here.
3. **Dense/sparse bit-identity (§3)**: designed for (anchored block steps,
   canonical tie batches, integer kicks, gate B8) but untested — r5 does not
   exist and root-clock event keys are step 4, unbuilt. The missing rung is
   the finding; a test scene must include the kick/carry interleave, not
   contacts only.
4. **View gather (§2)**: survives analysis — the retarded-time function is
   monotone (unique crossing), point-mass image branches never appear or
   vanish, −p·u is exact for stationary fields, and moving lenses are
   already B16. Residual: Newton-seed cost at extreme β is unmeasured; r6
   does not exist.
5. **Two-body doll at 1PN (§1)**: survived r3 v3 (precession 1024/1024,
   assists 64/64); close binaries route to the dense order by design. No
   fresh attack available cheaper than r3's.
6. **Binet cells (§1)**: survived r1 (m ≥ 16; the in-band map was replaced by
   the Darwin compilation after a first-order slope error at turning points);
   ~38 crossings per cycle against 350–700 fixed steps. Survives.
7. **The cost table's "≈ 0" row (§6)**: holds for tubes, fails inside CW
   dolls (attack 1); H_live, the real decider for 10⁹ in 8 GB, is still
   unmeasured (known risk on the board).

## The lens

A premise red-team overweights long-horizon drift and underweights what the
player sees in the first minute (arrival, combat feel) — those live in the
view and contacts, which I judged by analysis rather than probes. The
eccentric-ellipse numbers are IC-conditioned (disclosed above); only the
rest-family numbers are clean model error. AI decisions (the cost table's
largest unknown row) are off-plan by Julien's decision and were not attacked.
