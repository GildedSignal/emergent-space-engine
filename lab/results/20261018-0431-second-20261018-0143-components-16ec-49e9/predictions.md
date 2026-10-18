# Predictions (written before the decisive flights)

The context: 16ec's first checker graded gold but read the burn-arm "kill" as an instrument
artifact — the harness injects the player's thrust at `p.u.now` at frame 60, and the presented
tick drifts with the 12 ms budget, so flag-off burn controls diverge among themselves. The wiki
page names the next probe: "a pinned-input harness first, then the bisect if a real difference
survives". Mechanism fact read from the code before flying: `Universe::digest` hashes the
decision log (`self.inputs`, universe.rs:~1352) directly, so any two runs whose injection ticks
differ are digest-unequal **by construction**, physics aside; `Universe::input` clamps the
decision to `t.max(event_time(player))`, so a pinned tick only stays pinned if it is beyond the
player's committed item at injection.

My experiments (all `nladder 10000 <mode> 60 1800`, canonical cut pinned at 1.2×10¹⁰ ticks):

- **E-pin:** inject at a fixed tick `ES_INJECT_TICK` (2.03×10⁹ = 10,000 game-s, far past the
  ~1,800 game-s presented at frame 60 and past the player's next item) instead of `p.u.now`.
- **E-ship:** the shipped harness unchanged, but printing the injection tick.
- **E-straddle:** `ES_LEAVE_LOG2=28` (2^28 root units ≈ 2.65 AU, inside the belt's [2, 4.2] AU
  apoapsis span) so part of the belt refuses the skip (range straddles leave) and part still
  skips — the `slow_cycle` branch never fired in any of 16ec's flights.

**Design note (after the smoke test, still before any decisive flight).** `Universe::input(T)`
with T ahead of the presented tick synchronously pulls the player's whole history to T
(measured ≈ 0.8 µs/tick: a 4.5×10⁷-tick pull burns ~35 s of CPU), so the pinned arm uses the
engine's own canonical decision path instead: `Universe::schedule(T, word)` — "a decision
taken at that tick whenever the engine gets there" (universe.rs:1099) — which is O(1), logged
at exactly T, and taken during the normal advance. T = 365,400,000 = the nominal frame-60
presented tick at rtf 1800 (1,800 game-s); the presented tick can only lag nominal, so
T ≥ presented ≥ event_time in every run and the schedule call is never refused. The
shipped-harness arm keeps `input(p.u.now)` untouched.
- **E-decomp:** print the flight-window deltas of the clock-path census and `stats.boundaries`
  (both paths) in one shipped command, so the decomposition denominator regenerates.

## The predictions

- **H1 (mechanism visible).** Two shipped-harness burn runs print different injection ticks
  (presented lag differs under load) and different digests. If the ticks come out equal this
  window, the mechanism is unfalsified but unshown — I report it as not-shown, not as held.
- **H2 (pinned A/A).** Two pinned burn controls are bit-identical (same digest, same cut):
  with the decision tick fixed, the whole flight is schedule-independent.
- **H3 (the claim on the burn arm).** Pinned burn ctl vs fast: bit-identical digest; the fast
  arm skips ≈ 19.4k belt boundaries and reads out the ~330 player passages (the shipped-harness
  skip pattern), `slow_cycle` 0. **If these digests differ, the fast path truly moves a
  thrusting population and 16ec's burn kill stands as real** — I then bisect the first
  diverging event as far as the window allows and report.
- **H4 (the straddle branch).** With `ES_LEAVE_LOG2=28`: `slow_cycle` > 0 AND `fast` > 0 (a
  mixed belt: apoapsis+slack beyond 2^28 refuses, inside skips); deaths > 0 (belt bodies
  actually past leave die) **equal in both arms**; digest ctl = fast. Any digest difference on
  this arm kills the fall-through as built.
- **H5 (decomposition).** The regenerable flight-window clock share is ≤ 19% (checker's bound
  ≤18%/≥82% from whole-process vs window counts); the clock path stays the minority of
  boundary mass at N = 10⁴.
- **H6 (positive control).** My rebuilt patch still reproduces the coast digest
  `a725217f1dcd9f2a` ctl = fast at 100% skip (16ec's known answer; guards against my harness
  edits changing the physics).

## Kill criteria

Any digest divergence at the same pinned cut between ctl and fast on the pinned-burn or
straddle arms kills the fast path as built on those populations (16ec's P5, inherited). A
pinned A/A divergence (H2 failing) means the flight is still schedule-coupled somewhere I have
not read — that would void E-pin as an instrument, not the fast path.
