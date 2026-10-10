Working...
Check complete. `check.md` written (24 lines, first line `Grade: silver`); nothing else in the run folder changed (`__pycache__` from my imports removed).

**Grade: silver.**

**Reproduced bit-identically:** shipped record (`probe_hlive.py` → raw/post JSON, 7 s), gold job `cold_k0` (Λ exactly 0.44492011071143167…, npz bitwise), W=0.1 job (0.23721629221305496, npz bitwise — the held-out geometry of the closed-form kill), controls (×126), full `gold_post.py`, and the xhi ladder rung via a memory-safe chunked rerun (Λ = 0.5410163155878738 / 5.796242416896214 / 46.80371753425165, n_enc 2946 — exact). `predictions.md` (03:58:44) predates the first gold output (04:00:53).

**My attacks (5):** an independent multi-start instrument (the fix the author named but never tested) lands Λ(1e-4)=0.5177 on seed k0 — between ultra-greedy and xhi at half the ultra cost, confirming both the greedy-basin mechanism and the floor quantification; elementwise, ultra drops b_min >20× on 3211/65294 identical pairs (max ×84943); a new analytic σ_e→0 control (absent from the run) passes at 0.1–1.2% across all ρ, repairing the positive-control hole the closed-form demotion opened; design-table arithmetic recomputes as printed; widest-bin/blunt controls hold in all 20 jobs.

**Why not gold:** the headline Λ(1e-4)=0.525 is a certified floor, not a converged number — the ladder's last 4× step still moves +8.5%, PG7 failed its own pre-registered VOID line (escalated, honestly disclosed), and the only boundary-straddling verdict (q=1e-6 marginal-FITS) plus q_v* inherit that floor and a corr extrapolated from one (M,q) point. The one experiment: close the instrument with the non-greedy minimiser (~90 s/seed as prototyped) and re-issue the three numbers with symmetric bars. Everything else — both corrections (q_v* 2.8× lower), the closed-form demotion, the basin diagnosis — meets the gold bar and is now independently confirmed.
