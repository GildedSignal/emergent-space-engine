# Dossier — redteam e07f: the Binet ISCO strip

**Claim.** The Binet cell's frozen band coefficient makes orbital stability a property of
the *band*, not of the *body*, so the design's innermost stable orbit is a cliff displaced
by up to a full band — with rung r1's frozen convention a strip of orbits **inside the true
ISCO is wrongly stable, so a ship parks at r = 5.95 M forever while exact GR plunges it in
8.8 orbits** — and r1's frozen ISCO criterion cannot see any of it.

**Bottleneck.** Bottleneck 0 (the representation), aimed at r1's scheduled clean re-run
(H0205: DISPUTED, "needs a clean PASS"). Not a speed gain: it stops a blind gate from
certifying a law whose headline GR behaviour (the ISCO, the thing a player goes to a black
hole to feel) is wrong by construction at the rim. It deletes the design's "the innermost
stable orbit… and plunges all emerge" as written: they emerge at the wrong radius, as a
cliff, with a phantom stable shelf.

## Evidence (float64, M = 1; oracle = the same Binet equation r1 freezes, un-frozen:
u″ + u = 1/h² + 3Mu²; circular h² = r²/(r−3))

`cd lab/results/20261010-1706-redteam-e07f && python3 binet_isco.py` (3.5 s),
`python3 addendum.py` (8.9 s). Both scripts and raw outputs are in this folder.

- **The strip.** r1's frozen convention (u_k at the band's geometric centre, rings
  2^(k/16)): the band containing 6M is [5.9073, 6.1688); its centre 6.034 makes
  1 − 6u_k > 0, so stability holds for the whole band. Misclassified set:
  **r ∈ [5.9073, 6.000), width 0.093 M = 1.54% of 6M, one-sided (effective ISCO
  5.9073, −1.54%)**. Inner-edge convention: r ∈ [6.000, 6.1688), **+2.81%**, one-sided
  the other way. Every fixed per-band convention has a wrong strip, up to one band wide,
  glued to 6M.
