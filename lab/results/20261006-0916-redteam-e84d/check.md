Grade: silver

**Abstract for the integrator.** A1 (the belt) reproduces bit for bit and survives every adversarial probe: 5.75% chaotic at Jupiter μ (5.6%/6.6% on new seeds; 5.1%/8.9% at τ_a 2×/½×; **0.125%** in a non-resonant sub-band [0.50,0.60]; 3.5% at T=2400 — steady, not growing). The §6 "bursts" row and the gate ladder genuinely have no belt-with-planet scene (B15 has no belt, B17 two single resonances, B18-belt planet-free); a B20/B15-extension is one step. A2 does not survive checking: the eq.-13 parse fails its own ν→0 validation (3.5 against the exact Schwarzschild 6.5 = 39/4−13/4, with 39/4 on x₂²); corrected, the doll's advance error at p=20M, ν=0.25 is ≈ **1.3%, not 10.2%**, and B11's tolerance there is **81%, not 1.8%** (2·8/p is a fraction, not percent). A6 (stale Minsky premise in representation.md §1) is verified true.

**Reasons.**

*Reproduction (clean tree, empty patch.diff — nothing outside the run folder was edited).*
- All five belt configs from `run.log` reproduce every field bit for bit: f_chaotic = 0.75% (μ=1e-6), 2.125% (3e-5), 5.75% (9.54e-4), 28.625% (1e-2), 0.0% (cold); ~90 s wall for five parallel runs.
- `eob_2pn.py` reproduces its own table exactly (10.19% at p=20M; 1% boundary 267M). The code's numbers are what the dossier says — the physics parse is what fails (below).
- Timestamps: `predictions.md` (24 m before script final edit, 19 m before `sweep.jsonl`) predates the decisive run; run order consistent with `run.log`.

