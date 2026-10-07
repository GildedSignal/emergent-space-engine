# Dossier — 20261007-1032-quant-7578 (Quant lens)

## Claim

The two-tier encounter certificate's cost is a **burst, not a load**: the median candidate pair pays
zero numeric-window evals while the extreme pair pays 10³–2×10⁴; one body's synchronous re-setup
(what a kick re-pays) is p99 ≈ 20 ms at N = 10⁴ and ≈ 80 ms at N = 10⁵ single-threaded here — 2–3
frames of 30 FPS for **one** body — and candidate degree per body grows ∝ N (×9.97–9.99 per decade,
both held-out seeds) even under the crate's ρ = 1/N scaling, so the allocator's quantum must be the
pair (µs), never the body.

## Bottleneck

Board #4 (smoothness/allocator: "the algorithm that allocates the work to prevent those heavy tails,
it's the most important one", CL 09-25 14:28) and the top scaling risk (candidate work tracking real
encounters). Everything published so far (r8 v2, q-candidate-degree, components-4643) reports
**means** (work per encounter, cone per body, 92% window-setup share); the allocator budgets frames,
which are decided by tails and nanoseconds — both unmeasured until now. No 10× compute claim; this
is the latency/tail half of the certificate's adoption case, and a frame-bust warning with numbers.

## Evidence

Instrument: `tail`/`tailc` subcommands added to `crates/encounters/src/main.rs` (this run's patch,
saved by run.sh; the certificate itself untouched). Uniform belt σ_e = 1e-2, a ∈ [1, 1.5],
ρ = 1/n — byte-identical spec to the shipped `scale n`. i7-4790 (shared VM), single-threaded setup
timing; orders of magnitude only, integrator re-measures on the M1.

Reproduce (each ≤ 60 s except 10⁵ ≈ 130 s):

```
cargo build --release -p emergent-encounters
for seed in 888 999; do for n in 1000 10000 100000; do
  $CARGO_TARGET_DIR/release/encounters tail $n $seed 256; done
  $CARGO_TARGET_DIR/release/encounters tailc coorbital $seed 128; done
python3 lab/results/20261007-1032-quant-7578/analysis.py   # reads decisive.jsonl
```

Held-out seeds 888/999 (decisive.jsonl):

| n | deg_mean | deg max/mean | evals p50/p999/max | setup ms mean/p99 | ns/pair |
|---|---|---|---|---|---|
| 1e3 | 89–94 | 2.2 | 0 / ~1.5k / 2.4k | 4.8–5.6 / ~9 | ~20k |
| 1e4 | 862–864 | 2.7 | 0 / ~1.5k / 6.4–6.9k | 10.5–11 / 19–23 | 3.3–3.9k |
| 1e5 | 8608–8609 | 2.9–3.2 | 0 / 0 / 19.8–21.8k | 42–47 / 72–87 | 1.3–1.6k |
| co-orbital 300 | 299 (= N−1) | 1.00 | 0 / ~0.9k / 1.3k | 3.9 / 5.3–5.7 | ~13k |

Key facts: (1) degree per body ×9.97–9.99 per decade of N — tier-1 output in a fixed-volume doll is
N-linear regardless of ρ (the cone's R-term dominates eps at σ_e = 1e-2: candidates are orbit
crossings); (2) per-pair cost falls with ρ (~20 µs → 1.3 µs) so per-body cost tracks degree, not ρ;
(3) the numeric-window burst never disappears — at 1e5 its probability sinks below p999 while its
**max triples per decade** (7k → 21k evals ≈ ~1 ms/pair); (4) qsteps p999 ≤ 28 everywhere: the
Diophantine step is never the burst, the window numerics are; (5) controls: shipped `scale n 10000`
(separate seed) agrees on cone_pairs (4.35M vs 4.30M) and cone_per_body (870 vs 861), and the
co-orbital control shows the degenerate all-pairs signature (deg = 299 for every body) — the
instrument fails visibly where concentration exists.

## Predictions

`predictions.md`, written before seeds 888/999 (dev seed 777 only): P1 degree ∝ N **held** (9.99,
9.97 in [8.5, 11.5]); P2 thin degree tail **held** (max/mean ≤ 3.18 vs bound 3.2, trend rising with
N); P3 window burst **held at 1e4**, and at 1e5 sharpened: p999 → 0 but max ~21k — the burst hides
deeper and gets heavier rather than vanishing; P4 kick re-pay p99 **held** (19–23 ms in [8, 25]) with
one marginal edge violation (max/mean 3.22 vs bound 3.2, seed 888); P5 co-orbital control **held**;
P6 qsteps **held**; P7 (means unstable ≥ 1.25× across seeds) **failed** — means were stable (1.18×),
so the earlier 3.7× swing of the shipped `scale n 10000` mean (9.1 µs/pair) is *not* reproducible as
seed noise and stays unexplained; suspect its 150-body sample or belt-global `Sorted::e_max`
(one eccentric outlier widens every body's scan). Flagged, not resolved.

## What would make it wrong

Timings are one shared 2014 x86 box — absolute ms shift on the M1 (likely ~2× faster); the burst
*structure* (0-median, 10³+-max evals; degree ∝ N at fixed volume) is algorithmic, not hardware.
The ρ = 1/n scaling changes ρ across the N ladder, so the ns/pair-vs-N cache-capacity question is
confounded and **unmeasured** here; a same-ρ ladder (degree then ∝ N²·ρ) is the follow-up. If the
skin caps window work per pair, P3's tail numbers move — they describe today's certificate.

## Cost of adoption, fit with PRINCIPLES

No code change proposed; three budget numbers go to the allocator and `b-encounter-skin`: (a) the
setup quantum is the pair — µs mean, ~1 ms worst today — so per-pair resumability makes any frame
budget slicable, while a per-body chunk is a frame-buster at belt scale; (b) the skin needs a
per-pair window cap, not just deferral (the max grows with N below the p999 horizon); (c) per-doll N
must be bounded (degree ∝ N in one doll) — the doll partition already in the design is what keeps
tier-1 per body O(1), matching "compute only surprises" and the fixed-density regime q-candidate-degree
certified. Julien: "i care about the p95/99 results i want the game to be smooth" (CL 09-25 14:06) —
P3/P4 are exactly those percentiles, and the mean-based reports to date could not see either.

## The lens

Quant frames costs as tails and capacity, and this run measured tails well — but it did not measure
cache-line traffic (no perf counters taken), heat, or the p99.9 *frame* under concurrent load, and it
accepts the certificate's exactness as given. The blindness to shave: a per-pair work cap (adopting
(b) above) must not quietly weaken the exact-window guarantee — that trade belongs to the
certificate's owner, priced in error type, not in nanoseconds.
