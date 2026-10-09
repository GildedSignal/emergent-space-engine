# Predictions — 20261009-0621-system-7f97 (written before any run)

Question: is the plane's kick cadence (`Config::step_log2 = 7` → 2^7 = 128 kicks per
radial period / passage, the same fraction for every body, regime-blind) a tick in
principle 14's sense — work with no validity claim behind it?

Cases below are held out (not tuned on): I have not run the plane at any step_log2
other than the default. Prior knowledge I do carry: B17 is documented to pass at
steps 4–6 (H0215); q-cadence's float replica put the behaviour frontier at 4–16
kicks/orbit for moons (f ≤ 0.45 R_H); six runs killed correctors.

- **P1 (B13 assists, the passage instrument).** ≥ 99% of 64 flybys within 1% of the
  reference's ΔE, ΔL at S ∈ {5, 6, 7}; still ≥ 99% at S = 4 (16/orbit); below S = 4
  the pass rate falls below 99% (the in-doll passage resolution binds).
- **P2 (B17 resonance, the phase-feedback instrument).** Passes at S ∈ {4, 5, 6}
  (documented); at S = 3 the e-pump ratio leaves [0.8, 1.25] — resonance is the
  regime where cadence is load-bearing, so the floor is regime-specific, not global.
- **P3 (cost).** Kick events per game-second fall ≈ 2× per unit of S removed, with
  per-kick price roughly flat, so S = 7 → 4 is ~8× fewer kick events on the same
  scene; total event count (kicks + boundaries + opens) falls by the same factor
  (kicks dominate the count).
- **P4 (H_live feed does NOT fall with cadence — the negative I expect).** The
  sigma-delta carry (step.rs `quantize`) releases velocity quanta at the total rate
  the tide supplies them, independent of how many kicks carry them: distinctions per
  orbit ≈ (tide Δv per orbit)/(velocity quantum), so lowering cadence does not lower
  the distinction rate, only the event and recompile count. If a measured quanta
  counter contradicts this, my reading of the carry is wrong and H_live *is*
  cadence-fed.
- **P5 (error type at the floor).** Where a gate fails at low S, the failure grows
  with horizon (walking/secular, B12's per-seed exponent rising with lower S on the
  same seeds), rather than appearing as a bounded oscillation. If exponents stay
  ~flat while pass rates fall, the failure is error *size*, not type, and lowering
  cadence globally is merely a threshold choice, not a representation question.

Decision rule (pre-registered): if P1 and P2 hold, the plane's default cadence is
8× above the behaviour frontier for the bulk and the cadence should be owned by the
same per-body validity budget the jet and the encounter skin read (one certificate,
three consumers). If P1 fails at S = 4, the frontier is tighter than the float
replica said and the cadence question collapses back into q-cadence's surface.
