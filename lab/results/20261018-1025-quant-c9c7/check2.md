Grade: gold

**Abstract.** Claim: on the shipped U-scan tier a belt-mix kick re-checks 0.484·N candidate pairs — the U-window saturates the band (reach = e/p + e_max/p + eps spans the whole U-span; fe6b's 0.0346·n is the unsaturated regime, X ≈ the band ratio) — so candidate rescans at 10⁹ cost 10⁷–10⁹ cores and the encounters row closes only on slack + flow: 92.3–92.5% slack-skippable, 0 violations at the belt quantum, slack dead at 10⁻⁵-class kicks. Reproduced bit-identically in a clean tree (all 19 lines, every deterministic field; 38 s). Blind adversarials all confirm (below). Gain: kills the row's rescan premise by 5–7 orders and prices the surviving closure at ≤ ~2 cores (cd3b's mint flow + stored slack). Adoption cost: none — a measurement closing one direction.

**Reasons.**

1. **Reproduction.** Applied `work/patch.diff` to the clean tree myself, built, ran the full regen command list: every count field of all 19 JSON lines matches exactly (timings excluded; shared machine). The instrument is faithful: `Sorted::reach(x) = x.e/x.p + e_max + eps_max` is the shipped law verbatim, the churn example's kick move is `main.rs kick`'s own move (a·(1+eps), phase-locked), and the patch to `kick()` only parameterizes previously-hardcoded spec values with defaults preserved. `pairs` = the kicked bodies' candidate lists (nk·0.484·N ✓), no hidden O(N²) setup. predictions.md predates the decisive runs (file-time order; held-out seed 777 declared there).

2. **Adversarial cases (mine, blind to checker 1).**
   - **n = 3×10⁶, fixed band [2,3)** — outside the author's range: scanned still 100%, cand = 1,555,493 = **0.519·N**. The Θ(N) law holds; the constant crawls up +7% via e_max/p 0.193→0.202, exactly the disclosed √ln N Rayleigh crawl. At 10⁹ the rescan cost is therefore *worse* than 0.484·N — the composition understates the ruin.
   - **σ = 0.02** — the saturation boundary between the author's 0.01/0.07: scanned 58%, cand = **0.162·N** against the σ-linear unsaturated prediction 0.164·N. The two regimes connect quantitatively as claimed.
   - **Band [2,12]** (10× wider, both seeds): still **0.15–0.154·N** — saturation is not a narrow-band artifact; "not O(1) at fixed density" holds for every belt-like band (uniform-a piles bodies at the inner U-edge; the median window covers 80% of the span). Asymptotic O(1) needs 2·reach < U-span, far outside belt geometry.
   - **fe6b at a second X** ([1,2], σ 0.01): 0.0511·N vs the formula's 0.0519 — the X identification is real. **σ = 0.2**: 0.862·N — a stirred belt deepens saturation.
   - **The author's named missing probe** (slack rare-violation hunt): n = 10⁵, nk = 20, **963,298 pair decisions** at the quantum — skippable 0.9219, **0 violations**, changed 0.0130. N-flat with the author's 0.9254/0.9227.

3. **Predictions.** P0, P1, P3, P4 held (P1: exponent 0.999 ✓; P4: rescan ≥ 10² cores measured ≥ 10⁷). P2 failed and is honestly reported as the finding: at fixed density the fraction is not flat (0.695·N vs 0.484·N) because saturation binds — the wiki's "O(1) at fixed density" closure hope dies at the belt's own mix. A diagnosed failed expectation, per H0183, and the same pattern as cd3b's gold ("one honest miss").

4. **Novelty.** The published page's open direction 1 asks exactly this constant ("if it is O(1) at fixed density the row closes"); no prior line holds the saturation result or fe6b's regime identification. The instrument re-derives fe6b's recorded gold constant at its own spec (0.0824→0.0843·N, X ≈ 1.5) — lineage, not repetition.

5. **Page.** Faithful; I corrected two spots in place: the slack evidence count (was "15.4k pairs × 64 kicks" — the kick arm used 16–24 kicks, ≤ 2.5×10⁵ decisions; now notes the 9.63×10⁵-decision extension, still 0 violations) and a checker-2 paragraph bounding the "NOT O(1) even at fixed density" domain (wide-band [2,12] still 0.15·N).

6. **Goal fit.** Board line "encounter work at 10⁹: what cuts it by 10³": this run shows the rescan framing is dead by 5–7 orders and that the churn that remains is exactly the surprises (armed flow, burn-priced re-arm). PRINCIPLES #3: "Nothing is evolved that can be derived when looked at" — the candidate set is bit-stable under quantum kicks (gained+lost ≈ 0 of ~10⁵–5×10⁵ pairs), so per-kick rescans are compute for no information. Two independent checkers reproduced and extended; both found the same label slip; neither found a number that overturns.

**Reservations (do not change the grade; recorded for the integrator).**
- Measured on the replica element tier (a,e floats, Binet cone), not the live velocity word — disclosed in dossier and page; the tier is the shipped encounters machinery and the same instrument as fe6b's gold, but if the live word's candidate semantics differ, the constant moves with them.
- The 10⁹ points are extrapolated 10³× in N (disclosed; structurally supported by the reach mechanism and my 3×10⁶ point; the crawl makes the quoted 0.484 an underestimate).
- Composition arithmetic is loose in spots: shipped-scan composes to ≈ 7.6×10⁸ cores (slightly above the quoted "10⁷–10⁸" band, which is the split-8/shipped pair), and the "~2×10⁹" exact re-cert uses the split-8 kick rate. Every variant is ≥ 10⁷ cores — the verdict is insensitive by orders.
- **Label slip** (both checkers independently): the fixed-density control's "anchor density 4×10⁴/AU²" is actually the control band's own density; the 10⁶-in-[2,3) anchor is 10⁶/(π·5) = 6.37×10⁴/AU². The control ran at 0.63× the anchor's density and its fraction *still* rose — the P2 kill is stronger than stated.
- Timing noise: dossier's 23.2 ms/kick (4.79 µs/pair) vs regen's 24.4 ms (5.05) — shared machine, immaterial.

**What the author missed.** The U-space pile-up (uniform-a ⇒ dN/dU ∝ U⁻²): the wide-band control was the one point that bounds the "not O(1) at fixed density" claim's domain, and it was not run ([2,12] still 0.15·N). The named 10⁶-pair slack hunt was left unrun (I ran it; it holds). The 10⁹ constant should be quoted as 0.48–0.55·N (the e_max crawl), which strengthens, not weakens, the rescan kill. The density label slip above.
