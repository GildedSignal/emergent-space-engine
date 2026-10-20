# Dossier — 20261020-1621-fermi-5f76 (fermi)

**Claim.** 8994's one-seed allocation constants are laws — the player-item scratch is 193.4–199.0
KB/item across three seeds and three decades of K (0.1% K-spread at fixed seed), the ladder top
is 57,344 B exactly everywhere — and the census now counts the mechanism the backtrace was asked
for: **two array-builds per player item** (one doubling ladder to the 56-KiB cap, one short),
plus a ~57 KB/item floor of ~225 small calls; the one K-sensitive constant is the ship term's
per-kick marginal, which RISES with K (1.45 → 2.99 KB/kick from 10⁴ to 10⁵), widening the 10⁹
bandwidth row to 10–42% of 60 GB/s — still closing, no pooling mandated.

**Bottleneck.** budget-1e9 od 6(c) verbatim ("one more seed before the 194 KB/item and ~244–366
B/body chain constants are cited as laws") plus od 6(a) answered at the census level (which
growing arrays the player item builds — names still need the backtrace, counts do not). Gain:
no 10×; the decision rows ("no pooling subsystem is machine-mandated"; "the player term is a
negligible ~19 KB/game-s rate at 10⁹"; cc9d's read-set priority) now rest on a 3-seed, 3-decade
law instead of one draw, and the with_capacity line's target is now TWO arrays, not one.

**Instrument.** 8994's `alloc_scope` verbatim (env-gated TLS scope marker in `advance()` +
counting GlobalAlloc, per-scope size census) plus one disclosed addition: an env-gated seed
override (`ES_SEED`, default 1 = shipped bits; `alloc_scope.rs` line 118), because the seed is
hard-coded at 1 in the example. Flight args verbatim to 8994's arms: `alloc_scope <K> coast 30
2000 12`. Patch = work/patch.diff (8994's patch + the seed knob).

**Evidence** (this box, load ~1.5, each arm 18 s wall, RSS < 100 MB; x86 → M1 orders only;
regen = `regen.sh`, ~2 min warm build + 5×18 s flights + analysis):

Control A1 (seed 1, K=10⁴) reproduces 8994's D1: item 11.35 KB/kick (11.35), base 2.04 KB/game-s
(2.03), kicks 108,282 (108,383, 0.1%), ship items 42,415 (42,422).

| arm | seed | K | player KB/item | >2KiB ladder KB/item | small calls KB/item | ship KB/item | ship KB/kick | item KB/kick |
|---|---|---|---|---|---|---|---|---|
| A1 | 1 | 10⁴ | **193.4** | 136.0 | 57.4 | 3.7 | 1.45 | 11.35 |
| A2 | 2 | 10⁴ | **193.8** | 137.3 | 56.5 | 2.8 | 1.53 | 10.14 |
| A3 | 3 | 10⁴ | **199.0** | 137.3 | 61.7 | 3.0 | 1.45 | 10.18 |
| A4 | 2 | 3×10⁴ | **193.8** | 137.9 | 55.9 | 2.9 | 2.18 | 8.41 |
| A5 | 2 | 10⁵ | **194.0** | 139.7 | 54.3 | 2.3 | **2.99** | 7.23 |

- **The player constant is a law** (P1/P2 held): 193.4/193.8/199.0 across seeds; 193.8/193.8/
  194.0 across K at seed 2. The ladder census behind it, per player item: rung means double
  (3,263→6,528→13,055→28,658→**57,344**, one 2.2× step at rung 3→4), rung COUNTS per item =
  2.07–2.12 starts reaching rungs 1–3 and 1.03–1.06 reaching the cap — **two array-builds per
  item: one full ladder to the 56-KiB cap (~109 KB traffic ≈ 1.9× top, the "2× top" law), one
  short ladder dying by rung 3 (~23–29 KB)**, plus ~225 sub-2-KiB calls (≈1.4 per pulled body,
  ~55–62 KB) — that is 8994's "1.7 full-ladder-equivalents" decomposed: 1.0 capped + 1.0 short
  + small calls. Seed 2 additionally shows a rung-1-only third start (r1 3.1–3.2 vs 2.08); the
  top stays 57,344 B. Realloc share 79–80% of the player term in every arm.
- **The ship marginal is the one K-sensitive row** (new): per ship-item it falls (3.7→2.3 KB),
  per fired kick it RISES (1.45→2.99 KB, 10⁴→10⁵). The page's "1.6 KB/kick stream marginal" is
  the bottom of the range. Re-based 10⁹ row at λ = 4–8.4×10⁻⁵ (4–8.4×10⁶ kicks/wall-s):
  **6–25 GB/s = 10–42% of 60 GB/s** (was "11–23%"). Still closes on the marginal reading; no
  pooling subsystem becomes machine-mandated. The player term at 10⁹ is unchanged and negligible:
  0.097 player items/game-s × 194 KB ≈ 18.8 KB/game-s.
- Base 2.04–2.88 KB/game-s coast (P5 held); the mixture per kick dilutes with K (11.35→7.23),
  reproducing 8994's checker's 6.31 at 10⁵ (P4 held at its K=10⁴ arm; the 10⁵ arm sits below the
  letter's [8,16] band by this known dilution — disclosed in predictions.md).

**Predictions.** predictions.md written before A2–A5 (A1 anchor disclosed): P1–P5 held, P6
half-held (one family, exact top, realloc-dominated — but >2KiB share 69–72% < the ≥75% letter;
the small-call floor is bigger than estimated). The unpredicted find is the ship marginal's
K-trend. No kill bar fired.

**What would make it wrong.** The scope marker still cannot name functions: "two array-builds"
is a count from rung multiplicity, not an identification (pull_ships vs the neighbourhood scan
vs a re-pull — od 6(a)'s backtrace question stands, now narrowed to two names). The 10⁵ rung is
the belt's top flown arm; the ship per-kick trend beyond it is an extrapolation with one point
of curvature. rtf 2000 flights carry 8994's schedule-elasticity caveat (kicks/game-s ÷ bodies
here reads ~1.9×10⁻⁴, 5× a9d7's rtf-100 λ — the cadence is budget-fed; all comparisons in this
dossier are within-instrument, same rtf). One box; orders only.

**Cost of adopting.** None: no engine change; the ledger rows re-base (player term law-grade,
bandwidth band widened 11–23% → 10–42%, still closing). The with_capacity one-liner's target is
now the two arrays (halves the ladder traffic), pending cc9d's read-set fix superseding it.
Fit with PRINCIPLES: "the best part is no part" (the pooling case stays unmeasured-needed);
"Measure before claiming" (a law cited at 10⁹ now has three seeds under it).

**The lens.** The Fermi estimate did its job before the run — the one-ladder model predicted
~115 KB and the measured 193.4 KB refused to close, which is exactly what forced the two-array
reading out of the rung counts. What the lens may have missed: the per-kick ship trend needed
the K-series to appear (a single-rung Fermi run would have re-cited 1.6 KB/kick); the "which
function" question is invisible to every counting allocator by construction.
