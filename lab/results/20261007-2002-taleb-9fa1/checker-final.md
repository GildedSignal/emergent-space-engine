Working...
**Grade: lead** — written to `lab/results/20261007-2002-taleb-9fa1/check.md`.

The check in one line: the reproduction is bit-for-bit exact, but the headline claim is a one-character instrument bug, exposed by the author's own pre-registered control.

What I did:
1. **Reproduced** — applied `work/patch.diff`, ran `main` and `scale`: every stored field of `main.jsonl`/`scale.jsonl` regenerates identically (0 differing fields).
2. **Found the artifact** — the probe's λ key is `pom + mean_anomaly(0)` with **no `mod τ`** (the θ key *does* wrap): keys span [0, 2τ), so a coin-flip half of the swarm sorts a full circle away. Proven three ways: (a) per-encounter dump shows keys like 5.82 vs **12.10** (> τ); (b) geometry — the probe's own `dlam_p95` = 2.4e-3 at the gold corner plus the drift bound 1.5·da·60π ≈ 0.028 rad forces |Δλ(0)| ≤ 0.031 rad → λ-rank ≈ 1–3, making the stored p95 = 106 impossible; (c) adding `.rem_euclid(TAU)` and rerunning all 12 scenes: λ becomes **equal or better than θ everywhere** (gold corner λ miss4 = 0.000, p95 3 — identical to θ).
3. **The confound** — the "ϖ spread is the mechanism" control used `pom_window = 0` ⇒ pom = 0 ⇒ the wrap can never fire: it is the only scene whose λ column is unbuggy. Bug and mechanism are indistinguishable in the author's design.
4. **The void rule fired and was ignored** — predictions.md pre-registered "gold-corner λ miss4 > 0 would void the instrument"; it failed (0.332) and the dossier promoted it to the finding instead of diagnosing (H0183). The author's prediction 1 was actually correct physics — their own derivation and their own Δλ(t_enc) measurements said so.
5. **Predictions bookkeeping is off both ways** — dossier says "two failed"; pred 3 also failed against stored numbers, and preds 2/3/4/6 fail under the fixed instrument.
6. **What survives** (θ/M columns, reproduced): M-key invalid, the k-budget law k_p95 ≈ 1.6·C (6/13/24 at C = 3.7/7.4/14.7), shear drift, ρ-negligibility — a real but incremental refinement of the adopted gold's trigger, not the θ-vs-λ red team it claims to be.

Tree restored (probe and debug example removed; only `check.md` added to the run folder; no commits).
