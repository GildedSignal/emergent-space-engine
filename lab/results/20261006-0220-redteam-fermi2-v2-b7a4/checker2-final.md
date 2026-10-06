Working...
**Grade: silver** — written to `lab/results/20261006-0220-redteam-fermi2-v2-b7a4/check2.md`.

**Reproduction (all bit-identical, ≤60 s each):** `sanity.py` 0.7 s, `kernel.py` 50.7 s (`decisive.log` + `kernel-table.json` byte-for-byte), `leakage.py` 3.7 s. `patch.diff` empty as claimed; `predictions.md` (30 m) predates `kernel.py` (18 m). Prior-run anchors (2877, 2395, 16081) verified from the `lab-20261002-0539-redteam-fermi2-21db` branch.

**My attacks confirmed every load-bearing claim:**
- **Artifact mechanism (K4):** the prior line-118 half-angle unwrap yields **1.998 turns** where the honest doubled-angle unwrap gives exactly **1.0000** per prior window at 6/4/3.1M — stronger than claimed.
- **Epoch formula:** matches independent quadrature at 7 new radii to ≤2.6×10⁻⁵; I also re-derived 512π√2·3f√g/√((2−3x)²+g²) algebraically from 256√2·|a−b|/√(a²+b²)·ωT_p — correct.
- **E-independence** exact to 9 decimals for E = 1.05…10; **mirror rotation sign rejected at O(1.8)** vs 3×10⁻¹³ (P3 pinned).
- r = 3.05M: geodesic measurement impossible (members plunge at all windows) — the table's 3.1M boundary is real.
- Prior "eccentric" scene recomputed: r_a = 7.5, e = 0.071 — the rosette relabeling is right.

**Why not gold:** P6's unbound half failed (6898/5320 vs <1500), and three summary headlines contradict the run's own printed tables (P1 "worst 9e-4" vs actual 3.5×10⁻³ at parab outbound; "transverse ≤2×10⁻⁴ at every scene" false at three scenes; "einsum 4+ digits" false at 3.1M) — plus the "5.57-orbit window" parenthetical misstates the prior 23.6's actual 1.64M window. Data all honest; sentences overstated. The gold path: derive and hold-out-validate the unbound amplitude-drift law, correct the three sentences.

Run folder left as found apart from `check2.md`; scratch files removed.
