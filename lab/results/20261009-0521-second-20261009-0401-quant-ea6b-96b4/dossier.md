# Dossier — 20261009-0521-second-20261009-0401-quant-ea6b-96b4 (second author)

**Claim.** The prior run's stage decomposition was measured on the wrong code path; with the timers
on the path the bench actually samples, one kick of the plane's resolver costs a mean 79.4 µs /
median 66–69 µs (made 35–37 µs, fleet members 70–71 µs; legacy split `fn kick`, 9180 of 9192
samples), **84.6% of it in the rebind's tube work** — not 59.3% — and the engine's own kick calls
reproduce the same shares independently (84.5–84.8%), so deleting the recompile (the jet/re-anchor)
addresses ~85% of the real kick, not 59%; the kick is compute-bound where it matters (the rebind
slows only 1.20× cache-cold; the small stages are the memory-bound ones: readout 2.78×, forces
3.14×); and two derived numbers of the prior claim were wrong and now regenerate from the record:
the true mean is 79.4 µs (not 52.6) and the true cadence 1.32×10⁻² kicks per active ship per
game-second (not 1.5×10⁻³ — the prior run divided by the 2046-ship fleet target, but only 232
ships were active on average), so the resolver saturates one core near **9.5×10³ ships at rtf 100**
— not 1.3×10⁵; the gap to 10⁹ is ~5 orders per core, not 3.

**Bottleneck.** Board focus line 1: "fewer kicks per orbit … kicks dominate the engine's cost".
This fixes the pricing of the jet/re-anchor lever the board already holds: its addressable pool is
84.6% of every real kick (not 59.3%), and a 20× cut on rebind would take the mean kick from
79.4 µs to 15.6 µs and capacity ×5.1 (to ≈4.8×10⁴ ships/core), not ×2.3.

