topic: contact-speed
status: open
closed-by:
valid-while:
updated: 20261018-0722-scout-6362
# The contact law's speed domain: which detected contacts exchange an impulse

## Current best

**[20261018-0722-scout-6362] The skip's open design question ("a real fix needs the contact
root |d| = reach — an integer-law design question", 1648) is answered in closed form: the
root normal decomposes on the lattice's own integer data as n·R = P − s·w with P rational,
w·P = 0 EXACTLY in integer arithmetic, and s = √D/|w|² the only irrational (D integer,
D ≥ 0 iff hit), so the exact root-normal impulse is Δw = 2√D·P/R² − 2D·w/(|w|²R²) — one
integer square root and one divide per component, no carried irrational state.** Verified
in a standalone float/integer toy at the shipped constants' class (R = 2048 quanta [1648's
gas], c = 2²⁰ quanta/chronon [8144's Q], k = 20 frac bits): grid arms b/R ∈ {0, ¼, ½,
39/40} × ρ = |w|/R ∈ {3, 30, 300, 512} (β to 1.0) — integer-rule impulse recovery
99.9855–100.0007% (worst exactly the pre-registered worst case, grazing × ρ = 3), angle ≤
1.1×10⁻⁴ rad, against the shipped rule's 0% on every arm (the skip reproduced in-toy);
adversarial random sweep, 200,000 arbitrary integer (d, w) pairs (22,072 crossed-in-bin,
143,248 misses): recovery min 99.4452% / median 100.0000%, angle max 2.177×10⁻³ rad, ZERO
fires on misses, w·P_num = 0 asserted on every pair; the root tick (ceil at 2²⁰ sub-ticks)
bounds the position offset at ≤ 1.9 quanta against the bin-end application's ≤ 1.05×10⁶
(R·ρ) — the impulse is identical, the schedule owns only the offset. Overflow at the
shipped magnitudes: max intermediate ~2^120 static worst case (7 bits headroom in u128),
104 bits measured on 50k shipped-magnitude pairs (24 bits headroom); k = 16 buys 4 bits,
not 16 (S ∝ 2^k). Checker extended the domain (20261018-0722, check.md): at the shipped
max |w| = 9.4×10⁵ with arbitrary geometry — recovery min 99.9914%, angle ≤ 2.1×10⁻⁴,
grazing to 1-quanta clearance worst 99.93%, classification exact. Mechanism = event-driven
MD's time-of-impact (Alder–Wainwright class; game
physics' CCD/TOI sweeps are the same quadratic) [both UNVERIFIED at source, no network in
the run]; adoption gates named: (1) re-derive on the shipped v1 operator (the toy shares
the reflection between oracle and rule — the normal/TOI recovery is proven, the Householder
4-normal composition is not), (2) the crossed-in-bin r5 scene with 1648's criterion (0.9c
head-on must exchange; the shipped skip is the negative control), (3) multi-pair-bin
ordering (event-driven MD's known failure mode; contamination measured ≤ 1.6% at fleet
speeds). Cost: one branch at the receding gate + one u128 isqrt, on 0.1–2.7% of detected
contacts (1648's rates) — but the firing test is the root-in-bin window via the
already-computed tau_ticks, NOT bare D ≥ 0 (D ≥ 0 alone fires on consumed and future
roots; measured exact in integers, 0 disagreements over 240k pairs, checker).

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
not a probe artifact. The fix rule of open direction 1 as worded
("resolve at τ\* = −d·w/|w|²; the v1 reflection needs no root") is the identity: in the
pair's COM frame N is purely spatial along d(τ\*) ⊥ w while both momenta lie along w, so
the reflection exchanges nothing, any masses — measured 0.3% of transport applied (the
multi-pair contamination residue) against 48%/1.1% for the contact-root arm. A real fix
pays the contact root |d| = reach (its normal carries ρ under a square root — closed
in closed form above); the cheap bin-end exchange under-impulses grazes 2× at slow
speeds (0.51% vs 1.09% at d2). Also: f50d's quantization innocence extends to these gases
at |k| ≥ 150 quanta (contacts within 5% — d1 is 4.4%; skip fraction equal), and breaks at
crawl speeds (|k| ~ 8: 826 vs 900 contacts, faster equilibration) — the velocity quantum,
not the skip, is the crawl-speed channel.


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
- **"The contact-root fix is an open integer-law design question" (1648's residue, "the
  normal carries ρ under a square root"): answered in closed form — the irrational is one
  scalar (s = √D/|w|²) beside the rational P with w·P = 0 exact in integers, and the
  quantized rule recovers ≥ 99.44% of the impulse over 200k adversarial integer pairs
  (20261018-0722-scout-6362). Not yet refuted: the shipped-operator composition (adoption
  gate 1).**

## Open directions

1. ~~**The fix, one rule**~~ — the design half is closed (20261018-0722-scout-6362: the
   root-normal closed form, one isqrt + one divide, verified in toy). What remains is
   adoption: (a) re-derive the closed form on the shipped v1 Householder operator (the
   toy's shared-reflection proof covers the normal and TOI, not the 4-normal
   composition); (b) freeze the crossed-in-bin r5 scene under 1648's criterion (a 0.9c
   head-on pair must exchange the exact v1 impulse; the shipped skip is the negative
   control; 8144's domain note: the shipped arms reach β 0.9, not 1.9×10⁶ quanta/chronon);
   (c) multi-pair-bin root ordering (event-driven MD's classical failure mode; ≤ 1.6%
   contamination at fleet speeds, 1648).
2. ~~**The slow grazing half**~~ **Measured innocent** (20261015-0724-dynamics-1648).
   What remains of this direction: *bound* pairs (the pump's 55–62% skip inside a trap —
   dwell under the skip vs a resolving twin is f50d's domain) and filling fractions ≫ 2%.
3. **The real rate in a flown fleet:** members share the frame velocity; the player's and
   leavers' relative speeds decide how often the threshold is crossed in play — unmeasured.
   The gas numbers bound it: at manoeuvre-scale relative speeds the skip channel is
   ≤ 10⁻² of transport; it bites only for deliberately fast crossers (missiles, flybys at
   a large fraction of v\*) — the class direction 1's fix restores.

## Contradictions

None open. f50d's scene rates and this decomposition agree (same law, blind vs solved);
f3ce/33f1's r5 arms sit in the exchanging regime by construction, a domain boundary, not a
conflict — recorded so no run reads r5's pass as contact-law correctness at speed. The
innocence and fast-half danger are the same fence read from two sides: the boundary is
|w| ~ depth, and both sides are measured. The toy's 0%-shipped column and 8144's
294/294 closed form are the same law at one vs many arms.

## Runs
- 20261015-0358-redteam-8144 (awaiting grade): the skip solved in closed form — skip ⟺ τ* ≤ 1,
- 20261015-0724-dynamics-1648 (awaiting grade): the slow grazing half measured innocent
- 20261018-0722-scout-6362 (silver): the fix's integer design answered — the root
