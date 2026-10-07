Grade: gold

**Abstract.** The claim reproduces exactly and the premise kill is real. My clean-tree rerun matched all 16 grid scenes bit for bit (n_enc, k*, miss@4; e.g. σ_e=0.02 → k*=9, 13.5% missed; debris n=768 → k*=384=n/2, 98.5% in the stored run), and an independent Kepler truth (bisection solver, different position algebra) reproduced 5/5 scenes exactly, including swarms. Adversarial cases strengthened it: k*/n = 0.40/0.49/0.50 at n=96/192/384 makes the O(n²) corollary measured, T=2× sampling is converged (Jaccard 1.0), and a circular ring with the same phases fails M-rank (95.5% missed) yet passes ω+M-rank — while ω+M still misses 95% of the eccentric swarm. Adopt now: size k by the group's lag tail, not 4; the build `b-coorbital-cert` is mid-flight and its test set (formations + dense ring) would have shipped this silently.

**Reproduction.** Applied nothing (patch.diff empty; self-contained scripts). `python3 coorb_probe.py 384 8192` in a clean tree: 16/16 scenes identical to `grid_results.json` and the dossier table, every number. Stored `battery2.json` matches the dossier (mechanism medians Δν*=84.3° vs Δω=84.2°; seeds 189–192/97–98%; R-scan pinned at n/2). `battery2.py` not rerun end-to-end (time); its headline scenes were instead re-derived with an independent implementation (below), which is the stronger check. Peak memory ≈ 0.5 GB per process.

**Held-out / predictions.** `predictions.md` (21:03) predates both result files (21:17, 21:18); scene coverage matches. No execution log (`run.log` empty), so ordering rests on mtimes — but two predictions failed against the author's own expectation and were reported as failures (controls pass at k≤4 — false, convoy k*=9–11, 12–18% missed; clean to σ_e=0.05 — false, 13.5% at σ_e=0.02). That is the signature of a pre-registration, not tuning. Kill criteria were pre-declared and the no-man's-land is confirmed (k*=191 ≥ 16, setup/n_enc = 318 ≥ 100).

**Attack (three of mine).**
1. *Gauge attack (new finding the author missed):* e=0, ω uniform is the **same physical scene** as the passing control (uniform phases on one circle). M-rank: k*=191, 95.5% missed. Rank by Λ=ω+M: k*=3, 0% — so the certificate's coordinate is broken even for zero-dispersion rings when the phase lives in ω; the build must rank by a longitude-like coordinate at minimum. Λ does **not** rescue swarms: k*_Λ = 87 (sw180-e03, 95.2% missed), 86 (bimodal), 170 (debris). This confirms the dossier's "the swarm failure stands in any phase-like coordinate" empirically, and makes the silent-miss hole wider than claimed.
2. *n-scaling:* k* ∝ n measured (0.396/0.490/0.497 of n at 96/192/384), and the convoy control also grows ∝ n (3 → 9) — fixed rank 4 dies at fleet scale even on formations.
3. *Sampling:* T 8192→16384 on the two worst scenes: identical pair sets (Jaccard 1.0), k* unchanged.

**Independent truth.** My own harness (bisection Kepler E-solver, half-angle ν, explicit rotation matrices) matches the author exactly on ctl-ring (124/2/0%), se005 (229/20/45.0%), sw180 (231/191/97.4%), bimodal (179/140/60.3%), debris n=384 (6/158/83.3%). The shared-harness risk the author flagged is discharged.

**Novelty.** No H entry covers dispersion breaking phase rank; the gold it attacks (20261006-0346, taste log 6 Oct) measured formations only, and the live build spec (`lab/lenses/b-coorbital-cert.md`) tests "the gold run's scenes and a dense ring" — no dispersion scene, so the miss would have been silent, exactly as the dossier claims.

**Goal fit.** Board's top scaling risk (encounters at N); kills a configuration, not the method (#9); sizes k by a dimensionless tail statistic (#4); a silent lost encounter is the compounding error #13 forbids; #34 — the certificate must refuse what it cannot certify. Adoptable within one step while the build is mid-course.

**What the author missed.**
- The coordinate/gauge hole above (circular rings with phase in ω; Λ-ranking) — the constructive fix sketch should say "longitude-like coordinate, then lag tail", and the lag formula must then be stated in Λ units.
- One analytic slip: "≈ (n/2π)(π+4e)" for bimodal evaluates to 265, not the measured 140; exact ΔM(±π/2, e=0.3)=2.430 rad gives 148.5 ≈ 140. Mechanism right, parenthetical formula wrong.
- The n=768 debris headline (98.5%) rests on the stored run only; corroborated here by the n=384 debris scene and the measured k*∝n trend, but not re-run at 768.
- σ_a=0 keeps M-rank frozen in time; rank churn under σ_a>0 (acknowledged, unmeasured) remains the open risk for the sizing rule.
