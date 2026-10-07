# Dossier — 20261007-1843-second-…-fermi-bb60-152f (second author on 20261007-1801-fermi-bb60)

## Claim

The checker's named experiment is done: the plane's real per-kick fold cost is measured on
**distinct** kicks (shipped harness `xtask universe --kick-bench`, 3 seeds × RTF {100, 1},
3,108 distinct rebinds), and the frontier is republished intersected with the 2.5×10⁸
tube-memory cap. **The original's operative claim survives, its corners die.** What survives:
the only binding compute constraint is strong-tide population × kick cadence × fold cost
(swing 2,300× from representation alone, at the memory-legal population), and the belt scene
still holds every non-kick wall by orders. What dies: every "fits" headline — the 64 ns hot
fold (exact-key memo hit rate **0.0** on every run; the only reuse signal is the quantized
cell, 95.1–95.7%, a law change), the "all-10⁹-strong-tide fits 15× under" (1.83× **over**
compute at the reachable fold, and 16 GB of tubes vs a 4 GB budget), the S2 absurd-bound
"fits" (3.5× over), and the "realistic 10⁷ fleet fits 13×" (2.8× over at the plane's
**measured** cadence 8×10⁻³ kicks/s/game-s/body — above the LEO rate; compute N* there is
3.6×10⁶ ships).

## Bottleneck

Board item 3 (cost at a billion) + the named handoff risk (hot-fold cost, unmeasured).
Gain: the design-carrying number is no longer synthetic — both legal reuse designs now
measure to the same cost, **~1.6–1.8 µs per kick** (jet re-anchor 0.05 compiles/kick × 34.7 µs
grid-median compile; quantized cell 4.5% miss × 34.7 µs), 27× above the dead 64 ns corner.
Adoption cost zero (a reordering plus one measured constant); it deletes the memo-hot
design path and points the lever at compile cost / re-anchor rate, not cadence.

## Evidence

Machine: this run's Linux/x86 box, shared; each command ≤ 60 s; state fields unavailable
in the container (macOS-only sysctls; recorded as such by the harness itself).

```
cd <repo> && cargo build --release -p xtask            # 48 s
xtask=target/release/xtask or $CARGO_TARGET_DIR/release/xtask
for s in 1 2 3; for r in 100 1:  $xtask universe --kick-bench --rtf $r --seconds 30 --seed $s
    -> kickbench-s$s-rtf$r.json   (shipped harness; digests byte-identical on rerun)
rustc -O decompose_bench.rs (vs profile-featured emergent-space + emergent-universe) && ./db 1|2|3
    -> decompose-out.txt           (whole kick + fresh Orbit::compile on the rebinds' own keys
                                     + exact ship-game-second cadence)
rustc -O compile_bench.rs && ./cb   -> compile-out.txt (compile grid: p = 2^4..2^24 M, e = 0..0.99)
python3 budget2.py                  -> budget2-out.txt (the republished frontier)
```

Measured (RTF 100 unless said):
- **Whole kick, distinct:** made ships 34.8–35.0 µs median (p99 50–71), fleet leavers
  72–92 µs median (p99 370–393). H0210's 29 µs (M1) confirmed in order.
- **Recompile cost:** fresh `Orbit::compile` on the rebinds' own keys: 3.6–3.8 µs on made
  (10–11% of the kick — "recompile-dominated" is false for them), 43–62 µs on leavers
  (48–57%; passages' own compiles extra). Grid: median 34.7 µs, p99 171 µs (strong field,
  e = 0.99), floor 3.3 µs (weak, circular).
- **Memo hit rates, distinct kicks:** exact key **0.0** (1,125/957/1,026 rebinds, all
  unique — the 5 October correction, now on the shipped harness); quantized 12+12-bit key
  95.1–95.7% at RTF 100 but 0–3.7% at RTF 1 (reuse appears only over many kicks per body).
- **Cadence:** 7.3–8.2×10⁻³ kicks/s/game-s/body (1,158 kicks / 142,120 ship-game-s, seed 1).
- **Determinism:** rerun byte-identical (`replay_digest`, `digest`, memo block); refused 0.
- **Frontier (budget2-out.txt):** memory wall 2.5×10⁸ strong-tide bodies (4 GB / 16 B tube).
  N*: today 2.4×10⁵ → designed 4.8×10⁶ (K1) / 3.6×10⁶ (measured cadence) → 2.5×10⁸
  (K2-averaged, **memory binds**, compute alone said 5.5×10⁸). Swing at the legal
  population: 2,300× = 114× (averaging) × 20× (35 µs kick / 1.74 µs fold).
- Unchanged walls (inputs unchanged): bandwidth 0.5%, encounters 2.3×10⁻⁸ cores, belt
  16 MB of programs, H_live folding argument, claim-check 175–600 vs "about 190".

## Predictions (`predictions.md`, written before all runs)

Held: P1 (exact hit 0.0 everywhere), P2 (95.1–95.7% at RTF 100), P3 for made (35 µs, p99
1.6× median), P6 exactly (memory binds the two optimistic rows; 16 GB at 10⁹). Failed,
Registration: `predictions.md` (18:46:21) precedes every saved record (first saved JSON
18:46:48), **but one exploratory seed-1 RTF-100 run went to the terminal just before it**
and already showed exact hit 0.0, quantized 95.5% and the made-kick 35 µs — P1, P2 and
P3-made were informed by it; treat them as reproduced, not predicted. Held out: seeds 2–3,
RTF 1, the decomposition, the compile grid, the cadence, the frontier.
swing's order survived, its number did not: 2.3×10³ vs 5.2×10⁴); P7 against me (the
realistic 10⁷ fleet is 2.8× **over** at the measured cadence, not ≥10× under); P3's p99
bound for leavers (4.3–5.1× median, not ≤3×).

## What would make it wrong

The 1.74 µs designed fold leans on law.md's 0.05 compiles/kick (a red-team number, not yet
a shipped path) and on this box's compile costs; the integrator re-measures on the M1.
The plane scene is one battle at RTF 100 — other scenes reprice cadence, exactly as the
frontier table exists to guard. The memory wall assumes a strong-tide body's standing state
(~16 B tube or scar) cannot be re-programmed away while it is being kicked every orbit;
if folded kicks keep fleet members indistinguishable from a program (the H_live argument),
the wall softens to the scar floor — same order (16–24 B). Cost of adoption: zero; deletes
the memo-hot design path and the "10⁷ fleet fits" expectation. Fit: "The cheapest compute
is compute not done" — the 2,300× swing is representation; and principle 13 is why the
quantized memo stays unadopted however well it hits.

## The lens

The second-author lens trusts the checker's framing and could not re-derive his
memory-frontier attack independently (it is quoted, then intersected). A Fermi lens still
prices steady state, not the tail: the leaver p99 (390 µs) and the designed fold's p99
(≈ 0.05 × 171 µs = 8.6 µs, 5× its mean) are allocator problems this table only flags.
And nothing here touches whether averaged kicks *behave* right (B12/r9 territory).
