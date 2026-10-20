# predictions.md — 20261020-0440-second-...-ca63

Written BEFORE the decisive matrix (the 15 flights below). Two calibration flights were flown
first and are disclosed: `calib_k100000_s17_idle` (instrument check vs 476d's record: crest
4,593 ms / 0.980 ev/body / 46.9 µs-ev, onset_gs 13,167) and `calib_k100000_s25_load16`
(onset_gs 13,129; 1.036 ev/body; 196.6 µs-ev). They fixed the flight windows (seconds/guard)
and forced one instrument change BEFORE any decisive flight: the crest onset is detected on the
events channel (argmax 1,500-gs window, grid 100), because an ms-based onset fires on load
contention noise at gs ~137. The bands below are set from the previous runs' record (2d26,
cc9d, 7b6f, 476d, its checker) and these two disclosed calibrations at 1e5 only; nothing at
2e5/3e5, no fence arm, and no replicate has been flown.

Decisive matrix (all: shipped nladder burn scene, seed 1, rtf 2000, 12 ms budget):
- idle (load ~0.25): 3× k1e5 s17, 3× k2e5 s10, 1× k3e5 s10 (held-out rung)
- load16 (16 CPU spinners on 8 vCPU): 3× k1e5 s25, 3× k2e5 s45, guard ES_FLIGHT_MAX_S=130
- fence (idle, ES_SCAN_TTL_S=16): 1× k1e5 s17, 1× k2e5 s17

## Predictions

- **P1 (game-time lock).** The crest's onset_gs (events-argmax) satisfies
  |median(load16) − median(idle)| < 750 gs at BOTH 1e5 and 2e5; idle 1e5 median ∈ [12,700, 13,800].
- **P2 (flat arrivals).** Crest events/body ∈ [0.95, 1.10] at every rung × regime flown, and the
  regime shift at a fixed rung is ≤ 0.08/body.
- **P3 (crest exponent).** α(1e5→2e5) on crest excess: idle ∈ [1.00, 1.45]; load16 ∈ [0.90, 1.45];
  |α_load − α_idle| ≤ 0.20. Held-out: idle α(1e5→3e5) ∈ [1.05, 1.40].
- **P4 (tail deleted by the fence).** At 1e5 idle: fence tail_ms ≤ 300 ms (≤ 0.15× the no-fence
  idle median ~1,900-2,000); fence crest ∈ [0.7, 1.4]× the no-fence idle median; fence held_max
  ≤ 50; fence crest events/body still inside P2's band.
- **P5 (cost).** Idle µs/event rises ≤ 15% per K-doubling; load16 multiplies µs/event by
  2.5-5× at both rungs; that multiplier is K-uniform within 30% (else α cannot carry across regimes).

## Kill criteria (any one fires → the re-anchored crest law is NOT adoptable as stated)

- **K1:** onset_gs medians differ > 1,500 gs between regimes at the same rung (crest not game-time-locked).
- **K2:** crest events/body outside [0.90, 1.10] anywhere, or regime shift > 0.10.
- **K3:** the 3-flight α bands of the two regimes are disjoint.
- **K4:** fence tail > 25% of the no-fence median tail (tail ≠ held-scan channel).
- **K5:** fence crest outside [0.5, 2.0]× the no-fence median crest (the fence touches the crest).

## Registered hazards

- The 2e5 idle arms run near the memory cap (the record's clean s10 flight lived; the s17 arm
  peaked 2,758 MB): an RSS kill voids that replicate, and I report it, not rerun it elsewhere.
- At load the ebb and ms-scale quantities are contention-bound by construction; only counts,
  gs positions and within-regime exponents are law candidates (the record's own lesson).
