# Predictions — written before the decisive runs

Scene: the shipped `restricted` CRTBP (star + one planet, sep 5 AU, radius 47,400 root
units, `Config::default()`), driven only through public API (`Universe::new`,
`add_body`, `add_doll`, `add_body_state`, `start`, `advance`, `input`). The prior run
(20261018-0543-taleb-6de0) diagnosed the μ=1e-2 runaway as a root-clock event storm
(kick ratchet + dt collapse, `dt = A/y`, `y = v²/2`) and called it "a latent clock
defect at any mass awaiting one positive-H_D ejection". Nobody has minted the ejection
at the flyable mass. These predictions are frozen before any arm runs past its smoke.

Arms:
- **P** (decisive): μ = 2⁻¹⁰ (the flyable/fiducial μ≈9.8e-4 of the chaos scenes), a
  Player ship born bound (circular 5 AU, 90° from the planet), clock constants derived
  bound, then a real burn through `input` to ≥1.2×v_esc, released, coasted.
- **S**: μ = 2⁻¹⁰, a Ship minted unbound from tick 0 (constants derived unbound).
- **B**: μ = Mass::ratio(1,99) ≈ 1.01e-2, same IC as S (reproduction arm, ties to 6de0).
- **C**: μ = 2⁻²⁰ ≈ 9.5e-7, same IC as S (mass scaling).
- **D** (control): μ = 2⁻¹⁰, Ship born circular at 6.5 AU, never burnt.

## Frozen predictions

- **P1 (the ratchet is mass-gated in rate only):** in P, after release, |v| grows
  one-signed beyond every bound-orbit value (exceeds 3×v_circ within the first 10⁵
  events) and the clock interval falls monotonically (allowing ±1 doubling noise) —
  the storm 6de0 saw at μ=1e-2 reproduces at the flyable mass.
- **P2 (freeze reachable in an affordable budget):** P's interval reaches ≤128 ticks
  (the shipped `MIN_STEP`, which `kick_clock`'s own path ignores) within 3×10⁶ ship
  events; S freezes too (I accept a factor ~3 either way between P and S: the birth
  constants differ).
- **P3 (the leave edge never collects it):** in P and S the ship's radius stays
  < 2³⁵ root units at cap (leave edge = 2⁴⁰); at the measured per-event displacement
  the remaining distance to the edge costs ≥10⁹ further events — the storm outlives
  any session and any frame budget.
- **P4 (frame ruin, the cost number):** once P's interval ≤ 128, one 338,375-tick
  frame (the ladder belt's measured frame) carries ≥3×10⁵ events for this ONE body
  (the belt population's measured dues: 1.64/frame, 11,700 bodies), at the measured
  wall cost per event ≥ 0.1 s per frame — the frame is dead by ≥4 orders.
- **P5 (mass scaling of the mint):** the mint rate d|v|/d(event) in B exceeds P's by
  ~10× (Δv/kick ∝ μ_p at fixed geometry and clock constants), and C at 3×10⁵ events
  has not frozen (interval still ≥ 2⁸) — freeze event count scales ∝1/μ.
- **P6 (the control is a control):** D holds a healthy cadence — interval stays within
  2× of its initial value over ≥2×10⁵ events, |v| stays within 10% of circular, no
  monotone growth, alive, zero refusals.

## Kill criteria for my claim (what would falsify it)

- P's interval does NOT collapse monotonically, or |v| does not grow one-signed past
  escape: then "latent at any mass" is wrong, the storm is μ=1e-2-specific — also a
  result, and 6de0's latent-defect sentence dies (scoped, with the measured trace).
- P freezes but the leave edge collects it within ≤10⁷ events: then the storm is
  self-bounded and the ruin claim shrinks to a bounded stall, not a permanent one.
- D collapses or refuses: the instrument is broken (VOID, no claim).

## Honesty notes

- P and S are not tuned: burn target 1.2–2×v_esc, whatever level reaches it cleanly;
  the frozen-regime frame window is measured once, not selected among trials.
- Wall/event caps: P,S ≤ 4×10⁶ events or 100 s; B ≤ 2×10⁶ or 80 s; C ≤ 10⁶ or 60 s;
  D ≤ 5×10⁵ or 40 s. Cloud timings, orders of magnitude only.