- **The falsifier (player-visible wrong outcome).** Near-circular orbit at r = 5.95,
  10⁻³ radial perturbation: exact Binet **plunges at φ = 55.2 (8.8 orbits)**; the band
  model (m = 16 *and* m = 32, r1's convention) **stays bound to φ = 400 with periapsis
  5.944 and zero ring crossings — the cycle memo holds it at cost ≈ 0 forever**. A fleet
  parked inside the ISCO is the cheapest physics in the design and it is not GR.
- **The mirror is milder than predicted.** Under the inner-edge convention at r = 6.05
  (truly stable) the wrongly-unstable band does not plunge the orbit: its hyperbolic
  fixed point lies below the band, so the orbit is ejected upward and oscillates
  r ∈ [6.04, 6.27]: same outcome, **apoapsis pumped +3.5%, periapses forbidden in the
  strip** (a periapsis hole).
- **The staircase.** In-band radial frequency √(1−6u_k): max error vs √(1−6/r) over
  (6.17, 7.0) is **31.5%** (at 6.172); the adjacent-band jump near 6.17 is
  **0.078 → 0.220 = 181.8%**. True ω_r at 6.05 is 0.0909; the first stable band gives
  0.2196 (2.4×). The smooth GR approach ω_r → 0 — the feel of the rim — is a cliff.
- **Refinement does not cure it.** Strips for m = 16/32/64/128 (below/above 6M):
  0.093/0.169, 0.093/0.037, 0.028/0.037, 0.028/0.004. Width is a dyadic-phase lottery
  (where 6M falls inside its band), never zero, worst case a full band at every m.
- **Identical black holes disagree.** Doll ring phase r₀ = 1.3 moves the strip to
  [5.9217, 6.0): two identical dolls give different effective ISCOs (5.9073 vs 5.9217).
- **The gate is blind.** r1's `isco` criterion probes L at r = 7 and r = 5.5 (±10%);
  both classify correctly under *both* conventions (measured), and the bound-seed sampler
  draws p ≥ 6.5 + 2e, so no seed sits in the strip. `isco_correct` = 1 while the strip is
  wrong. `shape` cannot catch it either (the phantom shelf keeps its shape perfectly).

## Predictions (predictions.md, written before the run)

Held: the strip and its one-sidedness both conventions (1, 2); the plunge-vs-park
falsifier at 5.95 (3, first half — exact plunged even faster than predicted); doll-phase
shift (5); r1 blindness (6, exactly); the staircase (7: 31.5% error, 181.8% jump against
predicted >10%/>25%); the Doppler factors (8). **Not held:** the mirror case (3, second
half) — the edge-convention band ejects a stable 6.05-orbit upward instead of plunging it
(outcome right, apoapsis +3.5%); and m = 32 does not leave the strip unchanged (4) — it
flips to the other side of 6M and shrinks to 0.037, confirming the dyadic-phase mechanism
but not the phase I derived by hand.

## Ranked attacks (the lens deliverable)

1. **Binet ISCO strip** (above). Criterion that should have caught it: r1 `isco` — it
   exists and is blind. Proposed addition before the clean re-run: near-circular sweep
   across the band containing 6M ± 1 band, plunge iff r < 6 against the oracle; and
   max adjacent-band jump of the radial frequency < 5%. Unmeasured here: whether the same
   strip shifts the photon-capture b-threshold (r1's ±3% cases); H0205's capture pass
   suggests the integrated threshold is less sensitive than the local sign.
2. **The view's cost premise breaks exactly at the game's headline.** §6 books the view
   flat: "≤ 1 sample per pixel per frame, GPU". But gathering at the past light cone of a
   kicked body needs its tube *version* valid at t_ret (a post-kick cycle extended
   backwards is a counterfactual orbit, not the history), and at β → 1 the cone sweeps
   the sources' histories k× faster than proper time: k = 1/(γ(1−β)) = 4.4 at β = 0.9,
   **14.1 at 0.99, 44.7 at 0.999**. Per-frame gather work per visible body is
   k × frame × kick-rate, not 1 (a combat body kicked 100/s viewed approaching at
   β = 0.99: ~23 tube versions per frame). Retention: the design's own 6×10⁴ kicks/s
   × 24 B ≈ 1.4 MB/s ≈ 5 GB per hour of universe time on the 8 GB target — eviction
   without checkpoints rewrites distant history retroactively; with checkpoints the
   gather pays replay. **No rung exists: §7 names r6 (view) but `lab/rungs/` has no r6.**
3. **Dense/sparse bit-identity has no frozen gate and one unstated requirement.** Kicks
   are exact integers (r2), so they commute; but contact resolution (quadratic +
   rounding carry) does not. Two causally *unordered* events touching the same body must
   be serialized identically by the slack queue and the dense scan, or bits differ. The
   design never states the same-body serialization rule. **§7 names r5; `lab/rungs/` has
   no r5.** Proposed criterion: one body, two unordered events (one contact, one kick),
   both orders, bits must be equal.
4. **"A kick updates the cycle by a multiply-add" diverges where players go.** Cycle
   derivatives blow up at the rim (∂ω_r/∂r = 0.45 at r = 6.05 vs 0.066 at r = 8: 7×)
   and at the parabolic separatrix (cycle length → ∞). Near either, the linear response
   is wrong and the cycle must be recompiled — a cost cliff, and a correctness bug if the
   multiply-add is applied blindly. No criterion covers kick-response validity (`repeat`
   only checks repetition).
5. **Two-body doll (premise 1) survives as scoped.** ν only in the energy map is exact
   at 1PN (textbook EOB; r3 v3 confirmed, 64/64 assists). Boundary: at 2PN ν enters the
   potential, so comparable-mass binaries (ν ≈ 0.25) mis-phase near merger — worth one
   frozen case if binary black holes ever become content.
6. **"Undisturbed orbits cost ≈ 0" survives** — via the cycle memo (H0205: ~38
   crossings/cycle, then memoized; ≤ 512 gate). Premise 2's "orbits repeat per cycle"
   also survived r1's exact-repetition check. The survivor has teeth: it is exactly what
   makes attack 1 free — the phantom shelf costs nothing, forever.

## What would make it wrong

The shipped law using per-body u (then the in-band equation is not a rotation, and the
design's own text and r1's frozen spec both say otherwise); or ISCO-adjacent play being
out of scope (it contradicts the goal: "lets the player feel what living at high c would
feel like" — the rim is the ride); or the oracle being mis-derived — it is the equation
r1 itself freezes (r1 line 10), so any checker re-derives it in minutes.

## Cost of adoption, and fit

Addition to r1's case list (a sweep and a staircase bound) before the clean re-run — a
strengthening, never a weakening. The representation fix is open and is the integrator's
call; per-band refinement provably cannot remove the cliff (the m-sweep above), and
special-casing the ISCO band would be principle 19's bandaid ("if you find yourself
fixing things that's oftentimes a signal that it is the wrong representation"). Principle
2 cuts the other way: "Behaviours matter… error *type* over error size" — park-forever
inside the ISCO is a wrong outcome class, not a rounding tail; principle 10's simplest
falsifier found it in 3 s of Python.

## The lens

A premise red-team overweights the exotic: I rank the ISCO strip first because the rim is
marquee content, but most play happens far from any horizon, where Binet cells are
excellent (H0205: 1% precession, exact repetition) and attack 2 (view cost at high c) may
cost more player-minutes than attack 1. I falsified the analytic premise in float64, not
the shipped integer/Minsky law — the checker should re-confirm the strip with the integer
map before the finding gates anything.
