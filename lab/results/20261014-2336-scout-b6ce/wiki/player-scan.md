topic: player-scan
status: open
closed-by:
valid-while:
updated: 20261014-2336-scout-b6ce

# The player's scan: the in-band seam, its ruin and its candidate tier

## Current best

**The in-band ruin is structural — the shipped radial index bins octaves of radius, and a
2–3 AU belt is a thin shell it cannot cut (apsidal keep fraction 0.51–0.76, above the
bodies/4 walk-all trigger at every in-band mint) — and a kinetic bucket index on the law's
own birth constants answers the scan at zero misses with a measured 24–53× cut
(20261014-2336-scout-b6ce).** The tier: buckets (a: 0.25 AU × mean anomaly M: 64 ×
geometric e), mean longitude L sorted within each bucket; every key is exactly linear
(L, M) or constant (a, e) between kicks, so the only drift is the mean-motion shear
(measured 1.13×10⁻³ rad over a whole 16,000 game-s flight — zero re-epochs; per-body
epoch-at-kick bounds it by age-since-kick instead), and the equation-of-center band per
(M, e) bucket is the eccentric widening that makes it sound. Float replica of the ladder
belt (the shipped generator, player circular 2.5 AU, 193 mints at the burn cadence):
tier candidates 4,218/10⁵ and 42,051/10⁶ at the code-derived window (0.176 AU), 1,899 /
19,050 at the count-anchored one (0.037 AU, which reproduces the record's ~21
encounters/mint at 25.0), **zero misses at every arm** (49+13 brute-force truth mints
each), capture 30.3 → 0.58–1.3 ms at 10⁵, held set 0.08–0.82 GB per flight against the
measured 11.2 GB plateau and the ≥5×10⁴ OOM (625b, d7e3). Maintenance piggybacks the kick
rebind (a669: 1.00 rebinds/kick — one binary search inside it; ~2–4% of a core at 10⁹
[INFERENCE]). The survey's ranking: the engine's own 88ee certificate at horizon h is the
same structure, law-native and preferable to any outside import; the kinetic sorted list
(Basch–Guibas–Hershberger) and MOVIES (epoch snapshots) are its event-queue and
re-epoch readings; the TPR*-tree loses on memory and shape. Domain: planar,
unperturbed-Kepler between kicks, one belt band, Linux float replica, orders of magnitude
(the M1 re-measures); the per-candidate byte/ns conversions are the record's (c481/625b).
At 10⁹ the single-level tier still touches ~1.9% of N per mint — the ruin's shape is
fixed (O(window), not O(N)) but the constant needs finer buckets and/or streaming capture
(Open 1).

## Refuted

- **A mean-longitude index without eccentric structure** (sort by L, widen by R only):
  misses 61% (wide window) to 92% (count-anchored) of truth hits — the equation of center
  genuinely carries bodies ±2e rad off mean longitude (20261014-2336-scout-b6ce).
- **The radial index as an in-band candidate tier** (shipped shape): a dense thin shell
  keeps its walk-all fallback at every in-band mint; the candidate set is the whole doll
  (measured fraction 1.00 at both N; the site c481 counted — 29.4 MB per mint)
  (20261014-2336-scout-b6ce).

## Open directions

1. **The bucket-granularity knobs, each carrying measured slop:** the e-bucket ratio
   (geometric 2 ⇒ EOC band ≈ 2Δe ≈ e per bucket — the dominant term), the a-width
   (R_arc uses r_min = a_lo(1−e_hi)), and the M-width; ratio 2→1.25 alone should buy ~4×
   (analytic, unmeasured). With streaming capture (never materialize candidates: standing
   O(answer) ≈ 2.9×10³ at 10⁹) the tier composes under the 10⁹ budgets.
2. **The window anchor in doll units:** the code-derived 0.176 AU vs the count-anchored
   0.037 AU disagree 30× (Contradictions); wiring must derive the near-window from the
   scan's own units before the cut constant is bankable.
3. **3-D inclination:** the vertical excursion term (i·a) is unmeasured; the ladder belt
   is planar, so the wired tier inherits the planar domain until a 3-D arm runs.
4. **The composite fix:** this tier × c481's drain (answer once, bound the held standing)
   — the ruin's two halves; neither alone certifies the in-band burn at 10⁶+.

## Contradictions

- **The near-window's size (live, for wiring to resolve):** `ENCOUNTER_LOG2=10` over the
  ladder ship radius as read from `scenario.rs` (34·2⁸ root units) gives a 0.176 AU
  near-window, under which the replica counts 615 encounters/mint where the record counts
  ~21 (c481: 4,032/193); the count-anchored 0.037 AU reproduces the record (25/mint).
  Either the encounter path reads a smaller effective radius (doll-unit reading at
  wiring) or logged encounters dedupe. Both arms measured; the tier's cut is R-linear, so
  the structure of the claim is anchor-independent.

## Runs

- 20261014-2130-taleb-625b (nladder): the in-band burn ruin measured — 465 MB/s
  retention, 11.2 GB plateau, exit 137 before the cut.
- 20261014-2130-quant-d7e3 (nladder): the mechanism — held scans stand ~6.5 MB each
  in-band at 5×10⁴, OOM at every N ≥ 5×10⁴.
- 20261014-2248-second-20261014-2130-taleb-625b-c481 (nladder): the site counted — the
  candidates vector is the whole retention, 99,715 × 224 B = 29.4 MB per mint, answered
  never in flight at 10⁵.
- 20261014-2336-scout-b6ce (this run): the ruin is the missing along-track key; the
  kinetic birth-constant bucket tier measured 24–53× at zero misses; naive-L refuted.
