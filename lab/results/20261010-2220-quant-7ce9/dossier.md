# Dossier — the kick's latency budget, decomposed (Quant lens)

**Claim.** On the shipped plane, one kick costs 41 µs (median), of which 72% is the rebind path (every kick rebinds), 25% is per-kick secondaries setup that 487 kicks per epoch recompute identically, and only 4% is the exact force arithmetic — so the cheaper-exact-kernel and memory-layout levers are killed for the plane, the lever is epoch-shared setup plus the rebind, and the exactness premium (27–30× an f64 twin per secondary-eval, flat from L1 to DRAM) only becomes the wall in dolls with many massive secondaries.

**Bottleneck.** "Fewer kicks per orbit at the same behaviour — kicks dominate the engine's cost" (board, live question 1) and "cheaper events" (bottleneck 3). This run names *where inside a kick* the ns go, so the next build does not spend a step on the wrong stage. Expected gains: epoch-sharing setup deletes ~25% of every kick at zero exactness cost and turns O(kicks × S) state evaluations into O(epochs × S) at belt scale; it deletes nothing else.

## Evidence

Machine: shared GitHub Actions runner, i7-4790 (Haswell), load 1.1–1.4 of 8 during the runs; Linux/x86, orders of magnitude only (the integrator re-measures on the M1). Outputs: `decompose.out`, `sweep.out` in this folder.

Decomposition (the real plane, `scenario::plane` seed 1, rtf 1, members 48; the kick-bench's own replay protocol — one sample per distinct pending ship kick at deterministic 60 Hz snapshots, pure resolver `step::process` only; 8,280 samples over 6 s of game time; S = 3 secondaries median):

| stage | median | share of kick |
|---|---|---|
| full `step::process` | 41.3 µs (p99 64.1, max 102.5) | 100% |
| setup: `ctx.secondaries` + `ctx.tide` | 10.1 µs | 24.5% |
| kernel: `force::acceleration` (exact, S=3) | 1.57 µs | 3.8% |
| residual: drift readout, sigma-delta, rebind | 29.6 µs | 71.8% |
| f64 twin of the same kick's forces | 0.087 µs | — |

- `rebind_rate: 1.000` — every one of the 8,280 kicks leaves a new tube entry. The residual is the rebind path (corroborates the 5 October memo finding from the cost side; attribution is by rate, not by timing `bind` itself).
- **Epoch concentration: 17 distinct (doll, tick) epochs for 8,280 kicks — 487 kicks per epoch.** Each of those kicks calls `ctx.secondaries(doll, t, i)`, which allocates a fresh `Vec<Secondary>` and re-evaluates every source's tube state at the *same* `t`; only the `except`-self member of the Vec can differ, and only for the few bodies that are themselves sources. Aligned block steps (`step::aligned`) make the sharing exact: identical inputs, identical outputs, no exactness cost.
- Working-set sweep (shipped `force::field`, S = 8, deterministic synthetic secondaries at plane-like magnitudes; exact vs an f64 twin on pre-converted mirrors):

| working set | exact ns/eval | twin ns/eval | ratio |
|---|---|---|---|
| 32 KB (L1) | 916 | 31.0 | 29.6× |
| 256 KB (L2) | 836 | 29.3 | 28.5× |
| 8 MB (L3) | 647 | 21.3 | 30.4× |
| 64 MB | 591 | 21.3 | 27.7× |
| 320 MB (DRAM) | 578 | 21.3 | 27.1× |

  No memory cliff anywhere in a 10,000× working-set range: the exact kernel is **arithmetic-bound at every scale the game will run**. `Secondary` is 96 B — one 128 B line when aligned, so the record already fits the M1's line.

Reproduce (each ≤ 60 s after a one-time build):
```
cd lab/results/20261010-2220-quant-7ce9/kickfloor && cargo build --release
/home/glmlab/lab-target-3/release/kickfloor decompose   # ~9 s
/home/glmlab/lab-target-3/release/kickfloor sweep       # ~3 s
```
(Bench source: `kickfloor/src/main.rs`; the exact path is shipped crate code throughout — `scenario::plane`, `step::process`, `ctx.secondaries`, `force::acceleration`, `force::field` — only the f64 twin is new code, formula per `force.rs` docs.)

**Predictions.** `predictions.md`, written before the binary first ran. Held: totals (41.3 vs 5–40 µs, at the edge), setup share, residual plurality, per-eval ns, no memory cliff. Missed: the exact/f64 ratio is 27–30× (predicted 5–15× — exactness costs twice my upper bound), the kernel's share is 3.8% not 10–40%, and epoch concentration is 487× (predicted ≤3×). One unregistered observation: rebind_rate 1.000.

**Kill rules** (frozen in `predictions.md` before the run): K1 fires — kernel 3.8% < 20%, so "cheaper exact kernel" is killed as the plane's next lever. K4 does not fire — no ns/eval doubling by 64 MB, so memory layout is killed as a lever at game scale. K3 does not fire (kernel share too small). K2's premise inverted: the premium is real (27–30×) but irrelevant at the plane's S.

**What would make it wrong.** (a) A belt doll where aggregates make S large: at S ≈ 300 the kernel would be ~180 µs/kick and cross the 30% line — then the sweep's flat 578–916 ns/eval says the lever is the *arithmetic* (the `isqrt`/exact-division tail of `Scalar`), never the layout. (b) The residual→rebind attribution rests on rebind_rate plus the earlier memo finding, not on timing `bind` directly; a checker can split it via the `bind` API. (c) x86 timings, single-threaded, shared machine; the M1's 128 B lines and 4 P-cores shift the DRAM slope and the twin's cost (its f64 divide is ~13 cycles there). (d) The plane's kick mix (28 made bodies + 48 fleet members, S = 3) is one point in the space; rtf, member count and fleet order change the mix, not the shares' order.

**Cost of adopting.** The epoch cache: a per-(doll, tick) `Vec<Secondary>` computed once per kick epoch (with sources skipping self by index, not by rebuild), keyed exactly, invalidated each frame — small, local to `Ctx`, no law change, no gate affected (identical integer outputs). The rebind side is already the integrator's queue (cadence, memo); this run only prices it.

**Fit with PRINCIPLES.** "The cheapest compute is compute not done" (§1) and "Nothing is evolved that can be derived when looked at" (§3): 487 identical per-kick rebuilds of the same epoch's secondary states are exactly that. "Compute only surprises… no work for no reason" (§14). The kernel result obeys "Exact physics is the oracle, not the implementation" (§2): the premium is measured and left alone where it does not bind. And via negativa: two levers (micro-optimising the exact kernel, cache-line layout) are deleted before anyone spends a step on them.

**The lens.** Quant prices stages and tails; it measured a 60 Hz snapshot distribution (p99 2.1× median) on one scene, and its blind spot is exactly what it cannot price: the rebind path's cost is a *representation* question (what a tube recompile must redo), not an ns question, and shaving the exact kernel would have spent simplicity for 4% — the kill rules existed to stop that urge. It also did not probe parallel contention (the sweep is one thread) or the M1 itself.

Self-grade: **silver.** Real, reproduced on shipped code, predictions pre-registered, two levers killed, one lever named with a 487× concentration measured — one experiment away from gold: build the epoch cache and show the kick median drop ~25% on the plane, then rerun at belt scale where the epochs argument decides O(kicks) vs O(epochs).
