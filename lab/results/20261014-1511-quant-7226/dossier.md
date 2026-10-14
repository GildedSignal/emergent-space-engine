# Dossier — 20261014-1511-quant-7226 (Quant lens)

## Claim
The kick's surface search is first counted probe-by-probe on shipped code (**29.4 exact
readouts per search, worst 32, every fired kick**), its digest-identity harness is built and
green — and the obvious quant lever on it (a smarter probe policy on the same exact
predicate) is **killed as built**: three bracketed policies each crawl at ≤ 1.4 bits per
probe because the miss-side anchor's value dominates every chord; the named survivor is an
Anderson–Björck (or inverse-quadratic) update, not any policy tried here.

## Bottleneck
Board line 3: one kick = 75–160 µs against a ~50 ns floor (~10^3.3). The frame-cost record
prices the search at 45–57 % of a fired kick (20261014-0450-quant-1845). This run attacks
the search's *probe count* (the readout is 4.6 µs each, so probes are the whole cost),
the half the warm start (unmerged, gold-checked) leaves cold.

## Evidence (all on this box, Linux/x86 shared; orders of magnitude only)
**The census (shipped, `ES_FP` off — bit-identical semantics, digest equals the pristine
build's):** `xtask universe --kick-bench --seed 3 --rtf 100 --seconds 8` (m400, flying
pace, the search-heaviest arm): **802 `next_impact` searches, 23,552 exact probes — mean
29.4, worst 32**; `next_exit` searches **0** (every exit resolved by the passage's analytic
guess — the guess path carries its own endpoint probes, 1,188 of them); leaver kick median
197.7 µs, all-kick p99 407–460 µs across runs. Held-out seed 7: 1,225 searches, 36,367
probes (mean 29.7, worst 33), leaver 214.6 µs. 29.4 probes ≈ log₂ of the bracket: the
half-orbit bracket is ~2^30 ticks, so the shipped midpoint bisection is *exactly at its
information-theoretic floor for its policy class* — no probe is wasted, the policy wastes
the probes.

**Identity (the adoption precondition, held everywhere):** canonical and replay digests
**bit-identical** off vs on at every arm and seed (s3: `36637e67…`, s7: `cf58ac6e…`),
refused 0, and a new crate test (`the_false_positions_impact_is_the_bisections_impact`)
asserts fast = slow on every handed-out ship of a settled plane, from the binding event and
from periapsis, at the doll's surface and a doubled one — passes. The float chooses the
probe, the integer predicate decides (`to_f64`, "for observation only, never for an
outcome" — its documented contract).

**The kill (pre-registered rule fired):** with `ES_FP=1`, three probe policies, same
predicates, same digests: Illinois on absolute values **2.0× the probes** (mean 55.7, worst
58 — the halving flings a value hugging the level to the origin); Illinois on signed
distances **−4.6 %** (mean 28.0); a vertex-quadratic matched to the branch's flat
periapsis end **1.9×** (mean 54.6); pure two-point secant **1.5×** (mean 44.4, worst 57;
leaver kick median 197.7 → 306.2 µs). Kill rule: worst > 30 (fallback fired) and leaver
median must fall ≥ 25 % — it rose. **Mechanism, from the probe traces** (`ES_FP_TRACE=1`):
the crossing is *not* in the flat zone — the periapsis sits 3–7× the level deeper than the
miss end (deep dips, mid-branch crossings), the local slope is healthy and consistent
(~4.4 units/tick over 2×10⁷ ticks), yet every chord through the retained miss anchor
(whose signed distance is ~10⁸) lands a fraction |d_hi|/d_lo of the way across — a
one-sided linear crawl at ratio ≈ 0.23. **The tail, not the typical case, kills it**
(final regen trace, pure-secant arm): the first three traced searches converge in
**7, 5 and ≤ 4 probes** — the typical search would pay 4–6× fewer readouts — but a
subpopulation crawls past the 30-probe fallback (worst 57) and the mean lands at 44.4
against bisection's 29.4; the degenerate cases are the searches whose first chord lands on
the miss side and leaves the far anchor's huge distance in every later chord. The next
policy must treat that tail (Anderson–Björck's multiplicative retained-side penalty, or a
bail to bisection after ~8 probes), not the median.

Reproduce: `lab/results/20261014-1511-quant-7226/regen.sh` (~3 min: build + 4 bench arms +

## Predictions (predictions.md, written after the baseline only)
- P1 (< 10 mean probes) **failed**: best arm 28.0, all others worse. The mechanism reads
  (crawl diagnosed) but the number does not stand.
- P2 (leaver −25 %) **failed inverted**: +55 % on the final arm.
- P3 (digests identical, suite green with the policy live) **held** — the part that
  would have made it adoptable is done and reusable.
- P4 (made kicks < 10 %) held (−0.7…+8 %, no search on the made path).
- P5 (exit searches ~0 at m400) held, and is itself a finding: the passage guess retires
  the whole exit search where it applies.

## What would make it wrong
The census could over-count if the bench's kick population differs from live flight (it
replays the plane's own snapshots at 60 Hz, refused 0); the crawl diagnosis rests on traces
from two scenes at one pace — a scene whose crossings sit *near* the periapsis (grazing
dips) would flatter the quadratic policy, and the record's warm-start run measured exactly
that regime ("moves by under a tick" settles in two readouts). If the checker finds a
policy in this family that converges, the kill is a kill of my update rules, not of the
lever — the pre-registered rule says so.

## Cost of adopting / fit
Nothing to adopt: the probe policies stay off (default; `ES_FP` env-gated, off = shipped
verbatim). What is adoptable as instrumentation: the probe counters (`step::searches`,
printed by the kick bench) and the fast-vs-slow equality test — zero cost when unread, and
the contract any future search change must hold. PRINCIPLES #1: the cheapest compute is
compute not done — 23,552 probes for 802 crossings is the compute; the next run should
delete probes, not re-time them. Fit with #13 (errors never compound): the exact predicate
decides every step, which is why every arm stayed digest-identical even while the policy
crawled.

## The lens
The quant lens priced the tail (worst per search) before the mean and froze the kill rule
before the run — both earned their keep. What it missed: it reached for the market-microstructure
trick (approximate model guides, exact settles) without first checking *where on the branch
the crossings live*; one trace dump at minute 40 would have redirected the whole hour. The
shape prior ("flat at the periapsis") came from reading the code's monotonicity comment,
not from data.
