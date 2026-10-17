topic: contact-speed
status: open
closed-by:
valid-while:
updated: 20261015-0724-dynamics-1648

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

**The slow grazing half is measured: the skip is innocent in a cold dense gas — and the
proposed no-root fix is a no-op (20261015-0724-dynamics-1648).** Three f64 twins of the
shipped rule (exact mirror; skip-class pairs resolved at the contact root |d| = reach;
bin-end exchange) beside the shipped engine, on cold two-temperature gases (Q = 2²⁰,
reach 2048, N = 200–300, masses 1/64, T_A/T_B = 4, controls on both sides: the twins
bit-identical when no contact can skip; the fast control's 48%-of-transport drop
detected; classifier 98–100%; ledgers exact). **Fleet-scale price: skip fraction 0.1% of
detected contacts at closing 0.07 reach/chronon (d1), 0.9% at 0.2 (h1, held-out seed,
N=300), 2.7% at 0.34 (d2); dropped momentum transport 0.01% / 0.21% / 1.1%; equipartition
and relaxation identical within chaos noise (t_half ratios 1.00–1.19).** A ghosted pair
almost never comes back at fleet speeds (34 re-encounters after skips vs 29,792 after
exchanges in d1; 3% at d2) and contacts never avalanche (Fano 0.05–0.85): no cascade, no
gate needed. The in-situ per-ρ skip rate equals the driven-pair law max(0, 1−ρ) to
±0.09 at every speed (ρ≈0.15→0.79, 0.4→0.59, 0.6→0.40, 0.85→0.14, ρ>1→0; checker,
20261015: the ρ≈0.15 bin runs 0.757–0.800 against its 0.85 label at every speed — the
bin's mean ρ sits above its label; binning, not bias) — the closed form is a gas law,
not a probe artifact. **The fix rule of open direction 1 as worded
("resolve at τ\* = −d·w/|w|²; the v1 reflection needs no root") is the identity:** in the
pair's COM frame N is purely spatial along d(τ\*) ⊥ w while both momenta lie along w, so
the reflection exchanges nothing, any masses — measured 0.3% of transport applied (the
multi-pair contamination residue) against 48%/1.1% for the contact-root arm. A real fix
pays the contact root |d| = reach (its normal carries ρ under a square root); the cheap
bin-end exchange under-impulses grazes 2× at slow speeds (0.51% vs 1.09% at d2). Also:
f50d's quantization innocence extends to these gases at |k| ≥ 150 quanta (contacts
within 5% — d1 is 4.4%; skip fraction equal), and breaks at crawl speeds (|k| ~ 8: 826
vs 900 contacts, faster equilibration) — the velocity quantum, not the skip, is the
crawl-speed channel.


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
- **"Resolve at the closest approach with the v1 reflection — no root needed"
  (8144's open direction 1 as worded): the reflection at the τ\* normal is the identity —
  COM momenta are parallel to w, d(τ\*) ⊥ w, the flipped component is zero for both bodies
  at any mass; measured 0.3%/0.01%/0.01% of transport applied (c2/d2/h1) vs 48%/1.1%/0.2%
  for the contact-root resolver (20261015-0724-dynamics-1648).**
- **"The skip distorts slow dense gases" (the danger the slow half left open): measured
  innocent below |w| ~ reach/3 — 10⁻⁴–10⁻² of transport dropped, relaxation and
  equipartition unchanged within finite-N noise, no re-encounter cascade; the distortion
  channel is real only as |w| → reach and beyond (48% of transport at |w| ≫ reach)
  (20261015-0724-dynamics-1648).**

## Open directions

1. ~~**The fix, one rule:** resolve at the crossing the detection quadratic already finds
   exactly (τ\* = −d·w/|w|² is rational; the v1 reflection needs no root), re-scoping the
   double-resolution guard to consumed pairs.~~ **The no-root half is refuted** (the τ\*
   reflection is the identity, 20261015-0724-dynamics-1648); what stands is the *criterion*
   — a crossed-in-bin head-on pair at closing 0.9c must exchange the exact v1 impulse; the
   shipped skip is the negative control — and the fact that a real fix needs the contact
   root |d| = reach (irrational normal: ρ under a square root — an integer-law design
   question) or the cheap bin-end exchange (measured 2× under-impulse on grazes, right
   order). At fleet closing speeds nothing needs fixing (10⁻⁴–10⁻² of transport).
2. ~~**The slow grazing half:** shallow-depth grazers skip at any speed; a dense slow gas
   with many grazes was not measured.~~ **Measured innocent** (20261015-0724-dynamics-1648,
   table above). What remains of this direction: *bound* pairs (the pump's 55–62% skip
   inside a trap — dwell under the skip vs a resolving twin is f50d's domain, not
   re-measured here) and filling fractions ≫ 2% (multi-pair-bin contamination was ≤ 1.6%
   of skip-class contacts here).
3. **The real rate in a flown fleet:** members share the frame velocity; the player's and
   leavers' relative speeds decide how often the threshold is crossed in play — unmeasured.
   The gas numbers now bound it: at manoeuvre-scale relative speeds the skip channel is
   ≤ 10⁻² of transport; it bites only for deliberately fast crossers (missiles, flybys at
   a large fraction of v\*).

## Contradictions

None open. f50d's scene rates and this decomposition agree (same law, blind vs solved);
f3ce/33f1's r5 arms sit in the exchanging regime by construction, a domain boundary, not a
conflict — recorded so no run reads r5's pass as contact-law correctness at speed. The
new run's innocence and 8144's fast-half danger are the same fence read from two sides:
the boundary is |w| ~ depth, and both sides are now measured.

## Runs
- 20261015-0358-redteam-8144 (awaiting grade): the skip solved in closed form — skip ⟺ τ* ≤ 1,
- 20261015-0724-dynamics-1648 (awaiting grade): the slow grazing half measured innocent
