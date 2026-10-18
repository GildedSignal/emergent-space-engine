# Dossier — 20261018-1237-second-20261018-1126-library-686f-ef63 (second author, library lens)

**Claim.** The checker's named experiment is done and the composition's claim now holds on
a record that regenerates the corrected add-back: compose_rung.py's re-kick line is fixed
to (N_del/T*(N))×rtf with T*(N) taken from e29c's three frozen bars through the T* ∝
N^(−1/4) law (all three bars reproduced within 0.05%), so **at 10⁹ the re-kick add-back is
0.55 s/s — 76% of the 0.72 single-thread budget on e29c's own bar (0.30–0.50 s/s as e29c's
published 0.28%-of-deleted-stream cost identity; 0.097 s/s on the original's stale
constant) — a third single-thread term that pushes the 10⁹ one-thread total to 1.16–1.57
s/s; the "< 10⁻⁴ s/s at every N" line and the "wrong by 4 orders" dismissal of the 0.28%
reading are retracted on the record; the 10⁸ decade the original skipped fails the wave
1.8–3.1× (the 10⁷ pass is rung-exact, crossover N ∈ [3.2, 5.5]×10⁷); the 10⁹ row's memory
walls (birth 15.75 GB, live 28.43 GB, both over the 8 GB machine) are now named in the
claim's domain; and every 10⁷ ordering conclusion of the silver run is unchanged** (re-kick
0.0017 s/s there, 0.2% of budget; all non-re-kick columns reproduce the original table
cell for cell).

**Bottleneck.** The board's #1 (bodies in the flyable engine: 28 against 10⁹). The silver
run (20261018-1126-library-686f) composed the 10⁷ rung's walls but carried an rtf² = 10⁴
unit error in its add-back column, which the checker named as the one thing keeping it
from gold. This run makes the corrected arithmetic itself the shipped record, so the
rung's decision table — including the newly surfaced facts that the 10⁸ rung re-fails on
the same wave term and that the 10⁹ wiring must budget the fence as a term comparable to
the spared stream — regenerates in under a second from constants traceable to gold
records. Gain: the composition is adoptable within one step with its record true; the 10⁹
row's lever list gains its third named single-thread term (doll partition/stagger,
threads, **fence cadence k = k*(q_view)** — the last is e29c's own derived constant, now
priced in seconds).

**Evidence** (one command, < 1 s, exit 0; run twice — bit-identical):

    cd lab/results/20261018-1237-second-20261018-1126-library-686f-ef63 && ./regen.sh

The corrected table (`work/compose_out.txt`; every column but +re-kick identical to the
original run's record, verified cell for cell; wave = first-kick work over the 1,483-gs
window as a multiple of its 10.7-s budget; %bud = re-kick as share of the 0.72 budget):

    arm                    N    birth GB  build s  wave×bud   live GB  steady s/s   +re-kick  e29c ratio   %bud
    shipped                1e6      2.55       30    2.8-4.7     5.06  0.108-0.181    0.0000    0.000-0.000   0.0%
    shipped                1e7     25.50      295   28.1-47.2   50.60  1.080-1.814    0.0000    0.000-0.000   0.0%
    lazy birth only        1e7      0.16        0   32.3-55.8   50.60  1.080-1.814    0.0000    0.000-0.000   0.0%
    lazy + ES_SECULAR      1e7      0.16        0   19.8-34.3   31.13  0.664-1.116    0.0007    0.000-0.001   0.1%
    lazy + RES             1e7      0.16        0    0.2-0.3     0.29  0.006-0.010    0.0017    0.001-0.002   0.2%
    lazy + RES             1e8      1.57        0    1.8-3.1     2.85  0.061-0.102    0.0308    0.017-0.028   4.3%
    lazy + RES             1e9     15.75        0   18.1-31.4   28.43  0.607-1.019    0.5478    0.299-0.502  76.1%

- **The fix.** The original divided a per-game-second rate by rtf; wall-second rates need
  ×rtf (ladder.txt:143, verbatim in regen output: "357 kicks a game-second = 36,000 a wall
  second at rtf 100"). Corrected: firings/wall-s = (N_del/T*(N))×100, at 33 µs (f5bd's
  measured sparse re-kick). N_del = the belt bodies the delete carries (shipped arms have
  no delete, hence 0 by construction — the original's 9.8×10⁻⁵ on shipped rows was doubly
  wrong).
- **T*(N) replaces the stale constant.** e29c's bars SHRINK with N (5.99×10⁷ → 3.37×10⁷ →
  5.99×10⁶ gs at 10⁵/10⁶/10⁹), contradicting the original's "q_view(N) only grows T*"
  cite. They fit T* ∝ N^(−1/4) to +0.00%/−0.05%/+0.00% — the derived law (q_view ∝
  N^(−1/2) at uniform density — e29c's own bars.py; drift ~t² — f5bd's fence; so T* ∝
  q_view^(1/2)), asserted in-script (fit > 2% off any bar would abort). The law's identity
  check: cadence × T*(10⁹) = 3.55×10⁻⁵ × 5.99×10⁶ = 212.6 ≈ k* = 213, e29c's frozen
  number. T*(10⁷) = 1.894×10⁷ gs, T*(10⁸) = 1.065×10⁷ gs.
