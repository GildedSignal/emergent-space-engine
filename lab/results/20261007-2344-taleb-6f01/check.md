Grade: gold

Abstract: The adopted co-orbital certificate (gold 20261006-0346) silently drops contacts outside a domain far narrower than "under a formation": partner rank ≈ N·(spread)/2π, so M-rank drops 90–97% of contacting pairs at any realistic spread (even Δe=10⁻⁴), λ-rank survives static orientation but cracks with the epicyclic wiggle and window drift, and period/phase-density triggers are blind to all of it (dn_rel flat at 1.5e-4 while miss goes 0.6→97%). I reproduced every table bit-identically (pilot, wscan 10/10, escan 6/6) and confirmed the scaling law adversarially (fresh seeds, k=2/8, brute-force independence). Adoption: one gate S=N·(Binet extent + Δn·W)/2π ≲ k with λ sort-key, straight into the queued b-coorbital-cert build — with a safety margin my N=600 case shows it needs.

## Reproduction

Clean tree (`work/patch.diff` empty), script copied to /tmp (it writes JSONs to its cwd). numpy 1.26.4, Linux x86, load 3–7, mem <1 GB per process.

- `python3 cert.py pilot`: identical to author's `pilot.json`, all fields.
- `python3 cert.py wscan`: 10/10 cases identical, including `binet_radius` to the last digit.
- `python3 escan`: 6/6 cases identical (the N=600 e0.02 cases ran 93–138 s here vs 137–223 s author; shared machine, order of magnitude only).

## Predictions

`predictions.md` file time precedes every result JSON by 5–15 min (log order consistent). Held-out items I tested independently:

- Fresh seeds: D=0.5/seed 77 miss_M 76.2% (author 72.0%), dvec=1e-4/seed 99 85.5% (author 90.0%) — both within the promised ±5 pp; miss_λ 0 both.
- k-scaling: k=2 measured 88.1% vs formula 91.6% (holds); k=8 measured 43.4% vs 66.5% — the closed form is loose at large k, in the conservative direction (real misses fewer than modelled, so the derived zero-miss domain D*≈2πk/N understates safety).
- The author's two reported prediction failures (D=0.2/0.5 low; lamsafe 20% vs <2%) are honestly flagged and correctly diagnosed (the e·sin(Δϖ/2) term).

## Adversarial cases

1. **Gate soundness (my main addition):** dvec=1e-4 at N=600 (seed 55): full gate S = 2.72 < k=4 → phase tier engaged, yet the λ tier drops 3.2% of contacting pairs (max λ-rank 7). With the author's N=300 case (S=1.36, 1.7% leak) this shows the leak grows with N at fixed scatter while the gate passes: **S ≲ k separates catastrophic (S≫k: 20–97%) from clean, but does not deliver the certificate's zero-miss contract in the band S∈[1,k]**. The build needs a margin (or wider k), not bare S≲k.
2. **Brute independence, done right:** the author's cross-check fields are broken — `candidate_pairs` records (i,j) in λ-order (430/845 keys have i>j), so `truth_in_subsample`/`brute_agree` miss i>j events (my raw rerun gave a spurious `brute_agree: false`; the pilot's `true` was orientation luck with its single event). Recomputed with normalized keys on dvec=1e-3, 2000-pair subsample: brute 4 = pipeline 4, no discrepancy either way — the λ-adjacency truth list is complete here. Same bug inflates `contact_pairs` ~2× (241 oriented keys vs 125 distinct pairs; 149 vs 79 on the aligned control). I recomputed miss fractions unweighted over distinct pairs on 5 cases: they shift by ≤1 pp (e.g. lamcrack-N300 37.7%→38.5% miss_λ, D0.5 72.0%→72.0%) — the dossier's percentages stand.
3. **k=2 on the wscan family:** λ-leak appears (3.5%) once drift-rank S=1.35 approaches k — consistent with the drift term of the scaling law.
4. Wide-belt and rank-at-encounter behaviour confirmed in the reproduction (miss_λ_enc=0 everywhere, incl. wide-belt).

## Novelty

docs/HISTORY.md (through H0215), board taste log, docs/law.md: the gold's domain was never bounded; the nearest entries are the gold itself ("every real encounter lies within partner rank 4", adopted) and q-candidate-degree's "zero misses to 10⁶", which the gold overrode for concentrated workloads. This run bounds the override. Timely: `b-coorbital-cert` is first in lab/queue.txt and in the Codex sol queue — the gate lands before the build ships.

## Goal fit

Top scaling risk on HANDOFF (candidate work at scale / co-orbital concentration). Shows a premise of an adopted gold is wrong — at the motivating 10⁶ the certificate is safe only for exactly law-maintained lockstep (allowed spread ≈2.5×10⁻⁵ rad), invisibly to the natural triggers: a ruin path (principle 13, silent contact loss corrupting every downstream certificate), closed before the build. Principle 4: S = N·Δ/2π is the dimensionless number that chooses the regime; principle 22: the scatter the game itself creates decides the tier. The 10⁶ extrapolation is integer rank arithmetic, not float extrapolation (principle 24). The lens limits (speed, 3D, game-design call) are stated honestly.

## What the author missed

- The gate margin (adversarial case 1): percent-level leak at S∈[1,k], growing with N; a threshold at k/2–k/3 or a widened k is needed for a zero-miss contract. The author's own evec-1e-4 table row contains this leak but "working gate" was not qualified.
- The orientation-key defect: pair counts double in scattered cases and the brute cross-check is void as shipped (though the truth list itself is sound — verified here). "Pairs are the honest unit" is right; the pair key was not.
- The tier could re-sort mid-window (kinetic maintenance): then the failure appears as churn ≈ N·S swaps per window instead of dropped pairs — same S, same gate, but the build's failure mode should be stated per reading.
