Working...
**Grade: gold** — written to `lab/results/20261006-0737-components-4643/check2.md`; tree restored (patch reverse-applied, only `?? lab/results/` remains).

**What I did**

1. **Reproduced** everything from the dossier's commands with `work/patch.diff` applied in a clean tree (patch adds only the experiment binary — no crate edits, and `kicked_body` matches the crate's own `kick()` spec: same seed, index rule, element change). Every load-bearing counter reproduced **bit-for-bit**: setup 1,600,220 vs checks 131,824 (92.4%), wake p50 25,999 orbits, 99.7% > 100 orbits, cap over-firing 427×, stream 252,704 re-derivations → 111 fires, eval ratio 1.1×. The accounting closes arithmetically: deferred evals ÷ re-derivations = 19.25 ≈ the 19.7 setup evals/pair — the wake calendar pays almost pure setup re-payment, so its gain is capped at the ~8% check fraction by construction.

2. **Adversarial runs (mine):** ρ=2e-4 (declared held-out in predictions but *unreported* in the dossier — it confirms, 90.3% setup), ρ=1e-3 (87.7%), σ_e=0.3 (81.9%, cap 527×), wide-tube stream with 100× the fires (still 1.1×), dense τ=1 kicks. The kill is robust in every direction the harness can reach.

3. **Novelty:** taleb-3ec1 is "Next, not started" in HANDOFF; no prior measurement of wake deferral. Premise kill, pre-registered falsifications reported honestly, zero adoption cost.

**Defects found (flagged in check2.md, none touch the verdict):** the dossier's stream wall times (3.42/2.37 s) match neither the author's saved raw output (5.26/2.62) nor my rerun (3.50/3.23) — an unsaved rerun quoted as evidence; the τ=1 "0 misses" control is vacuous (0 events in the author's own run; my denser variants miss 10/18 and 402/842); the co-orbital formation case that could re-open deferral is unbuildable with `make_belt`, so the kill is scoped to sparse belts, as the dossier itself discloses.
