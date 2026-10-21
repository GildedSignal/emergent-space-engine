# notes.md — 20261021-1346-second-20261021-0429-scout-451f-8833

Second author on 451f (fleet-doll-speed). Timeline and decisions.

1. Read 451f's dossier, the checker's check.md, the corrected wiki page. The
   gold experiment: fix the IC sign (u0 − Γ(u0,w)) and the O(h) E-freezing,
   rerun angles × β × rp{18,100} + τ shapes, then read the sign-fixed in-plane
   excess (~9× z) — law or prey.
2. Built falsifier.py from 451f's with the two fixes, vectorized member RHS
   (guarded: rhs_check 4.4e-16 vs the original loop), τ-growth snapshots, and
   honest controls (eigen vs 4c79, u·u drifts, orthonormality — the three
   numbers 451f left unregenerable are diagnostics here).
3. Control runs exposed a real instrument bug beyond the checker's two: the
   log-map's quadratic term projected the Christoffel upper index on the
   vector tetrad, not the dual (round-trip bias up to 20·u² in-plane). Tested
   old vs dual against the TRUE exponential map (geodesic-integrated): dual
   wins 5–417×. Adopted as fix 3, measurement-licensed (mapcheck.json).
   Also normalized the member IC tangent: the truncated transport's O(ξ²)
   norm violation (up to 0.13 = a clock-rate artifact) is parameterization,
   not physics. udrift0 → 1e-15.
4. predictions.md, then the grid + conv ladder. Result: err = k·u EXACTLY
   (spread ≤ 7% over 2.5 decades). 451f's c₂ = k/u_max artifact. Frozen-repro
   ties 451f's stored z (8.4e-5 rel at 1e-4); fixed z@1e-4 flat under 8×
   refinement.
5. The linear channel could still be the propagated O(ξ²) IC truncation.
   Wrote the addendum prediction (A: physical; C: convention), then ran the
   exact-IC grid (all-order parallel transport along the true exponential
   map). C held: in-plane k drops 12–100×; the physical channel is
   near-isotropic, ∝ M/r, along suppressed ~10×. The τ-linear drift
   fingerprint confirms the convention channel.
6. Deliverables: falsifier.py (modes control/mapcheck/flyby/flyby2/conv),
   analyze.py → analysis.txt (every dossier number), regen.sh (2.5 min,
   asserts all controls), dossier.md, wiki page with od 1 closed.

Costs: each mode ≤ 60 s; regen 2m24s; memory < 100 MB.
