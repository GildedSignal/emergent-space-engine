# Dossier — 20261006-2240-b-belt-wire-a733

## Claim

The belt program is wired to its frozen gate: with `wt/belt`'s files brought into `crates/shipmem` and its quantile table derived at birth from its parameters (both ends of e dyadic, so no tail is capped), the `space` law implements `Law::belt_birth`/`belt_restore` and the full `Belt` interface, and **B18b goes from FAIL ("belt_birth is not implemented") to PASS on all five frozen runs** (birth 31 B for info 31 B; 9.7 B per scarred body against a 54-bit floor; 17 ns per regenerated body).

## Bottleneck

Board item "fitting 10⁹ in 8 GB (crates/shipmem: population programs plus scars)" — the belt program is the population store for smooth belts; until it spoke the judge's interface it could not be judged at all (B18b frozen on main since 5 October, failing every law). The gate now certifies 0.126 bits/body-class economics at birth (31 B for any n; 32 B at 10⁹) and ~10 B per history rewrite. What it deletes: the frozen 28 KB quantile table as *information* — it is now a working constant derived from the parameters at birth (red-team F4's rule), so a belt's store is its parameters and its scars, nothing else.

## Evidence (all commands ≤ 60 s; Linux/x86, orders of magnitude only)

```
cargo build --release -p xtask
target-dir/release/xtask behave --law space --gates B18b   # PASS, 16.9 s (below: full line)
target-dir/release/xtask behave --law space --gates B18    # FAIL, unchanged (see below)
cargo test --release -p emergent-shipmem                   # 5 belt tests + 2 codec, pass
cargo test --release -p xtask space_belt                   # 3 tests, pass
cargo test --release -p xtask the_space_law_belt           # 1 judged 2^20 run, pass
cargo test --workspace --release                           # all pass except lattice-metal's
                                                           # fuzz_free_worlds (no Metal device;
                                                           # fails identically on pristine main,
                                                           # verified in a scratch worktree)
```

Before/after detail lines are in `gates-before-after.txt`. The passing line:

> B18b PASS belt: 5 runs, every criterion; worst: chi2 |z| 2.80 (limit 4.5), serial |z| 3.13 (5), KS 0.56 of critical; four tail ends: count |z| 1.46 (4.5), shape KS 0.55 of critical, conditional mean |z| 2.07 (pooled 1.09), other columns 0.77 of critical; birth 31 B for info 31 B; 17 ns to regenerate and hash a body; bytes at 1e9: 32 B (3.2e-8 B/body); after 12 epochs at 1e-2 11.4% are scarred, 9.7 B each (floor 54 bits): 1.10 GB at 1e9 (reported)

B18 (the memory ladder) reads `bytes_per_body`/`MemoryScene`, an interface this lens does not touch: FAIL before and after, same "12 not answered" line. Nothing else in the space law changed (two added trait methods).

**Two substantive findings beyond the wiring:**

1. **`wt/belt`'s frozen table would have failed B18b's bottom tail of e.** Its 4095 central midpoint cells put the whole bottom 1.2×10⁻⁴ of the e distribution in cell 0 (every u < 2⁵² maps to e = 1174440): against the judge's EBottom tests the belt would have X = 0 bodies at the reference's threshold (count z ≈ −7.2, limit 4.5) and no reach. The judge's own Dyadic control says the passing structure ("2¹² cells in each octave of the probability, at both ends"); the lab's table had it only at the top end. The derivation now resolves both ends: 4094 central cells, then 46 octaves × 64 cells plus the 64 exact deepest draws at each end (10,110 entries, 40,440 B, derived in ~1 ms at birth). This is why "derived at birth" was not a mechanical transcription of the frozen data.
2. **The table derivation is exact-op arithmetic only** (ln via the exponent plus a 14-term atanh series, ln(1−d) via a 12-term series, IEEE sqrt; no libm `ln`), so the same bits come out on every machine — the law's "canonical outcomes are exact and independent of … hardware". Regeneration itself is pure integer arithmetic (table lookup + counter mixes); two gate runs on separate process invocations reproduced identical statistics bit for bit.

Scars: each rewrite stores the body's zigzag delta against the program's body (a 50-bit replacement kick costs ~9.7 B including the ordinal's varint gap), inside the gate's window [0.5·floor, 2·floor + 2] ≈ [3.4, 15.6] B. Keys derive from the birth seed (odd, distinct, re-mixed on collision), so the whole belt is a function of (spec, n, seed) and the store carries no key material.

## Predictions

`predictions.md` was written before the decisive run (tuned only on a non-frozen seed at 2^20 and a 2^21 exact-law tail check). Every prediction held: all worst statistics inside the predicted ranges (chi 2.80 < 3, serial 3.13 < 4, KS 0.56 vs "< 0.5" — 12% over a soft prediction, still half the limit), birth ≤ 32 B (31), store growth ≤ 1 B (0–1), 11.4% scarred at ~10 B (9.7), B18 unchanged, no regression elsewhere. The held-out frozen seeds and both 2^23 sizes passed unseen.

## What would make it wrong

- The judged statistics ride on the mix() counter family; a long-range flaw at lags or seeds not exercised by the five frozen runs would show as serial/tail failures on other seeds (the lab's gold components-98bc evidence and B18b's own SplitMix-family controls argue against it).
- The conditional-tail discretization bias (64 cells per octave, midpoint convention) is bounded at ~0.01σ here; a different sigma or e_bits spec is re-derived, not re-tuned — but only σ = 0.07 / Q30 is judged.
- Cross-machine bit-exactness of the derivation is argued (exact ops only) but tested on one machine family; the M1 re-measure settles it.
- Cost of adopting: `Prog` in shipmem loses `Copy` (the belt carries its derived table behind an `Arc`); hot paths clone instead of copy (an atomic increment where a register copy was). The judged path does not go through `Prog`.

Fit with PRINCIPLES: "Store the generator, not the generated" (the store is parameters plus scars; the table is derived, never stored); "a table derived from them is not information" (B18b's freeze wording, honoured); "Exact means deterministic and reproducible" (exact-op derivation, bit-identical across processes). The gold bar for this lens — patch applies to main, tests pass, named gates improve or hold, nothing else regresses — is met with B18b improved and B18 held.

## The lens

A wiring lens sees the interface and the gate, and trusts the lab's statistics more than it should: I initially transcribed the frozen table's top-end indexing to the bottom end and only a distributional pre-check (bottom tail deficient by 21%) caught that the fraction bits included the leading one. A lens less close to the judge might also have missed finding 1 above until the gate said KILL. What I did not do: judge the belt under *other* seeds/specs than the frozen ones (the checker should), or measure birth-derivation cost on the M1.
