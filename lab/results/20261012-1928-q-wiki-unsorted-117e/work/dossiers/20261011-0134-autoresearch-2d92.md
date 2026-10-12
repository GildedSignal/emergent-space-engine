# Dossier — 20261011-0134-autoresearch-2d92

**Claim.** Exact i64 fast paths for the lattice law's visit predicates (`hit64`, `first_hit64`,
guarded by the GPU's own exactness certificate, i128 fallback) cut the contact engine's cost per
event by 11–16% on the contact-dense tracks with bit-identical outcomes, and the profile now
says where the rest of the cost lives: the neighbour-visit loop (43%) and the calendar heap
(16%), not the exact arithmetic.

**Bottleneck.** Board item 5 / "Headed next" 5: contacts at scale in the plane's Fermi-frame
battles; the ladder's `ops / fired` and `ns / event` are the cost measures. Not a 10×: an
adoption-ready constant-factor cut plus the map for the next run.

**Evidence** (GitHub Actions Linux, 8 vCPU, shared; 3-rep means; digests checked every run):

| track | n | main ns/fired | final ns/fired | gain | digest |
|---|---|---|---|---|---|
| gas 0.1 (tune) | 256 | 3394 | 2928 | 13.7% | same |
| gas 0.1 (tune) | 1024 | 3721 | 3272 | 12.1% | same |
| gas 0.1 (tune) | 4096 | 4328 | 3793 | 12.4% | same |
| gas 0.1 (held out) | 64 | 2912 | 2592 | 11.0% | same |
| gas 0.1 (held out) | 16384 | 5386 | 4767 | 11.5% | same |
| gas 0.3 (held out) | 1024 | 3690 | 3098 | 16.0% | same |
| random (held out) | 4096 | — ns/body 1793 | 1649 | 8.0% | same |
| crowded axes (held out) | 4096 | — ns/body 2163 | 1955 | 9.6% | same |

Ops counts are unchanged (ops/fired 94.4 at gas 4096, `scaling.rs`): the change is pure
arithmetic, the algorithm untouched. The engine's cost test (`cargo test -p emergent-engine
--release --offline --test cost`) passes on both trees, orders equal, numbers within noise
(the battle scene's cost sits in apply/upkeep, not the predicates).

Reproduce (each ≤ 60 s):
```
cargo test -q -p emergent-lattice --release --offline            # incl. new equivalence test
cargo test -q -p emergent-lattice-event --release --offline      # equality vs Chronon (bit identity)
cargo run -q -p emergent-lattice-event --release --offline --example scaling   # ladder table, `equal yes`
cp lab/results/20261011-0134-autoresearch-2d92/work/bench.rs crates/lattice-event/examples/
cargo run -q -p emergent-lattice-event --release --offline --example bench -- all   # ns/fired + digests
```
`work/main-3reps.txt` / `work/final-3reps.txt` hold the A/B raw runs; `work/cost-{main,final}.txt`
the engine runs; `work/patch.diff` the change (also saved by run.sh).

**Predictions** (`predictions.md`, written before the decisive run): the constraint held —
digests bit-identical on every held-out case. The magnitudes did not: I predicted 25–45% on gas
(11–16% actual), 20–35% at fill 0.3 (16%), 30–55% on random/crowded (8–10%), 20–40% on the
engine's cost test (≈0, noise). Miss diagnosed: I estimated `first_hit`'s cost from its i128
source, but LLVM already folds the sext·sext products to single 64-bit multiplies, so the None
path (90% of calls) was near-parity already; the win is in the hit-search iterations, adds and
compares. Lesson: read the generated code (or profile) before pricing an arithmetic change.

**What would make it wrong.** A guard bug: the domain proof (|d_c| ≤ 2²⁶, |w_c| ≤ 2¹⁶,
reach ≤ 2²⁴ keeps every intermediate in i64 or one widening product; worst case |d+w·m|² ≤ 2·dd)
is checked by the new equivalence test (200k visitor-regime cases + 50k deep searches + corners,
vs the i128 truth) and by the whole equality suite. Linux/x86 timings: orders of magnitude only;
the integrator re-measures on the M1. If a world's cell side exceeds ~2²⁴ units the guard fails
and the i128 path runs (correct, no gain — same as today).

**Cost of adopting:** one patch, no API change (`hit64`/`first_hit64` are new `law` functions
with the domain documented; the two `EventCore` call sites guard and fall back). No new state,
no schedule dependence. PRINCIPLES fit: 16 ("physics loves e while we love 2… no it's about
what's cheapest to compute"), 26 ("steal from what works": the GPU crate's own i64 certificate,
extended to the CPU visitor), 2/13 (exact means deterministic: same bits, errors cannot compound
— the fast path is a different arithmetic for the same function, not an approximation).

**The lens:** autoresearch optimises locally; it found a constant factor. The structural change
that would beat it, per the profile: the visit loop's 43% is paid per neighbour per prediction —
a covering certificate that batches re-predictions (one sweep over a cell's pairs instead of per
body), or a calendar without sift-down on every later-set (14%), is the next run's lever. Neither
is reachable by tuning this representation's knobs (round 2: no effect).
