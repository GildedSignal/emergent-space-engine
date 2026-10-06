Grade: gold

**Abstract.** Kill of the taleb-3ec1 deferral lead on the belt kick workload: pairs are indeed dormant (99.7% of first in-window passages >100 orbits ahead, median 26,000 — reproduced bit for bit), but 92% of per-kick evals are numeric-window *setup*, which calendar wakes re-pay at every kick; deferral's measured ceiling is 1.1–1.2× evals (1.5× wall on my rerun), not the predicted 5×. Analytic zero-setup windows over-fire 427× (276–528× across my probes). The lever stays the slack skin (12.6×, HANDOFF). Adoption is a design decision, nothing to build: drop the wake calendar. Blemish: the dossier's wall-clock digits match no archived log (they regenerate in family); the deferred harness has a disclosed exactness hole the structural argument does not lean on.

## Reproduction

Applied `work/patch.diff` to the clean tree, built `dormant` offline, ran every dossier command. All load-bearing counters reproduce **bit for bit**: split σ_e=0.01 (e_setup 1,600,220; e_check 131,824; ≥100-orbit share 117,984; wakes p50 25,999.1, >100 frac 0.997; cap 1,817,897 vs 4,262 = 427×; q_wake 1,010,833 vs q_all 1,038,129), split σ_e=0.05, and all three stream rows (kicks 2,484; re-derivations 252,704 → 111 fires; eval ratio 1.1; misses 37/extras 11; dense and sparse variants identical). The `split` workload provably matches the crate's `kick()` spec (same n, σ_e, ρ, seed, horizon, kicked-body formula; eps = 1e-5 ∈ the crate's epss). "Eval" is one relative-state solve in both paths (`pairs.rs` counts them identically), so the 92%-setup accounting is a fair common currency.

## Predictions

`predictions.md` predates the decisive batch: run folder born ~07:39, predictions ~07:49, the archived load lines bracket the decisive run at 07:55:20–07:55:58, dossier ~07:56. P1 held (98.7% ≥ 80%, and on both held-out densities); P4, the pre-named risk, is the finding. P2 and P3 were the *design's* predictions and were falsified and reported as falsifications, with the disclosed harness defect — this is the honest shape of a kill, not a failed dossier.

## Attack (three adversarial families of my own)

1. **ρ = 2e-4** (declared held-out, never run by the author): setup 90.3% of evals, wakes >100 orbits 99.5%, cap penalty 276×. Law holds.
2. **σ_e = 0.3 eccentric**: setup 81.9%, wakes >100 orbits 99.8%, cap penalty 528×. Holds, stronger.
3. **ρ = 1e-2 concentrated** (the boundary the dossier itself names): the law inverts exactly there — wake p50 248 orbits, cap penalty only 8× — yet deferral still gains just 1.6× evals / 1.7× wall (harness missing half the events there). The kill is correctly scoped to sparse belts and in fact extends beyond its stated scope.

## Novelty

First measurement of the taleb-3ec1 lead — HANDOFF "Next, not started": "99% of setup work lands on dormant pairs, defer it". The dormancy is independently reproduced; the deferral economics are new. No HISTORY entry measures them. q-skin's 12.6× is quoted correctly from HANDOFF.

## Goal fit

Board focus item 3 (encounters without work per orbit/element change). It deletes the next planned encounters component (the wake calendar) and shows the lead's premise inverts: the work is not where the dormancy is. PRINCIPLES §9: "A failed experiment kills that configuration, never the method" — the method's exact wake math (`first_hit`) is explicitly not on trial. §1: the compute not done is the re-setup. Adoptable within one step: a decision, zero code.

## Why gold despite two blemishes

The spine — dormancy real, setup dominant and structurally re-paid by any wake design (both paths call `sections()` per candidate pair per kick, and e_def/e_eager = 0.92 confirms), analytic windows over-firing by 10²–10³× in sparse belts — is bit-reproducible, adversarially robust, and adoptable now. The blemishes: (a) the dossier's wall digits (8,676/649 µs; 3.42 s vs 2.37 s; "1.4×") appear in no archived log (raw-output says 11,996/907 µs and 2.0×; my rerun 12,385/944 and 1.5×) — they regenerate in family under load noise, and the dossier itself stamps wall as orders of magnitude only, so I flag rather than demote; (b) the deferred harness's 30–37 misses are disclosed with a correct insensitivity argument. Neither touches a load-bearing number.

## What the author missed

- **Currency nuance:** a check eval chains Newton refinements, so by wall the check fraction is nearer a third; deferral's honest ceiling is the measured ~1.5× wall, not 1.08×. The dossier prints both numbers but headlines the eval currency.
- **A stronger claim left on the table:** even in the concentrated regime where the recency law inverts, deferral still buys under 2× — the kill's scope is wider than "sparse belts".
- **eps is hardcoded** at 1e-5 in the experiment; the crate's `kick()` spans 1e-9…1e-3 and the dossier cites it rather than measuring it in this harness.
- **The miss bug was never localized**; a zero-miss deferred harness would have made P2's falsification airtight without the caveat.
- **Record hygiene:** quote only archived numbers; two wall figures had no log backing.