*Adversarial cases (mine).*
1. Seeds 8, 9 at Jupiter μ: 5.625%, 6.625% — the population is not a seed artifact; the same Kirkwood structure (bins pile at the 2:1/5:2 end).
2. Threshold τ_a = 0.006 / 0.0015: 5.125% / 8.875% — the classifier is not manufacturing the result near its floor.
3. **Mechanism control**: band [0.50, 0.60] (between the 3:1 and 2:1 first-order resonances) at the same μ, e, N: f_chaotic = 0.125% (1/800). The chaos lives where the resonance network is. This is the strongest confirmation the checker could have asked for.
4. T=2400, N=400: 3.5% vs 5.75% at T=1200 — no growth (P6's ≥1.3× does not fire); the fraction mildly declines as drifters scatter out.

*Where A2 breaks (checker derivation, all reproducible).*
- The shipped `eob_2pn.py` contradicts itself: its docstring says the doll is `(1−6X)^{−1/2}−1 = 3X + 13.5X²`, then line 36 uses `3X(1+3.5X)` = 3X + 10.5X². Exact Schwarzschild's bracket coefficient is 4.5 in X_Ω=(MΩ)^(2/3) and 6.5 in the paper's own variable X_n=(Mn_radial)^(2/3) (n ≡ 2π/P_pericenter, eq. 11); both checked numerically against (1−6X)^{−1/2}−1.
- The claimed ν→0 parse validation is circular: 27/4−13/4 = 3.5 is arithmetic, not physics. With 39/4 on x₂² (the heavier body) instead of x₁² — the natural reading of the mangled eq. 13, and required by consistency with Tucker–Will per the paper's own footnote — b1−b2 → 39/4−13/4 = **6.5 = exactly the Schwarzschild coefficient in X_n**. The parse then validates. At ν=0.25 the swap changes nothing (x₁=x₂), so B(0.25)=6.1667 stands, but the doll in the same variable is 6.5, giving |error| = 0.3333X/(1+6.1667X): **1.27% at p=20M, 0.59% at 50M, 0.31% at 100M**, crossing 1% near p≈28M — not 10.2%/4.7% and a 267M boundary. The direction flips sign (ν *reduces* the advance below test-mass).
- The B11 comparison misreads units: (1% + 2·8/p) at p=20 is ≈ 81% (the record says the 1PN oracle's own next term is ~8M/p: H0203 "oracle's own truncation ≈72% at p=20", H0206), not 1.8%. So the doll sits ~60× inside B11's band at p=20 and ~8% of the band at all p. "Structurally blind" describes a recorded, deliberate compromise (r3 v3's judged-seed machinery), not an unnoticed hole. The corrected A2 residual — a sub-1.3% doll error at p=20M, ν=0.25 — is at most a fence note for p ≲ 30M, not a premise kill.

*Predictions.* Written before the decisive run and honestly scored: P4 (cold = 0%) and P5 held; P2 half-held; P1's librator half, P3 (control 0.75% vs ≤0.125%) and P6 failed — all disclosed. Note the instrument was swapped after predictions (Lyapunov → a-diffusion, disclosed in run.log) and τ_a was calibrated on the same control that P3 then declared clean; my threshold probes bound the resulting ambiguity.

*Novelty.* A1 is new as a measurement: H0203 established "resonance kills averaging" as a rule; nobody had measured the steady chaotic fraction vs μ, its ~1 event/synodic-period rate, or the absence of any belt+planet gate/cost row (B18-belt is planet-free, gold components-98bc is the program/memory side; the 6 Oct co-orbital gold is the encounters tier). A2's surviving kernel (1PN oracle weak at small p) is already in the record (H0203/H0206). A6 verified: law.md:20 records `space-darwin16-v1` replaced the Minsky in-band map on 30 September while representation.md:32 still calls it "the primary in-cell solution".

*Goal fit.* A1 names a missing cost row on the plane the player meets early (principles 14, 12, 29; "the algorithm that allocates the work to prevent those heavy tails") — measurement-first, no representation change, adoptable in one step. It respects "every body is real" by refusing to average the gap bodies away.

**Why silver, not gold.** The run's own pre-registered kill criterion for the "bursts" premise (≥15% at Jupiter μ) did not fire there — it fires only at μ=1e-2 — and several held-out predictions failed; and the second measured claim (A2) is wrong in its headline numbers for reasons above. A1 alone is real and adoptable, but "gold" requires the held-out predictions to hold and the claims to stand as filed.

**The one experiment that would make it gold.** Settle A1's *steady-state* question: T ≥ 5000 orbits at 3–4 μ values with ejection/migration tracked separately, so the chaotic fraction's plateau-vs-decay is measured (the Kirkwood gap emptying is itself the emergent history — a decaying transient still needs a cost row, but a different one), and re-file A2 with the corrected parse and doll (expected outcome: no defect beyond p ≈ 30M; drop the 267M boundary and the B11-blindness claim).

**What the author missed.**
- The ν→0 check they cite as their parse validation is precisely the check that falsifies it: exact Schwarzschild in their own docstring gives 13.5X², i.e. bracket 4.5 (or 6.5 in the paper's radial-frequency variable), never 3.5. They validated arithmetic, not physics.
- 2·8/p is a fraction; B11's precession band at p=20 is ~81% by design, and the design record already prices the 1PN oracle's truncation there (H0203, H0206, r3 v3 judged seeds).
- "Paying exact conjunction work forever": at T=2400 the fraction declines (3.5% vs 5.75%) — at Jupiter μ the population partly self-depletes; the honest claim is a slowly renewing reservoir, not a perpetual tax (at μ=1e-2 the belt is destroyed outright — 28.6% chaotic, max drift 9×10⁶).
- f_resonant ≈ 0 means the regular-resonant (rotating-doll) remainder is unmeasured by their instrument, not zero; the "non-averaged total" is f_chaotic plus an unknown, and P1's second half (≥10% librators) is the failed prediction that would have measured it.
- The conjunction rate (a^{−1.5}−1) counts all conjunctions, not close ones; as the missing cost row's rate it is an upper bound.
