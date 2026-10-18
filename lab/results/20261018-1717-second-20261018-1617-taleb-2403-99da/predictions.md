# Predictions — 20261018-1717-second-…-99da (second author on 2403)

Written BEFORE the decisive K = 6.5×10⁵ flights (the 10⁵ arms below are calibration in
already-measured territory: 2403's two checkers flew 10⁵ coast/burn; my bands for those
arms quote their record, not my tuning). The named gap (check2.md): the 10⁶ burn arm,
"sliced" under this window's 2 GB process cap — true 10⁶ builds at ~2.3–2.4 GB (b_per_body
≈ 2.35 kB × 10⁶), so the slice flies the largest K that fits: 6.5×10⁵ (build ≈ 1.53 GB,
end ≈ 1.6 GB, view gather self-skips by the example's own 55 s guard). That covers 81% of
the log-distance from 10⁵ to 10⁶; the last 19% rides the measured per-body law (P5).

All ladder arms: `nladder <K> coast|burn 15 100 <budget_ms>` (15 wall-s, rtf 100, budgets
12 default / 24 / 5). Conventions fixed before the flights: distinct = census classes t+L;
the cut is game time ≥ 150 s on BOTH sides; the multiplier is λ_distinct(burn)/λ_distinct(coast)
in that window, both arms flown by this run's harness.

- **P1 (coast arrivals are K-flat).** k650-coast entries within [0.85×, 1.15×] of my
  n100k-coast count, and census class t ≥ 80% of distinct. A count far above 1.15× breaks
  K-flatness (weakens the fence arithmetic); far below means frames lagged (named, not fatal).
- **P2 (the multiplier carries; the claim's core).** same-convention distinct ratio at 6.5×10⁵
  in **[6, 40]** (measured 12.8× at 10⁴, 13.2× at 10⁵). **Kill: < 2.**
- **P3 (the drain loses ground as service scales with K).** held_max (probe, burn 12 ms) at
  6.5×10⁵ **≥ 400** and ≥ my 10⁵ value; upper band 6,000 (it is load-elastic: quote the band,
  not the point).
- **P4 (margin restores service — the budget pair).** held(burn, 24 ms) ≤ 0.25 × held(burn, 12 ms).
- **P5 (the per-body law anchors the 10⁶ slice point).** b_per_body at 6.5×10⁵ in
  **[2200, 2500] B**, implying a 10⁶ build of 2.2–2.5 GB — over the cap: the slice is forced
  by a measured law, not chosen.
- **P6 (the backlog costs memory, and burn more than coast).** foot_end − foot_build at
  k650-burn in **[+15 MB, +250 MB]** and strictly greater than k650-coast's drift.
  (2403's original P6 failed here: it promised ≥ +100 MB and measured +21 MB, then marked it
  held. This band is written to be checkable against the log as written.)
- **P7 (derived, not flown).** the 10⁶ wall under continuous burn = 8 GB ÷ (λ_distinct_burn ×
  (10⁶+38) × 224 B) — expected band **[15, 150] game-s** from P2's ratio and the 10⁵ anchors.

Outcomes are filled in the dossier exactly as the log reads, held or not; no band is edited
after a flight.
