# Predictions (written before the decisive run)

Target premise: representation.md L59/L116 — "Aggregates are one sample each, and the
screen caps the work at about one sample per pixel" + L58 "A blackbody is seen at k·T
with beaming k⁴, which in log form are additions. A type × log k table gives the sprite."

Instrument: standalone float NumPy, exact SR Doppler factors k = 1/(γ(1−β·n̂)), truth =
Σ k_i⁴ per member (bolometric intensity transformation, exact), MC with fixed seeds
(PCG64), analytic lognormal Jensen control on both sides.

I tuned NOTHING on the Monte Carlo yet. The analytic lognormal derivations below are my
priors; the MC rows, the observer-motion (θ) arm, the strobe time series, the tail shares
and the sample-count table are held out.

## Pre-registered expectations

1. **Instrument control (analytic arm):** for lognormal ln k ~ N(μ, s²), the shared
   log-word readout (geometric mean, F = N·e^{4μ}) underestimates the true flux
   E = N·e^{4μ+8s²} by exactly exp(8s²)·(1 + O(1/N)). MC must reproduce this to within
   MC noise (<1% at N=10⁶). If it does not, the instrument is broken and the run is VOID.

2. **Newtonian negative control:** the k = 1 readout misses the flux by e^{4μ+8s²} − 1
   (orders of magnitude at β ≥ 0.9): at β 0.9 head-on, μ = ln(1/(γ(1−β))) = 1.47, so the
   truth is ~10²× the Newtonian sprite. If the instrument shows less than 30× there, VOID.

3. **Low-β control:** belt-realistic regime (bulk β ≈ 10⁻⁵–10⁻³ c, dispersion 10⁻⁵ c):
   one-sample flux error < 0.5%, strobe invisible. The premise is SAFE exactly where the
   shipped belt rung (B18) tests it. (This is the rung-blindness claim, so I expect it.)

4. **One-sample flux error (median over draws), flagship regime:** driven by CV(k⁴) =
   sqrt(e^{16s²}−1). Predicted: bulk β 0.9 with LOS dispersion σ_β 0.05 → s = σ_ln k ≈
   d ln k/dβ|_0.9 · 0.05 = 5.26·0.05 ≈ 0.26 → median |error| ≈ 0.67·CV ≈ 0.9 (≈90%),
   worst draws ×3–5. At β 0.99, σ_β 0.005 → s ≈ 0.25 → same class. At β 0.5, σ_β 0.05 →
   s ≈ 0.067 → ≈18%.

5. **Shared log-word bias (the "log form are additions" reading):** exp(8s²) − 1:
   β 0.9/σ.05 → ≈ +70%; β 0.5/σ.05 → ≈ +4%. Deterministic, not sampling noise — a
   systematic the letter cannot see.

6. **Strobe (frame-to-frame per-pixel sample swap, 60 frames, swap per frame):**
   jump amplitude = 4·|Δ ln k| between consecutive draws; median ≈ 4·1.13·s (half-normal
   mean of |N(0, 2s²)|·... I expect the median around 4·s·1.2). At s 0.26 → ≈ 1.2 in ln
   (≈ 3–4× flux per frame); visibility bar ~1–2% contrast → the boundary sits near
   s ≈ 0.005, i.e. LOS dispersion ≈ 10⁻³ c at β 0.9 (0.1% of c — below any battle's
   manoeuvre speeds). Held-out: exact boundary and the β 0.99 row.

7. **Tail share (principle 20, "averages crush tail events" made physical):** fraction
   of Σk_i⁴ carried by the top 1% of members. Lognormal prior: at s 0.26 (β.9/σ.05)
   ≈ 10%; at s 0.5 (β.99/σ.01) ≈ 35%. A one-sample readout draws a tail member ~1% of
   frames — the sprite is 99% of frames a member that carries ~1/3 of the brightness
   story. Held-out: exact numbers.

8. **Observer-motion arm (player at β_O, static crowd with angular extent):** σ_ln k
   across the crowd = |d ln k/dθ|·σ_θ with d ln k/dθ = β_O sinθ/(1−β_O cosθ); at θ = 90°,
   β_O 0.9: 0.9/rad. A formation spanning ±0.05 rad → s ≈ 0.027 → strobe ≈ 12%/frame on
   a formation whose members all share the SAME velocity (dispersion zero). Held-out: the
   β_O 0.99 row and away-from-90° angles.

9. **Cost corollary:** samples needed for a 5% total-flux bar ≈ (CV/0.05)² → at s 0.26
   ≈ 700 (vs the cap's 1); for a 2% per-pixel bar ≈ 4×10³. The "~1 sample per pixel"
   cap breaks by ~10²–10³× at the flagship regime.

10. **Colour:** sampled colour k_s vs flux-weighted true colour k̄_F = Σk⁵/Σk⁴: ratio
    spread ≈ the k spread itself (~e^s); at s 0.26 → colour temperature off by ×1.3
    median, ×2 tail (5800 K star drawn as the wrong blackbody band).

## What would make the premise survive

If CV(k⁴) stays under ~2% at every regime the player can reach (β ≥ 0.5 crowds with
plausible dispersions, β_O ≥ 0.5 observer), the one-sample readout is fine and the
premise stands. My priors say it fails by orders of magnitude instead.
