# Predictions — the cursor for gravity-at-c (run 20261005-1540-q-gravity-cursor-05b0)

Written before any of the decisive runs (`exact`, `cost`, `burst`, `laplace`).
Smoke compile checks only before this file. All numbers below are predictions, not
measurements; what happened is appended in the dossier.

Setup: integer worldlines (i64 times and positions, c = 1), consumer steps obey
|Δx|² ≤ Δt² in integers (law "nothing past c"), so the past cone of a later kick
contains that of an earlier one — k\* is non-decreasing by theorem, and the cursor
(one while-loop of squared-form tests per kick) must equal brute force exactly.

- **P1 exactness.** Cursor == brute-force `max{k : t ≥ t_k and (t−t_k)² ≥ |x−x_k|²}`
  at 100% of kicks, over ≥ 10⁷ kick tests: β_consumer, β_source ∈ {0.1, 0.3, 0.5, 0.9}
  (including head-on closing pairs), news rates λ from 10⁻² to 10² events per
  light-crossing, plus exact lightlike ties ((t−t_k)² = |x−x_k|² must count as arrived)
  and a 1000-event burst. I predict zero mismatches and zero backward moves of k\*.
  Any mismatch means either a cursor bug or that quantized steps broke cone inclusion.
- **P2 cost.** Mean integer tests per kick per source ≈ 1 + (news events entering the
  cone per kick), independent of history length K; brute force costs K per kick. The
  bound total tests ≤ total kicks + total events holds exactly (each test either
  advances — at most once per event — or is the single failing test of one kick).
  p99 ≤ 3 tests/kick at λ ≤ 1. Worst single kick = burst size + 1 (then back to 1).
- **P3 Laplace control through the cursor** (equal-mass binary, c lowered so
  v_orb/c = β; version recorded every step; news = evaluate version k\*'s Kepler
  elements at now):
  - naive retarded (pull toward the position at t_ret) spirals out: unbound
    (e ≥ 1 or a doubles) within 8 orbits at β = 0.3 and within 25 at β = 0.1;
  - news via cursor stays bound: |dE| < 5×10⁻³ and |Δa|/a < 1% over 100 orbits;
  - inst stays bound: |dE| < 10⁻⁵;
  - the cursor-driven and brute-force-selection news runs are **bit-identical**
    (same versions selected at every step ⇒ same float ops).
- **P4 lag and memory.** Version lag (newest − k\*) ≈ (separation/c) / dt exactly in
  the every-step policy; with a news-only policy (record only real news), a pure
  binary generates 0 news events (two-body elements are exact), so history per source
  collapses to one tube (16 B) + one cursor word (4 B per body–source pair) — against
  the every-step ring's 16 B × cadence × light-orbits.
- **P5 galaxy scale (analytic, stated per scale).** Star-system retention
  R_infl/c is hours (Sun's doll, 50 AU: ≈ 7 h) ⇒ depth ≈ 1. Galaxy scale: a cell's
  ghost lives (cell radius)/c ≈ 3×10³–3×10⁴ yr; alive ghosts per cell = news rate ×
  retention ≈ 10⁻⁴–10⁻³ (sparse). That case requires ghosts to ride generators (the
  cell's orbital program: zero kicks) — a stepped ghost would roughly double the
  body count for the retention window.
