Working...
Check complete. `check.md` written to the run folder; nothing else touched; tree clean (patch applied for reproduction was removed).

**Verdict: gold.**

Summary of the check (45 min, all runs well under 2 GB):

- **Reproduction — exact.** All three dossier commands regenerate every stored number bit-identically (`run 1 600` 21 s, `run 100 600` 35 s, `run20 1 600` 41 s), including engine counters (kicks 244034, refused 680163) and the source calibration (≤ 0.1 root units). The sweep's 8 stored rows also reproduce exactly; my sweep died at the same 600 s wall cut as the author's, corroborating that header note.
- **Predictions — genuine.** `predictions.md` (17:20:24) precedes all decisive outputs (17:21:42–17:25:06); P1–P5 held, and P6's timing miss (predicted >10 min, measured 37 s) is honestly reported and then exceeded (`run20` denser than predicted).
- **My five attacks — all survived:** gm 1/9 (111× mass: 44 rebinds, all in the swept range, 0 drops/0 disagreement/0 oracle mismatch); β = 0.99999 kinked and mutual ×0.9 (one order beyond the author's worst case); combined moving-observer × kinks × stale jumps; jumps every 30 frames; and a direct G(t)-monotonicity probe — 0/44 downward jumps at rebinds, confirming the dossier's bracket-contract mechanism. (My first audit instrument false-alarmed on the kick-free control and was discarded — the two-sided-control discipline working as intended.)
- **Nits found (recorded, none load-bearing):** the 0.9c case's 0-swept-kinks explanation is wrong (kinks fall early in the flight, not "first light later than the window"); "~60 rebinds at log2 20" overstates the measured 3–22; the "~4e-8 relative" deflection is mostly a mass-independent baseline — the 1/999 source's own tide is ~6×10⁻¹¹ relative, making the empty regime claim *stronger*.
- **Novelty/goal fit:** the premise is representation.md §2 / open rung r6; the kinked family and the thrust-scope note are new, adoptable in one step with no engine change.