**Evidence** (Linux x86, i7-4790, loadavg 0.3–0.9, 13 GB free; each command ≤ 40 s; orders of
magnitude only, M1 re-measures). Instrumentation: `work/patch.diff` (git apply on the clean tree
`a838a28`) puts per-path timers in `crates/universe/src/step.rs` — LEGACY = `fn kick`, CLOCK =
`kick_clock` (the energy register, law v2), each with call counts and rebind counts — and the bench
(`xtask/src/universe/kick_bench.rs`) tags every sample with its path and doll, adds `mean` to every
percentile group, records `ships_mean`/`game_seconds`/`cadence`, and separates three accumulator
phases (bench replays / bench cold replays / the engine's own calls during `frame()`), fixing both
of the checker's traps (wrong path; cold+warm double-count).

```
cargo build --release --locked --offline -p xtask
X=/home/glmlab/lab-target-0/release/xtask
$X universe --kick-bench --seconds 10                              # digest control (also run clean first)
$X universe --kick-bench --members 2000 --seconds 30 --rtf 100     # warm, the decisive run
$X universe --kick-bench --members 2000 --seconds 30 --rtf 100     # repeat (share stability)
KICK_COLD=1 $X universe --kick-bench --members 2000 --seconds 30 --rtf 100
$X universe --kick-bench --members 2000 --seconds 20               # rtf 1
python3 analyze.py kick-*.json                                      # every number below
```

- **Digest control.** Clean and patched binaries at default args give the identical
  `replay_digest dac49af3…` and identical memo counts; the m2000 runs give `ca74ff5a…` with memo
  quantized hit 0.970988618611917, 260 shapes, 8962 rebinds — bit-identical to the prior run's
  saved JSONs and to my repeat. The instrumentation changes no behaviour; the identical cold-run
  digest is also the in-record proof that `process` is pure (the checker's point 5, now cited).
- **Population** (doll_histogram + paths): 9192 samples = 9180 legacy `fn kick` (8827 fleet
  members: doll2/L0 9137 + doll2/L1 4; doll3/L0 39; 353 made) + **12** `kick_clock` (all made,
  doll0). The prior run's "(all kicks)" table was these 12.
- **Stage shares, legacy path, bench replays (n=9180):** rebind **84.6%**, gather 8.8%, readout
  4.9%, forces_quant 1.4%, other 0.3%; no-fire (sub-quantum, carried) 0.04%. Engine's own calls
  (n=9213, an independent population): rebind **84.8%** (84.5% in the repeat). Repeat run: 84.3%.
  Shares stable to ±0.3 points.
- **Clock path (n=12):** rebind 59.6%, gather 22.5% — the prior run's 59.3%/21.8% exactly; its
  label "(motion law v2)" was wrong for the medians but its stage table *was* this path's.
- **Units audit** (the prior run's 10³ trap): legacy `calls × mean = 9180 × 79.30 µs = 728.0 ms =
  legacy_total_ns` — exact, in-record. The engine phase (9213 × 76.2 µs = 701.8 ms) audits too.
- **Cold/warm paired (n=9192):** 95.50 / 68.36 µs median = **1.40×** (prior run: 1.379×). By stage
  (per call, warm→cold): rebind 69.0→83.0 µs (**1.20×**), gather 7.2→9.7 (1.34×), readout
  3.7→10.3 (**2.78×**), forces_quant 1.0→3.2 (**3.14×**). The dominant cost is the least
  cache-sensitive: the rebind is compute, the 15% tail is memory.
- **Cadence/capacity, now regenerable:** ships_mean 231.7, game_seconds 3000, cadence =
  9192/(231.7×3000) = 1.322×10⁻² kicks per active ship per game-second; capacity =
  1/(79.38 µs × 1.322×10⁻² × 100) ≈ **9.5×10³ ships/core at rtf 100** (≈3.8×10⁴ on 4 P-cores).
  The prior run's 1.27×10⁵ divided kicks by a fleet (2046) that was 8.8× larger than the ships
  actually active; the rtf-1 run's first-handout kicks (median 384 µs, n=3) confirm its cold-shape
  observation.

**Predictions** (`predictions.md`, written after the digest control, before the decisive runs).
Held: legacy ≥ 98% (99.87%), rebind > 75% (84.6%), stage ordering, no-fire < 20% (0.04%),
cold/warm 1.2–1.5× (1.40×), warm-phase shares match the warm run within 5 points (85.0 vs 84.6),
clock path 55–65% (59.6% — the prior table's source). **Failed, honestly:** the mean landed at
79.4 µs, above my 40–60 µs band — I anchored the band on the prior run's 52.6 µs, which this run
shows was never this population's mean (the leaver tail, p99 372 µs, carries it; medians reproduce
bit-comparably). The units audit inside prediction 4 held exactly.

**What would make it wrong.** The shares are wall-clock sums over ~10⁴ calls of 4 hand-picked
regions; a cost that straddles a region boundary lands in "other" (0.3%). `?`-refused kicks record
no stages (refused = 0 in every run here). The scene is one seed at one fleet fill level (mean 232
active of a 2000 target): cadence is the intensive measure but was measured while the fleet was
still filling; a full belt at 10⁶ ships can raise encounters per ship, so 9.5×10³/core is this
scene's number, the *ratio* rebind≈85% is the portable one. Law v2 (`kick_clock`) remains
effectively unbenched — 12 samples, and only because the bench catches it when a Kick happens to
sort first; a clock-body bench needs its own sampler (checker's point, still open). Cloud x86, not
M1; medians inflate ~1.5× under load 3.75 (prior checker's probe) while shares and digests do not
move.

**Adoption cost and fit.** Nothing to adopt in the engine: the numbers re-price a lever the board
already holds (jet/re-anchor, the adopted design since the 5 October artifact). PRINCIPLES 1 ("the
cheapest compute is compute not done"): the measurement now says the recompile is 85% of every
real kick, confirmed by the engine's own calls, and that it is compute — so delete it, don't tune
the cache. PRINCIPLES 10 ("measure before claiming"): the 59.3% and the 1.3×10⁵ were both
measurements of the wrong thing; both corrections are in-record. The patch is instrumentation
only, 300 lines incl. the bench's tagging, digest-proven inert.

**The lens.** A quant prices paths; it can miss that the *cadence* is the truer lever — 1.3×10⁻²
kicks/ship/game-s is itself the number to delete (board: cadence beats correctors), and this run's
capacity correction (5 orders, not 3) makes that more urgent, not less. The cold-stage split
(readout 2.8×, forces 3.1×, rebind 1.2×) is a lever the prior run averaged away: if the rebind is
ever cut, the residual kick becomes memory-bound and layout starts to matter — the opposite advice
of the whole-kick 1.37× figure.
