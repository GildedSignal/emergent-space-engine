# Predictions (written before the probe; tuned on nothing)

Probe: `probe_index.py` — toy belt screening, structural truth (envelope overlap × synodic sweep ≥ π within horizon T), NOT physics. Two axes:
- **Dilution axis:** fixed region [1, 1.5] AU, N = 2k→32k (density ∝ N). This is the board's top scaling risk as stated.
- **Concentration axis (formation):** N bodies on one orbit (σ_a = 5e-4), the 6 Oct co-orbital case.

Indices compared: **A** = envelope-overlap enumeration (element-sort tier); **B** = phase-rank-k among overlap partners (matching-engine style). Maintenance = endpoint swaps per kick under κ kicks/orbit (plane: 32).

| # | Prediction (held-out; tuned on N=2k only) | Kill criterion |
|---|---|---|
| P1 | A's work per real conjunction grows ≈ N^1.0 on the dilution axis (pairs ∝ N², encounters ∝ N) | flat work/encounter for A |
| P2 | B with k=4: zero missed conjunctions at all N on both axes; work per real conjunction ≈ constant (≤ 8 evals + maintenance) | rank needed for zero miss grows with N, or any miss |
| P3 | Pericenter-key maintenance: swaps per kick per body grows with local density (∝ N on dilution axis); phase-key stays N-independent where relative drift is small (formation) | swaps flat in N for pericenter key |
| P4 | Formation: A pays ≈ N²/2 evals (the 135×/40 TB structure); B pays N·k | A sub-quadratic on the formation |
| P5 | The rank needed to keep zero misses concentrates in the high-e tail (misses at e 0.7–0.9 for radial-window filters, per r8) — a two-tier add-back, not a wider first tier, is the right shape | misses spread uniformly over e |

Numbers I commit to in advance (2σ): A work/encounter at N=32k dilution ≥ 8× its N=2k value; B work/encounter at N=32k ≤ 2× its N=2k value; formation A evals ≥ 10⁶ at N=2k fleet... (adjusted: fleet N=4k → ≥ 4×10⁶ pairs).
