# Predictions — 20261013-2252-second-20261013-2130-library-ae3d-7497

The experiment (the checker's named one): log kicks per body per orbit on shipped
scenes (the `plane` scenario the benches fly), with the changeover level and the
clock flag per kick, and read the shape of the per-body distribution. Written
BEFORE any probe of my own runs (nothing measured yet; the priors below come from
the wiki: 27ce, 7f97, 174d/0f2a, fermi-367f — not from this run's data).

Cases I have not tuned on, and what I expect there:

- **P1 (the tube bulk is flat per orbit, by construction).** Planets, the moon,
  the orbiters and the skimmers step at `step_for` = 1/2^6 of their own radial
  period, so after per-orbit normalisation their kick counts agree within ~2×
  (alignment stubs, exit caps and sub-kicks near passages account for the rest).
  Coefficient of variation across those bodies ≤ 0.5 on the idle scene. Per
  game-second the same bodies span ≥ 2 decades of rate, purely as 1/P_orbit
  (orbital frequency, not surprise).
- **P2 (the clock bodies are regime-spread).** The root-doll haulers and the
  player run the v2 clock, whose step is regime-scaled; expect ≥ 10× spread in
  kicks per orbit across the 12 haulers (far-field steps are far longer than
  1/64 of the period), and the spread to be state-dependent, not constructional.
- **P3 (the head is real and sparse, when anything happens).** On a scripted
  burn flight the player alone takes ≥ 30% of the scene's kick events (the
  waterfall: hundreds of items inside a few frames), and passage sub-kicks
  (level ≥ 1) concentrate on the few bodies then engaged: the top 3 bodies carry
  ≥ 50% of all kick events. On the idle scene (no burn) no body exceeds ~4× the
  median per-orbit count and the top-1 share stays < 20%: no head without a
  driver.
- **P4 (the verdict on rule 2).** As a universal ladder rule ("promotion is by
  rank in the surprise distribution") it dies: the shipped per-orbit bulk is flat
  by construction, so rank and a fixed fraction pick the same bodies there. What
  survives is narrower and already scheduled another way: the head (player burn,
  passages, the battle's hand-outs) is light-cone due-ness, which the shipped
  calendar already orders by deadline, not by rank. So the fixed fraction stands
  for the bulk, and rule 2's live content reduces to what rule 4 (buy the option)
  already says.
- **P5 (the battle's stream).** At members = 4,000, resolved events are
  dominated by hand-outs and the fleet origin's own kicks rather than by any
  body's kick stream (fermi: 67% hand-outs at 8 game-s); per-body kicks of
  handed-out members are single digits each — flat across members, no rank
  structure.

Kill criteria for my own claims: if the tube bulk's per-orbit CV exceeds 1, P1
dies and the bulk itself is heterogeneous (rule 2 revives). If the idle scene
shows a top-1 share > 30% with no burn, P3/P4 die and the rank rule stands as
written. If the burn flight's player share is < 10%, P3 dies.
