# Dossier — 20261014-1719-fermi-cf45 (Fermi lens)

## Claim

The belt's cadence is the **doll's clock, not the body's**: every root-doll ship is stepped at
`2^step_log2` kicks per period of the **doll's shortest secondary** (measured 77.24 d, κ_eff = 237
after the Δs octave rounding and a +7.9% position refinement — interval 2.814×10⁴ s p50, **flat in a
across 2–3 AU**, 24× faster than the own-period law `step_for` gives the same bodies), so effb's
published 10⁹ rate law `rate = 2⁷/P_own` ("a pure birth constant... the whole bill") is the
secondary-doll law read onto the root doll: **wrong by 15–31× at the plane's own belt**, and the
recomposed 10⁹ steady-state kick bill at the shipped `step_log2 = 7` is 148× over the flying-pace
frame budget even at the M1's 30 µs events (8.2 cores at 231 µs, 1.07 at 30 µs, 0.10 Carlson,
0.0039 at the key arm; rtf 1) — the dial still fits, but only at its coarse end: step_log2 ≈ 0
(≈ 1 kick per 77 d per body, 1.16× — borderline) at 30 µs, step_log2 ≤ 2–3 at Carlson
(0.45–0.90×), step_log2 5 at the key arm (0.14×); as shipped (7) only the 0.11 µs key arm fits
(0.54×).

## Bottleneck

