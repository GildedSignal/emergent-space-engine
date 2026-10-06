# Predictions — dormant deferral of encounter setups (components lens)

Written before the decisive run. Component: the encounters re-certification path
(`crates/encounters`), the board's top scaling risk; the open lead from taleb-3ec1
("99% of setup work lands on dormant pairs, defer it"), listed under "Next, not started".

Design under test: a pair pays setup once per element change (as now), but its next
in-window passage becomes a **wake** on a calendar (one exact `first_hit` query); the
exact checks run only when a wake fires, and a kick on either body re-derives the wake
instead of re-enumerating the whole horizon. Exactness: elements are fixed between
kicks, so a wake derived at kick time stays valid until the next kick on either body.

- **P1 (recency law).** On the `kick` workload (n = 10 000, σ_e = 0.01, ρ = 1e-4,
  horizon 1000 orbits), ≥ 80% of the exact-check evaluations of one re-certification
  land on passages more than 10 orbits ahead of the kick.
- **P2 (stream gain).** Under a Poisson kick stream (τ ≈ 25 orbits per body), deferred
  wakes cut total evaluations ≥ 5× versus per-kick full-horizon enumeration, with
  identical encounter lists per inter-kick segment (zero misses, zero extras).
- **P3 (width penalty).** Replacing numeric windows by the analytic arc-cap window
  (zero setup evaluations) raises the wake rate ≤ 20×; if it is worse, deferring setup
  itself is not worth it and only the checks defer.
- **P4 (risk, named).** Numeric-window setup evaluations may dominate per-kick cost and
  are NOT deferred by wakes (still paid every kick). If so the gain is bounded by the
  check + walk fraction, and the honest dossier says so.

Held out (not tuned on): a second density (σ_e = 0.05) and a second ρ (2e-4), plus the
checker's own adversarial picks. Falsifying P2 (gain < 5× or any miss) kills the
deferral configuration, not the method.
