# Dossier — the mint-knots conflict adjudicated: two instruments, two quantities, one table

## Claim

The page's 100× conflict is resolved by measuring both published quantities in ONE binary,
ONE run each: **624a's "traversed fraction" (14% cycles) is panel-landing share — a
1/n table-size floor plus probe scatter — and 1991's (0.04–0.6%) is the binding's
lifetime share; both reproduce exactly, they are different quantities, and the real
per-mint law is a third thing: post-mint quadrature is read TRAFFIC (10–20% of the arc's
panels, cadence-decoupled), while every closed row rebinds in < 1/64 of a period.**
The CPU lever stays blocked at the clock totals (1991's kill confirmed structurally:
`from_shape` sinks period/proper/advance from the full-arc last-knot sums at mint), and is
priced by traffic — not by walking — once totals are O(1) (Carlson); the store lever
(~90% of cycle panels, ~99.3% of passage panels never run quadrature post-mint) stands.

## Bottleneck

`mint-knots`, flagged **conflict to resolve** in the index: 1991 (main side) vs 624a
(theirs), disagreeing ~100× on "the traversed fraction" and drawing opposite conclusions
(lazy compile prices no CPU vs 4–7× CPU cut). This decides how the kick-cost row
(75–160 µs vs ~50 ns floor) and the memory row (~5,100 B/body) share one lever. The page
also names the belt fork open (one-kick-per-period cadence).

## Evidence (all from `regen.sh`, ~7 min; Linux/x86 shared box — orders of magnitude only)

Instrument (work/patch.diff, +229/−5 across `census.rs` (new), `orbit.rs`, `kick_bench.rs`):
per minted `OrbitShape`/`Passage` — `quad`: panels whose `node()` arithmetic actually ran
post-mint (the expensive quadrature; refine brackets, `at_radius`, tail bisections);
`probe`: panels whose precomputed `.sum` word was only read (bisection mids, table reads,
totals); `walk`: psi spread of post-mint quadrature ÷ compiled span (1991's quantity,
measured over all traffic instead of one close-tick read); `interval/period`: closed from
the bench loop at each body's next processed kick. Controls: **the patched binary
regenerates the shipped records bit for bit** (default `b42da477294f7619…`, m400-rtf1
`8c242b023e8b79e4…`, replays `a693ac68…`/`0de3a82c…`; refused 0 on every arm), and
`regen.sh` re-verifies them on a pristine rebuild (patch reversed). rtf100 digest
reproduces across reruns (`bedd3d9a…`, seed 3 `f8126518…`).

