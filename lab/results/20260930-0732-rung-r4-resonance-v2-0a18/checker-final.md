Working...
Check complete. Deliverables: `metrics-check.json` (bit-identical to the author's) and `check.md`, both in the run folder; nothing else touched, no git operations.

**Verdict (verdict.py): KILL of arc-g8, arc-g16, arc-g8-half** — positive control passes, both negatives fail as required, no disputes.

**Reproduction** — bit-exact: all law JSONs, ic-scan, and all 40 sample arrays identical from the author's scripts in a clean tree; my metrics-check recomputation matches every digit. `predictions.md` predates all decisive outputs; its four predictions held.

**Independent audit** — implementation is sound: all four Gauss rates match FD of my own restricted acceleration to ≤4×10⁻⁷; truth oracle matches my DOP853 (rtol 10⁻¹²) to 6.7×10⁻⁵ in e over 20 synodic, and a 4800-step extension confirms ladder convergence; my from-scratch law reimplementation reproduces the author's bit-for-bit.

**Attack sharpened the kill:** window-refinement to 512 kicks/orbit converges to a limit that still over-pumps ~2× — the flow map is exact at generic phases but carries a constant-in-h +5.8% bias at conjunction-phase windows, so the failure is structural to first-order-in-μ arc integration, not quadrature or window scale (explains g16 pumping harder than g8). Two fidelity findings reported: (1) the author's `w2 = 4.0` radian reading gives truth R = 0.227 vs the rung's frozen 0.867 (4° gives 0.830) — unflagged by the author, but verdict-robust (arc-g8 fails that case 3.86×/0.041); (2) the truth JSONs were patched post-hoc (`windows`/`orbits`) because `metrics.py` crashes on `r4v2.py truth` output as-is — physics unaffected, but undisclosed. Micro-window inflation confirmed harmless (2.4×10⁻⁸ of real kicks); the libration-metric degeneracy at exact commensurability verified (`none` → R = 1.000 exactly).
