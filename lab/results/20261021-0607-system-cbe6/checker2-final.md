Working...
Check complete. Summary of what I did and found:

**Grade: gold** — written to `lab/results/20261021-0607-system-cbe6/check2.md`.

**Reproduction (clean tree, blind to check.md):** applied `work/patch.diff` at 595fdd47, built, re-ran all 11 arms — every worst-Jacobi value, kick count, death (strong s4: 2/6 gone, refusals 274/340), and P5 zero matches `evidence/ladder.txt` to the printed digit. The "verbatim instrument" claim holds on line-by-line comparison with `jacobi.rs`.

**Adversarial cases (all beyond the author's domain, all confirmatory):**
- **Eccentric draw** (the author's named untested gap; plane hauler e≤0.25 via `e_q48`): step 4 PASS both seeds (worst 3.2e-5), step 3 FAIL — floor placement unchanged, gap closed from above.
- **Exterior circles 6.5–7.5 AU** (regime never flown): PASS at step 3 (3.4e-5), FAIL at step 2 — ≥1 octave coarser, the conjunction unit's predicted direction; though this point doesn't discriminate conjunction from own-orbit beyond ~2× at unequal Hill distances (honestly noted in the check).
- **10× horizon** (1000 periods): 1.2e-5 at step 4, identical to 100 periods — no walk.
- **72 fresh draws** (36 ships × 2 new seeds): max 1.6e-5 at step 4, class FAILs at step 3 — no hidden tail.

**Judgement:** P1/P2/P3/P5 held; P4 half-failed exactly as disclosed (floor at step 4, not ≤ step 2), changing the headline headroom by <2× (both ~10³) while yielding the run's insight — the conjunction unit — which survived every attack. Novelty stands: the page's priors are replica/probe; this is the belt floor on the shipped instrument under B12's frozen bar, which is the missing half of the board's top macro row (the desync grid's belt constant, 2⁻⁴ planet-period, with a measured cliff). Weakest joints named: the ~10³ composition is cross-scene (9,000/orbit anchor not re-measured), the near-cliff certificate is draw-sensitive, and 7076's folder is absent from this checkout.

**Cleanup:** appended one `[checker2]` line to the run's `wiki/kick-cadence.md` (current best 13/15 lines, page 140/300); deleted my throwaway example and the applied patch so the tree is as I found it.
