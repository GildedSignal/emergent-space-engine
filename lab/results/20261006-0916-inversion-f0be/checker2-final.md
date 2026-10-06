Working...
`check2.md` written. The author's folder is otherwise untouched (verified listing; the only additions are `check2.md` and the regenerated `.pyc`), no commits made.

**Grade: lead.** Summary of the check:

**Reproduced:** patch applied (adds `s4.log` only), `python3 probe.py s1` bit-exact in 25 s, dense validators 4=4 and 2=2 — every stored number regenerates. The instrument is wrong, not the log.

**The kill:** the entire maintenance prong rests on `overtakes_per_orbit = |Δrank|/2` where ranks come from sorting `λ = ϖ + atan2(…) ∈ (−π, π]`. That coordinate has a branch cut: every body crosses it once per orbit, and each crossing bills as ~(n−1) swaps. S4's counts are literally n(n−1)+{193, 2163, 4627}. Two independent wrap-free counters (unwrapped-λ ranks; pairwise sin-sign crossings with an antipode filter) agree with each other within 2% and contradict the probe by 96–97% everywhere:

- S1 (the gold's control): **580 true overtakes = 0.73× the watch** — the dossier's "26× more than it watches" inverts.
- S4: 632/8,840/35,094 → 1.2×/4.3×/8.6×, not 32×/129×/257×; pre-registered "10× at n=1024" fails on corrected counts (8.6×).
- S3 (e=0.9): 115,774 true = 56× — the one regime where the claim survives correction in spirit.

**What stands:** the correctness half is sound and honest (rank 1 at every contact, down to 0.1ρ spacing — strengthens the gold), and the corrected S4 law ≈ 0.033·n² is still quadratic with a watch crossover at n_c ≈ 120, so the concern's direction deserves one clean rerun with a wrap-free counter over an e-spread ladder. That's the path to gold I named; as delivered, the headline numbers are the artifact class the lab already canonized on 5 October — counting events that aren't events (a body crossing λ=π passes nobody).
