# Predictions (written before rt_bounded_family, rt_quad_scan, rt_half ran)

Calibration already seen (not held out): creep scan is a cliff — λ ≤ 1e-13/horizon keeps
every ship under the 1e-12 floor (arrow exactly 0.000, PASS); λ = 1e-12 gives arrow 39.1
(FAIL). No λ lands the arrow near 5 on clean histories. Receipt-vs-Linux: same corpus
and code (sha256 verified), planted-bounded arrow −2.806 (receipt, macOS) vs +0.812
(here) — the statistic is platform-noisy at O(±3) around zero.

Held-out predictions:

1. **quad(k) — memoryless quadratic slow-state error** (bounded, no memory, same
   magnitude class as the passing planted-bounded): the through-origin affine fit
   cannot remove curvature; residual ∝ Δa·(a_i+a_j−2a₀) grows with state diffusion,
   hence with dt. Predict: FAIL at every k (4e-11 … 4e-9) with pooled arrow well
   above 5 (≥ +15), sensitivity "RESOLVED" (the law's own residual, ~1e-7, masks the
   2e-10 injection, but own arrow >> 5 so injected arrow >> 5 too). That is a
   confident "compounding" label on a bounded, memoryless law — a false positive the
   doc's own caveat ("local-affine … is a model assumption") predicts but has not
   measured.

2. **hump(A) — bounded error, zero at both horizon ends**: pairs always have i in the
   first half, j in the second; |d| = A|sin²_j − sin²_i| rises with dt for fixed j,
   falls for fixed i. Sign of the rank score is genuinely uncertain. Predict per-ship
   z median in (−25, +10); verdict FAIL either way — if arrow ≤ 5 then sensitivity is
   UNSUPPORTED (residual ~A >> 2e-10 masks the injection). If the median z is ≤ −15,
   the one-sided pooled test becomes cancellable (see 4).

3. **slab(9e-5, τ=5P)** — bounded, settles early: residual after the state fit is
   noise-level at most pairs; predict PASS-side behavior (arrow small, but
   sensitivity likely UNSUPPORTED because dmed ~ early-pair residual >> 2e-10;
   so FAIL/UNSUPPORTED — a refusal, not a misgrade). **slab(9e-5, τ=100P)** —
   rises through the whole horizon: predict FAIL with arrow > 5 (indistinguishable
   from a leak within the horizon; a true boundary case, reported as such).

4. **half(λ, A) — leak λ/horizon on the 8 outer ships (a₀ > sep), hump(A) on the 8
   inner**: pooled arrow is a mean over above-floor ships. If hump z_inner ≥ −10,
   arrow stays > 5 → FAIL (pooling premise survives this probe). If hump z_inner
   ≤ −15, arrow lands under 5 with 8 of 16 ships leaking at 2e-9/horizon — and
   sensitivity then decides: if the inner residual floor (A) masks the injection
   everywhere, injected arrow ≈ own arrow ≤ 5 → UNSUPPORTED (honest refusal), so a
   clean PASS misgrade needs the outer ships' floor low enough that the injection
   saturates their z (+30) while inners stay ≤ −13. I predict UNSUPPORTED-FAIL or
   plain FAIL; a clean PASS is possible only in a narrow window.

5. Per-ship z under bounded laws (planted-bounded measured: worst +5.8 with median
   +0.3) already exceeds the 5 cutoff individually while pooled passes: predict the
   same for every bounded shape here — the per-ship null is ~5× wider than the
   independent-rank variance the cutoff assumes.
