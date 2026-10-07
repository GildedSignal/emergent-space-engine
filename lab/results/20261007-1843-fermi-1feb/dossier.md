# Dossier — 20261007-1843-fermi-1feb (Fermi lens)

## Claim

At 10⁹ bodies the budget breaks in this order — compute first, live memory (H_live) second, bandwidth third — and the two binding numbers are the **affordable hot fraction of the billion** (≈ 5–10 % at rtf 1, ≈ 0.05–0.1 % at rtf 100, with the law's designed ~3 µs kick; ~25× less with today's 87 µs recompile-every-kick resolver) and the **H_live reabsorption rate** (≥ 37–292 MB of scar distinctions per game-second must be reabsorbed at 10⁹, or the 4 GB state budget fills in 14–110 game-seconds hot, ~23 game-days even for cold year-orbit belts).

## Bottleneck

Board items "cost at a billion" (3), "fitting 10⁹ in 8 GB" and the risk-list's unmeasured "distinctions created per game-second (H_live)". This run puts the first measured numbers on both: per-body event rates and per-event cost from the shipped plane (not a model), and the first H_live creation-rate estimate with the steady-state requirement it forces on the allocator. It deletes nothing by itself; it sizes the two levers everything else hangs on (kick cost below ~3 µs, and reabsorption at the creation rate) and kills the idea that 10⁹ fits without either.

## Evidence

Machine: shared Linux x86 runner (8 vCPU), orders of magnitude only; the integrator re-measures on the M1. Binaries built from main at this run's checkout (`cargo build --release -p xtask`, CARGO_TARGET_DIR=/home/glmlab/lab-target-1). Raw JSON beside this dossier in `work/`; arithmetic in `work/budget.py`.

Reproduce (each ≤ 35 s):

```
/home/glmlab/lab-target-1/release/xtask universe --describe --seed 1
/home/glmlab/lab-target-1/release/xtask universe --bench --rtf 100 --seconds 20 --seed 1
/home/glmlab/lab-target-1/release/xtask universe --bench --rtf 100 --seconds 15 --members 400 --seed 1
/home/glmlab/lab-target-1/release/xtask universe --kick-bench --rtf 100 --seconds 10 --seed 1
python3 lab/results/20261007-1843-fermi-1feb/work/budget.py
```

Measured anchors:

- Scene: 28 bodies + fleet of 48 members (76; `--members 400` → 417). rtf 100 held (median 100.0, lowest 1 % 58; 21 overflow frames in 1200).
- Event rate, per body per game-second (game-s = wall × rtf; `events_per_second` in the dashboard is per **wall** second — divide by rtf): total 0.048 (48 members) / 0.037 (400 members); belt-like (kicks+opens+boundaries only) 0.015 / 0.019. Stable within ~1.3× across a 5.5× member change → usable as an N-independent per-body constant.
- Kick cost (pure resolver, `--kick-bench`): plane-made ships median **35.2 µs** (p99 59 µs); fleet members median **90.1 µs** (p99 449 µs). Exact cycle-memo hit rate **0.0** (663 rebinds, 663 distinct exact shapes): every kick recompiles; the quantized 12+12-bit memo would hit 93 % but is a law change (re-rounds the orbit each kick; board, 5 Oct).
- Today's store: **5067 B per body** (316× the 16-byte logical tube; no population programs in the plane).

Derived budget at 10⁹ (`work/budget.py`, tubes 16 B from law.md, belt program 0.126 bits/body from gold components-98bc, 4 GB of the 8 GB for body state, ~6 effective M1 threads, 60 GB/s, 256 B touched per event):

