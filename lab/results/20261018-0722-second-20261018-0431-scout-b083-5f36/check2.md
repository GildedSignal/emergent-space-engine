Grade: silver

**Abstract.** Second author on scout-b083, reproduced end to end and attacked past its domain. The rigid-ring flight on the shipped binary: read list = phase window (32 vs analytic 32.6 at (K=10⁴, ρ=1e-5) and again at (10⁵, 1e-6); 96 vs 97.9 at my 3·10⁴), candidates = 1.00·K, engine answers = the exact-integer replica at every scan; the shipped ANSWER is a quantization-signed residual (47–53% of the window on their rings, 19% at mine), unstable across decode points (15→31→12; 10→32→0 at e=0.3). The 2D curve C(δ,Δa) stayed sound at 0 misses on 15 cells beyond every swept axis (h=90, σ_a=3e-3, ρ=1e-5, σ_φ 0.005–0.05). Closure 0.67 ms/scan at 10⁶ (~3×10³× on the observer's answer term). Silver only because prediction B3's ±25% size clause failed and is reported "held".

## Reproduction

- `regen.sh` from a clean tree with `work/patch.diff` applied: exit 0, every deterministic count bit-for-bit — windows 32/32 at both (K, ρ), ANSWERS 15/18/16 across intervals {2, 2¹², 2²⁴}, the swing 15→31→12, candidates 10009/100009 = 1.00·K + 10, 0/48 selector misses, unwidened miss 83.5%, lookup 3.2 µs, tier scan 0.67 ms. Timings on this box agree (1.75–2.1 µs/cand circular, 3.7–4.2 eccentric).
- Replica fidelity checked against the shipped sources, not just the author's word: `law.rs` `hit`/`hit_narrow` requires approaching in every branch and `tier2.py::hit_exact` copies it branch-for-branch; `Scan::compute`'s quantization (`q_exp = reach.exponent()−20`, `near = reach·2¹⁰`) matches the Rust replica; and the shipped scan's interval is `max(step, 2)` (universe.rs:1162), so "the scan's own interval" = 2 is the real operating point, which is what makes the window claim load-bearing.
- The replica/engine agreement held at every scan in the author's six flights (15/15, 18/18, 16/16 ×2 orientations, 13/13–16/16 at e≈0.1 and K=10⁵) and at all three of mine below — 15 instances, counts identical, first-ids corroborated from the printed prefixes.

## Adversarial cases (three plus, one outside the author's tested range)

1. **Selector, outside the swept grid** (`/tmp/adv1.py`, author's own code, cells moved): 15 cells beyond every swept axis — h = 90 (a decade past 9) at e ∈ {0.1, 0.3, 0.5}, h = 0.05–0.1 (below P/10), σ_a = 3e-3 (bins widened to cover), ρ = 1e-5 (a decade up), σ_φ 0.005 and 0.05, and the σ_a = 0 keys class at h = 90. **0 misses in all 15.** The soundness mechanism survives my push; the price does grow with horizon (reads/hits 68× at (0.5, 1e-3, h = 90) vs the author's 32× at h = 9) — the class dial worsens past their two horizons, which their sweep understates.
2. **Flight at e = 0.3** (their eccentric arms were 2⁻⁴⁸ and ≈0.1): replica still matches the engine (10/10, 11/11, 11/11); read list = in-window at the scan interval (20/20); the residual is an exact half-coin (10/20, split 10/0/10) and the swing is **10→32→0** — at one decode point the shipped answer is empty, at the next near-full. The instability claim strengthens; "≈ half" does not generalize.
3. **Flight at K = 3·10⁴** (between their decades, new angle 0x10000000): candidates 30,009 = 1.00·K + 10 ✓; window 96 against analytic 97.9 ✓; but the answer is **18/96 ≈ 19%**, not ≈ half — the residual fraction is scene-dependent. The page's "≈ half the window" overstated a law from two scenes; corrected in place (see below).
4. B-block float replica rechecked: near 316, answers 50/41, perturbed 316/316 — the noise-decided claim reproduces.

## Predictions

`predictions.md` predates the decisive runs (file order in the folder; 33m → 17m → 10m). Held: B1 in its stated scene (47–53% vs the 30–70% band), B2 (15/17/15 across a 2²² interval range), A1's held-out branch fired and is reported as such (the 1D widening misses at e = 0.1–0.2), C1/C2. Honestly reported misses: A2 (32× vs 10–15× predicted), A3 (69–84% vs 10–20%). **One mislabel: B3 pre-registered "sizes within ±25% of each other"; the flown 15→31→12 violates it by 2.6×, and the dossier's summary says "B3 held".** The violating numbers are printed openly beside the label — a mislabel, not concealment — but the lab's own precedent (1 October red-team: silver for "one held-out prediction failed … and was reported as held") caps this at silver.

## Novelty and the page

- The fold-in is faithful against the evidence; the new content (flown residual + decode-point instability, the 2D curve as the only sound form, the store-grounded O(log K) price retiring 19.2 ns/member) is not in the live wiki page, docs/HISTORY.md or the b083 entry. The two refutations it adds ("empty answer", "1D selector sound") are genuinely new corrections of b083's checker bracket.
- Corrections I made in place on the author's page: "≈ half the window" → "a scene-dependent fraction … 47–53% on the author's rings, 19% at K=3·10⁴" (Current best and the first Refuted entry), plus a checker2 bracket recording the selector's 0 misses on 15 beyond-sweep cells and the e=0.3/K=3·10⁴ swings. Nothing else touched.

## Goal fit

Board bullet 1's live question (the observer crowd term, 604c's ~500×-over): the per-scan answer term 1.9–4.4 s → 0.67–1.6 ms at 10⁶ (~3×10³×), now grounded on flown constants rather than the float extrapolation, and the capture walk is deleted with the 3.2 µs lookup. PRINCIPLES #3 (compute only surprises: the 10⁴ flight computed nothing for 9,977 of 10,009 candidates) and #13 (naming the quantization coin as compounding-risk-to-compile-away). The law-level question it surfaces (should `hit` see sub-quantum relative motion, or should same-key members get a store-side d·w ≡ 0 certificate) is correctly left to the integrator.

## The one experiment that would make it gold

Re-register and fly the answer fraction as a **distribution** across decode points and scenes (e ≥ 0.3, more angles, a fleet beside a 10⁵ belt) with an honest letter — what is invariant is "neither empty nor law-decided, unstable", and the fraction ranges ~0–100% (my flights show 0, 19, 47–53 and ~97%) — closing the B3 mislabel and replacing "≈ half" with the measured law. The law-level certificate alternative (d·w ≡ 0 for same-key members) would close it from the other side.

## What the author missed

- The residual fraction is not "≈ half" — it is a scene-dependent coin bias spanning 0–100%; the page stated a two-scene number as the letter (corrected).
- B3's ±25% clause failed; reported "held".
- The selector's price trend with horizon: 32× at h = 9 is not the corner — 68× at h = 90 (same cell, one decade out); the two-horizon sweep understates the dial.
- The dossier's inline window formula "K·2·asin(near/2r)/2π" drops the both-sides factor (it evaluates to 16.3; predictions.md's K·near_arc/π = 32.6 is the right form).
- The dossier's eccentric arm is e = 2⁴⁸/10 ≈ 0.1, not the stated 0.05 (the page's existing correction is right; verified e_q48 = 28147497671065 → 0.0999…).
