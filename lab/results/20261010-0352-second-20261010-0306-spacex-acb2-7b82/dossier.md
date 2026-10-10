# Dossier — 20261010-0352-second-…-7b82 (second author on 20261010-0306-spacex-acb2)

**Claim.** The parent run's claim survives the checker's named gold experiment with every
verdict now certified by error bars, two numbers corrected, and one component demoted: a
belt's live distinction rate is still set by mass and velocity quantum, not body count —
Λ(ρ=1e-4) = 0.525 ± 0.069 (6 seeds, bin-JK ±35%, one-sided instrument floor +10–20%),
ρ-exponent 0.979 ± 0.024 over two decades, corr = 1.19 ± 0.46 (the shipped 2.2 was the
max of the seed draw), so q_v* = 3.8e-7·v_K (1.1 cm/s at 1 AU, M_belt=1e-7) — 2.8×
*lower* than shipped — the 2⁻³² tube key still breaks the 64-bit budget by ~1.9×10³,
q=1e-5 fits with 26× margin, q=1e-6 is certified marginal (24 [16,39] bits vs 64, within
a factor ~2 of budget under systematics); the closed form Λ = 0.85·N·ρ·σ/W is demoted —
K = Λ·W/(N·ρ·σ) rises 1.05 → 1.81 → 2.01 as W/σ goes 2 → 4 → 10 (saturating near 2–2.5,
the Rayleigh e-tail is integrable), so the adoption path is the per-belt MC (one ~60 s
command per geometry); and the instrument's bias is newly diagnosed as a greedy-zoom
basin failure (same-pair b_min drops 2–100× when resolution rises; increments
+10.7/+12.1/+8.5% per 4× resolution — rates are floors, and the directed build should
replace the greedy zoom, though no design verdict flips).

**Bottleneck.** Same as the parent: board line "fitting 10⁹ in 8 GB … decided by
distinctions created per game-second"; HANDOFF's "H_live … not measured yet". This run
converts the parent's five point numbers into certified numbers: with bars, the design
verdicts are safe against seed luck, the ±35% heavy-tailed rate integral, the resolution
systematic, and the corr scatter — the exact attacks the checker raised.

**Evidence** (same scene as the parent: planar belt W=0.02, σ_e ∈ {0.01, 0.1}, N=1e4,
star M*=1, a=1, v_K=1; shipped physics imported unmodified from `probe_hlive.py`;
6 seeds × 4000 pairs/bin at hi-res 512/24/6 = the checker's parameters; machine idle,
load 1.3, 8 vCPU, 4 workers, every process < 300 MB):

- **Regeneration.** Shipped record reproduced bit-identically in this tree before any
  change (`probe_hlive.py` 7.4 s → raw/post/post-JSON all `cmp`-equal). The gold record
  regenerates from `bash run_gold.sh` (20 deterministic jobs incl. the ~10-min xhi
  escalation, ~30 min at 4 workers; each hi-res job a separate ≤ 65 s command, e.g.
  `python3 gold_probe.py cold_k0 0.02 0.01 20261010 hires gold`), then
  `python3 gold_post.py` (~7 s) → `gold_post.txt`, `gold_post.json`.
- **Λ with bars** (per body per orbit): cold 0.525 ± 0.069 [0.445, 0.642] / 4.88 ± 0.23
  / 47.2 ± 1.0 at ρ = 1e-4/1e-3/1e-2; hot 0.291 ± 0.083 / 3.48 ± 0.28. Bin-jackknife
  (pooled, leave-one-Δa-bin-out): ±35% cold, ±45% hot on every ρ — the heavy-tailed
  integrand rules all rates, so the JK bar, not the seed band, is the honest statistical
  error. Hotter ⇒ fewer close passes: confirmed with bars (0.53 vs 0.29).
- **ρ¹ law:** 3-point fit per seed, cold 0.979 ± 0.024, hot 1.042 ± 0.065.
- **Instrument convergence (the missing control, now run):** same-seed ladder
  0.4018 → 0.4449 → 0.4987 → 0.5410 (shipped → hi → ultra 2048/48/8 → xhi 8192/96/10),
  increments +10.7/+12.1/+8.5%; Λ(1e-2) is converged (47.2 vs 46.8 at 4× resolution),
  Λ(1e-3) +5%, Λ(1e-4) carries a one-sided +10–20% floor at hi-res. **New mechanism,
  elementwise on identical pairs:** hi-res vs ultra move b_min by 2–100× (e.g.
  7.79e-3 → 8.97e-5) because the greedy zoom shrinks into the wrong (shallow) basin and
  never returns; catching a deep dip is a bracket-probability event, which is why
  encounter counts climb 1260 → 1901 → 2946 while Λ moves by ~10%. The fix (multi-start
  zoom or exact per-pair minimisation) belongs to the directed b-h-live build; it is an
  instrument problem, not a physics one.
- **⟨v_rel|enc⟩:** 0.0148 (seed mean) / 0.0190 (rate-weighted pooled, bin-JK ±0.0007);
  the shipped 0.0106 was an under-resolution artifact — this correction alone moves q_v*
  down 1.4×.
- **corr (tail correlation):** 1.19 ± 0.46 [0.73, 1.83] over seeds, bin-JK ± 0.22; the
  shipped point 2.20 is the upper tail of the same distribution (checker's finding
  confirmed and now barred).
