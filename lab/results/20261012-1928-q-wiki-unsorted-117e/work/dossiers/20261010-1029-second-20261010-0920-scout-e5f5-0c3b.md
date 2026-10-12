# Dossier — run 20261010-1029-second (second author on 20261010-0920-scout-e5f5)

**Claim.** The checker's named experiment, run: per-(cell, shell) accumulators (FMM
interaction shells, member quanta) **do kill the compounding leak** — the deferral
error becomes bounded and near-stationary where every scalar-accumulator variant of
the original run grew or persisted (dipole aggregates: max 52→60q over a 3× horizon,
+16%, vs v2's ×79 growth to 228q and v3's persistent 3.6×10⁴q) — **but not at the
letter of the criterion**: the steady error is ~(3–10)·L·q, not ≤ L·q (median 18–22q
≈ 3Lq, max 43–60q ≈ 9Lq at L=6 levels), and the cost is O(log N) per body at ~11×
the leaky scheme's constant (585.6 deliveries/body/time at N=16 384, measured
two-size exponent 0.231, level terms saturating at ~160/ring), not the original
2.1×10⁴× advantage (≈ 28× over naive here; ≈ 10³ extrapolated to N≈10⁶). The exact
partition is proven as an integer assert. One new constraint: the accumulator's
effective quantum floors at the event-strength scale (renewal overshoot
E[s²]/2E[s] ≈ 0.042 ≫ θ below q ≈ 0.004), so tightening q below that fails to
tighten error or cost (measured at q=0.001: error ×8 in q-units, cost ×4.1).

**Bottleneck.** Same as the scout run: the board's "the light cone keeps growing" /
R5's gravity-as-news taken literally (O(N) deliveries per event). The question left
open by the silver: does the FMM-shell partition make quantum-gated accumulation
*correct* (bounded, non-compounding) at O(1)-per-body cost?

**Evidence** (toy identical to the scout's: 2D periodic patch, σ=1, c=1, Poisson
news λ=1/body/time, strengths log-uniform [0.005, 0.5], 1/d² falloff, quantum q;
leaf cells k=16 bodies; N = 4 096 and 16 384 as the checker specified).

Scheme under test (`shells.py`): DIRECT = exact arrival-timed broadcast to the
source's 3×3 leaf neighbourhood (no per-event rings → no ring/square complement to
mismatch); SHELLS = one accumulator per (source leaf, ring level l) holding
(strength A, dipole p), member set = receivers whose tree-code separation level
l\*(R,D₀) = l (smallest l with wrapped Chebyshev distance of the level-l ancestors
in [2,3] — the square-annulus tiling of everything outside the 3×3), member quantum
θ_l = q·(1.5·c_l)², flush delivers (A,p) from the leaf centre to member bodies,
arrival-timed. **Partition proof (canonical, integer):** for every configuration
the l\*-table asserts each (source leaf, receiver leaf) pair has exactly one channel
(9/40/147/588/240 member leaves per channel at side 32; 9/40/147/60 at side 16;
uniform over sources). Every number below regenerates from shipped code
(bit-identical, verified by rerun).

