# Dossier — 20261010-0100-fermi-c11c (Fermi lens)

## Claim

At the shipped law's measured **63 µs per distinct kick** (a cycle compile — the memo hits
0% at both the exact and the quantized key on distinct kicks, 3 seeds), the 10⁹ budget's
first breaker is **kick compute in dense regimes, not storage and not H_live**: a billion
low-orbit bodies overshoot an 8-core machine **42× even with fully averaged tides**
(4,800× unaveraged), while belt-scale kick compute (1.5×10⁻³ machine), belt H_live
(≤ 10 bits per game-second per billion bodies) and storage under population programs
(15 MiB) all fit with 2–3 orders to spare — so the one lever worth a rung is amortizing
the per-kick cycle compile across bodies (or batching it), which must buy ≥ 40× , not more
sparsity.

## Bottleneck

Board item 3 ("cost at a billion", ~190–600 cores today) and the H_live risk ("not measured
yet", HANDOFF). The gain on offer: naming the term that breaks first concentrates the next
rung on compile amortization (≥ 40× on the worst regime) and deletes the alternatives
(memo-as-keyed, more averaging) from the lever list. It also prices B18b's real target:
today's plane store is 5,077 B/body (591× over 8 GB at 10⁹), so the catalogue's working set,
not the 16 B tube, is the storage number to close.

## Evidence

Machine: this Linux box (i7-4790, 8 vCPU, load 1.4, 14 GB free at start; shared). The
benches' own `machine_before/after` is macOS-only (`sysctl`) and printed "unavailable"
here; load/memory recorded by hand above. Orders of magnitude only; integrator re-measures
on the M1.

```
cargo build --release -p xtask                                        # 39 s
$CARGO_TARGET_DIR/release/xtask universe --kick-bench --seconds 20     # 0.06 s → kick-bench.json
$CARGO_TARGET_DIR/release/xtask universe --bench --rtf 100 --seconds 20 # 20 s  → bench-rtf100.json
python3 budget.py                                                      # → budget-out.txt
```

Measured (`kick-bench.json`, seeds 1–3 stable):
- median 63.4 / 57.8 / 46.5 µs per distinct kick (p99 60–91 µs; leavers 386 µs);
- memo on distinct kicks: exact 0.0, quantized 0.0 — all seeds;
- whole plane at rtf 100: 328 events/s on 71 bodies, frame CPU p50 4.6 ms / p99 10.8 ms,
  rtf lowest 1% = 9.7, 56/1200 overflow frames; engine cost 69 µs per fleet item,
  300 µs per ship item; `bytes_per_body` = 5,077.

Budget table (regenerable, `budget-out.txt`), 10⁹ bodies at rtf 100, 8 cores:

| term | rate | cost | verdict |
|---|---|---|---|
| low orbit, unaveraged (32.5/orbit) | 6.0×10⁸ kicks/s | 4.8×10³ machine | breaks 4,800× |
| low orbit, averaged (0.285/orbit) | 5.3×10⁶ kicks/s | 42 machine | breaks 42× |
| belt 3 AU, unaveraged | 2.0×10⁴ kicks/s | 0.16 machine | fits 6× |
| belt 3 AU, averaged | 183 kicks/s | 1.5×10⁻³ machine | fits 660× |
| storage, tube floor 16 B | 14.9 GiB | 1.9× of 8 GB | breaks 2× |
| storage, shipped store 5,077 B | 4.7 TB | 591× | breaks 591× |
| storage, population program 0.126 bit | 15 MiB | 0.002× | fits 500× |
| H_live, belt scars (32–128 bit) | 2.3–9.4 bits/game-s | — | fits ≥ 5 orders |

Derived caps: affordable distinct kicks ≈ 1.3×10⁵/s machine-wide → **2.4×10⁷ low-orbit
bodies at today's cost** (3.9×10⁶ if fleet members pay the leaver's 386 µs); 10⁹ low-orbit
bodies need t_kick ≤ 1.5 µs — 42× below today, and below even a naive drift update, so the
billion must live at belt scale with dense islands, and those islands need compiled
generators amortized across bodies, not per-body compiles.

## Predictions

`predictions.md` was written before the run. Held: P3 (tail 1.4–7.1 ≤ 30), P5 (H_live
9.4 bits/game-s ≪ 1 kB), P6 (board's "190 cores" is 3× optimistic vs H0190's own rate —
under 10×, report only), and P4's conditional direction (averaged low-orbit "fits iff
t_kick < 1.5 µs" — it does not). Failed, informatively, in the same direction: P1
(predicted ≤ 30 µs, measured 46–63 µs — the compile is dearer than my prior) and P2's
quantized half (predicted > 50%, measured 0%: on *distinct* kicks the 12+12-bit key merges
nothing on the plane's own scene; the 5 Oct 94.5% was measured on repeats). P4's "belt
unaveraged ≥ 3 orders under" also failed at the measured t_kick (0.16 machine ≈ 6× under):
my drift-update prior for a kick was ~1000× too cheap.

## What would make it wrong

The kick-bench's 32 samples per seed are few, but three seeds agree within 27% and the
whole-plane engine costs (69–1,478 µs/item) corroborate the compile scale. It would be
wrong if the M1's cost per distinct kick is ≪ this box's (x86→M1 rarely buys 40×), or if
formations in the real game share cycles so well that per-body distinct-kick cost is the
wrong basis — that is precisely the lever, unproven. Adoption cost: none (numbers and a
verdict, no code changed). Fit with PRINCIPLES: "Compute only surprises" (§3) — the
surprise-free kick recompiles today, and "The best part is no part" (§17): the compile, not
the kick, is the part to delete. H_live's tiny belt rate is §24 ("the memory floor is
information") made concrete.

## The lens

The Fermi lens multiplies rates; it does not open the resolver to see what the 63 µs is
made of (compile vs bind vs arithmetic), nor does it test whether a batch of N similar
bodies compiles once — a mechanism lens must. The scene is one plane at 71 bodies; the
belt and low-orbit rates come from the record (H0190, r8 v2), not re-measured here.
