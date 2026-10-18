# Predictions (written before the decisive experiment)

Topic: encounters open direction 1 (cd3b's "one missing constant") — per-kick certificate
churn at 10⁹-scale cell occupancy. Mechanism class: kinetic-data-structure flight-plan
updates (Basch–Guibas: a moving object's update recomputes its certificates' failure
times, not the structure) + MD Verlet-skin deferral (re-arm on slack exhaustion, not per
kick). fe6b's 0.0346·n is read as pairs re-checked per kicked body (346 µs at n = 1e4,
1 µs/arm — the reading that reproduces cd3b's "10¹–10² cores after split 8").

Toy: planar 2-body-Kepler belt cell at the shipped 10⁹ 2-D density (1e9 over
pi·(3²−2²) AU² = 6.37e7/AU²), e Rayleigh 0.07 (the ladder belt), occupancies
n ∈ {1e2, 1e3, 1e4} at fixed density (cell width W = n/(ρ·2π·a)), horizon 8 intervals =
1.81 mid-belt orbits (shipped rebuild), kicks dv/v = 2⁻²³ at random anomaly/direction
(p99 arm 2⁻²⁰, and 2⁻¹⁷ for the linearity/falsification arm). Arming = the shipped
tier's Phase-A shape: armed iff a mean-longitude meeting lands in [t0,t1] with the
crossing longitude in the pair's B = 5e5 m reach arc (cd3b's conjunction reach).

- **P1 (baseline, the fe6b structure):** wholesale re-arm candidates per kicked body =
  n−1 (Θ(n), slope ≈ 1). The toy's own constant; no claim it equals 0.0346 (fe6b's X
  and anchor are not in the record I can read here).
- **P2 (the missing constant):** armed flips per kick per body ≤ 0.01 in the dilute
  cells, slope < 0.3 in n; and the re-arm-relevant near-horizon band (partners whose
  first-meeting due sits within [0, H + margin]) measures ≤ 0.1 per body at n = 1e4 —
  the slack-aware per-kick work. [Amended before any run: the band is predicted to grow
  ∝ n² at fixed density (n·W ∝ n²) until the physical event floor — so the letter "O(1)
  in n" is expected FALSE while the absolute number fits the budget at the shipped
  cell sizes; both are measured, and the cell-size law is itself a design output.]
- **P3 (the due-walk geometry, amended before any run):** per-kick due-move is
  multiplicative, δdue ≈ due·(δn_i/Δn_pair): median cell-mates (due ~ 1e5 intervals)
  walk 1e3–1e4 intervals per 2⁻²³ kick — huge — while in-horizon pairs (due ≤ 2H) walk
  < 0.1 intervals: the walk is small exactly where arming is decided, which is what
  makes slack sound (b509's fleet "< 10⁻³ intervals" measured the in-window class).
  Moves scale linearly in dv across 2⁻²³/2⁻²⁰/2⁻¹⁷.
- **P4 (failure regime, named):** in the concentration arm (n = 1e4 packed 1e3× denser,
  shared-a phase-concentrated fleet-class cell) the standing/near set per body grows to
  ≥ 1 and flips/kick ≥ 0.1 — concentration is where per-kick O(1)-class work fails
  (taleb-09b5's ruin class; b509's 16.8 newly-armed/kick at F = 1e4 is the same class,
  UNVERIFIED constant, different scene).
- **P5 (controls):** (a) closed-form arming is a sound superset of a brute-force
  conjunction scan on a live wide band (0 missed events, extras = superset slack
  reported); (b) a no-margin schedule (horizon = rebuild window, no between-rebuild
  re-arm) loses > 0 events on that band at the 2⁻¹⁷ falsification kick — the instrument
  can fail; (c) the P2 sign reproduces at a second seed.

Kill: flips/kick > 0.1 or band(1e4) > 1 ⇒ deferral does not close the row at the
shipped cell sizes (negative dossier). P5a misses > 0 ⇒ instrument broken, VOID.
