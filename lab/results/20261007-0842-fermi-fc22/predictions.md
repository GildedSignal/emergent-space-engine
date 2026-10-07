# Predictions (held out before the decisive computation)

Question: is H_live (distinctions created per game-second) bounded in steady play at 10⁹ bodies, and which budget term breaks first on the 8 GB M1?

Anchors already measured (not predictions): the plane store today is 2349 B/body at N = 28 (example `plane 100`), the tube word is 16 B, 8 GB / 10⁹ bodies = 8 B = 64 bits/body all-in.

Predictions for the decisive script (`ledger.py`), cases I have NOT yet computed numerically:

- **P1 (belt gravity scars are void).** For a 10⁹-body belt at a = 2.5 AU, σ_e = 0.02, individual mass 10¹⁵ kg (a 40-km rock), quantum q_v = 10⁻⁶·v_kep: the rate of quantum-crossing gravitational kicks per body per game-second is ≤ 10⁻³⁰ (i.e. identically zero for any canonical purpose).
- **P2 (no belt-body mass makes gravitational scars matter).** The mass per body needed to reach the scar budget threshold (10⁻⁸ crossings per body per game-second, = ~30 bits/body over a 300-hour game) exceeds 10³⁰ kg — stellar. Belt-belt gravitational relaxation can never be a memory term.
- **P3 (collisions are real but negligible).** Physical collisions (contact radius, belt total mass 10²¹ kg) number between 1 and 100 per 300-hour game across all 10⁹ bodies — a ledger ≤ 10⁻⁶ of budget.
- **P4 (the fleet ledger is player-scale, not N-scale).** A 10⁶-ship formation (10⁹ kg ships, torus 10⁵ m thick) at 2.5 AU produces 10³–10⁵ sub-km flybys per 300-hour game; the ledger is bounded by ship deaths (reabsorption), not by fleet size.
- **P5 (throughput does not break).** At the plane's cadence (2⁷ kicks/orbit), 10⁹ bodies at 0.39–5.2 AU need ≤ 3×10⁴ kicks per game-second; with the known averaging lever (0.3 kicks/orbit) ≤ 10 per second. Not the breaking term.
- **P6 (calibration against r8 v2's truth).** My encounter-rate model, evaluated at the rung's geometry (N = 10³, ρ = 10⁻⁴·a, σ_e = 10⁻²), lands within two orders of magnitude of the rung's measured ~10⁻² encounters per body per orbit. If it misses by more, my rates are suspect.
- **P7 (the store is the breaking term).** A tiered store (one Home-like system materialized at tube precision, the rest as birth programs + 32-bit coarse words) fits in ≤ 6 GB at 10⁹ bodies with ≥ 2 GB headroom for the (near-zero, per P1–P4) ledger.

If P1 or P2 fails (gravitational scars matter at reachable masses), the "distinctions decide 10⁹" premise is live and the ledger design becomes the bottleneck. If they hold, the memory bottleneck is the store's representation (uniform tube precision), not dynamics.
