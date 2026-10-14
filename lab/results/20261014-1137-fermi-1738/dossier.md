# Dossier — 20261014-1137-fermi-1738

## Claim

**The published 10⁹ encounter wall (7.7×10³ cores skin-on, "1,925× over", "7,051× the
kick term") does not regenerate in any single consistent frame: 90fb's "0.966/0.077 cores
per 10⁴-cell" is the partitioned TOTAL of the whole billion (proof: my re-derivation
reproduces 90fb's own "max rtf on 4 cores: averaged + skin = 5,216" exactly), effb's ×10⁵
cells re-bills the billion's kick stream once per cell, and the magnitude survives only
as the contiguous-topology cell of the honest policy cube — which spans nine orders of
magnitude (0.077 cores to 3×10⁷ cores at flying pace) on three measured policy
constants: cadence (457×, the H0190 averaging, `step_log2`), topology (2.2×10⁴–1.1×10⁵×,
islands vs one contiguous belt), skin (12.6×, built) — so the board's "cut encounters by
10³" is a content-policy product, not unmeasured engine work, except for the one true
wall: the contiguous belt's candidate count ∝ N, which no index cuts (measured).**

## Bottleneck

The board's #2 item (encounter work at 10⁹: "~10³–10⁴ cores: what cuts it by 10³") and
HANDOFF's interlock line. The board's number inherits effb's composition; if the
composition is wrong the next 10³ lever is mis-addressed (it orders builds). Gain: the
ledger the wiring decision (H0216, the belt's `step_log2`) is priced against becomes
consistent, and the one remaining engine question is isolated (candidate count on a
contiguous belt). Cost of the run: reading two scripts + one shipped anchor run.

## Evidence

`bash regen.sh` (≤ 2 min: one shipped cargo build already cached + one 5 s anchor run +
the ledger script). Raw anchor: `kick-anchor.jsonl`; output: `ledger2-out.txt`.

1. **The anchor regenerates on this box (P1 held):** `cargo run --release -p
   emergent-encounters -- kick` prints pairs_per_kick **812.8** (all four eps),
   us_per_pair **8.82–8.96 µs** x86 (90fb's box: 8.84), us_per_kick 7,166–7,284,
   changed_fraction 0.0024 and slack_skippable 0.9458 at eps 1e-9 — identical to 90fb's
   stored record within 1%. M1 factor from the frozen M1 anchor: 4,345.4/7,275.5 =
   0.597 → M1 5.35 µs/pair (90fb used 5.35).
2. **The "per cell" label is wrong (P2 held):** 90fb's `budget.py` computes
   `kicks_s = N·K_AVG/P·RTF` = 222/s — the whole billion's kick stream (averaged
   cadence 0.28/orbit, rtf 100) — times ONE island's wake (812.8 pairs × 5.35 µs =
   4.34 ms) = 0.966 cores. My ledger reproduces 90fb's own bottom row ("max rtf on 4
   cores: averaged + skin = 5,216") **exactly** (4/0.000766 = 5,221): the 0.966/0.077 is
   the partitioned total, i.e. the billion runs at rtf 5,216 on 4 cores in that frame —
   not "1,925× over".
3. **effb's ×10⁵ is a double count (P3 held):** `enc_skin = 0.077·(N/1e4)` bills the
   billion's kick stream once per cell. Its magnitude (7.7×10³–9.66×10⁴) lands inside
   the contiguous-belt range (1.65×10³–8.15×10³ skin / 2.1×10⁴–1.0×10⁵ no-skin at
   averaged cadence, rtf 100) by structural identity — 10⁵ cells × 812.8 = 8.13×10⁷ ≈
   the contiguous pair count — not by the cell arithmetic written. The published label
   ("the working point is 10⁵ cells of 10⁴") contradicts the number: 90fb's own verify
   control shows index cells keep candidate sets IDENTICAL to global
   (`global_pairs_per_kick == cells_pairs_per_kick` = 18,703.5 exactly at n=10⁶,
   0 mismatches) — cells deliver locality (us/pair 8.68→3.95, 2.3×) and keying, never a
   pair-count cut. Only an isolated island (a belt of 10⁴ total) carries 812.8.
4. **The corrected cube** (all M1-implied, skin-on 12.6×, global 5.35 µs/pair, N = 10⁹;
   per game-second, ×100 at flying pace; budget 4 cores) — `ledger2-out.txt`:

   | cadence \ topology | islands 812.8 | contiguous X=150 | contiguous X=1.5 |
   |---|---|---|---|
   | averaged 0.28/orbit (H0190) | **0.00077 (0.077)** | 16.5 (1.65e3) | 81.5 (8.2e3) |
   | unaveraged 32/orbit (H0190) | 0.088 (8.8) | 1.9e3 (1.9e5) | 9.3e3 (9.3e5) |
   | shipped κ=128/orbit (ctx.rs:44) | 1.4 (140) | 3.0e4 (3.0e6) | 1.5e5 (1.5e7) |

   Levers: cadence 457× (0.28→128), topology 2.2×10⁴×/1.1×10⁵× (islands→wide/narrow
   contiguous), skin 12.6×, locality 2.3×. Max-rtf on 4 cores: averaged+islands 5,216;
   shipped+islands 2.9; shipped+contiguous 1.3×10⁻⁴.
5. **At the shipped cadence nothing fits 10⁹ at flying pace (P4 held) — including the
   kick term itself:** effb's kick constants made consistent: 231 µs → 0.94 cores per
   game-second = **94 at flying pace**; Carlson 30 µs → 12.2; only the key arm (b29a,
   0.11 µs) fits (0.045). effb's published ratio "encounters/kicks = 7,051×" mixes
   frames (its kick term at rtf 1, the encounter term carrying 90fb's rtf 100 inside
   the 0.077): consistent ratios are ~10² (islands) to ~10⁵ (contiguous) per
   game-second. The ordering conclusion (encounters bind the cold rail, not kicks)
   SURVIVES in every consistent frame except averaged+islands, where neither binds.
6. **The wired wall (H0216's held-out ~5.2×10⁵) recomputed (P5 held):** walls at flying
   pace, skin-on: islands 2.9×10⁷ (shipped) to 5.2×10¹⁰ (averaged); contiguous-wide
   1.2×10⁶ (shipped, quadratic in N — pairs/kick = 0.0175·N) to 4.9×10⁷ (averaged).
   The honest walls are all ABOVE effb's held-out number; the wiring's `step_log2` +
   topology choices are worth ~10⁴× in where the first wall lands — the decision
   effb's open direction 8 named is even more load-bearing than it published, because
   its own encounter term was priced at the averaged cadence, understating the
   cadence's effect on the binding term by ~500×.

## Predictions

`predictions.md` written before the anchor run. P1 held exactly (all five anchor
constants within 1%); P2 held (the reading is forced by 90fb's own stored verify rows);
P3 held (every regenerated number in the table above); P4 held (kick term 94/12/0.045
cores at flying pace); P5 held (the surviving direction + the isolated candidate-count
wall); P6 not triggered (anchor regenerated). One prediction of mine was wrong in
passing: my first wired-wall draft extrapolated contiguous walls linearly in N — the
cost is quadratic (pairs ∝ N); corrected in `ledger2.py` with the √ solution.

## What would make it wrong

- The 0.28/orbit averaged cadence is H0190's premise-probe result, not shipped belt
  code (the belt's cadence is unwired, a design choice); if the wired belt lands at
  some intermediate κ the cube's rows interpolate — the composition audit is unaffected.
- The pairs law is calibrated on Rayleigh σ_e = 0.01 belts (90fb's own caveat) and
  measured to n=10⁶ (law-checked to 10⁷); a colder belt scales the contiguous columns
  down ∝ σ_e, a fleet breaks the random-pom assumption entirely (taleb-09b5).
- The M1 factor is one frozen anchor (4,345.4 µs) over my box's run; a 2× machine error
  moves no conclusion (the audit is about composition, not constants).
- The skin's 12.6× is the board-adopted factor; the anchor's own slack_skippable at
  tidal eps is 18.5× (0.9458) — my table uses the conservative number.
- If the checker reads 90fb's "per CELL" as intentionally meaning "per cell at cell
  pair-geometry, summed over the billion's kicks" then effb's ×10⁵ is the only error;
  both readings agree the published 1,925× is not regenerable — the label and the
  multiplication cannot both be right.

## Cost of adoption

Zero code. The integrator re-reads the scoreboard line "encounter work at 10⁹:
~10³–10⁴ cores" as "the contiguous-belt cell of a policy cube whose other cells fit";
the wiring decision (belt `step_log2`, topology) is priced by `ledger2.py`; the one
remaining 10³-class engine lever is named (candidate count on a contiguous belt —
group certificates / phase-neighbour / flux aggregation, all with prior gold or lead
runs). effb's cadence law, kick term, memory rows and two-rail reading stand; only its
encounter term, the 1,925×/7,051× ratios and the held-out 5.2×10⁵ fall.

## PRINCIPLES

- "Measure before claiming" / "a headline the log contradicts" (the run lessons): the
  headline did not regenerate — found by re-deriving, the cheapest probe there is.
- "Agreement is not independence" (my lens's own rule): effb's ledger and the board
  agreed because both read the same mislabelled row; two documents sharing one harness
  bug. The verify rows (18,703.5 = 18,703.5) were in 90fb's own stored evidence all
  along.
- "the cheapest compute is compute not done" (#1): the cube says the cheapest 10³ on
  encounters is choosing not to create the events (cadence/topology at generation), not
  cheaper discovery.
- "A failed experiment kills that configuration, never the method" (#9): what dies is
  one composition, not the cascade constants (all of which reproduce).

## The lens

Fermi estimates trust cited constants; I re-ran only the one shipped anchor (5 s) and
otherwise audited arithmetic and semantics against stored evidence — the lens is
strongest exactly where a number's frame (whose kicks, whose rtf, per what) is doing
the work, and weakest on machine-level couplings (cache behaviour of 10⁵ independent
cell indexes at 10⁹; the queue term 90fb measured at 0.032 cores no-skin, which I did
not re-price per cell). The cube's cadence axis also assumes the belt's events are
recompiles that wake the cascade one-for-one; if the wired tier batches wakes per cell
per epoch the shipped-cadence rows fall by the batch factor (unmeasured).
