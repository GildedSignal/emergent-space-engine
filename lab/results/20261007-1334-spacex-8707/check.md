Grade: silver

**Abstract.** Claim: for a plane-like belt (30k bodies, Jupiter-analogue, 1000 yr, 3 seeds), secular H_live after one program refit is ~10⁻³ scars/body/yr at q=10⁻³ (≈0.03 scars/game-s at 10⁹; ≈50 B/real-s at rtf 100), saturating in ~5–7 sim-yr, so planetary secular dynamics cannot force 8 GB at session scale; the memory risk lives in encounters and the player. Reproduced **bit-identically** — all seven output files (null, convergence pair, three belt seeds, aggregate); decisive seeds 159 s wall. Null 4.4e-12, exponent 0.573. My attacks (causal refit +1.2% residual; pure 2:1 belt, 5× rate; 3× stronger perturber, ejections at same order) leave the 4–5-order margin intact. Silver: 3 of 7 held-out predictions failed (disclosed), and the scene is a uniform-in-a float surrogate, not the frozen B18b sampler.

**Reasons.**

*Reproduction.* Clean tree (work/patch.diff is empty; the work is entirely in the run folder). Every dossier command rerun: `null_1000.json`, `conv_dt05/10.json`, `belt_s{7,8,9}.json`, `aggregate.json` all **bit-identical** to the stored files. This is the exact-regeneration record that past silvers lacked (5 October lesson).

*Predictions.* `predictions.md` (13:52) precedes the decisive outputs (13:54–13:55); smoke files are earlier. 4/7 held: null 4.4e-12 ≤ 1e-11 ✓; exponent 0.573 ∈ [0.5, 0.7] ✓; fit-noise 0.4% ≤ 30% ✓; session-lag — I measured it directly: 0.93% crossed at t=2 yr < 5% ✓. Three failed, all disclosed: near/far ratio 1.33 vs ≥2 (pre-registered fallback applied — split dropped); coherence 70% vs ≥80%; T* 5–7 yr below the [10, 300] bracket (safe direction).

*Adversarial cases (mine).*
1. **Causality of the refit.** The harness fits F(a), g(a) over the full 1000-yr span — an oracle a live engine lacks. Refitting on ≤ 200 yr only changes late-time residual RMS from 0.02062 to 0.02087 (+1.2%). The framing hides no future information.
2. **Pure 2:1 belt** (a ∈ [3.15, 3.35], the churn tail as the whole scene): exponent 0.839, rate 5e-3/body/yr at q=1e-3 — 5× the mixed belt, still 3–4 orders below memory pressure.
3. **Stronger perturber** (m=3e-3, e_p=0.2, σ_e=0.15): bodies start ejecting after ~20–50 yr (a → hyperbolic) — a regime change into encounter-class events — yet the raw distinction rate stays ~5e-3/yr. Margin absorbs it; the regime does not.

*Novelty.* HANDOFF.md:70: H_live "not measured yet"; it is in the current build queue. The concept is registered (law.md, H_live as memory budget; plane.md readout) and shipmem/components-98bc measured static program bits (0.126 bits/body — store size), not the live creation rate. First measurement; no H entry contradicts it.

*Goal fit.* Measures the named board item "10⁹ in 8 GB decided by distinctions per game-second" and deletes the secular risk: no new store, no new gate; one number for B18's reported-at-10⁹ line plus a refit cadence. PRINCIPLES #6, "Store the generator, not the generated": the secular generator is two smooth fields plus a clock, and the measurement says that suffices between refits.

*Why silver, not gold.* The gold line requires the held-out predictions to hold; 3 of 7 failed (honestly, one with its pre-registered fallback). Plus three labeling slips in the dossier, none load-bearing but all in its currency: (a) "median first-cross 6.2 / 21.7 yr" are the aggregate's T_cross values (RMS-reaches-q times); the true median body first-cross is 10 / 50 yr (seed 7); (b) "even at the early-time peak rate, +21 B per game-second; 4 GB fills in ~200 game-years" mixes rates — at 21 B/game-s the fill time is ~6–7 game-yr; 200–250 game-yr belongs to the long-run 0.5 B/s (years_to_fill_4GB = 7.89e9 s in aggregate.json). The honest un-refit margin is T* itself; (c) "19×" the inner belt — the stored bins give 21–30×. Also the headline "10⁻³/yr" is frac_final/1000, a 1000-yr average over a transient that saturates (0.9997 by 50 yr; early rate 3.9e-2, which I confirm); the conclusion survives either rate, but a session-scale H_live should quote the transient.

**The one experiment.** Rerun the same measurement on the plane's actual frozen B18b belt sampler (banded p, tails kept) at the same N and seeds — ideally through the shipmem/`behave --law plane` path — and relabel the two timing numbers. My pure-2:1 case bounds the scene gap at ~5×; if rate and cadence hold there, it is gold.

**What the author missed.**
- The rate is q-insensitive below 1e-3 (frac saturates at every q ≥ 1e-5): no quantum choice rescues memory; only refit does. Worth stating — it kills a tempting knob.
- The refit's own cost: at the 25%-scar point a refit must walk ~2.5e8 scars (~4 GB) to re-estimate F(a), g(a). Unexamined; that read pass is the one compute line this result adds to the plane.
- The regime hand-off: case 3 shows a modestly stronger perturber converts secular churn into ejections (encounter-class). The secular↔encounter boundary, not the secular side, is where the 8 GB question will be decided — the dossier points at encounters but not at the conversion.
- g(a) is fitted with zero weight on low-free-e bodies (|free0| ≤ 1e-4 → g_raw = 0), biasing g toward 0 in cold regions — conservative (inflates residual), but unstated.
