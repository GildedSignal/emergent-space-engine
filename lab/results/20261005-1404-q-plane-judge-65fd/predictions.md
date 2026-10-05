# Predictions (written before any gate run through the plane)

The decisive experiment is the table: `behave --law plane --gates {B12,B13,B14,B17} --plane-step {7,5,4,3}`.
Nothing below is tuned on a plane run through these gates; the only plane runs so far are the
adapter's own unit tests (a far ship at 4.1 sep: exact t = 0 round-trip; error 5.0e-4·sep at
2^7 kicks/orbit, falling like H² with cadence — attributed to the kicks, not the conversion).

Scene facts that shape the predictions (derived, not measured):
- B12-B14 share the Jupiter scene (sep = 5.27e8); B17's is a miniature (sep = 100), where the
  ship's radial period is ~3.1e3 ticks, so `MIN_STEP = 128` pins the kick step at 128 ticks for
  --plane-step 7, 5 and 4 (≈24.6 kicks per ship orbit) and 256 ticks for 3 (≈12.3).
- B14's moons sit 0.2-0.9 Hill radii out (0.22-0.99 of the doll's Laplace edge) and complete
  ~100-970 moon orbits in the 50 planet periods, so kicks grow ~15M at 2^7: I expect the 60 s
  phase limit to kill B14 at 2^7 on this 2-vCPU shared box, not the physics.

Predictions:

- **B12 (handoffs, Jacobi drift):** PASS at 7 and 5 (the split is symplectic and the changeover
  smooth, so the drift stays bounded; worst err well under 1e-4); PASS-with-margin at 4 (worst
  within ~3x of the 1e-4 bound); FAIL at 3 (largest err over 1e-4). Held-out risk I name before
  looking: if any of the 16 frozen ships dives below the planet's surface, the plane loses it and
  answers nothing, failing B12 at every step — the judge's reference lets a ship pass through the
  planet (a uniform sphere inside), the plane's law ends at the surface. I hold that at ~25%.
- **B13 (assists, ΔE and ΔL within 1%, zero failures tolerated among ~60 judged):** PASS at 7, 5
  and 4 (SyMBA's levels refine the encounter whatever the base cadence); FAIL or one-seed miss
  at 3.
- **B14 (Hill classes, then apsidal rates within 20%):** classes agree at every cadence (the full
  differential tide is in the kicks); the apsides hold at 5, get marginal at 4 (16 kicks per moon
  orbit begin to alias the apse) and fail at 3 (8 per orbit: sampling precession swamps the tide's).
  So: 7 TIMEOUT (machine, ~15M kicks), 5 PASS, 4 borderline, 3 FAIL on apsides.
- **B17 (resonance: pump in [0.8, 1.25], amplitude ratio ≥ 0.8, regime matched, controls within
  20%):** rows 7, 5, 4 bit-for-bit identical (the tick floor); PASS at 24.6 kicks/orbit held at
  ~60% — the drift is exact Kepler and ~50 kicks separate conjunctions, but the kick phase is
  locked to mean anomaly and the conjunction to a fixed anomaly too, so a systematic alias could
  push the pump past ±25%; at 12.3 kicks/orbit (step 3) FAIL or marginal on pump/amplitude.
- **Kicks per orbit** (the trace): ~2^step_log2 per tube radial period within a factor of two
  (steps are powers of two of ticks), except B17 where the 128-tick floor pins it as above.
- **Wall time:** B13 seconds; B12 tens of seconds at 7; B14 dominated by the judge's own 768
  reference moon runs, paid again in every process. If `echo`'s own B14 or B17 phase exceeds the
  60 s limit on this box, those rows are machine-VOID whatever the law: I check echo first and
  report it as such.
- **Controls:** echo passes all four; planted-kick fails B12 and B13; planted-notide and
  planted-apsides fail B14; planted-average fails B17. These prove the gates still bite through
  the same `restricted` path the plane answers.
