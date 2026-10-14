# Predictions — 20261014-1137-fermi-1738 (written before the decisive run)

Question: does the published 10⁹ encounter wall (7.7×10³ cores skin-on, "1,925× over",
effb/90fb) regenerate from a consistent frame?

## The composition hypothesis (from reading both scripts, before any run)

1. 90fb's `budget.py` computes `kicks_s = N * K_AVG / P * RTF` = 222/s — the **whole
   billion's** kick stream (averaged cadence 0.28/orbit, P = 4 yr, rtf 100) — and
   multiplies by ONE 10⁴-island's wake (812.8 pairs × 5.35 µs M1 = 4.35 ms) = 0.966
   cores, labelling it "per CELL". It is the **total** cascade of the billion if every
   cell were an isolated 10⁴ island.
2. effb's `ledger.py` multiplies that by N/10⁴ = 10⁵ cells (7.7×10³/9.66×10⁴ cores),
   re-billing the billion's kick stream per cell.
3. effb's own kick term uses the code-derived cadence κ = 128–256/orbit (ctx.rs:44
   `step_log2: 7`) — ~1,800× 90fb's averaged cadence per game-second — so the two terms
   in the same ledger are composed at different kick rates AND different rtf frames
   (90fb ×100, effb's kick term ×1).

## Held-out predictions

P1 (anchor regeneration, this box): `cargo run --release -p emergent-encounters -- kick`
prints pairs_per_kick ≈ 812.8 ± 0.1, us_per_pair ≈ 7–11 µs (x86 shared; 90fb's box: 8.84),
changed_fraction ≈ 0.0024 at eps 1e-9, slack_skippable ≈ 0.946 at eps 1e-9.

P2 (semantics): the shipped code's own cells-mode record (90fb cascade.jsonl) shows
pairs/kick at n = 10⁶ ≈ 1.5–1.9×10⁴, i.e. ∝ n_total, NOT the 812.8 cell constant —
index cells do not cut candidate count; only an isolated island (a belt of 10⁴ total)
carries 812.8. [Already verified by reading the stored jsonl before writing this file;
the prediction is that nothing in the shipped code contradicts this reading.]

P3 (corrected totals, per game-second, M1-implied, skin 12.6×, global pricing 5.35 µs/pair,
N = 10⁹): the published numbers regenerate as:
   - islands + averaged cadence (90fb's own frame): 7.7×10⁻⁴ cores/game-s = 0.077 at
     rtf 100 (the "0.077 per cell" IS the partitioned total — fits the budget);
   - one contiguous belt + averaged cadence: 16.5–82 cores/game-s no-skin (X = 150–1.5),
     1.3–6.5 skin; at rtf 100: 1.6×10³–8.2×10³ no... with skin 1.6×10³–8.2×10³ at rtf 100
     — the magnitude of effb's 7.7×10³ headline survives ONLY as this cell of the cube
     (contiguous, averaged, flying pace), by structural identity
     (10⁵ cells × 812.8 ≈ 8.1×10⁷ ≈ the contiguous pair count), not by the cell
     arithmetic effb wrote;
   - shipped cadence (κ = 128, 1 AU → 4.06×10³ kicks/game-s at 10⁹): islands 17.7
     no-skin / 1.4 skin cores per game-s (0.55 skin at cells-local 2.1 µs); contiguous
     3.8×10⁵ / 3.0×10⁴ per game-s — 10⁶-class at flying pace.

P4 (the rtf frame): at a consistent flying pace (rtf 100) effb's own kick term becomes
12–109 cores (Carlson, code-derived cadence) — i.e. under the frame in which the
encounter term was billed, the KICK term itself busts the 4-core budget unless the
cadence is the averaged one or the key arm (b29a: 0.004 cores/game-s) is wired. The
"7,051× the kick term" ratio is a cross-frame artefact; the consistent ratios are
~150–1,900× (islands, per game-s) or ~10⁴–10⁵× (contiguous).

P5 (what survives): the board's ordering claim survives in direction — encounters, not
kicks, are the cold rail's binding term under every consistent frame except
islands+averaged — but the "further ~1.9×10³ cut" is mis-addressed: the only 10³-class
engine lever left is the contiguous belt's candidate COUNT (pairs/kick ∝ n_total ≈
1.7×10⁷ at 10⁹; group certificates / "what never needs a pair test"); cadence (457–914×,
the H0190 averaging) and topology (2.1×10⁴×, islands) are measured content-policy levers,
not engine work, and skin (12.6×) is built.

P6 (kill criterion for my own run): if the anchor does not regenerate (P1 fails by >3×),
the 90fb constants are box-dependent and my whole correction collapses to a framing
note — report as such.
