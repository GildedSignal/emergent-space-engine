# Predictions (written before bars.py ran)

The bars are derived from shipped constants only (client `xtask/src/universe/page.html`,
scene `crates/universe/src/scenario.rs:333`, law `docs/law.md` line 12) and the published
drift law (f5bd, on lab/wiki/library-directions.md). Held-out: none of these numbers has
been computed yet in this run.

- **P1 (the view's bar, q_view):** a belt body is drawn as a 2×2 px rect (`kind===4`,
  bodyPaint); the player differentiates a body's phase only against its neighbours, so
  q_view = (half the mean inter-neighbour separation)/r_mid, belt area π(3²−2²) AU²,
  r_mid = 2.5 AU = 1247.5 ls (AU_LS = 499.004784). Predict: **0.1–0.2° at N = 10⁵**,
  **0.03–0.07° at 10⁶**, and **(0.7–3)×10⁻³° at 10⁹** — the 10⁻³° class, scaling N^−1/2.
- **P2 (the contact's bar, q_contact):** the finest delivered miss quantum b* = 49 m
  (encounters page, ev = −45 coarse end), r_mid = 2.5 AU. Predict q_contact = b*/r_mid
  lands at **(5–9)×10⁻⁹°**, i.e. 6–8 orders below q_view(10⁹) and **strictly below the
  law's acting angle grid q_grid = 360°/2³² = 8.38×10⁻⁸°** (the tube's 32-bit periapsis
  angle). If instead q_contact ≥ q_grid, the angle channel could carry contacts and the
  margin representation (cf2a direction 1) is not forced by arithmetic.
- **P3 (the mass bar never binds):** the aggregate's dipole noise from per-body phase
  errors, as a fraction of the host's field at any consumer, = (M_belt/M_host)·θ/√N.
  Predict **≥ 10 orders below 1** for every M_belt/M_host ≤ 10⁻³ and N ≥ 10⁵ at θ =
  q_view(10⁹): the mass certificate has no angle bar of its own.
- **P4 (the fence never fires where we can fly):** with the bar at q_view, the belt's own
  measured max drift (2.2×10⁻³° at 7.41×10⁶ game-s, f5bd) is crossed only if q_view <
  2.2×10⁻³°. Predict: **q_view(N) > 2.2×10⁻³° for every N ≤ 10⁶** (zero belt re-kicks on
  every flight the harness can run to 8×10⁶ gs), and at 10⁹ the fence k* = T*(q_view) ×
  3.55×10⁻⁵ ev/B/gs lands at **k* ∈ [150, 300] carried kicks**, so the re-kick costs
  0.51–0.6/k* **≤ 0.5% of the deleted stream** (Musk's 10% add-back test passed with ≥ 20×
  margin).
- **P5 (the quotes):** all five quotes verify byte-identical against the fresh Readwise
  cache (verify_quotes.py exits 0). This is the run's held-out instrument property.

Kill criteria for the freeze as a whole: P1 landing coarser than 1° at 10⁹ (then the view
stops being a meaningful consumer at all), or P2 landing above q_grid (then contacts stay
an angle-bar question), or P4's k* < 30 at 10⁹ (then the re-kick is > 2% of the deleted
stream and the compose rung must carry it as a cost term).
