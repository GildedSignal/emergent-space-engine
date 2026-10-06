Working...
Check complete. **Grade: gold** — written to `lab/results/20261006-1249-inversion-fd48/check2.md`, tree restored, nothing else touched.

**What I did:**
- **Reproduced bit-for-bit** in a clean tree with the author's patch: every dossier command (echelon, table, 5 jams, 2 xchecks), ~11 s total. All numbers match the dossier and the stored JSONLs exactly, including the second xcheck (317 boundary disputes / 0 interior / only_truth 0) the dossier cites but its reproduce list omits.
- **Strawman check against the gold** (8d339c5, taleb-09b5): the author's rank semantics and trigger are the gold's own verbatim; the gold's dossier explicitly flagged the unproven invariant this run measures. The "either-metric" headline is not inflated — distance-only gives 34.9% (seed 27).
- **Adversarial cases:** (1) pure-Python independent instrument (no crate code) confirms the echelon: 15/15 encounters, pair (0,5) rank (5,5) at 0.9ρ, trigger 0.5999 fires; (2) passing-side control — in-domain dilute σ_λ=0.05 gives m̂ 0.89 and **zero** misses; (3) tail σ_λ=0.002 gives m̂ 22 and 55.3% misses; (4) m̂ is linear in n/σ_λ (3.1 → 5.6 → 11 → 22).
- **Novelty/goal fit:** no prior entry measures rank in-domain or audits the trigger; the trigger reads 47 on the motivating fleet (premise wrong), and the k=4 constant silently drops a third of real encounters exactly where adopted — the board's top scaling risk. Fix is one step: k_i = m_i + 1, m-triggered rebuild, re-derived trigger.

**Misses I flagged:** metric attribution (the adopted phase metric's honest number is 20.9%, still a kill), a mislabeled `table` row (sig_e 5e-5 vs the jam's 1e-5), the marginally-exceeded σ_λ=0.01 prediction band not flagged, the truth's boundary-minimum exclusion, and the unmeasured m-growth between rebuilds (the one experiment that would make the *fix* gold).