| Term | Today (87.5 µs/kick) | Designed (~3 µs/kick, law.md jet+re-anchor 0.05 compiles/kick) |
|---|---|---|
| Compute, hot everywhere | 3.2×10³ core-s per game-s (~530 M1s; rtf_max ≈ 0.002) | 110 core-s/game-s (~18 M1s; rtf_max ≈ 0.05) |
| Compute, belt-like everywhere | 1.6×10³ core-s/game-s | 55 core-s/game-s (rtf_max ≈ 0.11) |
| Affordable hot fraction (rtf 1 / rtf 100) | ≈ 0.2 % / 0.002 % | ≈ 5–10 % / 0.05–0.1 % |
| Memory, base state | today's store 633× over 8 GB; plain tubes alone 2× over; belt programs 16 MB per billion (fits) | same |
| Memory, H_live (no reabsorption) | fills the 32 bits/body budget in 14–110 game-s (hot, 64–16-bit scars); 27–108 game-s belt-like; ≈ 23 game-days at cold year-orbit rates (32 kicks/orbit / 3.15×10⁷ s) | same |
| Memory, steady state | reabsorption ≥ 37 MB/game-s (belt-like, 16-bit scars) to 292 MB/game-s (hot, 64-bit) | same |
| Bandwidth (256 B/event) | hot: 9.4 GB/s per unit rtf (16× over at rtf 100, fine at rtf ≤ 6); belt-like 4.7 GB/s per rtf | same |

Board cross-check (lens task 3): the 29-September headline "10⁹ orbiting bodies at today's rates would need about 190 cores" re-derives as ~532 M1-equivalents from the plane's own rates (2.8× — same order; "today's rates" have got ~3× heavier with the plane's exact per-kick resolver). The cold bracket (year orbits, 32 kicks/orbit) is ~10³ kicks/game-s at 10⁹: compute-free — the compute term spans nine orders between cold and hot, so **the hot fraction is the compute budget**, which is exactly the light-cone/partition quantity of principle 5, not a body count.

## Predictions

`predictions.md` was written before all runs. Held: scene size (76 in 40–150), belt-like event rate (0.015–0.019 in 10⁻⁴–3×10⁻²), term ranking with the board headline within 3× (2.8×). Missed, all informative: (a) made-ship kick cost 35 µs vs my 2–30 (1.2× out) and leavers 90 µs vs my 0.3–10 (**9× out, ordering inverted**: fleet members' kicks cost more than made ships', not less); (b) total event rate 0.048 vs my ≤ 0.03 upper edge (battle slices dominate the total); (c) bytes per body 5067 vs my ≤ 400 (**12.6× out**: today's store is far past even the tube). The kill-criterion note held: rates are honest only to an order (76-body scene, one seed per config; members 400 for stability).

## What would make it wrong

- The per-body rates come from one compact star system where every body is close-in; a real billion-body universe is mostly long-period orbits, so the belt-like rate is an **upper** bracket for quiescent regions (the cold bracket is 4–5 orders lower). If the game's typical billion is ≥ 99 % cold, compute stops binding and H_live becomes the first wall.
- The 3 µs "designed" kick is not measured: it assumes law.md's jet+re-anchor (0.05 compiles/kick at ~35 µs) and a kick body near 1 µs. If re-anchoring proves more frequent (the red-team's correlated-quantum-kick bound) the affordable hot fraction shrinks proportionally.
- Scar size 16–64 bits is an assumption (shipmem's B18 will measure it); the reabsorption requirement scales linearly with it.
- Shared-box timings, one seed per configuration, and `bytes_per_body` is the plane's whole record store, not the shipmem representation — orders only.

## Cost of adopting, and fit

Adoption is zero-code: these are the target numbers for work already queued (kick cost below ~3 µs — the memo/jet line; reabsorption at the creation rate — the allocator's H_live input, law.md line 13). Fit, PRINCIPLES: "Cost follows change and entropy" (3) — the budget's binding terms are event rate and distinction rate, not body count; "The memory floor is information" (24) — measured today at 316× the tube and ~250× the 32 bits/body the goal allows; "his direct influence is bounded and propagates at c at most" (5) — the hot fraction is a light-cone quantity, which is why it can be small.

## The lens

A Fermi run multiplies measured constants and can miss structure: it treats event rate as uniform per body (battles are local and bursty; percentiles of frame load, not means, decide smoothness — principle 12), it cannot see whether scars correlate (they do: one kick begets the next shape), and it prices the player as one body when the player is the seed of the hot fraction itself. The H_live reabsorption number is a requirement derived, not a mechanism demonstrated — the allocator must still show it can merge scars at 10⁻¹ of the plane's event cost, or the number is a wall, not a budget.
