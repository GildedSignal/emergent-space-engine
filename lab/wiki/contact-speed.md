topic: contact-speed
status: open
closed-by:
valid-while:
updated: 20261015-0358-redteam-8144

# The contact law's speed domain: which detected contacts exchange an impulse

## Current best

**The skip is solved in closed form, and it is a threshold in speed, not a tail: a detected
contact exchanges nothing iff its closest approach falls inside its detection chronon
(skip ⟺ τ\* ≤ 1, measured 294/294 arms, 0 misses), so a pair ghosts when its closing speed
exceeds its effective contact depth per chronon — v\* = reach/1477 m in units of c on the
fleet lattice, and every ship-scale contact above a few 10⁻³–10⁻² c closing passes through
(20261015-0358-redteam-8144).** Driven on the shipped reference stepper (`Chronon`,
`Law::RelativisticV1`, Q = 2²⁰): the skip probability at fixed ρ = reach/|w| is
max(0, 1−ρ) over arrival phase; the boundary is scale-invariant (reach 7–709 quanta, |w|
2–9.4×10⁵ quanta/chronon, closing β to 0.9 — checker2 corrected from the dossier's
1.9×10⁶, which no measured arm reaches); the gate is the batch convention, not a v1
artifact (the Newtonian resolver has it too, `law.rs:598` beside `relativity.rs:236`); the consumed
bookkeeping never re-fires a skipped pair (no exchange in 300 later chronons). Thresholds:
1 m reach → 6.8×10⁻⁴ c; 10 m → 6.8×10⁻³ c; the design's 0.5 m missile vs a 50 m ship →
3.4×10⁻² c (at its design speed it never collides); 100 m → 6.8×10⁻² c; 1 km → 0.68 c.
Belt conjunctions (~10⁻⁵ c) sit far below every threshold — the belt is safe, matching the
prior scene reading. The universe's sparse order resolves no contact impulse at all (it
logs them, `universe.rs:1176`); surfaces go through the tube machinery — the hole is
ship-vs-ship/debris in fleets and battles, the law the fleet lattice runs
("contacts happen inside the frame", `fleet.rs`). The prior blind rates are this same law:
87.5% inert in the relativistic gas, 55–62% in the two-body pump (f50d) — lattice-scale
bodies are ρ ≪ 1, as the decomposition predicts.

## Refuted

- "Contacts use the exact integer special-relativity law" (representation.md §2) below the
  dwell threshold: the contact is detected, logged, and resolved **never** — the receding
  gate drops the impulse of any pair whose closest approach is inside the detection bin
  (20261015-0358-redteam-8144; the gate itself is load-bearing for its other job, stopping
  second hits on already-resolved receding pairs).
- "The 87.5%/55–62% inert-contact rates are a property of those gas scenes": they are the
  same threshold measured blind — lattice-scale bodies at β 0.6 sit at ρ ≪ 1; the
  decomposition reproduces the direction and the rates follow max(0, 1−ρ)
  (20261015-0358-redteam-8144 reading f50d).
- "Some rung or gate would catch a missing impulse": none does — r5's frozen scenes are
  exchanging (ρ > 1) arms by construction (f3ce/33f1 measured per-contact bookkeeping ≠ 0),
  both orders share the gate so B8/bit-identity is blind, and the ledgers stay exact
  through a skip (nothing moves) (20261015-0358-redteam-8144; same shape as f50d's
  "invisible to every ledger by construction").

## Open directions

1. **The fix, one rule:** resolve at the crossing the detection quadratic already finds
   exactly (τ\* = −d·w/|w|² is rational; the v1 reflection needs no root), re-scoping the
   double-resolution guard to consumed pairs. Canon reset; r5 re-frozen with the criterion
   this run's probe is: *a crossed-in-bin head-on pair at closing 0.9c must exchange the
   exact v1 impulse; the shipped skip is the negative control.*
2. **The slow grazing half:** shallow-depth grazers skip at any speed (the effective depth
   √(reach²−b²), not reach, sets the threshold); the dropped impulse is small but a dense
   slow gas with many grazes was not measured (20261015-0358-redteam-8144's lens note).
3. **The real rate in a flown fleet:** members share the frame velocity; the player's and
   leavers' relative speeds decide how often the threshold is crossed in play — unmeasured.

## Contradictions

None open. f50d's scene rates and this decomposition agree (same law, blind vs solved);
f3ce/33f1's r5 arms sit in the exchanging regime by construction, a domain boundary, not a
conflict — recorded so no run reads r5's pass as contact-law correctness at speed.

## Runs
- 20261015-0358-redteam-8144 (awaiting grade): the skip solved in closed form — skip ⟺ τ* ≤ 1,
  294/294; v\* = reach/1477 m in c; a 0.5 m missile at 0.9c never collides; no rung sees it.
  (Checker2: reproduced byte-identical; held-out extensions all hold — oblique b ≠ 0 with the
  effective-reach form 453/453 (the head-only arms are b = 0; `d0 ≤ |w|` is exact only
  head-on, the τ* ≤ 1 form is the general law), mass 1:65535, reach to 709,936 quanta, and a
  reflecting-box pair at closing 0.9c exchanges 0 times in 334 re-encounters over 3000
  chronons (rev accounting exact); the "independent" integer reference `xtask/src/gas.rs:152`
  shares the gate, so the Chronon↔gas cross-check is blind to it too.)
