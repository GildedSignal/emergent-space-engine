Working...
Check complete. Verdict: **Grade: gold** — written to `lab/results/20261019-0435-fermi-0659/check.md`.

**What I did:**
- **Reproduced independently**: applied `work/patch.diff` in the clean tree, built, re-ran A1 — census and game lines bit-identical to the author's log. The runner's regen (exit 0) already matched every dossier number; I re-derived all the arithmetic (170,897/170,629 items, wave decomposition, means, λ, the 1.3 KB rescale, wake churn).
- **Verified the probe's causality in shipped code**: split path returns before `rebind` iff `dvq == [0,0]` (step.rs:424-433); clock path gates `rebind` on `next.velocity != st.velocity` (step.rs:691-694). The census counts exactly the promotion predicate; counters only (OFF = ON confirmed).
- **Four adversarial arms, all beyond the author's domain**: K=10⁵ (43,828/43,828 = 1.0000), K=10³ (710/710), wave 3 at 69.0k game-s (73,206/73,206, all ≥16 quanta) — the wave landing times (~14.3k/41.7k/~69k gs) also resolve the dossier's 27.6k-vs-23.4k prose wobble: the doll step is ~27.4k gs.
- **Pre-registration**: predictions.md mtime precedes the dossier, and its content (p ∈ [0.05, 0.8], 1–2 quanta) is incompatible with post-hoc fitting. P1's failure is the pre-registered kill criterion firing — the finding, per H0183.
- **Novelty**: the published page carried this as "the one unpriced dial" with arms ~10³–10⁴ apart; a9d7's rate was item-rate. Nothing prior measured the fired share.

**Page corrections in place**: "165k" → 170.9k/170.6k; "dead code on the plane" scoped to the belt's clock path (0.16–0.3% fires on the split); restored 097e's "corroborating — not first" credit clause the author deleted; added my adversarial arms to the checker block.

Tree restored to clean (patch reverted). One gold on the topic — it stays open, correctly.
