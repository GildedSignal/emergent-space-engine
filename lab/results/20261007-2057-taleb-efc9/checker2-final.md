Working...
Check complete. `check2.md` written to `lab/results/20261007-2057-taleb-efc9/` — **Grade: gold**.

**What I did (30-min window, all processes <0.6 GB):**

1. **Reproduced** the full grid in a clean tree (`coorb_probe.py 384 8192`): 16/16 scenes bit-identical to the stored results and the dossier table — σ_e=0.02 → k*=9/13.5% missed, swarm scenes → k*≈n/2 with 97–98% missed, controls pass at k*=2–3.
2. **Discharged the shared-harness risk** with an independent Kepler truth (bisection E-solver, different position algebra): 5/5 scenes matched exactly, including swarms and debris.
3. **Attacked with three adversarial cases of my own:**
   - **Gauge attack (new finding):** a circular ring with the *same physical phases* as the passing control fails M-rank (k*=191, 95.5% missed) when the phase lives in ω; Λ=ω+M ranking fixes that case (k*=3) but still misses 95% of the eccentric swarm — the certificate coordinate itself is broken, a wider hole than the dossier claims.
   - **n-scaling:** k*/n = 0.40/0.49/0.50 at n=96/192/384 — the O(n²) corollary is now measured, and even the convoy control's k* grows ∝ n (3→9).
   - **Sampling:** T doubled on the two worst scenes — pair sets identical (Jaccard 1.0).
4. **Predictions:** pre-registered (mtimes 21:03 < 21:17/21:18); two failed against the author's own expectation and were reported — the signature of honesty.
5. **Novelty:** no prior H entry; the attacked gold (20261006-0346) measured formations only, and the live `b-coorbital-cert` spec's test set contains no dispersion scene — the miss would have shipped silently.

**Flaws noted (none grade-changing):** the bimodal analytic parenthetical "(n/2π)(π+4e)"=265 ≠ measured 140 (exact gives 148.5 — mechanism right, formula slip); the n=768 debris headline rests on the stored run (corroborated by trend); σ_a>0 rank churn unmeasured.
