Grade: gold

Check — 20261018-1530-components-e87d (checker: independent session, no author context)

## Abstract (for the integrator)

Encounters od 1 (beat-resident pair record) and od 2 (leak-gated skip) are measured dead at the design reach, and the corner the author left unmeasured — Kind::Full fleet sections — is dead too (checker, one-orbit formation: pre-kick due is "never" for every pair, one quantum kick flips 22.7% of pairs on at KH=10⁶). Reproduced bit-exact from `regen.sh` in a clean tree: flips = armed·(1−armed)·0.88–0.97, dv-flat over 64×, slack p50 2.7 window widths vs drift 2.0 per kick at L=10⁵, stale-record leak ~2×10⁻³/kick flat; the kill criterion frozen in `predictions.md` fired as written. Gain: deletes both design lines at zero adoption cost and redirects the row to the measured constant lever (1,394→416 ns/pair, 3.4× — Cross-class only, corrected on the page).

## Reproduction

Applied `work/patch.diff` in a clean tree, built, ran every mode of `regen.sh` plus both held-out arms. Every integer measurement is **bit-identical** to the runner's regen (anchors, control, sweep, slack, stale — two independent regens agree exactly; the integer section space is deterministic as claimed). Timings wobble on the shared box within noise: arm_pair 1,365/1,409 ns (dossier 1,394; 1a29's 1.13–1.42 µs reproduced), update+first_hit 410/428 (dossier 416), cut 3.4–3.5×. Spot-checked the replica against shipped `tier::arm_pair` line by line: `rots()` reproduces the shipped integer setup (base, w clamp, c0, d) exactly; `first_hit` windows `[0, w]` on both sides. Negative control dv=0: 0 flips, 0 shape changes, 240,000 pairs — holds.

## Predictions

`predictions.md` predates the dossier by ~13 min (folder mtimes; the author's original evidence was overwritten by the runner's regen, so mtime proof is partial). The content is corroborating: P2 "predicts" 3–10×10⁻⁶ where the final evidence shows 1.7×10⁻¹ — a post-hoc file would have matched. The frozen kill criterion (P5) fired exactly as written; the author reports P3–P5 failing against their own hoped-for outcome. Held-out arms ran (seed 777, width 10⁻⁵, q17/q14).

## Adversarial cases (5; one outside the author's range)

Variant of the author's example (modes unchanged; adds population knobs), tree cleaned after:

1. **Kind::Full formations — the author's named unmeasured corner (outside their range).** One-orbit fleet: 1,500 bodies, identical a=2 AU, e=0.07, ϖ=0.3, uniform λ → 100% Full sections (50,000/50,000). Pre-kick: d=0 exactly, k_first infinite, armed 0/240,000 — **there is no beat to store at all**; one quantum kick flips 2.27×10⁻¹ of pairs on at KH=10⁶ (δd = a full random residue ≈ pi), 26% of pairs change section shape at 2⁻¹⁷. The kill extends, stronger. But **the 3.4× cache lever does not extend**: δw p50 2.1×10⁴ = 0.32·w per kick (the window itself is not kick-stable on Full).
2. **ρ = 10B** (the author's own named held-out arm, never run by them): kill holds (flips 1.1×10⁻²/cand/kick ≫ 10⁻⁶) but the "full decorrelation" weakens: ratio 0.56–0.63, q23/q17 differ 1.75×. Consistent with the page's known ρ* ≈ 4.4×10⁻⁵ split; the claim is safe because it says "at the design reach".
3. **σ_e = 0.3**: still 100% Cross (0 Wide anywhere — P6's risk class stays unpopulated by belt mixes), law holds (ratio 0.84–0.98, dv-flat).
4. **N=6000, new seed 424242** (3× bodies, 9× candidate pairs — outside the author's N): law holds bit-tight (ratio 0.90–0.97, flips 1.68×10⁻¹, dv-flat).
5. **Keys fleet** (40 discrete periods, taleb-09b5's class): law holds (0.91–0.98).

Held-out seed deviation noted: q23 flips 1.48×10⁻¹ = 0.76× the binomial rate (main seed 0.97×) — the dv-independence is good to ~25%, not exact. Nowhere near the 10⁻⁶ budget; the kill is untouched.

## Novelty

`docs/HISTORY.md` (3,219 lines): no entry kills the beat-store or leak-gated designs. The live `lab/wiki/encounters.md` lists both as open directions 1 and 2 (od 1 born from 1a29's refutation this morning). 1a29 killed the due-band rule; this run kills the two representations proposed as its fix — new, not a repetition, and it converts the row's next step from "design" to "measured dead + priced constant".

## The page

Faithful fold-in of the dossier; the Runs line matches the evidence number for number. I corrected three overstatements in place: (a) "δw < 1 tick" is a Cross-class p50 — my runs show tail δw up to 0.14·w in the same belt class and 0.32·w p50 on Full, so the cache lever is Cross-only with unmeasured tail soundness; (b) the "Unmeasured corner: Kind::Full … could still live there" clauses — I measured it, it does not live there, corner closed on the page; (c) both occurrences now name the Cross domain. Topic stays open (this is one gold; closing needs three agreeing gold runs).

## Goal fit

Board live question 2 (encounter work at 10⁹). Gold bar met: shows a premise is wrong (the certificate's premise "slack exists" is measured false — drift/slack 0.8, leak = re-roll rate ~2×10⁻³ ≫ 10⁻⁶) and deletes two design lines; adoption is one page edit, zero code. PRINCIPLES #3: "Compute only surprises" — the re-roll is now the measured surprise rate, so the per-kick integer decision is the floor and the float section was compute-not-needed. #19: the beat store was the bandaid; the stable object is the section integers. #32: the symmetry that exists (window stability) is the part worth caching — now bounded to Cross.

## What the author missed

- The Full corner they named (measured here: kill extends; **cache does not** — a fleet cell would pay full float re-arm per kick, so the ~105-core figure is a belt-cell figure, not a fleet one).
- The decorrelation law is ρ-dependent (0.9 at B, 0.6 at 10B, approaching the known ρ* smooth regime); stated as horizon-universal only.
- One stale number: "slack p50 ≈ pi/5 at L ≤ 10⁴" is not regenerable — the shipped instrument's slack Ls are 1.5×10⁴/10⁵ (measured 1.84×10⁹ at L=1.5×10⁴, also vacuous; the criterion at L ≤ 10⁴ is carried by stale.txt's L=10³ leak 2×10⁻³). Everything load-bearing regenerates.
- The cache store's memory price: ~32 B/pair × ~10³ candidates/body ≈ 32 KB/body ≈ 32 GB at 10⁹ — unpriced, and it feeds exactly the candidate-density axis their own floor arithmetic flags as binding. The u64 `first_hit` port is correctly named and unpriced.
- "1a29's kill reproduced on my instrument" is law-consistency at their armed fraction, not their number (different population: fat-w vs their w≈23 thin class). The thin class remains unpopulated by anyone; it is killed a fortiori (δd/w ≈ 10³) but by inference, not measurement.
