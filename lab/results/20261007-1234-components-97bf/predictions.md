# Predictions — run 20261007-1234-components-97bf

Component: the sparse order's event calendar (the plane's "one clock, one queue").
Incumbent: `lattice-event`'s `Calendar` — indexed 4-ary heap of (tick, body), one slot per
body, `pos` backpointers (copied verbatim as the benchmark's incumbent).
Candidate: hierarchical bitmapped timing wheel on integer ticks, intrusive doubly-linked
per-body nodes, ring of W = 2^21 buckets, indexed-heap overflow for delay ≥ W.
Both must deliver the identical (tick, body-id ascending) stream; digest equality is the
positive control. Negative control: no structure (linear scan of the per-body time array).

Workload (case A, engine-shaped): per delivered event one re-schedule (85% "later",
geometric-ish up to 2^20 ticks, quantized to epochs of 64 ticks; 15% near-immediate) plus
one external churn `set` from the same mixture — the shape the crate comment names
("re-predictions mostly move a slot later"). Cases: B all-earlier churn; C clustered
(delays ≤ 1024); D far horizon (delays up to 100·W, overflow-heavy). N swept 2^12..2^24,
3 seeds, single thread. Cloud timings are orders of magnitude only.

Decisive run = `bench A B C D` sweep at N ≥ 2^20. Predictions, written before it:

- P1 (correctness, must hold or the run is VOID): wheel and heap digests match on every
  case, seed and N; the linear control matches too.
- P2 (scaling): heap ns/op grows ≥ 2.0× from N = 2^12 to 2^24; wheel grows < 1.4×.
- P3 (ratio): at N = 2^24 case A, wheel total ns per op ≤ 0.25× heap (≥ 4× faster).
- P4 (tail, principle 12): case A at N ≥ 2^22: wheel p999/p50 ≤ 3; heap p999/p50 ≥ 4.
- P5 (negative control): linear scan ≥ 100× the wheel's cost at N = 2^16.
- P6 (floor): wheel ops touch ≤ ~8 words mostly L1-resident; measured wheel ns/op within
  10× of the 2-writes-2-reads floor on this machine (~4 ns/op single-thread lower bound
  from dependent 8B traffic; the exact number is calibrated, not assumed).
- P7 (named failure mode): case D degrades the wheel to within ~2× of the heap (overflow
  path); the wheel is not claimed universal — its horizon W must cover the certificate
  span or it reverts to a heap.
- P8 (sensitivity check): if the heap shows no growth with N (slope < 1.5× over the
  decade range), the benchmark fails to exercise queue depth and the scaling claim is
  withdrawn (VOID for P2/P3), whatever the ratios.

Extrapolation to 10^9 (not a prediction, a model): heap cost ~ log4(Q) random touches,
wheel cost flat; if P2/P3 hold, the incumbent calendar is ~30–300× over the floor at
10^9 bodies, and the measured crossover says the wheel wins already at the plane's
current 10^6 scale.
