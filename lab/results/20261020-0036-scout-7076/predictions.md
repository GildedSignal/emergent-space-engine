# Predictions — the cadence ladder on the frozen certificates

Written before the decisive experiment. Question: how coarse can `Config::step_log2`
(shipped 7 = 2⁷ kicks per radial period of each tube) go before the frozen gates that
judge the shipped engine (`behave --law plane --plane-step N`) fail? This is the board's
"how many kicks a body really need per orbit", measured on the only legal definition of
"needs" (the frozen certificates), and it re-prices the 10⁹ ledger's mandatory-Carlson
clause (budget-1e9/3aec: at split8 the cost bar is ≤ 4.9 µs/event; bar(N) = 4.9 µs · 2^(4−N)
at plane-step N, since split8 ≡ step 4 and the stream rate ∝ 2^(N−7)).

Controls (must hold before any ladder row counts):
- C1: step 7 (shipped) reproduces the record: B17 PASS, B13 60/64 with the same baselined
  reds (owner `range`, cadence-independent refusals).
- C2: step 6 reproduces HANDOFF's "B17 passes at step 6".
- C3: the `jacobi` example at step 6 stays in the shipped test's judged band (worst per
  ship < 1e-4 class).

Held-out predictions (not tuned on):
- P1 (error law): the worst per-ship Jacobi error on the Hill-radius class (example
  `jacobi`, 100 planet periods, ships at 1.5–3 R_H) rises ×4 per octave coarser
  (second-order split), until refusals/deaths break the curve.
- P2 (the knee): B17 (resonance: e-pump ratio in [0.8, 1.25], the regime r4 killed
  arc-integrated kicks in) is the first breaker, and the first failing octave is step 3
  (16× coarser). PASS at 7–4 (the 8× legality is the cited-not-reflown 7f97/1db4 row),
  FAIL from some octave in {3, 2}.
- P3 (B13): the flyby gate keeps 60/64 (the same 4 baselined reds) down to step 4, loses
  ≥ 1 further row at step ≤ 3 (the perijove arc unresolved: ΔE/ΔL 1% bars).
- P4 (B14): "times out" at the shipped cadence on the plane; at step ≤ 3 it finishes
  under the 60-s watchdog (fewer kicks), and its precession rows (10% bar) are the
  deepest-tide class — I predict it FAILS at step ≤ 2 but may pass at 3–4.
- P5 (composition): if the knee k* = 3, the Carlson bar becomes 9.8 µs — Carlson still
  mandatory but at 2× the slack (cd6e's composed kick 8–19 µs straddles it); if k* = 4
  the composed clause stands; if k* ≤ 2 today's measured M1 belt item cost (~26 µs)
  fits without Carlson; if k* ≤ 1 the mandatory-Carlson premise is dead outright.

Kill criteria for my own reading:
- Gates PASS at every octave to step 0 (1 kick per radial period): the cadence lever is
  unbounded by these certificates — the mandatory-Carlson clause dies; report as the
  finding (a premise kill), not as "the gates are wrong".
- Gates FAIL already at step 5 (4×): the composed split8 legality (cited, not re-flown)
  is in question — flag as a premise break in the other direction; check twice before
  claiming (load, PLANE_TRACE).

Domain, honestly: the gates judge the strong-tide restricted class (μ = 1e-3, sep
5.27×10⁸ M, Hill-radius ships, perijove flybys, 2:1/3:2 resonance) — the conservative
floor. The belt-real class (2⁻¹⁰ planet at 0.39 AU, belt at 2–3 AU) has far weaker
synodic coupling; its legal cadence can only be deeper, so the ladder's knee is an
upper bound on the needed kicks (a lower bound on cost slack). B12's in-tree verdict is
recorded with its caveat (the instrument under redesign, v3 not qualified) — it informs,
it does not decide.