| arm | population | mints/knots | quad% med | panels(+probe)% | walk% med | reads med | closes |
|---|---|---|---|---|---|---|---|
| default s1 rtf1 10 s | made cycles | 23 / 175 | **16.7 = 1/6** | 67 | **0.03** | 22 | 0 |
| m400 s1 rtf1 30 s (**1991's arm**) | member cycles | 55 / **5,480** | 5.8 | 28 | 6.6 | 420 | 0 |
| m400 s1 rtf1 | member passages | 82 / 12,419 | **0.68** | 5.4 | 0.006 | 28 | 0 |
| m400 s1 rtf100 30 s (**624a's arm**) | member cycles | 8,497 / 487,291 | **10.4** | **46** | 9.6 | 404 | 8,710 |
| m400 s1 rtf100 | member passages | 222 / 33,312 | **0.68** | 5.4 | 0.004 | 26 | — |
| m400 s3 rtf100 (held out) | member cycles | 7,161 / 402,479 | 10.9 | 50 | 19.9 | 402 | 7,379 |

1. **Both published numbers, same runs.** Default arm: quad 16.7% reproduces 624a's "20%"
   (median table 6 knots — ONE bracket panel per read IS the floor) while walk 0.03%
   reproduces 1991's 0.23% order. Fleet arm: panels 46% / quad 10.4% bracket 624a's
   14.3% (their landing count mixed quadrature brackets with sum-probe sites); passages
   quad 0.68% equals their 0.7% exactly. Member cycles 5,480 knots = 1991's population to
   the knot.
2. **rtf is a mint-count dial, not a cadence dial.** rtf1→rtf100: total mints 496→18,933
   (624a counted 18,967) while per-mint medians hold (quad 5.8→10.4%, walk 6.6→9.6%,
   reads 420→404). The 100× headline gap was definition, not dynamics.
3. **Lifetime ≠ traffic.** Every closed row (8,710 + 7,379) rebinds at interval <
   period/64 (1991's law, now measured on observed next kicks, not plan estimates); yet
   the psi spread of real quadrature is 6.6–19.9% — up to ~12× the lifetime window —
   because reads are not confined to it: per-frame state reads, reflection (inbound legs
   re-read the outbound half-table), and the resolver's exit/periapsis time-bisections
   probe the binding at scattered phases.
4. **Belt fork: absent, and bounded.** No closed row reaches interval ≥ period/64, let
   alone level 0 (the bench replays ship kicks only; the belt is unwired). Below 1/64,
   panel consumption is cadence-decoupled (traffic-driven); at one-kick-per-period with
   per-frame reads a body would traverse its table (laziness belt-neutral exactly there).
   The fork stays open, now bounded from the measured side.
5. **The 448-knot tail** (624a's od 2): quad 5–6 panels, probes 26–28, reads 474–731,
   walk ≤ 7.5e-5 — 1.2% of its panels ever run quadrature.

## Predictions (predictions.md, written before the decisive runs)

P1 half-held: panels reproduced, but my walk bound (≤ 2%) failed informatively — the
spread is 9.6–19.9%, traffic not lifetime; this failure IS result 3. P2 held (both
numbers in one run). P3 held (rtf invariance). P4 half (no level-0 rows, as predicted;
the extrapolation gains the traffic caveat). P5 wrong for mints (every tagged mint is
read at least once — never-quad is a panel-level fact, ~90% cycles / ~99.3% passages,
not a mint-level one). My pre-registered kill criterion (walk ≈ 14% on 624a's arm as a
true monotone walk) did not trigger: the default arm separates floor (16.7%) from walk
(0.03%) cleanly.

## What would make it wrong, adoption cost, fit

Wrong if: the close correlation misattributes (it uses the plan's next processed kick per
body — kicks that re-time without rebinding produce no close, disclosed as 10,223
unclosed rows, of which ~9,850 are resolver-internal fit mints never tagged); or if
address reuse merges rows (it cannot steal reads: a freed Arc cannot be read; cross-kind
collisions were caught — one impossible quad_frac 5.17 before the eviction fix, max 0.71
after — and the fix is in the patch). Adoption cost: none — this is an adjudication; the
page's next experiment is the composed lever (Carlson O(1) totals first, then
traffic-priced lazy panels), which neither run priced correctly as published.

Fit with PRINCIPLES: #31 "check incentives" / agreement is not independence — two runs
on one bench published different instruments under one name; #3 "compute only surprises"
— the surprise stream is read traffic, and the eager mint is the wrong unit to price it
against. Lens (SpaceX): the idiot index asked which of the two numbers was real; the
answer is "neither is the quantity that pays the bill."

## The lens

SpaceX's delete-first instinct nearly mis-fired here: the tempting move (adopt 624a's
4–7× laziness pricing) is blocked by a structural part the census confirms — the totals
are sunk at mint. The blind spot this lens carries: trusting that a measured ratio is
the requirement; both earlier runs measured real ratios of the wrong thing.

## Commands

`bash lab/results/20261020-1729-spacex-65b8/regen.sh` (≤ 7 min: pristine control, four
arms, determinism check, summary). Single arm, ≤ 60 s each:
`$CARGO_TARGET_DIR/release/xtask universe --kick-bench [--members 400] [--rtf 100]
[--seed S] --seconds T` with `CENSUS_CSV=<path>` for per-row data (in `out/`).
