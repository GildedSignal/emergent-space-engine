# Dossier — 20261010-0306-second-20261010-0100-fermi-c11c-4cb2 (second author, Fermi)

## Claim

The checker's named experiment, done, **refutes the silver's lever**: sharing one compiled
cycle across bodies — measured on the shipped law, N co-orbital ships provably sharing one
quantized shape — buys **1.09–1.17×** on every formation-like population (best tail case
6.3×, 7 samples), not the demanded **≥ 40×**, because the compile (`Orbit::compile` /
`Passage::compile`) is only **8–17% of a distinct kick** (5.6 of 52.9 µs on the plane's
made ships; 89 of 137 µs on the passage tail): the cost is the per-body fit, decode,
readout and bookkeeping. The first-breaker ranking itself survives (low orbit averaged at
**rtf 100**: 41.8 machines today, 38.3 with the best made-ship amortization — still
breaks; belt, storage and H_live unchanged), so the adopted premise becomes: **the billion
lives at belt scale, and dense islands need the per-kick rebind itself deleted (a
formation-level generator or secular law, law.md's step 5), not a memo.**

## Bottleneck

Board item 3 (cost at a billion) and the silver's lever sentence. This run deletes the
**compile-amortization lever** from the list (measured ceiling ≤ 6.3× against a 42× bar)
and re-aims the next rung at the resolver's unshared remainder: with the *whole* rebind
deleted (fit included, warm hit kept) a made-ship kick still costs 28.4 µs — 19× the
1.52 µs/kick the 10⁹ low-orbit budget needs. That floor is the number the dense-island
design must beat.

## Evidence

Machine: this Linux box (i7-4790, 8 vCPU, 15 GB; load 1.3→3.3 during the runs, 12.5 GB
available). Orders of magnitude only; integrator re-measures on the M1.

**The record regenerates from shipped code** (digests byte-identical):
```
cargo build --release -p xtask                                            # 39 s
$CARGO_TARGET_DIR/release/xtask universe --kick-bench --seconds 20        # → kick-bench-20s.json  (replay_digest = the run's)
$CARGO_TARGET_DIR/release/xtask universe --kick-bench --seconds 55 --seed {1,2,3}   # ≤ 0.2 s each
$CARGO_TARGET_DIR/release/xtask universe --bench --rtf 100 --seconds 20   # 20 s → bench-rtf100.json
python3 budget.py                                                         # → budget-out.txt (same table, today's box)
```
20 s seed 1: `replay_digest` and `digest` equal the run's stored JSON; median 58.2 µs vs
its 63.4 (shared-box noise, same as its checker saw). The budget table regenerates with
today's inputs at the 55 s window: 39.1 machines (low orbit averaged, rtf 100), cap
2.6×10⁷ bodies, 1,516 ns/kick needed.

**Attribution** (`bench/`, this run's own code driving only shipped public APIs; the plane
replay replicates the shipped loop, and its `replay_digest` **equals the shipped bench's**
at 20 s (seed 1) and at 55 s (seeds 1–3), so the buckets provably cover the record's own kicks;
each bucket min-of-5; attributed sum = 99–103% of `step::process` on every population):

| population (seed 1, 55 s) | process | bind | compile (shareable) | readout | secondaries | tau (orbit_state×2) | field | memo hit (warm) |
|---|---|---|---|---|---|---|---|---|
| made ships (n=25) | 52.9 µs | 25.3 (44%) | **5.6 (10.6%)** | 5.0 | 5.1 | 9.8 | 1.3 | 0.8 |
| leavers (n=12) | 136.7 µs | 108.8 | **89.1 (65%)** | 5.1 | 5.1 | 10.0 | 1.3 | 0.8 |

Within `bind`, `Rebinding::from_state` is 19.1 µs (made): the shareable compile is 5.6;
the other ~13.5 is `fit_key` + phase + residual — per-body state math. Seeds 2–3 agree
(made compile 4.95/5.14 µs; seed 3's leavers: 476.6 of 565.6 µs, 84% — the deep-passage
tail, 6.3× gain, still 59× over the bar after amortization).

**The amortization** (`coorbital` mode: N ships on one circle of the root doll via
`scenario::restricted`, one kick each — the clock law's fictitious step is ~1/orbit on a
stable circle): at N = 64 and 400, radii 6×10⁵ and 2×10⁶, rtf 100 and 1000, all 400 kicks
land in **1 quantized shape** (400 kicks/shape; 373–398 *exact* shapes — the exact key
drifts per kick). The premise is real; the payoff is not: per-kick 19.8–32.9 µs, compile
15–17%, **gain 1.14–1.17×**. `python3 amort.py` → `amort-out.txt` regenerates the verdict
from the JSONs.

**The checker's two corrections, folded in:** the quantized memo's 0% on distinct kicks is
window-dependent (26 shapes / 31 cycles at 55 s = 16% hit, matching its 55 s probe; exact
stays 0%), and the 42×/≥ 40× figures are rtf-100 figures (0.42 machine at rtf 1 for the
averaged billion).

## Predictions

`predictions.md`, written before the decisive runs. **Held:** P1 (attribution shares;
coverage ≥ 65% — measured 99–103%), P4 (the verdict: amortized ≥ 15 µs, gain ≤ 1.3× on
made, ≥ 25× short of 40×, ≥ 10× over the 1.52 µs bar), P5 (quantized 16% at 55 s, exact
0%), P2 on the median basis (leaver bind 80% of median, passage compile 65%; on the *mean*
basis bind is 32% — the tail's heavy kicks are compile-heavy, the typical ones are not).
**Failed, informatively:** P3's exact-key half — co-orbital bodies do *not* share exact
shape keys across kicks (398 distinct for 400 kicks); only the law's 12+12-bit cell is
shared, confirming dbd4add's split at formation scale. P6's ±25% held on seeds 1 and 3;
seed 2's made median ran +37% over the shipped bench's (box load 3.3 during that pair) —
the compile-share numbers are min-of-5 and stable across all seeds.

## What would make it wrong

The M1's compile share could differ, but the refutation has 6× headroom on the best
population and 34× on made ships, and holds under every basis tried (min-of-5 both sides;
the shipped bench's own single-shot totals as base: made 1.09×, leavers 1.31×). It would
be wrong if formations in the real game kick with *passage*-dominated profiles at
population scale (seed 3's 84% share suggests a 6.3× ceiling even there — still short),
or if "batching" means something stronger than sharing the compiled trajectory (deleting
the rebind per body: priced here at a 28.4 µs floor, still 19× over). Adoption cost: none
(numbers and a verdict; no crate, gate or doc touched — `bench/` is new code in this
folder only). Fit with PRINCIPLES: §19 — "a fix signals the wrong representation": the
memo patches a per-kick compile that the formation representation would not have; §3
"compute only surprises" — a formation's kicks are not surprises, and the measurement
shows the surprise-free path is not a cached compile but no rebind at all; §10 — the
simplest falsifying test ran first and killed the lever.

## The lens

The second-author lens measures what the shipped code does; it cannot measure a *different
law* (a formation generator whose kicks cost ~0.8 µs — the memo-hit cost is the closest
proxy and suggests such a law exists to be built). The co-orbital scene is one circle in
the root doll with one far planet; real fleets scatter (eccentricities, evasive burns),
so 1 quantized shape is an upper bound on sharing — but the gain ceiling is set by the
compile *share*, not the sharing factor, so dispersion cannot rescue the 40×. Kick counts
per ship in the windows are small (1–3 per orbit); the per-kick attribution does not
depend on the count.
