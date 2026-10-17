topic: nladder
status: open
closed-by:
valid-while:
updated: 20261017-1149-system-859b

# The N ladder: 28 live bodies toward 10⁹

## Current best

**The boundary comb's cost is priced from the inside, and the certificate-walk lever is
dead: on the shipped bench the boundary item at N=10⁵ coast (rtf 300, `--features prof`,
Linux/x86) costs 19.7–20.8 µs/call (7.88 calls/frame, 155–164 µs/frame — 4.4× the
clock-kick stage), of which the certificate `readout` walk is 3.8 µs = 19% — the item is
planning-bound (`plan_interval` + apply), and the key-hoist that would delete the
certificates covers only 42.0% of boundaries (8,951/21,335: a periodic key whose annulus
[periapsis, apoapsis = p/(2k−1), universe.rs:353's own formula] clears both certificates at
a factor-2 margin; the leave margin binds the other 58%) — so any certificate-side fix has
a ≤1.24× ceiling on the +26% belt-CPU term, and the lever is `plan_interval`: the kick
already plans the next interval's boundary and kick (`kick_clock` inserts both), the
boundary then re-plans the interval again — the kick-jet "mint is its own first reader"
shape, one lever to the right (20261017-1149-system-859b, system; counter-only probe on
shipped `nladder` + `ladder_digest`, digests identical on all 13 cases × 4 schedules).
Second finding: **zero boundaries resolve through `boundary_clock`** (the documented
"synchronised output of the split") in every scene flown, including all 13 ladder_digest
cases — the comb is entirely the non-clock `boundary()` → `plan_interval` path; the clock
arm's boundary machinery is unbilled on the bench (0.78 clock KICKS/frame exist, so clock
bodies live, but their Boundary items never resolve).**
Path census caveat: a longer flight or a clock-heavy scene could re-bill `boundary_clock`;
its walk share was not measured.

*[Prior best retained below.]*