The board's #1 (bodies in the flyable engine toward 10⁹) and #5 (scale to 10⁹): the steady-state
event rate is the belt's whole CPU bill (effb's own framing, 1738's cube cadence axis), and its
central constant was composed from the wrong clock. Expected gain: the 10⁹ kick stream recomposes
up 24× (p50); what it deletes is a wrong dial anchor — the integrator's `step_log2` decision at
belt wiring must anchor on **P_D (the doll's shortest secondary) × the f'(U_P+c) refinement**, not
on each body's own period.

## Evidence (all from `regen.sh`, one Linux box, shared, load ~2-5; each run ≤ 60 s)

Instrument: `crates/universe/examples/cadence.rs` (this run's only code change; read-only on
shipped APIs: `rec().interval`, `b.kick.len`, `binding::Trajectory::Cycle::period`, `ext`'s clock
set by `plan_clock`; nothing patched, digests untouched). Seed 1 default; held-out seed 11 and
N=1000/seed 3.

- **The root doll's sources** (planets about the star): 6.6735×10⁶ s (**77.24 d**), 3.0642×10⁷ s
  (354.6 d), 3.4714×10⁸ s (4,017.8 d). P_D = 77.24 d — the record's "Cinder 88 days" (ladder.txt,
  belt_first's doc) is off by 14%; the wave anchor is the 77.24-d source.
- **Belt (root doll, n=3,700; 700 at N=1000)**: planned interval p50 **2.814×10⁴ s** (p01–p99
  2.675–2.895×10⁴, ±4%); rate **3.553×10⁻⁵ /game-s/body**; kicks per own orbit p01/p50/p99
  **2,674 / 3,899 / 5,484**. Arithmetic: 2⁻⁸·P_D = 2.607×10⁴ × 1.079 (the `dt/ds = f'(U_P+c)`
  refinement at the belt's position) = 2.814×10⁴ ✓; κ_eff = P_D/interval = **237** per 77.24 d.
- **The discriminator (flat vs a^1.5)**: mean interval by a-quartile 2.818 → 2.812 → 2.813 →
  2.805 ×10⁴ s (log–log slope ≈ **−0.006**; the own-period law demands +1.5, a 1.84× rise).
  Identical at seed 11 and N=1000.
- **The counterfactual**, `step::step_for(binding, 7, None)` on the same bodies (what the
  secondary-doll law gives them): p50 **6.77×10⁵ s** — the measured interval is **24.1× shorter**
  at p50 (effb's κ-rounded band: 15–31×).
- **Three instruments agree**: plan interval (3.553×10⁻⁵/s), per-body event counter (belt only:
  exactly 4.00 events = 2 kicks + 2 boundaries per body over 60,333 game-s → 3.32×10⁻⁵/s, 7%), and
  the external anchor: first kicks at interval/2 ≈ 1.407×10⁴ s sit **inside** taleb-6138's measured
  wave window (13,037–14,542 game-s, 199,700 bodies) — reproduced, not fitted.
- **Steady state** (t = 60 ks, ≥ 2 intervals in): interval p50 unchanged at the sixth digit; the
  clock does not tighten or drift (the belt is ≥ 0.7 AU from any secondary).
- **Composition at 10⁹** (`compose.py`, measured ρ = 3.55×10⁻⁵/s): stream 3.55×10⁴ kicks/game-s →
  8.2 cores (231 µs), 1.74 (49 µs, this box), 1.07 (30 µs, M1), 0.103 (2.9 µs Carlson), 0.0039
  (0.11 µs key arm). Flying pace (rtf 100, 0.72 core-s/wall-s = 7.2 ms/game-s): affordable stream
  240 kicks/game-s at 30 µs → the shipped config is **148× over** (242× at 49 µs, 14.3× at Carlson,
  0.54× at the key arm). Dial: each step_log2 octave halves the stream; fitting needs step_log2 ≈ 0
  (≈ 1 kick per 77 d per body) at 30 µs, step_log2 ≤ 4 at Carlson, unchanged step_log2 = 7 at the
  key arm.
- **The wave at 10⁹** (birth-program artifact, all bodies born at tick 0): first kicks cluster at
  1.34–1.45×10⁴ game-s → 10⁹ kicks over ~1.1×10³ game-s = 9.1×10⁵ kicks/game-s, **26× the steady
  stream**; at rtf 100 even the key arm pays 10 s/s (14× the whole 4-core box). Birth-phase
  staggering over one interval is not optional at 10⁹.

## Predictions

`predictions.md` was written before the run (its derivation used the record's 88 d; the measured
P_D is 77.24 d). Held: P2 (interval inside [2.2, 5.5]×10⁴ s; wave anchor matched), P3 (the
discriminator: slope −0.006 vs bar < 0.15), P4 (kicks/orbit 2,674–5,484 vs band 1,100–2,800 —
**14% above my p99 upper edge**: I under-guessed the rounding octave; direction and mechanism as
predicted), P6 (steady state ±0.01%, bar ±30%), P7 (instruments within 7%, bar 25%). Prediction C
was right that the global counter is battle-dominated in a 60 ks window at small N (101,624 kicks,
belt share ~7%); the per-body counter settles the belt rate. **Miss, disclosed:** P1/P5's locals
arm — my locals' readout carried a doll-unit conversion bug (5×10⁻³ s intervals), so I make **no**
locals claim; effb's roster reconciliation (3071/7497 natives at 202–223 kicks/orbit live in
secondary dolls) is supported by the code path (`step.rs:554` reaches `step_for` only when
`!on_clock()`), not re-measured.

## What would make it wrong

The measurement is on the ladder's belt (Rayleigh e 0.07, periapsis > 1.2 AU, planar, prograde) at
2–3 AU: a belt **inside** the 77.24-d source's orbit, near a secondary (f' refinement → shorter
intervals), under thrust (thrust steps cap the clock, `plan_clock`), or a root doll whose shortest
secondary changes (a source rebinds: P_D itself moves — the doll's clock is dynamic, worth one
probe) would shift the constant, not the law. The composition arms are other runs' measured costs,
not re-measured here. If `BodyRec::interval` lied about the *executed* cadence the per-body event
counter would have caught it (it agrees to 7%).

## Cost of adoption

Zero code: a re-anchoring of the belt-wiring `step_log2` decision (effb's own dial, right lever,
wrong anchor) and of the 10⁹ ledger's kick term. The physics question it opens is real: at the
shipped step_log2 a 2–3 AU body takes 2,674–5,484 kicks per own orbit — 5–11× the board's old
"≤ 512 events per orbit" bar and ~80–170× H0190's 32/orbit averaged ladder — because the doll's
shortest secondary taxes every root-doll body alike; the coarsening's certificate (Jacobi/B-gates)
is the integrator's one-step follow-up.

## PRINCIPLES

#22 "the simulation tells us what's next not us" and #3 "compute only surprises": a 77-day clock
applied to a 3.5-year orbit resolves the perturber, not the body — the surprise rate of a far belt
body is the secondaries' synodic pull, and the law's own clock (`dt/ds = f'(U_P+c)`, ext.rs: "the
step is a property of the state, not a choice") already encodes it; only the *count* per P_D is a
choice. #18 "the right representation": the two-clocks split (doll clock for root ships, own-period
`step_for` inside secondary dolls) is one law at two scales — the error was composing one record
from the other's doll.

## The lens

The Fermi estimate came first and nearly closed the case before any run (interval ≈ P_D/2⁷⁻⁸
predicted the wave window taleb had already measured); the run's value is the flat-in-a
discriminator and the κ_eff/ refinement constants, which no estimate can pin. What the lens may
have missed: I did not measure the locals' clock (bug, disclosed) or the clock's dynamic response
to a source rebind; and my composition inherits other runs' cost arms verbatim — a checker should
re-run `cadence.rs` (one command) and re-derive `compose.py`'s four products from the printed
constants.
