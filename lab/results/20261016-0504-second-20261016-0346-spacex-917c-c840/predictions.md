# Predictions — 20261016-0504-second-…-spacex-917c-c840 (second author)

Written BEFORE the decisive armed runs. The parent run (spacex-917c) flew the stagger's
frame effect; the checker's named gold step is ed3a's open direction 2: the behaviour
gates armed, B13/B14-class precession under the shifted first-kick tide phase.

Setup: spacex-917c's own `work/patch.diff` (the ES_STAGGER stagger, applied verbatim on
this tree), one patched binary; OFF = `env -u ES_STAGGER`, ARMED = `ES_STAGGER=1`. In the
plane's B12–B14 scenes the ship is born bare (`add_body_state(Kind::Ship, ..)` then
`start()`), so `plan_clock` takes the staggered path: the first kick moves by
hash(id)·2·half − its original half-step offset. The offset fraction is id-derived, and the
adapter builds a fresh universe per seed with the SAME ship id, so every seed in a gate
gets the same fraction of one step.

- **P1 (B13 armed = B13 off, gate verdict unchanged).** Off, the plane's B13 baseline is
  60/64 judged-pass (HANDOFF: baselined red). The stagger moves ONE kick of the ship by
  < one step; the gate's thresholds are 1% of ΔE/ΔL. Predicted armed judged-pass: **60/64,
  band [58, 62]** (the 4 red seeds are marginal flybys; a sub-step phase shift may flip at
  most the marginal ones, either way). The per-seed ΔE/ΔL numbers may differ in low digits;
  the verdict line must stay `B13 FAIL 60/64`-class (red as baselined, not worse).
- **P2 (armed ≠ off at the state level, i.e. the instrument can see the stagger).** At
  least one judged seed's ΔE or ΔL changes between arms at ≥ 4 significant digits (the
  kick time moves, the integer state moves, the float boundary shows it). If NO number
  moves, the gates are blind to the stagger and the legality question is not answered by
  them — that would be a finding, not a pass.
- **P3 (B14 frozen gate: timeout in both arms).** HANDOFF: B14 times out on the plane
  (256 moons × 50 planet periods × 64 samples). Predicted: `B14 FAIL (timeout)` in BOTH
  arms, identical verdict lines. The frozen gate cannot judge the stagger on the plane.
- **P4 (B14-class probe, the checker's actual question).** A reduced Hill probe (moons at
  0.2–0.9 R_H, circular and e0 ≤ 0.3, ~10 planet periods, apsidal rate per
  hill.rs's estimator) flown armed vs off vs the restricted reference: predicted the
  armed and off apsidal rates agree with each other within **1e-3 rad per planet period**
  (the law's own per-orbit precession error is ~1e-6 relative; one shifted kick out of
  ~2^step_log2 per orbit moves the rate by far less), and both stay within B14's frozen
  10% of the reference wherever the off arm already is. Band: |rate_armed − rate_off| ≤
  1% of |rate_ref| for every judged moon; class (bound/escaped at 1.5 R_H) identical
  armed vs off for every moon.
- **P5 (ladder_digest armed identity holds on this tree too):** 13/13 bit-identical armed
  vs pristine (the checker found this; the belt-program births there carry ext, so the
  stagger never engages). If instead any digest moves, the stagger's legality surface is
  larger than the checker measured — report which cases move.

Kill criterion for the parent claim: if armed B13 drops below ~56/64 (the shift breaking
non-marginal flybys), or the probe's armed/off apsidal rates differ by > 10% of the
reference rate on any judged moon, the stagger is NOT legality-free and the parent's
"adopt as birth default" direction dies (the wave cure would need a birth-time-lawful
form instead).
