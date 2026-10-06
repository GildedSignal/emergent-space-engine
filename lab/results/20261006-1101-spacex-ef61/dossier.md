# Dossier — 20261006-1101-spacex-ef61 (SpaceX lens)

**Claim.** On the plane's real kick path, the shipped attribution "rebinding fit and compile" is not
the made-body kick's dominant cost: tube **readouts** are (~50% of a made kick: the state readout,
the force gather's reads of the parent tide and secondaries, and the double proper-time readout in
`rebind`), while fit+compile is ~24%; compile dominates only the rarer **passage** rebinds of handed-out
members (~420 µs each, and the tail ladder is *not* the cause — it is the shape's band/knot build).

**Bottleneck.** HANDOFF's plane bottleneck #3 ("a kick costs 29 µs, 15 of them in rebinding fit and
compile", Sol's job, blocked until 9 Oct) and board focus #1 (kicks dominate the engine's cost). The
expected gain from relocating the lever: the readout family is ~2× the fit+compile budget, so a
readout-side fix buys ~2× more than the compile-side fix it would replace; on passages the compile
lever stands (~5× the made-kick total per event).

**Evidence** (Linux x86, shared 8-vCPU box, orders of magnitude only; medians of the shipped
`xtask universe --kick-bench`, seed 1, 20 s = 1200 frames, 32 replayed distinct pending ship kicks;
the instrumented build adds thread-local stage timers that write nothing — both digests are
bit-identical to the uninstrumented baseline: `2fd6e1ce…` state, `c5d2cd0c…` replay):

Made-body kicks, 23 samples, median 45.7 µs (baseline 43.4):

| stage | µs | share |
|---|---|---|
| forces (secondaries + tide + acceleration) | 10.9 | 24% |
| rebind minus from_state (2× proper-time `orbit_state`, decode, clone) | ~12.3 | ~27% |
| residual (at_radius + angle + Residual::between) | 5.5 | 12% |
| compile (cycle, mean 7.6 knots) | 5.9 | 13% |
| fit_key | 5.1 | 11% |
| readout (state) | 4.1 | 9% |
| quantize | 0.1 | 0% |

(`bind_whole` = 28.8 µs; nested fit+compile+residual = 16.5 µs; the ~12.3 µs gap is the rebind
overhead listed above. `rebind` reads the *old* tube's `orbit_state` twice for proper time — two more
full phase inversions per kick.)

Leaver kicks (fleet hand-outs), 9 samples, median 370 µs: compile 234 µs (63% of the kick, 87% of
bind), readout 7.3, forces 9.2, fit 5.4, residual 9.6. About 5 of the 9 are passage compiles at
~420 µs each. **Tail panels: 2.2 per kick (20 total)** — the 15/16 tail ladder is *not* where the
time goes; the passage's shape build (band loop + `append`'s dyadic knot ladder) is [INFERENCE from
code + elimination; passage knots are not tallied]. Cycle rebinds among leavers cost the same ~6 µs
as made bodies (18.2 knots mean).

Memo: exact and quantized hit rates both 0.0 (26 distinct shapes for 26 cycle rebinds) — consistent
with the 5 October correction.

Reproduce (each ≤ 60 s):
./target/release/xtask universe --kick-bench --seconds 20          # baseline (uninstrumented HEAD)
# apply this run's patch (stage timers in crates/space, crates/universe, xtask), then:
./target/release/xtask universe --kick-bench --seconds 20          # staged.json: stages_*_us
./target/release/xtask universe --kick-bench --seconds 20 --seed 7 # held-out seed
```
Patch and raw JSONs: `lab/results/20261006-1101-spacex-ef61/work/` (`baseline.json`, `staged.json`,
`staged-seed7.json`; the diff of the five touched files is `instrumentation.diff`).

**Predictions** (`predictions.md`, written before the instrumented run):
- Held: digest unchanged by instrumentation; fit_key 10–20%; readout 10–20% (9%, edge); compile
  dominates leaver kicks (63% vs predicted 80–95%); memo 0%.
- **Failed:** (1) compile at 45–60% of a *made* kick — it is 13%; the dominant made-kick cost is the
  readout family (~50% counting the force gather's reads and the double proper-time readout).
  (6) the passage tail ladder at 100–300 panels — it is ~2–4 panels; the passage cost sits in the
  shape's band/knot build. Held-out seed 7 (`staged-seed7.json`, 23 made + 1 leaver samples): same
  structure — made compile 5.7 µs against forces 10.1 + readout 3.8; the one leaver kick has
  compile 410 µs of a 451 µs bind (91%), with 27 tail panels: the tail count varies by scene, and
  compile dominates it.

**What would make it wrong.** This is one scene (one star system, one fleet) on Linux x86 with 32
samples; the M1's balance may differ (HANDOFF's 29 µs/15 µs fit+compile claim was measured there —
if the M1's readouts are relatively cheaper, the lever moves back to compile). The rebind-overhead
split (~12.3 µs) is by subtraction, not direct timing. Passage-knot counts are inferred, not tallied.

**Cost of adopting.** Nothing to merge: the instrumentation is a lab probe (the patch restores
cleanly; `run.sh` saves it). The finding redirects effort: before optimizing `fit_key`/compile for
the common kick, count the readouts per kick (state, tide, secondaries, proper time ×2, decode ≈ 5+
phase inversions) and delete or reuse them — e.g. the two proper-time readouts differ by one known
interval and the previous answer's knot/psi is in hand; a warm-started inversion changes bits (it
terminates on a quantum), so the exact deletion must instead *cache the phase inversion per tube
between events* or read proper time from the knot table's running sums, not re-solve it.

**Fit with PRINCIPLES.** "Compute only surprises" (3): a kick's own event changes one body's state,
yet the resolver re-derives five independent phase inversions of tubes that did not change (the old
tube read twice for proper time is pure re-derivation of known information). "The best part is no
part" (17): the deleted readouts are the cheapest compute there is. "Measure before claiming" (10):
the 29 µs/15 µs attribution did not survive a stage-level measurement on the real replay path.

**The lens (SpaceX).** The idiot index ranks the readout family first (~20–24 µs vs a floor of one
table lookup + adds per already-solved phase), fit/compile second. What the lens may have missed:
sample size (32 kicks, one scene, one machine) — a distribution over scenes could rebalance the
stages; and I did not verify the M1's original 29 µs decomposition, only that Linux's differs.