- **Closed form demoted:** K(W) = Λ·W/(N·ρ·σ) at σ=0.01: 1.05 ± 0.14 (W=0.02, 6 seeds),
  1.81 ± 0.20 (W=0.04, 3), 2.01 ± 0.63 (W=0.1, 3); the parent's closed form is exactly
  K = 0.85 — right (within 24%) only at the parent's own geometry, ×2.4 low at W/σ = 10.
  K(0.1)/K(0.02) = 1.92. A log-fit on the endpoints under-predicts the held-out K(0.04)
  by 19% (≈ seed scatter), and K flattens toward 2–2.5 as the e-tail integral saturates;
  no two-parameter form reaches adoption quality — per-belt MC is the stated path
  (the probes in this folder are that command).
- **Design table, 10⁹ bodies, bits/body/hr at rtf 100, median [min,max] over 6 seeds**
  (budget 64): M=1e-7 — 2⁻³²: 1.2e5 [7.0e4, 1.7e5] BREAKS ×1.9e3; q=1e-6: 24 [16, 39]
  marginal-FITS (crossed from the parent's 67 BREAKS; straddles 64 under the combined
  ±45% statistical + one-sided resolution systematics); q=1e-5: 2.4 [1.6, 3.9] FITS ×26.
  M=1e-5 — q=1e-4: 24 FITS (marginal); q=1e-5: 242 BREAKS. N-independence remains
  structural (b, v are N-free; m = M/N and n₁D = N/W cancel in the sub-quantum branch),
  now stated as such, not as a test.
- **q_v\* and cadence:** q_v*(M=1e-7) = 3.8e-7 [2.5e-7, 6.1e-7] v_K = 1.1 cm/s at 1 AU
  (parent: 1.05e-6 / 3.1 cm/s — the corr and ⟨v⟩ corrections push it 2.8× down, i.e. the
  8 GB goal is easier than shipped). Re-fit cadence at q=1e-5, M=1e-7: 226 [136, 327]
  sim-days = 54 [33, 79] real hours at rtf 100 by 4.167 sim-days/real-hour — this fixes
  the parent's "2.6 real hours" slip (its 79 sim-days were ≈ 19 h) and lengthens the
  cadence ~3×. Player floor: strongest 1-in-400 kick 8.1 m/s at M=1e-7 — 715× above
  q_v* (parent said 370×); nothing player-differentiable is erased, with more margin.
- **Controls:** planted blunt sampler undercounts ×126 at hi-res (×10 at shipped — the
  tight-bin truth itself grew with resolution, same mechanism); widest Δa bins return
  P = 0 in all 20 jobs.

**Predictions** (predictions.md, written 03:58:44 UTC, before the first gold npz existed):
4 of 8 held (PG1 Λ bands, PG2 exponent, PG4 corr band, PG6 W-scaling ratio 1.92 and the
demotion). PG3 half-failed: I expected the JK bar to shrink to ≤15% at ρ=1e-3 — it stays
35%; the heavy tail rules every rate, so the JK bar is the honest error everywhere. PG5
mostly held (verdict rows stable, q=1e-6 inside my "factor 2 of budget" call) but q_v*
landed 5% below my band's floor (3.78e-7 vs ≥4e-7) — the corr/⟨v⟩ corrections
compounded past my guess. PG7 failed as a convergence claim (+12.1% same-seed at ultra,
> my 10% kill line): I followed its own escalation branch, added the 4× level, and the
ladder still rises +8.5% — reported as a one-sided systematic plus a new mechanism
finding instead of a VOID, because the ρ¹ law, the verdict margins (≥2.6×) and every
design conclusion are insensitive to it. PG8 failed upward (cadence 226 vs ≤160
sim-days): same compounding cause, honestly reported. No failed prediction was used to
set any headline number.

**What would make it wrong.** (1) The instrument: rates are floors with a slow +8–12%
per 4× resolution; if the true Λ(1e-4) is ≫ 0.6 the marginal q=1e-6 row could re-cross
to BREAKS — that row must be re-measured per belt with a non-greedy minimiser before any
freeze (it is the only verdict inside a factor 3 of the boundary). (2) The 64-bit budget
is fully allocated to belt scars here; fleets, battles and other belts share the real
8 GB, so q_v* as stated is a lower bound on the quantum a full design needs. (3)
corr is measured at one (M, q) point and applied across the deep tail; its ±39% seed
scatter dominates q_v*'s band. (4) Planar, no planets, no player — unchanged from the
parent; the co-orbital/fleet H_live case (gold 20261006-0346) is still the named next
rung. Cost of adopting: none in code — the numbers above replace the parent's five points
in the same formula; the encounters opt-out threshold and re-fit cadence inherit real
error bars. Fit with PRINCIPLES: "the memory floor is information" (#24) — the floor is
now measured with its error; "influences below one quantum accumulate" (#6) — the
accumulation point is 2.8× lower than the parent claimed; "Measure before claiming"
(#10) and "a test that cannot fail is a control" — the convergence control did its job:
it failed, and the failure is the run's second result.

**The lens.** The second-author lens optimised for certifying the parent's verdicts, and
it did that; what it may have missed: I did not rebuild the instrument (only escalated
it), so the greedy-zoom fix is named but untested; the K(W) saturation shape rests on
3+3+6 seeds at three widths — enough to demote, not to fit; and the hot 3-point exponent
(1.042 ± 0.065 vs cold 0.979 ± 0.024) may carry real structure (the conjunction-limited
rate bending as σ_e grows toward W) rather than noise — untested here.