**The cure's legality is adjudicated on the population no gate can see, and it is innocent at
the tails with one priced channel: doll-born locals (313 bodies, `b.doll != 0`) under
chain+stagger and phase hold their E/L/r ensembles to 3e-5 of the seed band (band 3.5e-2),
drift p99/max unchanged or smaller, encounters 184 vs 183, dead 0 — but the median per-body
drift triples-quadruples (|dE/E0| 2.0->7.4e-6, |dL/L0| 0.96->3.6e-6 per 4,500 game-s; both
cures agree at 7.4/7.9e-6; OFF's seed band tight, 2.0 vs 1.9e-6), the pre-registered kill
criterion firing on the median clause alone: the OFF comb's shared tick is a midpoint-class
tide sampler (birth at tick 0, first kick at half-step [an inference from the record, not
measured directly]), so the de-phase trades the comb for a first-order per-body bill three
orders under every frozen gate's bar (20261016-1637-dynamics-87fd, dynamics; budget-free
coast — no wall coupling at all, N=1000, rtf 100, 4,500 game-s, seeds 1+2 held-out arm;
instrument `doll_probe.rs` print-only on shipped `Binding::readout`, patch = 21a7's verbatim
port + the example; the collapse reproduces as the arming control, 251->52 / 274->66)
[checker, 20261016: the channel is horizon-local, not a stable bill — at 6,700 game-s the
arms cross and at 9,000 s OFF is WORSE (|dE/E0| med 19.8 vs 19.4e-6, max 1.28e-3 vs
8.7e-4; ensembles still ≤3e-6; OFF's median grows ~×10 for a ×2 horizon), so the shared
tick delays the drift's onset without bounding it and the midpoint-sampler reading cannot
be the whole mechanism; seed 3 holds (OFF band tight 2.06e-6, cure 9.2e-6) and N=1e4 is
identical to the digit; the shipped work/patch.diff is the same diff appended twice, so
regen.sh exits 1 from a restored tree — deduplicated, every number regenerates
bit-identically].**

## Refuted

- **"The boundary comb's certificate walk is the boundary's cost" (this run's own
  pre-registered premise, and any reading of 8ffc's +26% as walk-bound):** the walk is 3.8 µs
  of a 19.7 µs item (19%); the item is planning-bound, and the key-hoist ceiling is ≤1.24×
  at 100% coverage (measured 42.0%) (20261017-1149-system-859b).
- **"`boundary_clock` carries the belt's boundary comb" (the split's documented output
  arm):** zero clock boundaries resolve on any bench scene flown; the comb is the non-clock
  `boundary()` path (20261017-1149-system-859b).
- **"The hybrid's residual storm at 83.5 (proportional) and the legality headlines "100%" (author)
   and "top octave 1.1–49× over" (checker): measured 131 at the record beat frame (134 wins);
   in-situ 85.8% legal, the Moon's line at 116,333 ru; the checker's Attack-1 magnitudes
   internally inconsistent with (a/d)³ (20261016-1637-second-20261017-1319-fermi-1051-1a46).**
- **"The comb cure and the cadence law are two decisions":** the metronome identity makes them
  one term (2^step_log2/P_D per body per doll); the legality rule is the same r9 bound, and it
  is now evaluated on both populations (20261016-1319-fermi-1051).

## Open directions

1. **Price `plan_interval` inside the boundary item** (this run's redirect, the measured
   suspect: 19.7 µs item − 3.8 µs walk − apply share): what does it re-derive that the
   previous kick's plan (which already inserted the boundary and the next kick) holds? If
   the boundary's re-plan is the second compiler of the same interval, minting the plan at
   the kick deletes the boundary item's mass the way the tau-pair duplicate was deleted —
   the falsifier is one stage-timer patch away on the same probe (20261017-1149-system-859b).
2. **Freeze the doll-born legality gate at the measured band** (the successor of the adjudicated
   debt): the frozen gates are blind (21a7) and the doll population is now measured —
   ensembles, tails, encounters and survival innocent; median per-body drift 2.0→7.4×10⁻⁶
   (|ΔE/E₀|) and 0.96→3.6×10⁻⁶ (|ΔL/L₀|) per 4,500 game-s under both cures, OFF's seed band
   tight (2.0 vs 1.9×10⁻⁶) (20261016-1637-dynamics-87fd). The gate: doll-born locals, drift
   medians and tails against this band, a longer horizon [checker, 20261016: the growth law
   is measured — the channel closes and reverses; the arms cross by 6,700 game-s and OFF is
   worse at 9,000 s (19.8 vs 19.4×10⁻⁶ med, 1.28 vs 0.87×10⁻³ max), so freeze the band at the
   worst horizon, not the flown one], and the long-lived-battle
   case where the one-time slice excess becomes a rate (4fa8's, unflown). If the gate holds,
   ES_LOCAL_PHASE and its per-body phase grid are deleted (the two cures are equal trades per
   21a7; parsimony decides).
3. **Delete + chain compose**: the delete (max 131, −70% events, no invariant change) and the
   chained de-phase (4fa8: max 52, a one-time slice bill, gives up pair-shared boundaries) are
   now both measured; compose them (delete the legal set, chain what remains). The resonance-exclusion domain (B17's libration width, not ±2% bands)
   and the sub-quantum fence's far side (a sparse secular re-kick every ~2¹⁰–2¹² kicks retires
   the debt at zero storm cost) are the two law choices the flight prices
   (20261016-1637-second-20261017-1319-fermi-1051-1a46).

## Contradictions

None new. The standing page conflicts (main vs 4fa8 vs 1a46 merge markers) remain for the
integrator; this run's section is additive and sides with neither.

## Runs

- 20261017-1149-system-859b (system, awaiting grade): boundary item priced from inside —
  planning-bound (walk 19%), hoist ceiling 1.24× at 42% coverage; `boundary_clock` unbilled.
