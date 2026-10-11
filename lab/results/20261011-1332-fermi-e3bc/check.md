Grade: silver

**Abstract.** Claim: at 10⁹ bodies the binding terms are per-event compute (compile 8.5–25 µs → rtf ≈ 3, ~31× short of the plane's rtf 100; the jet as specified 1.6× short) and per-active-body cycle memory (0.75–3.4 KB each, no sharing in sparse belts, capping sparse-active at ~10⁶–10⁷ across 8 GB), not memory bulk or bandwidth. Reproduced: deterministic outputs bit-for-bit, timings within load noise. Adversarial: high-e compile runs 53–98 µs (2–4× the top rung), populated-memo hits 782 ns (not 422), and `crossing_state` at 429 ns refutes "no cheap readout tier" for crossing-indexed reads — so the jet is really 1.6–7× short. Every conclusion survives with worsened margins. Silver: P2 failed; the jet term rests on an assumed ε.

## Reproduction

Clean tree, `git apply work/patch.diff`, then the dossier's one command. Build 3.2 s, run 1.2 s.

| metric | bench.txt | this check |
|---|---|---|
| compile e<0.2 | 8,542 ns | 10,308 ns (+21%, load noise) |
| compile 0.2–0.6 | 25,292 ns | 26,905 ns (+6%) |
| memo hit / state eval / control | 422 / 4,630 / 5.4 ns | 410 / 4,539 / 5.6 ns |
| integer floor | 3.17 ns | 3.13 ns |
| cycle bytes, memo collapse, all sinks | — | **bit-for-bit identical** |

Determinism, the machine-state header, and prediction precedence all hold: `predictions.md` 13:40:47 < bench 13:45:09 (header 13:45:08Z). Journal inputs verified in source: H0190 K1/K2 (32.5 kicks/orbit, 114×) and the economics row (0.6 core per 10⁶ at ~50 µs → r_kick 1.2×10⁻², exactly the dossier's derivation); H0210 (rtf 100, kicks 29 µs); law.md (jet re-anchor ~0.05 compiles/kick; tube 16 B). The identity's arithmetic checks: 10⁵ kicks/s × tier cost / 8 cores → rtf 3 / 17 / 63–190 / 27,000; ceilings 3×10⁷ and 6×10⁸ at rtf 100; 0.8 µs per kick whole-machine budget. `state()` confirmed unmemoized (root solve + quadrature per call), so P1's premise is sound. Cycle-bytes method is sound (`knots: Vec<Knot>` 88 B, `crossings: Vec<usize>`, plus base struct).

## Adversarial cases (three, all run)

1. **High-e tail** (e 0.6–0.9 and 0.9–0.99, p 20–1000): compile costs **53 µs** (~48 knots) and **98 µs** (~88 knots), zero errors — 2–4× the ladder's top rung. The compile tier at e>0.9 affords rtf < 1 at 10⁹ all-active, and the jet (0.05 × 98 µs) ≈ 4.9 µs → rtf ≈ 16, ~6× short. The dossier's "31× / 1.6× short" are the optimistic edge; direction unchanged, margins worse. (Strong field p 2–6 M: 1000/1000 errors — no bound orbits that deep; physics, not a defect.)
2. **`crossing_state`** (the crate's own "direct table read, no quadrature or root solve"): **429 ns** including velocity — 10.8× below `state`. The P2-failure claim "no cheap readout tier between the memo hit and the full readout" is false for crossing-indexed reads (true for arbitrary-phase reads; kicks are at fixed drift phases, the gather reads crossings). The jet's ε was assumed ≈0; with a real per-kick readout (0.43–4.6 µs) the jet is 1.6–7× short of rtf 100, not 1.6×. The adoption decision (re-anchor ≤ 0.03/kick or compile 2× cheaper) survives, but its margin band straddles the "2× cheaper compile closes it" branch.
3. **Populated memo**: 10⁵ exact-distinct entries (fill 19.4 µs each ≈ compile, consistent) → hits cost **782 ns**, not 422. Realistic-occupancy memo-hit tier halves: rtf ≈ 100, not 190. Same order, still closes at rtf 100.

Plus one un-run critique: the integer floor is measured on a 64 KB L2-resident array; at sparse-active scale the (E, L) store is ≥100 MB and random updates are memory-bound (~100 ns), so "rtf 27,000" is ~300× optimistic as a realistic tier (legitimate as a labeled floor; the lens section admits cold-cache gaps without quantifying this one).

## Novelty

No prior measurement of the per-tier ladder, cycle bytes, or memo-key collapse exists in HISTORY.md, the docs, or this container's results. H0192's 16.8 µs is oracle gate-query cost; H0210's 29 µs is the plane's end-to-end kick; the board's "190 cores" is derived from those journal numbers — this run decomposes it with shipped-code tiers and honestly reports the 2× gap (300–350 by its own rate vs 174.5 by the board's). The belt/formation split (1.0× vs 37×) cross-confirms the co-orbital gold (20261006-0346-taleb-09b5) from an independent mechanism, and kills a live plan: H0213's "the quantized memo needs a hook in crates/space" — the hook's value in belts is now measured at ~zero (compile traffic does not amortize across a sparse belt; a fortiori for the exact `ShapeKey`, which is finer than the 12+12 `memo_key` measured).

## Goal fit

Board #3 (cost at a billion), #5 (memory), and the focus item "fitting 10⁹ in 8 GB". It sizes the jet, b-h-live and b-encounter-skin before they land, and deletes two plans. PRINCIPLES: #10 "Measure before claiming"; #24 "The memory floor is information" (the active set's ~1 KB/body floor is 10⁴× the program — the information question at 10⁹ is the active set, not the population); #3 "Compute only surprises" (the identity is the surprise rate made arithmetic); #27 "i just care at about how fast it runs compared to real time" (rtf is the output).

## Why silver, not gold

- **A held-out prediction failed** (P2: readout predicted 0.03–0.3 µs, measured 4.6 µs). It was disclosed prominently and is the run's most informative result, but the grade's letter says the held-out predictions held — and lab precedent (1 October law red-team: "Not gold: one held-out prediction failed... and was reported as held") bars gold on exactly this.
- The tier numbers are each the optimistic edge: high-e tails 2–4× worse (unmeasured), populated-memo hits 1.85× worse, the floor L2-resident, the jet's ε assumed rather than measured. Individually orders-of-magnitude fine; together they make the headline "1.6× short" a 1.6–7× band.
- It is decision support (nothing to merge, by design); it deletes plans, not components, and the premise it corrects (compile-per-kick scaling) was already flagged on the board as a problem rather than held as a premise.

## The one experiment that would make it gold

Anchor the identity on the shipped plane's real kick path — the author's own proposed probe, one run: in the plane's bench, count bodies kicked per parent orbit and the cycle-cache miss rate at belt scale, and time the actual per-kick readout the jet path pays (`crossing_state` vs `state`) plus the realized re-anchor rate. That replaces the assumed ε and the worst-case active fraction with measured ones, and makes the jet budget decision (re-anchor ≤ 0.03 compiles/kick, or 2× cheaper compile, or active fraction ≤ 6×10⁸) adoption-ready on the M1.

## What the author missed

1. `crates/space` already ships a cheap crossing-indexed readout (`crossing_state`, 429 ns) — the P2 conclusion "no cheap readout tier exists" overclaims, and the jet arithmetic should have used it.
2. The eccentric tail (e 0.6–0.99: 53–98 µs, 0 errors) was never measured though the taste log's own encounters work flags e 0.7–0.9 belts; the ladder's top rung and the jet shortfall there are understated 2–4×.
3. Memo hits were costed at 1-entry occupancy; at 10⁵ entries they are 782 ns. Tier cost and occupancy are coupled.
4. The averaged kick rate has a factor-2 ambiguity inside H0190 (0.01 core per 10⁶ ships at ~50 µs → 2×10⁻⁴, vs 1.2×10⁻²/114 → 1.05×10⁻⁴); the run silently took the optimistic end. At 2×10⁻⁴ every rtf halves (jet ≈ 32, 3× short) — conclusions unchanged in direction, but the choice should have been stated.
5. The floor's L2 residency (64 KB working set) — see above; a one-line caveat would have fixed it.