- **Steady-state error** (pre-history t₀ ∈ [−30, 0] so accumulators are warm —
  necessary because the top ring's flush cycle θ₃/F·A₀ ≈ 13.4 time units exceeds
  T; the cold-start run's apparent growth 0→21.5q was this warm-up transient):
  - dipole aggregates, N=16 384, q=0.01: max 42.9/51.8/50.7/57.7/57.2/59.9q and
    median 17.2/18.7/18.6/20.3/20.0/22.0q at t=2..12. Growth t=4→12: max +15.6%,
    med +17.6% — the mild residual is the multipole-truncation random walk plus
    the still-growing light cone (box crossing is 64 time units), not compounding.
  - scalar control (same runs, p zeroed): max 78.8→98.5q, med 25.2→33.4q. The
    scalar−dipole gap at t=12 (98.5−59.9 ≈ 39q) isolates the monopole bias walk:
    carrying the dipole is required, as predicted.
  - N=4 096: max 49.6→50.9q, med 15.9→16.8q over t=2..6 — flat, weak N-growth of
    the bound with level count.
  - Contrast at the same horizon (cited from the scout's shipped record, which I
    reproduced from its scripts): v2 grows 2.9q→228q (×79) by t=12; drop grows
    2.9→14.7q by t=6; v3 sits at 3.6×10⁴q persistent.
- **Cost, per body per time** (steady): direct 144.7 (= 9×16, the 3×3 broadcast);
  flush by ring level [114.7, 149.2, 162.1, 14.9] at side 32 (top ring
  wrap-truncated; side 16: [114.5, 149.3, 16.4]) — the per-level term saturates
  near 160, so total = 144 + ~160·n_rings, n_rings = log₂(side/4)+1: **O(log N) per
  body**, measured exponent 0.231 over N=4 096→16 384. Totals: 425.0 (N=4 096),
  585.6 (N=16 384) vs naive 4 096/16 384 — ratios 9.6× / 28×; extrapolated
  ≈ 1 100 at N≈10⁶ (7 rings) → ≈ 10³× (the leaky v2's analytic 2.1×10⁴× advantage
  shrinks ~20×; the exact partition is what costs). Writes 4/body/time, emissions
  0.26/body/time, accumulator words 0.41–0.64/body (nonzero (A,p) triples),
  in-flight ≈ 5–10 events/body (1-word accounting; ×6 with full payloads — the
  same payload caveat the checker raised against v2 applies). Bursts: p99/median
  = 1.06 (447/473 per body per time) — smooth.
- **Fine quantum q=0.001:** error 490→516q max, 141→160q median (×8 worse in
  q-units than q=0.01), cost ×4.1 not ×10. Cause: the renewal overshoot — an
  accumulator flushes at θ plus a residual event of mean size ~E[s²]/2E[s] ≈ 0.042,
  so below q ≈ 0.004 the overshoot, not q, sets the residue and the rate. The
  quantum floors: **q below the event-strength scale buys neither accuracy nor
  cheapness** (the scout's "the certificate's quantum sets the bill" holds only
  above that floor).
Reproduce (deterministic, seed 20261010; warm suite ≈ 15 min, each config 28–349 s,
peak RSS 0.34 GB measured at side 16 and all configs under the 2 GB limit — but
over the 60 s preference per config; `--cold` regenerates the exploratory
cold-start suite ≈ 4 min):

```
cd lab/results/20261010-1029-second-20261010-0920-scout-e5f5-0c3b && python3 shells.py
```

**Predictions** (`predictions.md`, written before the decisive run): held — P1
partition assert (the core); P4 scalar grows visibly beyond dipole (98.5 vs 59.9q);
P2 direct = 144; P6 memory comparable to v2. Missed, all reported above: P2's flush
term (predicted 57/ring, measured 115–162 — my annulus arithmetic used 12·4^l
leaves where the [2,3] ring has 40·4^l; exponent 0.23 vs predicted 0.12, the
top-ring wrap truncation at both sizes steepens it); P3's magnitude (predicted
max ≤ 25q, measured 43–60q: a receiver is covered by ~40·4^l pending accumulators
per level, not the ~12·4^l I modelled, and their vector cancellation is weaker than
assumed) and the letter "≤ L·q" (measured ~3Lq median, ~9Lq max); P5's fine-q
scaling (predicted ×10 cost and q-invariant error, measured ×4.1 and ×8 — the
renewal-overshoot floor, which I had not modelled). The warm-up transient was not
in my predictions either: the first (cold) run grew 0→21.5q and I diagnosed it as
the top ring's 13.4-time-unit cycle exceeding T before trusting any growth number.

**What would make it wrong.** The steady-state plateau rests on the pre-history
construction; a horizon ≫ the top ring's cycle *and* ≫ the box crossing (T ≳ 64 at
side 32) could still reveal growth — at this toy's sizes that run costs ~10× more,
and the scalar−dipole gap already shows a real walk underneath. The error bound's
constant depends on the strength distribution's overshoot ratio (log-uniform here);
a heavy tail near the quantum would raise it. The cost model is fixed-density; the
scout's checker already showed clustering multiplies constants (1.74×), not
exponents, for the ring scheme — assumed to carry over, not re-measured. The
O(log N) term is real, not an artifact: each scale's annulus holds its own quanta.

**Cost of adoption, fit.** The integrator's decision, stated as a trade the silver
left implicit: exactness costs ~11× deliveries and turns O(1) into O(log N) per
body at this toy's quanta — if the engine adopts "gravity is news" with cell
accumulators, the FMM-shell partition is the *correct* bookkeeping (the integer
proof ships in `shells.py`), and the member quanta are the dial: θ = q·d²·κ trades
error ∝ κ against cost ∝ 1/κ, floored at κ ~ E[s²]/2E[s]/d² by the overshoot.
PRINCIPLES: "Errors never compound" (13 — now satisfied by construction, and the
run measures what it costs); "influences below one quantum accumulate … aggregates
can become a source" (6); "light cones partition compute" (5 — literally the
shells); "Compute only surprises" (3 — the 3×3 broadcast and cell-wide member
delivery do carry sub-quantum arrivals to some receivers; a receiver-side gate
cannot be added without breaking the partition, which is exactly the v3 lesson).

**The lens (second author).** What this lens may have missed: I measured delivery
counting only (one arrival = one unit); the cell-deposit/lazy-read representation
(1 write per flush into a cell word, bodies read on demand) would cut the member
broadcast cost ~pop/k per flush but moves the cost to read time — unmeasured
here. The monopole/dipole choice was measured; quadrupole moments were not (they
should shrink the walk further at 5 words per accumulator). And the finest lever —
the leaf size k against the 3×3 broadcast constant — was left at the harness's
k=16 (144 direct; k=4 would read ~36 but adds a ring level).
