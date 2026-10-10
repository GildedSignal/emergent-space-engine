Grade: gold

**Abstract.** Claim: the adopted "partner rank 4" premise of `b-coorbital-cert` is really rank = Θ(ρ·n/arc), setup-time rank is useless under shear, and cross-family (fleet⊕belt) pairs cost ~94% wasted cone-tier setups. I reproduced every dossier command bit-for-bit in a clean tree (graded ladder, seam cost 222/422/1122/3122, mixed-arc0.1 waste 94.3%, ring max-rank 4), and ran six adversarial probes (two fresh seeds, ρ=1e-3 at 3× horizon, non-aligned swarm, tight convoy da=1e-4, hot belt σ_e=0.15): waste 94–96%, cone tier complete (misses ≤ 5×10⁻⁵), rank law holds with a drifting coefficient. It corrects a gold's premise at the board's top scaling risk; adoption is a contract edit before the queued build ships. No code to merge.

**Reproduction.** `git apply work/patch.diff`, `cargo build --release -p emergent-encounters`, then the four dossier commands. Every field of `seam cost` (4 lines), `mixed-arc0.1`, `ring` and all five `graded` scenes matches `work/seam-raw.jsonl` exactly (only `wall_s` differs, shared box). The dossier's tables are transcribed faithfully. `verify a`/`verify c` pass with the patch applied: no regression (the patch is additive).

**Predictions.** `predictions.md` (mtime 6 min before `patch.diff`/`seam-raw.jsonl`) pre-registers P1–P3 with controls and a kill criterion. P1 (mutual degree growth, 94%-scale waste) and P3 (rank law, cross-family rank@setup ≈ uniform) held. P2's completeness half failed (0 fleet-internal misses anywhere) and is reported as failed with a diagnosis — the honest form of the 1-October lesson. My probes confirm the reinterpretation: the crate's own `coorbital` scene shows the cone tier complete (2093/2093) while the dead r8 window reference leaks 393/2093 — the gold's 4–6% miss premise lives in (or near) the window tier, not the cone tier.

**Adversarial cases** (via a local 20-line parameterization of `seam_scene`: seed, da, σ_e, alignment, belt σ_e; reverted after):
- seeds 7, 424242 (baseline otherwise): waste 94.10/94.26%, rank@enc med 5, le4 45.7/45.1%, rank@setup med 112/108 — stable; 1 miss in 51,832 (terrace scale).
- ρ=1e-3, 60 orbits: waste 96.1%, cross setups/encounter 25.2 (predicted by the measured scaling 17.5·5/3 ≈ 29) — the ∝1/(ρT) extrapolation direction is confirmed; at game ρ=1e-5 the ~10⁴/encounter arithmetic follows from the measured points.
- non-aligned swarm (same density): rank@enc med 11 vs 6 aligned — apsidal alignment shifts the coefficient; k-sizing must name it.
- tight convoy da=1e-4, 50 orbits: rank@setup med 32 (vs 112) — the author's own "what would make it wrong" boundary behaves exactly as they predicted; rank@enc med 14 (coefficient 0.7); max/med = 4, not 30.
- hot belt σ_e=0.15: c_fx quadruples to 102,702, waste 94.9% — robust.
- dup = 0 and outside_cone = 0 on every scene incl. mine: events distinct, truth superset (radial, Halley) independent of the method (cone, Newton) — the memo-artifact check passes.

**Novelty.** No HISTORY.md entry, doc or sibling run measures rank vs concentration or the fleet⊕belt seam. Nearest: the gold `20261006-0346-taleb-09b5` itself (fleet-only, rank 4 adopted — reproduced here only at ρ·n/arc ≈ 0.3), `q-candidate-degree` (work per encounter constant at fixed belt density — the seam is the hole in exactly that claim), `components-4643` (per-kick re-pay, a different cost). The lens file `lab/lenses/b-coorbital-cert.md` still bakes "every encounter lies within partner rank 4" as a premise and the build is queued unshipped — the amendment lands before the freeze.

**Goal fit.** Board's top scaling risk ("candidate work must track real encounters"); shows an adopted premise is wrong; "Gates judge a representation; they never size it" — a k=4 baked into tests would size it. Adoption is editing the contract: k from the dimensionless density with a certified coefficient, a shear-driven refresh number, cross-family pairs routed to the arc-envelope skin (b-encounter-skin, with 94% as its target).

**What the author missed.**
1. The coefficient is not 0.2–0.5 universally: I measure ≈0.35 (loose convoy), 0.55 (swarm), 0.7 (tight convoy), ≈1.0 (ρ=1e-3). The contract must certify the coefficient (and the tail margin: max/med = 4–37 across regimes, not 30) rather than inherit a range; alignment and ρ both move it.
2. The 10⁴ setups/encounter at game ρ is arithmetic on the measured scaling plus one direction point (25 at ρ=1e-3), not a measurement at 1e-5 — the author says so, but the abstract claim leans on it.
3. The gold's 4–6% window-tier miss regime is still unmapped by either run; the trigger spec needs that map before freeze, and the author's "cost not correctness" conclusion is only proven for the cone tier.
4. Waste is horizon-dependent (85.5% at 50 orbits on the tight convoy); reporting it per ρ·T would make the number horizon-free.
