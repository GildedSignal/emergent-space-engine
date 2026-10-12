# Dossier — 20261008-0458-dynamics-7166 (lens: dynamics and attractors)

## Claim

The frozen contact law `es-lattice-relativistic-v1` is **smooth in the dilute regime — per-chronon contacts are Poisson (Fano 0.98–1.4) and per-chronon ops p99/p50 ≤ 1.7 at every N tested — but the contact process is not Poisson at scale: the Fano factor grows with N at fixed packing, in a walled gas (1.2 → 6.4 → 30.5 at fill 0.2, 1024 → 16384 bodies) and in the engine's own stock battle scene (1.7 → 3.5 → 13.6 → 40.2 at spacing 5q, 400 → 25 600 bodies), while per-body contacts over a battle crossing grow ≈ √N (optical depth) — a tail that grows with fleet size and no gate measures; the law itself has no energy drift (trapped gas E/E0 = 1.00 at 3600 chronons, all three laws; a two-body cradle conserves exactly to 10⁶ ticks).


## Bottleneck

Smoothness and the allocator (board #4, OC#36 "i care about the p95/99"). The event core's wake/batch cost premise ("a partner's stale slot only costs a spurious wake-up") assumes thin-tailed event rates; this run measures those tails on the real law for the first time. Order of magnitude at stake: whether per-frame battle cost stays O(median) as fleets grow, or the tail (Fano 30 at 16k bodies, fill 0.2) starts eating frames. Nothing to delete yet; one gate candidate (a Fano/tail gate on the contact law at fleet scale).

## Evidence

Machine: GitHub Actions Linux runner, 8 vCPU (i7-4790-class x86), load 0.4–0.9, 14 GB free. All numbers integers or event counts; timings are order-of-magnitude only (cloud rule).

Instrument: `crates/lattice-event/tests/avalanche.rs` (per-chronon Δops/Δfired from `Metrics`, `EventCore`, scenes `worlds::gas` and a spacing-parameterised copy of the engine's `scenes::battle`); `crates/lattice-event/tests/inst_check.rs` (cross-checks). Commands, each well under 60 s:

```
cargo test --release -p emergent-lattice-event --test avalanche gas_packing -- --nocapture   # 24 s
cargo test --release -p emergent-lattice-event --test avalanche instrument_control -- --nocapture
cargo test --release -p emergent-lattice-event --test inst_check -- --nocapture             # 4 s
cargo test --release -p emergent-lattice-event --test avalanche battle_front_scaling -- --nocapture   # fixed harness, run by the checker
```

Positive control (lone body in a box): flat 10 ops/chronon, zero batches — the instrument measures the law, not itself. Identity control: `EventCore` equals the `Chronon` reference (world digest and fired count) at ticks 300–1700 on gas(1024, 0.05) — the sparse path the plane flies is the reference.

Trapped gas (walls, radius q, |k| ≤ q/8, 1500 chronons after 200 burn-in):

| fill | n | contacts/tick mean | Fano | ops p99/p50 | max same-tick pairs |
|---|---|---|---|---|---|
| 0.05 | 1024 | 5.2 | **0.98** | 1.57 | 16 |
| 0.05 | 4096 | 20.5 | 1.10 | 1.32 | 44 |
| 0.05 | 16384 | 85.6 | 1.14 | 1.17 | 126 |
| 0.1 | 16384 | 177.8 | 1.41 | 1.17 | 241 |
| 0.2 | 1024 | 25.0 | 1.20 | 1.66 | 71 |
| 0.2 | 4096 | 104.5 | **6.44** | 2.05 | 265 |
| 0.2 | 16384 | 526.1 | **30.5** | 1.62 | 962 |
| 0.4 | 4096 | 265.8 | 12.35 | 1.44 | 4074* |


Battles (stock `scenes::battle` parameters, spacing 5q, mixed responses, fixed harness):

| n | contacts/tick mean | Fano | ops p99/p50 | max ops / p50 | contacts per body |
|---|---|---|---|---|---|
| 400 | 2.1 | 1.72 | 2.79 | 29 | 4.7 |
| 1600 | 12.2 | 3.54 | 1.67 | 18 | 9.2 |
| 6400 | 66.5 | 13.58 | 1.33 | 14 | 18 |
| 25600 | 242.1 | 40.22 | 1.31 | 13 | 27 |

Energy: `Chronon` on gas(1024, 0.05) for 3600 chronons — E/E0 = 1.00 (Newtonian), 1.00 (Relativistic), 0.99–1.00 (RelativisticV1); contact rate flat at ~4.6–5.1/tick. Two-body cradle (equal masses, 10⁶ ticks, ~247 contacts): E/E0 = 1.000000 for all three laws; unequal (1 vs 4, 396 contacts): +1.4% (Newtonian), −8.9% (V1) — rounding both ways, no runaway.

## Predictions

In `predictions.md`, written before the decisive run. Scorecard, honestly:

- P1 low fill (Fano < 3 at fill ≤ 0.2, no growth with n): **held at fill ≤ 0.1** (Fano ≈ 1, the Poisson premise is true there); **failed at fill 0.2** — Fano grows with n (6.4 at 4096, 30.5 at 16384). The boundary is not in fill alone but fill × n; I did not predict that.
- P1 high fill (cage clustering, Fano > 10 or max_batch ≥ 30): mixed — max_batch ≥ 30 is a genesis artifact, not dynamics; Fano at fill 0.6, n=1024 is 1.12 (the jammed gas rattles uniformly — clustering appears only with n). My "boundary in (0.4, 0.7)" is not established.
- P1's max_batch ≤ 10: failed (16–241 dynamically, ~n^0.45 at fill 0.05); it is the max same-tick pair count, mildly super-Poisson but far from percolation at dilute fill.
- P2 (stock battle, spacing 5q, mixed responses): **run post-fix** (`battle_front_scaling`, 6 s). p99/p50 < 8: **held** (1.3–2.8 at every n; max/p50 12–29, the front-crossing spike). Fired per body over the crossing grows with n (4.7 → 9.2 → 18 → 27 for 400 → 25 600; my √n estimate was 5.6 → 11 → 22 → 45 — direction and rough size confirmed). `max_batch` ≤ 12: held at n = 400 (10), failed at larger n (34, 122, 407 same-tick pairs) — but p99 ops stay thin, so the pairs do not form one indivisible blowout at this spacing. **Fano grows with n (1.72 → 3.54 → 13.58 → 40.22)** — the same clustering growth as the gas, in the engine's own scene; this was not predicted (I predicted thin tails at all n).
- P3 (mono-disperse battle packing sweep, n=6400): **not run** post-fix (the probe is in the tree: `battle_packing_sweep`). No claim made.

Two artifacts caught and fixed during the run, both disclosed: (a) my first per-tick delta subtracted the burn-in snapshot, making every series cumulative — a plausible "firestorm" that cross-checking against `Chronon` killed (agreement at tick 300 forced the re-read); (b) the gas genesis degeneracy above. Lesson for the lab's book: agreement between instrument and reference at one checkpoint is what exposed the instrument; measure at several.

## What would make it wrong

The Fano growth could be finite-size (saturating above ~16k bodies) — then it is a curiosity, not a transition; a checker should add n = 65,536 at fill 0.2 (about 30 s). It could also be a residual of the gas generator's grid (correlated rows) rather than dynamics: rerun with `worlds::random` (rejection-sampled, no grid) at matched density. If both hold (Fano still grows, random placement too), the clustering is dynamical and the gate is missing.

## Cost of adopting, fit with PRINCIPLES

Adoption is one measurement habit, not code: the contact law's tail behaviour (Fano at fleet scale) joins the plane's smoothness dashboard, and `worlds::gas` gets its jitter fix so dense probes are possible. Fits PRINCIPLES #12 ("minimize spike compute and average compute usage so that you get a bigger simulation that runs smoothly") and the lens's "event rates: what is the branching ratio" — the answer at dilute packing is: branching ≈ Poisson, no cascade; at fill 0.2 and 16k bodies the assumption weakens with n. Also on record, usefully: no thermal drift — "errors never compound" (#13) holds for the law's energy carries in the regimes tested (flat to 3600 chronons; exact in equal-mass cradles).

## The lens

The dynamics lens made me look for a phase boundary in packing; the real structure is in N at fixed packing (a tail that grows with fleet size), which I found only after my instrument bug was caught — the lens also made me trust the "attractor" story too quickly. Missed: the battle-front probes (P2/P3) never ran post-fix; the connected-component size of a same-tick contact batch (the truly indivisible unit) is not measured — `max_batch` counts pairs, not components.

## Grade (author's self-assessment)

**Silver.** Real, reproduced, controls on both sides, one named experiment from gold: establish whether the Fano growth at fill 0.2 is dynamical (random-placement control + n = 65k) and whether it appears in real battle scenes (`battle_front_scaling`, already in the tree). If it saturates or vanishes, this collapses to "the contact law is Poisson-smooth everywhere reachable" — a premise confirmation, still worth one line in the board.
