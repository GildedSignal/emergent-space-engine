Working...
Check complete. `check.md` written; nothing else in the run folder touched, scratch work isolated in `/tmp/hcheck`.

**Grade: silver**

**Reproduced exactly:** all five scenes regenerate deterministically from the shipped `h_live.py` (S1 λ 0.8601/sat 0.984/Pesin 1.207; S2 H(1e-4)→9.46; S3 bursts, enc_frac 8.5/24.5/45.5%). One disclosure gap: stored S0 JSON predates the final script (missing `frozen_frac` key), but all shared numbers regenerate.

**The decisive adversarial finding:** the "stable chaos, T_Lyap ≈ 1.2 orbits" load-bearing surprise is an instrument artifact. The Benettin shadows integrate a *different map* than the main bodies — drift at updated `ash**-1.5` vs main's birth-frozen `n`, both half-kicks at the end epoch. With an honest same-map shadow (same 1e-9 offset): λ_median = 0.0005/orbit (1700× smaller), 0% saturation. The artifact magnitude matches my Fermi estimate from the drift-rate mismatch (λ≈0.95 predicted vs 0.86 measured), and step-halving (0.8835 vs 0.8837) confirmed it's a rate mismatch, not chaos. All λ/KS numbers in the run are invalid.

**What survives and strengthens:** the scar-entropy core is untouched by the bug — secular belt flat at ~6 bits/body after a 2-orbit transient, and my 64-orbit rerun extends the flatness 4× beyond the author's window; resonant/encounter rates 0.13–0.6 bits/body/orbit; the 64-bit/10⁹ budget holds everywhere (P4); the shipmem form-chooser rule stands, simplified. First H_live measurement (HANDOFF "not measured yet").

**Silver, not gold** because the claim sentence's inversion ("H_live is not the KS rate") was supported only by the fake λ — with honest shadows there is no measurable chaos in S1 to contrast. One experiment from gold: honest-shadow λ per regime (S3's encounter belt may be genuinely chaotic) plus conditional entropy H(scar | birth elements), which the stored data already supports.
