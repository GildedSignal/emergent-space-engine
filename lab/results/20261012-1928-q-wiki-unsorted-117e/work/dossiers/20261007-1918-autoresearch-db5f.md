# Dossier — 20261007-1918-autoresearch-db5f

**Claim.** The Darwin compiler (`crates/space`, `Orbit::compile`) is within
~1.5× of its bit-identical speed floor on this hardware: a three-round
autoresearch loop over its real cost structure moved ns/compile by only
−1.2% (kept: knot/crossing vector preallocation, +8 lines, bit-identical,
all 40 crate tests pass), and the two arithmetic rounds measured +0.6%
(noise, reverted) and +11% slower (regression, reverted) — so the next 10×
on the board's kick bottleneck is not per-compile arithmetic but
cross-compile reuse (the shape memo), which measurement here confirms is
the right lever, not a proxy.

**Bottleneck.** Board line 1 focus: "fewer kicks per orbit … kicks dominate
the engine's cost"; taste log: the plane recompiles an orbit on ~99% of
kicks, so ns/compile ≈ ns per kick event. Expected gain from this lens was
an honest 1.2-2×; the measured answer is that even that is nearly gone.
What it deletes: any further plan to micro-optimize the compiler's inner
arithmetic bit-identically; the effort belongs to the memo (already in
flight) and to panel count (a law decision, not an optimization).

**Evidence** (Linux x86 runner, 8 vCPU, shared; orders of magnitude only per
the lab rules; every keep/revert decision re-measured as interleaved A/B
after load rose 0.65 → 1.2):

- Reproduce: `lab/results/20261007-1918-autoresearch-db5f/measure.sh`
  (min-of-5, pinned core) and `…/ab.sh` (interleaved pristine-vs-patched
  via `git stash`). Bench source: `…/bench/` (own crate, path dependency on
  `crates/space`; build ≈ 5 s warm). Baseline pristine: 16546-16576
  ns/compile geomean over 44 keys; kept patch: 16373-16387 (−1.2%).
- Cost attribution (temporary counters + standalone op copies, `bench/src/ops.rs`):
  cos() 42 ns/node = 26-31% of ns/compile; div_word 18 ns; u128 `/` 25 ns;
  isqrt 91 ns; weak panel arithmetic ≈ 331 ns vs ~650 ns per knot wall-clock;
  knots ≈ bands ≈ 16·log₂((1+e)/(1-e)) — the panel count, i.e. the law's own
  resolution decision, is the structural cost driver.
- Bit-identity: digest `05cbbb1d…` (44-key tuning corpus) and `c8c103c7…`
  (160-key held-out corpus) identical on pristine and patched.
- `cargo test --release -p emergent-space`: 40/40 pass on the patched tree.
- Cloud timing caveat honored: all numbers are x86 runner orders of
  magnitude; the integrator re-measures on the M1.

**Predictions** (`predictions.md`, written before the held-out run): all
three held — (1) held-out digests identical; (2) cost moved 0.6-1.8%, inside
the predicted 0.5-2%; (3) mean knots/key 70.8 inside [44, 85], per-knot
cost 946 ns on the held-out mix, ~45% above tuning because the randomized
mix reaches the compact general path (`node()`) that the tuning grid barely
sampled — noted, not tuned on.

**What would make it wrong.** A checker measuring on the M1 could find the
preallocation gain disappears (different allocator/cache geometry) — the
patch would then be pure churn to drop; and if the plane's memo (Sonnet's
wiring) reaches its predicted 95-98% hit rate, ns/compile stops being the
kick cost at all, making even a true 2× here irrelevant to the board line.
The negative result on arithmetic rounds would be wrong only if some
non-bit-identical restructuring (e.g. different panel widths) is allowed to
count as "same behaviour", which is a law change, not this lens.

**Cost of adopting.** Eight lines in `OrbitShape::bound`, exact band count
already computed by the same predicate the loop uses; no API, storage or
arithmetic change; digest-proven bit-identical; fits PRINCIPLES #1 ("the
cheapest compute is compute not done") and #2 (behaviours fixed as
constraints — exact integer outputs unchanged, verified on unseen keys).

**Fit with PRINCIPLES.** "Measure before claiming" — the claim here is a
measured ceiling; "a failed expectation is not automatically a failed
method" (H0183) — the −11% round is reported as a microbench-distribution
lesson (op probes must sample real call-site operands), not buried.

**The lens.** A local search finds local optima: this loop confirms one and
bounds it. What structural change would beat it: not any bit-identical edit
— either reuse across compiles (ShapeMemo/QuantizedMemo, in flight) or a law
decision to cut panel count (e.g. coarser bands far from the separatrix),
which changes sums and belongs to the law's owner with the gates as judge.