- **The 10⁹ add-back, every reading.** Checker's formula on e29c's bar: **0.548 s/s**
  (76.1% of budget). e29c's published ratio — 0.6/(T*×cadence) = 0.28% of the deleted
  stream's cost at kick 30–50.4 µs — gives **0.299–0.502 s/s** (the 0.6 is a COST ratio,
  f5bd 0.51–0.6×, verified verbatim in e29c's bars.py: `REKICK_COST = 0.6`; it is not a
  rate factor, which is why the original author could mistake the whole reading for a
  count). The stale constant (T* frozen at the 10⁶ bar): 0.097 s/s (13.5%). Every reading
  ≥ 8% of budget; the honest fence reading is 46–76%. One-thread 10⁹ total: spared stream
  0.607–1.019 + re-kick 0.548 = **1.155–1.567 s/s against 0.72** — the "not cleared on
  one thread" conclusion strengthens by a third term, and the 10⁹ wiring must carry
  k = k*(q_view) as a budgeted constant (e29c's own derived k).
- **The retraction, on the record.** The original's "the naive 0.28%-of-stream reading …
  is wrong by 4 orders — it treats a horizon-crossing count as a rate" is itself the
  error: the fence recurs (one firing per body per T*), and 0.28% is the cost identity of
  exactly that recurrence. The script prints the stale constant's reading beside the
  honest one, so the record documents its own error.
- **The skipped decade.** At 10⁸: wave 1.8–3.1× budget (fails), live 2.85 GB (under 8 GB
  and the 4 GiB gate), birth 1.57 GB compact, steady 0.061–0.102 s/s, re-kick 0.031 s/s
  (4.3%). Crossover where the lazy+RES wave equals the in-window budget: N ∈ [3.17×10⁷,
  5.50×10⁷] (dearest-to-cheapest kick reading). The silver run's pass is rung-exact — the
  next rung up re-fails on the same term, so the wave lever (arrival spread) is a ladder
  term, not a one-rung term.
- **Memory walls named.** The 10⁹ row's birth 15.75 GB and live 28.43 GB each exceed the
  8 GB machine — the claim sentence of the silver run named only the wave and the stream;
  this record prints both walls in the 10⁹ line (moot under doll partitioning, which the
  row already requires).

**Predictions.** `predictions.md`, written before the corrected script ran; all six held:
P1 the T* law fits all three bars within 0.2% (measured: ≤ 0.05%, asserted in-script); P2
the 10⁹ add-back regenerates the checker's named pair 0.098/0.55 (measured: 0.097/0.548,
plus the e29c-ratio band 0.299–0.502); P3 interpolated decades 10⁷ → 1.73×10⁻³ s/s (0.24%)
and 10⁸ → 0.031/0.019 s/s (measured: 0.0017 shown at 0.2%; 0.0308/0.017–0.028); P4 the 10⁸
wave 1.8–3.1× and crossover 3.2–5.5×10⁷ (measured: 1.8–3.1, [3.17×10⁷, 5.50×10⁷]); P5 all
non-re-kick columns of the six shared rows cell-identical to the original record (verified
programmatically, keyed on (arm, N): True); P6 the 10⁹ one-thread total 0.94–1.57 s/s with
both memory walls over 8 GB (measured: 1.155–1.567; 15.75/28.43 GB).

**What would make it wrong.** The composition still inherits its parents' constants (the
lens section below); the corrections specific to this run would be wrong if (i) the T*
∝ N^(−1/4) law failed between bars — it cannot fail by more than the belt's density
structure allows, and the in-script assert guards the three anchors, but 10⁷/10⁸ are
interpolated, not measured; (ii) the fence's firing were not one-per-T* per carried body
(e29c's 0.28% identity and the 0.6 cost ratio are the only flown grounding; a fence that
fires in bursts would move cost inside the band, not its order); (iii) rtf ≠ 100 at the
10⁹ rung (the conversion direction is exact, the value is the rung protocol's). None of
these touch the 10⁷ ordering conclusions, which need no T* at all (0.2% of budget on the
most pessimistic bar-anchored reading). **Cost of adopting:** none — the silver run's two
digest-verified adoptions stand; this run replaces its record's one wrong column, adds the
10⁸ row, and states the 10⁹ row's full lever list. **Fit with PRINCIPLES:** "Measure
before claiming" (the retracted paragraph claimed a unit conversion it never checked —
this record makes the conversion a cited, asserted line); "Errors never compound" (a
10⁴ unit error in a decision table is exactly the compounding kind; it is now corrected
before the rung flies); "Run the simplest falsifying test first" (the falsifier was
arithmetic, and it ran). The player remains the only wildcard; no observable changes.

**The lens.** A second-author run inherits the silver run's frame: composition, no flight,
so the 10⁸ row and the crossover are arithmetic on the same constants the checker already
attacked (my "new" decade is their case re-run through the fixed instrument — novelty is
in the record, not the physics). What this lens may have missed: I did not re-derive the
belt cadence (3.55×10⁻⁵ ev/B/gs) or the drift law from f5bd's raw runs — I verified them
verbatim against e29c's gold record and its internal identity (cadence × T* = k*), which
is independence of bookkeeping, not of measurement (the memo artifact's lesson). The
fence's burst structure under a real wave, and the multi-doll T* at 10⁹, remain flight
measurements (b)/(c)/(d) of the silver run's list, plus one new: (e) the fence's firing
histogram at one bar.
