# Predictions — 20261009-0709-second-20261009-0621-system-7f97-1eca (second author)

Written before any run of the split. What I already know (not held out): the uniform
sweep of the first run (B13 60/64 at S=7 falling to 3/64 at S=4; B17 PASS at 4–6,
FAIL at 3) and the checker's S=9/10 degradation (58/64, 53/64 — B13 is not
cadence-limited past S=8). What is held out: everything about the implemented
clock-path split itself. I have not run a single line of it.

**The experiment.** The split (crates/universe, env `UNIVERSE_CLOCK_SPLIT=1`): the
clock's Δs is re-derived at every kick from the body's own dimensionless coupling
κ = U_P(x)/c — one bit of Δs per octave of κ, anchored at κ = 1 (the doll's edge,
where U_P equals the doll's c) at the configured `step_log2` (the shipped 7), floored
three octaves below (the bulk: 16 kicks per P_D). Shells for one planet, κ = R_H/r:
r ≤ 2R_H → 2^7, (2,4]R_H → 2^6, (4,8]R_H → 2^5, r > 8R_H → 2^4. The in-doll
`plan_interval` path is untouched. With no env set the law must be bit-identical.

- **P1 (B13, the passage instrument).** With the split, B13 lands within 2 of the
  shipped 60/64 (58–62) with worst ΔE within ~3× of 2.1e-2, and the same 9
  oracle-domain draws replaced. Reasoning: the flyby's error is made where U_P is
  within a factor ~2 of its edge value (the k=7 and k=6 shells), which keep the
  shipped resolution; the (4,8]R_H shell carries ≤ 1/4 of the coupling at 4× coarser
  kicks — second-order there. Named risk: the approach lag — a k=4 step spans
  ~5.7R_H near 8R_H, so a diving ship takes its first fine kick only at ~2–3R_H; if
  B13-split < 56/64 the lag is the cause, and the cure is a forward-looking κ (the
  trajectory's next periapsis, which the law already reads for crash planning) —
  that would be the next experiment, and the split stays silver.
- **P2 (B17, the resonant bulk).** PASS — and because the moons' conjunction
  distances are ~0.6·sep against R_H = 0.022–0.069·sep (κ ≈ 0.03–0.05 < 1/8), every
  kick sits in the k=4 shell, so the split is *bit-identical* to the uniform S=4 run
  the first author measured: pump [0.9905, 1.0028], libration 0.981, 34/34 regimes.
  If any number differs, my κ-shelling argument is wrong somewhere and I must find
  where before claiming anything.
- **P3 (B12, errors never compound).** On the shipped scene, B12-split's median
  growth exponent is within 0.1 of B12-shipped(7) and its worst err within ~3×. The
  re-derivation is a composition of exact flows (each step's Δs a pure function of
  the integer state at its kick), so no new compounding channel exists in the map;
  the honest risk is the carries: fewer, larger kicks quantize differently, and B12's
  horizon (repeated R_SOI crossings) is where that would show.
- **P4 (the belt cost run — the clock path's own number).** On a belt of 2,000
  clock bodies (a ∈ 1.8–3.6 AU, e ≤ 0.25, no fleet, no player), kicks per game-second
  fall ~8× against the shipped cadence (every belt body sits at κ < 1/8 → k=4, so
  the frontier is exactly the uniform S=4 bulk rate), boundaries fall with them
  (one boundary per clock step), and the digest changes (the law changed; that is
  the point). Wall time falls roughly with the kick count.
- **P5 (the bench scene, the conflation named by the checker).** The shipped bench's
  kick stream is dominated by in-doll leavers (the `plan_interval` path, untouched by
  the split), so the split moves its kick-bench samples only marginally: 126–250
  against uniform-7's 630. The first run's "5× off the bench" was mostly the in-doll
  path moving with `Config::step_log2`; the belt run is the clock path's honest
  number, and I will report the bench as the in-doll-dominated scene it is.
- **P6 (default-path bit-identity).** No env set: the bench digest is 21c73edc… and
  B13 is exactly the shipped 60/64. This is the control on both sides: if it breaks,
  every comparison above is void.

**Decision rule (pre-registered).** If P1, P2, P3 and P6 hold, the split is validated
on the shipped gates — one rule (κ-anchored, Sundman-sloped) replacing the doll-wide
constant, 8× bulk saving with the passage resolution intact — and the claim is gold
against the checker's named experiment, with the belt run as its cost leg (P4) and
the S=9/10 saturation folded in (the claim never says cadence fixes passages). If P1
fails at 56–57/64 I report the split as real-but-not-adoptable-yet (the lag) and name
the forward-looking κ. If P2's numbers move at all, I stop and re-derive before
claiming anything about B17.
